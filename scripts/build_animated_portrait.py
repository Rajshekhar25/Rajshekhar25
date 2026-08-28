"""
Generates the two animated SVG layers (intro shimmer, loop drift/return)
from the verified grouping arrays, as portrait-frame-local path groups
ready to embed in the banner.

Loop timeline (total 14.2s, matches the doc's stated total exactly):
  0.0 -3.0s  portrait fully visible (hold)
  3.0 -4.3s  bands fade out + translate toward the logo target (1.3s)
  4.3 -12.9s displaced/hidden (spans all 3 logo holds + 2 logo-to-logo
             transitions -- the portrait doesn't reposition per-logo,
             it moves out of the way once and returns once)
  12.9-14.2s bands fade in + translate back (1.3s)

The logo target is a PLACEHOLDER (portrait-frame center) -- real traced
logo centroids aren't available yet (network fetch is down). Swapping in
the true value is a one-line change: LOGO_TARGET below.
"""

import os
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import io
import numpy as np

ASSETS = os.path.join(_REPO, "assets")
SCRATCH = os.path.join(_REPO, "scripts", "_build")

dots = np.load(ASSETS + r"\dot_pattern.npy").astype(bool)
ys, xs = np.where(dots)
group_id = np.load(SCRATCH + r"\intro_group_id.npy")
band_id = np.load(SCRATCH + r"\loop_band_id.npy")
H, W = dots.shape

# portrait-frame geometry (must match build_banner.py)
PORTRAIT_X, PORTRAIT_Y = 34, 76
PORTRAIT_W, PORTRAIT_H = 380, 431
SX, SY = PORTRAIT_W / W, PORTRAIT_H / H

# PLACEHOLDER convergence point -- portrait-frame center; see docstring
LOGO_TARGET = (PORTRAIT_X + PORTRAIT_W * 0.5, PORTRAIT_Y + PORTRAIT_H * 0.5)

def runs_to_spans(row_bool):
    spans, x, w = [], 0, len(row_bool)
    while x < w:
        if row_bool[x]:
            s = x
            while x < w and row_bool[x]:
                x += 1
            spans.append((s, x))
        else:
            x += 1
    return spans

def path_for_indices(idx_mask):
    """Build a crispEdges path from a boolean mask over the (ys,xs) dot list."""
    sub_y, sub_x = ys[idx_mask], xs[idx_mask]
    grid = np.zeros((H, W), dtype=bool)
    grid[sub_y, sub_x] = True
    parts = []
    for y in range(H):
        row = grid[y]
        if not row.any():
            continue
        py = PORTRAIT_Y + (y + 0.5) * SY
        for (x0, x1) in runs_to_spans(row):
            parts.append("M%.2f,%.2fH%.2f" % (PORTRAIT_X + x0*SX, py, PORTRAIT_X + x1*SX))
    return "".join(parts)

# ============================================================
# INTRO layer: 60 groups, staggered fade-in over ~2s, then a
# single hand-off fade-out timed to when the loop's first
# outward transition begins (t=3.0s) -- after that, the loop
# layer owns all subsequent visibility.
# ============================================================
N_GROUPS = 60
INTRO_SPAN = 2.0      # groups fade in across this window
FADE_DUR = 0.75        # each individual group's own fade-in length
HANDOFF_AT = 3.0       # matches the loop's portrait-hold end

rng = np.random.default_rng(20260828)
begins = np.sort(rng.uniform(0, INTRO_SPAN - FADE_DUR, N_GROUPS))

intro_elems = []
for g in range(N_GROUPS):
    m = group_id == g
    if not m.any():
        continue
    d = path_for_indices(m)
    b = begins[g]
    intro_elems.append(
        f'<path d="{d}" stroke="var(--portrait-ink)" stroke-width="{SY:.3f}" '
        f'fill="none" shape-rendering="crispEdges" opacity="0">'
        f'<animate attributeName="opacity" values="0;1" dur="{FADE_DUR}s" '
        f'begin="{b:.3f}s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="1;0" dur="0.01s" '
        f'begin="{HANDOFF_AT}s" fill="freeze"/>'
        f'</path>'
    )
intro_svg = "\n".join(intro_elems)
print("intro layer: %d groups, %d bytes" % (N_GROUPS, len(intro_svg)))

# ============================================================
# LOOP layer: 94 bands, translate + fade out/in on the 14.2s
# timeline. Small per-band time jitter on the transition edges
# so the dissolve reads as organic rather than a synchronised
# snap across all bands at once.
#
# IMPORTANT: this <animate> has begin="{HANDOFF_AT}s" (3.0s), and SMIL
# measures keyTimes as elapsed time SINCE AN ELEMENT'S OWN begin, not
# since document t=0. Computing keyTimes as absolute_time/LOOP_DUR (as a
# first pass here did) silently shifts the whole cycle by +3.0s against
# what actually renders. Every keyTime below is therefore expressed as
# elapsed-since-begin: elapsed = absolute_time - HANDOFF_AT.
# ============================================================
LOOP_DUR = 14.2
T_HOLD_END = 3.0     # == HANDOFF_AT: hold entirely owned by the intro layer
T_OUT_END = 4.3
T_IN_START = 12.9
T_IN_END = T_IN_START + (T_OUT_END - T_HOLD_END)  # return takes as long as the exit: 14.2

def elapsed_frac(t_absolute):
    return round((t_absolute - HANDOFF_AT) / LOOP_DUR, 4)

loop_elems = []
for b in range(N_BANDS := int(band_id.max()) + 1):
    m = band_id == b
    if not m.any():
        continue
    d = path_for_indices(m)
    cx = xs[m].mean() * SX + PORTRAIT_X
    cy = ys[m].mean() * SY + PORTRAIT_Y
    dx = (LOGO_TARGET[0] - cx) * 0.42
    dy = (LOGO_TARGET[1] - cy) * 0.42

    jitter = rng.uniform(-0.35, 0.35)
    out_end = min(T_OUT_END + jitter, T_IN_START - 0.4)
    in_start = max(T_IN_START + jitter, out_end + 0.4)
    in_end = min(in_start + (out_end - T_HOLD_END), HANDOFF_AT + LOOP_DUR - 0.05)

    kt = [elapsed_frac(T_HOLD_END), elapsed_frac(out_end), elapsed_frac(in_start),
          elapsed_frac(in_end), 1.0]
    assert kt == sorted(kt), ("keyTimes not monotonic", kt)
    kt_str = ";".join("%.4f" % v for v in kt)

    opacity_vals = "1;0;0;1;1"
    transform_vals = (f"0,0;{dx:.2f},{dy:.2f};{dx:.2f},{dy:.2f};0,0;0,0")

    loop_elems.append(
        f'<path d="{d}" stroke="var(--portrait-ink)" stroke-width="{SY:.3f}" '
        f'fill="none" shape-rendering="crispEdges" opacity="0">'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="{transform_vals}" '
        f'keyTimes="{kt_str}" dur="{LOOP_DUR}s" begin="{HANDOFF_AT}s" repeatCount="indefinite" '
        f'calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1;0.4 0 0.2 1;0.4 0 0.2 1"/>'
        f'<animate attributeName="opacity" values="{opacity_vals}" keyTimes="{kt_str}" '
        f'dur="{LOOP_DUR}s" begin="{HANDOFF_AT}s" repeatCount="indefinite" fill="freeze"/>'
        f'</path>'
    )
loop_svg = "\n".join(loop_elems)
print("loop layer: %d bands, %d bytes" % (N_BANDS, len(loop_svg)))
print("logo target placeholder (portrait-frame center):", LOGO_TARGET)

io.open(SCRATCH + r"\intro_layer.svg", "w", encoding="utf-8").write(intro_svg)
io.open(SCRATCH + r"\loop_layer.svg", "w", encoding="utf-8").write(loop_svg)

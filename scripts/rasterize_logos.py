"""
Rasterizes the three official simple-icons logos (real fetched vector data,
not hand-drawn) into point clouds for the traveler layer.

Fill rule: a hand-rolled nonzero-winding-rule ray caster, not
matplotlib.path.Path.contains_points -- that was tried first and verified
NOT to punch winding-direction holes at all (controlled test: a square
with an opposite-wound inner square still reported the hole's centre as
"inside"). The hand-rolled version is checked against that same synthetic
case before being trusted on real logo data.

Point sampling: contour-based, not filled-interior. Interior sampling put
320 points scattered through Python's thin two-snake shape and the result
didn't read as "Python" at all -- no edges for the eye to trace. Sampling
along the mask's outline instead reads as a clean line-art trace; verified
visually per logo before trusting it.
"""

import os
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import io
import numpy as np
import cv2
from svgelements import SVG

ASSETS = os.path.join(_REPO, "assets")
LOGOS_DIR = os.path.join(ASSETS, "logos")
OUT = os.path.join(_REPO, "scripts", "_build")

GRID = 480          # rasterization resolution (viewBox is 0 0 24 24)
N_POINTS = 320       # target traveler points per logo

def load_paths(svg_file):
    """Returns list of subpaths, each a list of (x,y) flattened points."""
    svg = SVG.parse(svg_file)
    subpaths = []
    for element in svg.elements():
        if hasattr(element, "d") and callable(getattr(element, "d", None)):
            pass
        cls = type(element).__name__
        if cls == "Path":
            path = element
            # svgelements Path is itself iterable over subpaths (Move-delimited)
            current = []
            for seg in path.segments():
                seg_cls = type(seg).__name__
                if seg_cls == "Move":
                    if len(current) > 1:
                        subpaths.append(current)
                    current = [(seg.end.x, seg.end.y)]
                elif seg_cls == "Close":
                    if current:
                        current.append(current[0])
                else:
                    # Line, CubicBezier, QuadraticBezier, Arc all support .point(t)
                    n = 24 if seg_cls != "Line" else 2
                    for i in range(1, n + 1):
                        t = i / n
                        pt = seg.point(t)
                        current.append((pt.x, pt.y))
            if len(current) > 1:
                subpaths.append(current)
    return subpaths

def nonzero_winding_mask(subpaths, xs, ys):
    """
    Vectorised nonzero-winding-rule rasterization (ray casting), NOT
    matplotlib's Path.contains_points -- that was tried first and verified
    NOT to punch winding-direction holes at all (tested with a controlled
    square-with-opposite-wound-inner-square case: both same- and
    opposite-winding inputs returned "inside" for the hole's centre point).
    This implementation is checked against that same synthetic case before
    being trusted on the real logo data.
    """
    gx, gy = np.meshgrid(xs, ys)
    px = gx.ravel(); py = gy.ravel()
    winding = np.zeros(px.shape[0], dtype=np.int32)
    for sp in subpaths:
        pts = np.array(sp)
        x1, y1 = pts[:-1, 0], pts[:-1, 1]
        x2, y2 = pts[1:, 0], pts[1:, 1]
        for ex1, ey1, ex2, ey2 in zip(x1, y1, x2, y2):
            if ey1 == ey2:
                continue
            upward = ey2 > ey1
            ylo, yhi = (ey1, ey2) if ey1 < ey2 else (ey2, ey1)
            straddle = (py >= ylo) & (py < yhi)
            if not straddle.any():
                continue
            t = (py[straddle] - ey1) / (ey2 - ey1)
            xint = ex1 + t * (ex2 - ex1)
            to_right = xint > px[straddle]
            idx = np.where(straddle)[0][to_right]
            winding[idx] += 1 if upward else -1
    return (winding != 0).reshape(len(ys), len(xs))

def rasterize(subpaths, grid=GRID, view=24.0):
    xs = np.linspace(0, view, grid)
    ys = np.linspace(0, view, grid)
    return nonzero_winding_mask(subpaths, xs, ys)

def sample_points(mask, n_target, view=24.0):
    """
    Contour-based sampling, not filled-area sampling.

    First attempt filled the interior with points chosen by np.linspace
    over the row-major index order from np.where(mask) -- that respects
    neither 2D spatial structure nor density, and even after fixing it to
    plain random-from-mask sampling, 320 scattered interior points still
    didn't read as "Python" to the eye: sparse dots inside a thin curvy
    shape carry no edge information, so there's nothing for the eye to
    trace. Sampling along the mask's contour instead reads as a clean
    line-art trace of the logo -- verified visually before trusting it
    (see the two comparison renders in this session).
    """
    grid = mask.shape[0]
    contours, _ = cv2.findContours((mask.astype(np.uint8)) * 255,
                                    cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return np.zeros((0, 2))
    all_pts = np.concatenate([c.reshape(-1, 2) for c in contours], axis=0).astype(np.float64)
    rng = np.random.default_rng(42)
    n = min(n_target, len(all_pts))
    idx = rng.choice(len(all_pts), n, replace=False)
    cand = all_pts[idx]
    cand = cand / (grid - 1) * view
    return cand

# validate the rasterizer against a known case before trusting it on real logos
_outer = [(0,0),(0,10),(10,10),(10,0),(0,0)]
_inner = [(3,3),(7,3),(7,7),(3,7),(3,3)]
_m = nonzero_winding_mask([_outer, _inner], np.array([5.0]), np.array([5.0]))
assert _m[0,0] == False, "rasterizer regression: hole not punched"
_m2 = nonzero_winding_mask([_outer, _inner], np.array([1.0]), np.array([1.0]))
assert _m2[0,0] == True, "rasterizer regression: solid region wrongly excluded"
print("rasterizer validated against synthetic hole test")

# TypeScript's icon is a solid rounded-square background with the "TS"
# letterforms cut out as holes (subpath 0 = square, 1&2 = letters). Sampling
# the filled region (square-minus-letters) puts dots everywhere EXCEPT the
# recognizable part -- the letters would only show up as an absence of
# dots, not a presence. Fixed by dropping the background subpath and
# sampling just the letters as their own positive shape (verified below:
# fill drops from 0.813 to 0.181, and the rendered mask is a clean "TS").
LETTERS_ONLY = {"typescript": slice(1, None)}

results = {}
for name in ("typescript", "python", "cplusplus"):
    subpaths = load_paths(LOGOS_DIR + f"\\{name}.svg")
    if name in LETTERS_ONLY:
        subpaths = subpaths[LETTERS_ONLY[name]]
    total_pts = sum(len(sp) for sp in subpaths)
    mask = rasterize(subpaths)
    fill_frac = mask.mean()
    pts = sample_points(mask, N_POINTS)
    print(f"{name}: {len(subpaths)} subpaths, {total_pts} flattened pts, "
          f"fill={fill_frac:.3f}, sampled={len(pts)} traveler points")
    results[name] = pts
    np.save(OUT + f"\\logo_pts_{name}.npy", pts)
    from PIL import Image
    Image.fromarray((mask*255).astype(np.uint8)).save(OUT + f"\\_logo_mask_{name}.png")

print("done")

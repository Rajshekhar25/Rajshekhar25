"""
Emits the traveler layer as SVG: ~320 small dots that fade in as the
portrait fades out, hold in TypeScript formation, morph to Python, hold,
morph to C++, hold, then fade out as the portrait fades back in.

Timing uses the SAME lesson learned building the loop layer: keyTimes are
elapsed-since-this-element's-own-begin, not since document t=0. begin and
dur are matched exactly to the loop layer's so both stay in lockstep.
"""

import os
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import io
import numpy as np

SCRATCH = os.path.join(_REPO, "scripts", "_build")

pts_ts  = np.load(SCRATCH + r"\traveler_ts.npy")
pts_py  = np.load(SCRATCH + r"\traveler_py.npy")
pts_cpp = np.load(SCRATCH + r"\traveler_cpp.npy")
N = len(pts_ts)

HANDOFF_AT = 3.0
LOOP_DUR = 14.2
T_OUT_END   = 4.3   # traveler becomes visible, TypeScript formed
T_LOGO1_END = 6.3
T_TR2_END   = 7.6   # Python formed
T_LOGO2_END = 9.6
T_TR3_END   = 10.9  # C++ formed
T_LOGO3_END = 12.9
T_IN_END    = 14.2  # traveler fades out, C++ shape held while invisible

def ef(t_abs):
    return round((t_abs - HANDOFF_AT) / LOOP_DUR, 4)

keytimes_abs = [HANDOFF_AT, T_OUT_END, T_LOGO1_END, T_TR2_END, T_LOGO2_END,
                T_TR3_END, T_LOGO3_END, T_IN_END, HANDOFF_AT + LOOP_DUR]
kt = [ef(t) for t in keytimes_abs]
assert kt == sorted(kt), kt
kt_str = ";".join("%.4f" % v for v in kt)

opacity_vals = "0;1;1;1;1;1;1;0;0"

DOT_R = 1.6

elems = []
for i in range(N):
    x_seq = [pts_ts[i,0], pts_ts[i,0], pts_ts[i,0], pts_py[i,0], pts_py[i,0],
              pts_cpp[i,0], pts_cpp[i,0], pts_cpp[i,0], pts_ts[i,0]]
    y_seq = [pts_ts[i,1], pts_ts[i,1], pts_ts[i,1], pts_py[i,1], pts_py[i,1],
              pts_cpp[i,1], pts_cpp[i,1], pts_cpp[i,1], pts_ts[i,1]]
    x_str = ";".join("%.2f" % v for v in x_seq)
    y_str = ";".join("%.2f" % v for v in y_seq)
    elems.append(
        f'<circle r="{DOT_R}" fill="var(--portrait-ink)" opacity="0">'
        f'<animate attributeName="cx" values="{x_str}" keyTimes="{kt_str}" '
        f'dur="{LOOP_DUR}s" begin="{HANDOFF_AT}s" repeatCount="indefinite"/>'
        f'<animate attributeName="cy" values="{y_str}" keyTimes="{kt_str}" '
        f'dur="{LOOP_DUR}s" begin="{HANDOFF_AT}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="{opacity_vals}" keyTimes="{kt_str}" '
        f'dur="{LOOP_DUR}s" begin="{HANDOFF_AT}s" repeatCount="indefinite"/>'
        f'</circle>'
    )

traveler_svg = "\n".join(elems)
print("traveler layer: %d dots, %d bytes" % (N, len(traveler_svg)))
io.open(SCRATCH + r"\traveler_layer.svg", "w", encoding="utf-8").write(traveler_svg)

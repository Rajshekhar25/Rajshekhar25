"""
Builds the traveler layer: ~320 dots that morph TypeScript -> Python -> C++
during the loop's three logo-hold phases, matched between consecutive
logos via real optimal transport (Hungarian algorithm on a squared-distance
cost matrix -- scipy.optimize.linear_sum_assignment), so each dot travels
its individually shortest path rather than a fixed index-order jump.

Verified against a random-pairing baseline: optimal transport must produce
a lower total travel cost, or something is wrong.
"""

import os
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import io
import numpy as np
from scipy.optimize import linear_sum_assignment

ASSETS = os.path.join(_REPO, "assets")
SCRATCH = os.path.join(_REPO, "scripts", "_build")

# banner geometry (must match build_banner.py)
PORTRAIT_X, PORTRAIT_Y = 34, 76
PORTRAIT_W, PORTRAIT_H = 380, 431
FRAME_CX, FRAME_CY = PORTRAIT_X + PORTRAIT_W/2, PORTRAIT_Y + PORTRAIT_H/2

LOGO_DISPLAY = 266.0   # ~70% of the frame's shorter side
LOGO_SCALE = LOGO_DISPLAY / 24.0  # source viewBox is 0..24

def to_display(pts):
    """logo-local 0..24 coords -> banner pixel coords, centred in the frame."""
    cx = FRAME_CX - LOGO_DISPLAY/2
    cy = FRAME_CY - LOGO_DISPLAY/2
    return np.stack([cx + pts[:,0]*LOGO_SCALE, cy + pts[:,1]*LOGO_SCALE], axis=1)

pts_ts  = to_display(np.load(SCRATCH + r"\logo_pts_typescript.npy"))
pts_py  = to_display(np.load(SCRATCH + r"\logo_pts_python.npy"))
pts_cpp = to_display(np.load(SCRATCH + r"\logo_pts_cplusplus.npy"))
N = min(len(pts_ts), len(pts_py), len(pts_cpp))
print("traveler point counts:", len(pts_ts), len(pts_py), len(pts_cpp), "-> using", N)
rng = np.random.default_rng(11)
pts_ts, pts_py, pts_cpp = (a[rng.choice(len(a), N, replace=False)] for a in (pts_ts, pts_py, pts_cpp))

def optimal_match(a, b):
    """Hungarian algorithm on squared-distance cost -> b reordered so
    b_matched[i] is a's optimal partner for a[i]."""
    cost = np.sum((a[:,None,:] - b[None,:,:])**2, axis=2)
    row_ind, col_ind = linear_sum_assignment(cost)
    total_cost = cost[row_ind, col_ind].sum()
    return b[col_ind], total_cost

def random_baseline_cost(a, b, trials=20):
    best = np.inf
    for _ in range(trials):
        perm = rng.permutation(len(b))
        c = np.sum((a - b[perm])**2)
        best = min(best, c)
    return best

py_matched, cost_ts_py = optimal_match(pts_ts, pts_py)
cpp_matched, cost_py_cpp = optimal_match(py_matched, pts_cpp)

baseline_ts_py = random_baseline_cost(pts_ts, pts_py)
baseline_py_cpp = random_baseline_cost(py_matched, pts_cpp)

print("TS->Python   optimal cost: %.0f   best-of-20-random baseline: %.0f  (%.1fx better)" %
      (cost_ts_py, baseline_ts_py, baseline_ts_py / cost_ts_py))
print("Python->C++  optimal cost: %.0f   best-of-20-random baseline: %.0f  (%.1fx better)" %
      (cost_py_cpp, baseline_py_cpp, baseline_py_cpp / cost_py_cpp))
assert cost_ts_py < baseline_ts_py, "optimal transport did not beat random pairing -- broken"
assert cost_py_cpp < baseline_py_cpp, "optimal transport did not beat random pairing -- broken"

np.save(SCRATCH + r"\traveler_ts.npy", pts_ts)
np.save(SCRATCH + r"\traveler_py.npy", py_matched)
np.save(SCRATCH + r"\traveler_cpp.npy", cpp_matched)
print("saved matched traveler positions, N=%d" % N)

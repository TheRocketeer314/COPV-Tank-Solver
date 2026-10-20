import numpy as np
import ezdxf
from scipy.interpolate import splprep, splev

SCALE = 1000.0      # 1000 if your CSV is in metres, 1.0 if already mm
TOL   = 0.01        # max allowed deviation from your data, in mm
DEGREE = 3

def load(fn):
    d = np.loadtxt(fn, delimiter=",", skiprows=1)   # skips the header row
    return d * SCALE                                # columns: x, r

def fit(pts):
    # drop consecutive duplicate points (splprep fails on them)
    keep = np.r_[True, np.any(np.diff(pts, axis=0) != 0, axis=1)]
    pts = pts[keep]
    tck, _ = splprep([pts[:, 0], pts[:, 1]], k=DEGREE, s=len(pts) * TOL**2)
    return tck

def add_spline(msp, tck):
    t, c, k = tck
    n = len(t) - k - 1                      # splprep pads c with trailing zeros
    ctrl = [(c[0][i], c[1][i], 0.0) for i in range(n)]
    sp = msp.add_spline(degree=k)
    sp.control_points = ctrl
    sp.knots = list(t)
    # actual end points of the fitted curve (for the closing lines)
    (x0, x1), (y0, y1) = splev([0.0, 1.0], tck)
    return (x0, y0, 0.0), (x1, y1, 0.0)
import numpy as np

from ..illuminants import whitepoints_cie1931
from ._color_space import ColorSpace


class CIELAB(ColorSpace):
    def __init__(self, whitepoint=whitepoints_cie1931["D65"]):
        super().__init__("CIELAB", ("L*", "a*", "b*"), 0)
        self.whitepoint = whitepoint

    def from_xyz100(self, xyz):
        def f(t):
            delta = 6 / 29
            out = np.array(t, dtype=float)
            is_greater = out > delta ** 3
            out[is_greater] = 116 * np.cbrt(out[is_greater]) - 16
            out[~is_greater] = out[~is_greater] / (delta / 2) ** 3
            return out

        xyz = np.asarray(xyz)

        fx, fy, fz = f((xyz.T / self.whitepoint).T)
        return np.array([fy, 125 / 29 * (fx - fy), 50 / 29 * (fy - fz)])

    def to_xyz100(self, lab):
        def f1(t):
            delta = 6 / 29
            out = np.array(t, dtype=float)
            is_greater = out > 2 / 29
            out[is_greater] = (out[is_greater] + 4 / 29) ** 3
            out[~is_greater] = 3 * delta ** 2 * out[~is_greater]
            return out

        lab = np.asarray(lab)
        L, a, b = lab
        return (
            f1(np.array([L / 116 + a / 500, L / 116, L / 116 - b / 200])).T
            * self.whitepoint
        ).T

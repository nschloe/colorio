import numpy as np

import colorio


def test_show():
    cs = colorio.cs.CIELAB()
    # cs = colorio.cs.CIEHCL()
    # cs = colorio.cs.CIELCH()
    # cs = colorio.cs.OsaUcs()
    # cs = colorio.cs.IPT()
    colorio.data.HungBerns().show(cs)


def test_residuals():
    cs = colorio.cs.CIELAB()
    ref = 4.3485681879882305
    res = np.average(colorio.data.HungBerns().stress(cs))
    print(res)
    assert abs(res - ref) < 1.0e-14 * ref


if __name__ == "__main__":
    test_show()

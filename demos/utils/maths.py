import numpy as np


def __cos_interp(a, b, cnt):
    ts = np.linspace(0, 1, cnt)
    return a + (b - a) * (1 - np.cos(np.pi * ts)) / 2.0


def interpolate(vs, cnt):
    fp = []
    for i in range(len(vs) - 1):
        fp.append(__cos_interp(vs[i], vs[i + 1], cnt))
    fp = np.array(fp).flatten()
    x = np.linspace(1, cnt, cnt)
    xp = np.linspace(1, cnt, len(fp))
    return np.interp(x, xp, fp)

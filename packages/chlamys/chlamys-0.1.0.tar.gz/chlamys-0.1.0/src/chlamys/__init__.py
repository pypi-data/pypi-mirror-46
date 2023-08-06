__version__ = '0.1.0'

from itertools import chain

import numpy as np
import sympy as sy
from scipy import spatial


class Delaunay1D:
    def __init__(self, base):
        indices = np.argsort(base)

        self.simplices = np.stack([indices[:-1], indices[1:]])
        self.sorted_base = base[indices]
        self.convex_hull = indices[[0, -1]]

    def find_simplex(self, x):
        x = x.ravel()
        sorted_base = self.sorted_base

        found = np.searchsorted(sorted_base, x) - 1
        found[x == sorted_base[0]] = 0
        found[found == len(sorted_base)] = -1

        return found


def plane(x, bases, heights):
    bases, heights = map(np.array, [bases, heights])

    alpha = np.linalg.solve(bases[1:] - bases[0], heights[1:] - heights[0])
    return (np.stack(x, axis=-1) - bases[0]).dot(alpha) + heights[0]


def cubic_patch(interpolands, bases, heights, grad):
    dim = bases.shape[1]
    x = [sy.Symbol('x_{}'.format(i)) for i in range(dim)]

    monomials = sy.expand((1 + sum(x))**3).args
    monomials = [m/sy.lambdify(x, m)(*(1 for _ in x)) for m in monomials]

    monomials_f = [sy.lambdify(x, m) for m in monomials]
    monomials_grad = ([sy.lambdify(x, m.diff(x[i])) for m in monomials] for i in range(dim))

    lhs = iter([])
    for fs in chain([monomials_f], monomials_grad):
        lhs = chain(lhs, [np.array([f(*x_val) for f in fs]) for x_val in zip(*np.transpose(bases))])
    lhs = np.array(list(lhs))
    rhs = np.ravel([heights] + np.transpose(grad).tolist())

    coeffs = np.linalg.pinv(lhs).dot(rhs)

    lbda = sy.lambdify(x, sum((c*m for c, m in zip(coeffs, monomials))), "numpy")
    return lbda(*interpolands)


def _interp_functor(interpolator, interpolands, anchors_base, *anchors_args):
    anchors_base = np.array(anchors_base)
    anchors_args = tuple(map(np.array, anchors_args))
    interpolands = tuple(map(np.array, interpolands))

    delaunay = (spatial.Delaunay(anchors_base) if anchors_base.shape[1] >= 2
                else Delaunay1D(anchors_base[:, 0]))
    simplex_map = delaunay.find_simplex(np.stack(interpolands, axis=-1))
    simplex_outer_loc = np.unique(delaunay.convex_hull)

    simplex_outer_base = anchors_base[simplex_outer_loc]
    simplex_outer_args = tuple(arg[simplex_outer_loc] for arg in anchors_args)
    interp = (interpolator(interpolands, simplex_outer_base, *simplex_outer_args)
              if len(simplex_outer_loc) == anchors_base.shape[0] - 1
              else np.full(interpolands[0].shape, np.nan))

    for i, s in enumerate(delaunay.simplices):
        mask = simplex_map == i
        masked_interpolands = tuple(dim[mask] for dim in interpolands)

        simplex_base = anchors_base[s]
        simplex_args = tuple(arg[s] for arg in anchors_args)

        interp[mask] = interpolator(masked_interpolands, simplex_base,
                                    *simplex_args)

    return interp


def interp_levels(anchors_base, anchors_height, interpolands):
    return _interp_functor(plane, interpolands, anchors_base, anchors_height)


def interp_1st_order(anchors_base, anchors_height, anchors_grad, interpolands):
    return _interp_functor(cubic_patch, interpolands, anchors_base,
                           anchors_height, anchors_grad)


def _dtanh_dx(x):
    return 1 - np.tanh(x)**2


def test_function(*xs):
    return sum(map(np.tanh, xs[::2])) + sum(map(np.cosh, xs[1::2]))


def test_gradient(*xs):
    grad = list(xs)
    grad[::2] = list(map(_dtanh_dx, xs[::2]))
    grad[1::2] = list(map(np.sinh, xs[1::2]))
    return tuple(grad)

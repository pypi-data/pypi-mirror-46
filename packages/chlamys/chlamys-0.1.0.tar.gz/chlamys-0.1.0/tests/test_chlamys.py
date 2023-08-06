from itertools import product

import numpy as np

import chlamys as ch


def test_interp_levels():
    np.random.seed(0)
    d = 7
    n = 20

    anchors_base = np.array(list(product(range(2), repeat=d)))
    anchors_height = ch.test_function(*np.transpose(anchors_base))
    interpolands = np.random.rand(d, n)

    ys_bench = np.mean(anchors_height)
    ys_hat = ch.interp_levels(anchors_base, anchors_height, interpolands)
    ys = ch.test_function(*interpolands)

    assert np.max(np.abs(ys - ys_hat)) < np.max(np.abs(ys - ys_bench))


def test_interp_1st_order():
    np.random.seed(0)
    d = 3
    n = 20

    anchors_base = np.array(list(product(range(2), repeat=d)))
    anchors_height = ch.test_function(*np.transpose(anchors_base))
    anchors_grad = np.stack(ch.test_gradient(*np.transpose(anchors_base)), axis=-1)
    interpolands = np.random.rand(d, n)

    ys_bench = ch.interp_levels(anchors_base, anchors_height, interpolands)
    ys_hat = ch.interp_1st_order(anchors_base, anchors_height, anchors_grad, interpolands)
    ys = ch.test_function(*interpolands)

    assert np.max(np.abs(ys - ys_hat)) < np.max(np.abs(ys - ys_bench))

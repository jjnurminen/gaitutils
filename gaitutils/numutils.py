# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 11:17:10 2016

Misc numerical utils

@author: jnu@iki.fi
"""

import numpy as np
from scipy.signal import medfilt


def rising_zerocross(x):
    """ Return indices of rising zero crossings in sequence,
    i.e. n where x[n] >= 0 and x[n-1] < 0 """
    x = np.array(x)  # this should not hurt
    return np.where(np.logical_and(x[1:] >= 0, x[:-1] < 0))[0] + 1


def falling_zerocross(x):
    return rising_zerocross(-x)


def isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def _baseline(data):
    """ Baseline data using histogram. Subtracts the most prominent
    signal level """
    data = np.array(data)
    nbins = int(len(data) / 10)  # exact n of bins should not matter
    ns, edges = np.histogram(data, bins=nbins)
    peak_ind = np.where(ns == np.max(ns))[0][0]
    return data - np.mean(edges[peak_ind:peak_ind+2])


def center_of_pressure(F, M, dz):
    """ Compute CoP according to AMTI instructions. The results differ
    slightly (few mm) from Nexus, for unknown reasons (different filter?)
    See http://health.uottawa.ca/biomech/courses/apa6903/amticalc.pdf """
    FP_FILTFUN = medfilt  # filter function
    FP_FILTW = 5  # median filter width
    fx, fy, fz = tuple(F.T)  # split columns into separate vars
    mx, my, mz = tuple(M.T)
    fz = FP_FILTFUN(fz, FP_FILTW)
    nz_inds = np.where(np.abs(fz) > 0)[0]  # only divide on nonzero inds
    cop = np.zeros((fx.shape[0], 3))
    cop[nz_inds, 0] = -(my[nz_inds] + fx[nz_inds] * dz)/fz[nz_inds]
    cop[nz_inds, 1] = (mx[nz_inds] - fy[nz_inds] * dz)/fz[nz_inds]
    return cop


def change_coords(pts, wR, wT):
    """ Translate pts (N x 3) into a new coordinate system described by
    rotation matrix wR and translation vector wT """
    pts = np.array(pts)
    return np.dot(wR, pts.T).T + wT

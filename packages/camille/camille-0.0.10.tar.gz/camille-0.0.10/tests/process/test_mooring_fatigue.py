#!/usr/bin/env python
import numpy as np
import pandas as pd
import pytest

from camille import process
from camille.process.mooring_fatigue import _calculate_stress
from camille.process.mooring_fatigue import _calc_damage
from camille.process.mooring_fatigue import _is_bad_data
from camille.process.mooring_fatigue import sncurve
import math

refcase = [0.60727647, 0.14653493, 0.19643957, 0.56821631, 0.88833878, 0.29612997,
           0.59539649, 0.6996683,  0.10524973, 0.12334626, 0.68401331, 0.85985292,
           0.73141117, 0.36808646, 0.94015761, 0.85626572, 0.76956161, 0.49777263,
           0.54066458, 0.45931667, 0.82204694, 0.76816398, 0.66417278, 0.62238591,
           0.61302659, 0.0158001,  0.35254166, 0.54150519, 0.14868205, 0.91848263,
           0.8989403,  0.90866213, 0.831834,   0.48128077, 0.60999729, 0.78850529,
           0.67725795, 0.76098028, 0.96626931, 0.91693159, 0.19347573, 0.4920361,
           0.16060596, 0.10603582, 0.0017221,  0.6250337,  0.43623379, 0.54612575,
           0.00411415, 0.91371242, 0.08600793, 0.77993431, 0.89695114, 0.43309567,
           0.70051438, 0.05484055, 0.0673957,  0.68068416, 0.12452928, 0.00811467,
           0.33861137, 0.61719287, 0.49407856, 0.8300253,  0.29934456, 0.7107892,
           0.38225825, 0.02715285, 0.0189073,  0.68926121, 0.46134276, 0.25709821,
           0.46942654, 0.68086762, 0.3117921,  0.89299606, 0.43332419, 0.04576419,
           0.09044587, 0.28137508, 0.365343,   0.94461639, 0.48949621, 0.03472242,
           0.79210514, 0.94612641, 0.25696703, 0.61546048, 0.04270415, 0.6681445,
           0.79452558, 0.41156153, 0.4671666,  0.01783284, 0.8529705,  0.56580293,
           0.62133836, 0.74723755, 0.28597705, 0.7421038]


mooring_fatigue_ref = [6.4859627078e-009, 3.5345447785e-009, 3.9938747139e-009,
                       803.74980110e-012, 117.05442998e-012, 10.982139239e-009,
                       1.0279664453e-009, 328.62042941e-012, 1.8520613514e-009,
                       12.749063259e-009, 8.3602889329e-009, 7.0418189868e-009,
                       3.4846384931e-009, 8.1067037076e-009, 1.7290944491e-009,
                       7.9628828987e-009, 17.716393440e-009, 13.768516462e-009,
                       13.476337649e-009, 2.5509061348e-009]

sn_curve = { 'logA': math.log10(6e10),
             'm': 3,
             't': 0,
             'tref': 25,
             'k': 0 }

def test_process():
    series = pd.Series(data=refcase, name='bridle1')
    res = process.mooring_fatigue(series,
                                  window_length=1,
                                  fs=5,
                                  sn_curve=sn_curve)
    assert np.allclose(res.values.T, mooring_fatigue_ref)


def test_index_set_to_window_start():
    index = pd.date_range(start='1/1/2018', periods=len(refcase))
    series = pd.Series(data=refcase, name='bridle1', index=index)

    assert_index_set_to_window_start(series, 1, 5, index)
    assert_index_set_to_window_start(series, 2, 5, index)
    assert_index_set_to_window_start(series, 2, 7, index)
    assert_index_set_to_window_start(series, 4, 3, index)


def test_calc_damage():
    damage = _calc_damage(refcase, sn_curve)
    assert np.allclose( damage, 1.34471920175778e-010 )


def test_floating_point_roundoff_causing_unexpected_zero():
    try:
        _calc_damage(np.array([22.169702635236565, 22.16970263523657,
                               22.169702635236565, 22.16970263523657],
                               dtype=np.float64),
                               sn_curve)
    except ValueError:
        pytest.fail("Exception raised, possibly caused by floating point "
                    "roundoff creating unexpected zero value")


def test_nan():
    data = [np.nan, 0, 0, 2, np.nan]
    is_bad = _is_bad_data(data, 100)
    assert is_bad


def test_valid():
    data = [1, 0, 0, 2, 1]
    is_bad = _is_bad_data(data, 100)
    assert not is_bad


def test_sudden_jump():
    data = [0, 0, 0, 1000, 0]
    is_bad = _is_bad_data(data, 100)
    assert is_bad


def test_constant():
    data = [1, 1, 1, 1, 1]
    is_bad = _is_bad_data(data, 100)
    assert is_bad


def test_calculate_stress():
    signal = np.array([2, 1, 3, 2, 4])
    ref = np.array([0.07307389, 0.03653695, 0.10961084,
                    0.07307389, 0.14614779])
    stress = _calculate_stress(signal)
    assert np.allclose(stress, ref)


def assert_index_set_to_window_start(
        series, window_length, fs, unprocessed_series_index):
    nsamples = len(series)
    res = process.mooring_fatigue(series,
                                  window_length=window_length,
                                  fs=fs,
                                  sn_curve=sn_curve)
    step = window_length * fs
    first_invalid = nsamples - (nsamples % step)
    assert (res.index == unprocessed_series_index[:first_invalid:step]).all()


def test_scalar_params():
    x = [12.73, 47.83, 41.05, 30.05, 24.58]
    expected = [2.90847971e7, 5.48340227e5, 8.67384717e5,
                2.21114804e6, 4.04022558e6]

    result = sncurve( x,
                      logA=np.log10(6e10),
                      m=3, t=0,
                      tref=25,
                      k=0 )

    assert np.allclose(result, expected)


def test_array_params():
    x = [22.49, 25.13, 4.83, 30.44]
    expected = [3.63122134e9, 2.08467115e9, 7.94811873e12, 7.99423221e8]

    result = sncurve(x,
                     logA=[12.192,16.32],
                     m=[3.0,5.0],
                     k=0.05,
                     tref=25,
                     t=0)

    assert np.allclose(result, expected)

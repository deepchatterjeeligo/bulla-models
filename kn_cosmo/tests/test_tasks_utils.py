"""Tests for utility functions"""
from .. import utils


def test_get_meta_information():
    res = utils._get_meta_information(
        'sed_cos_theta_0.7_mej_0.06_phi_15_T_3.0e+03.txt'
    )
    assert res[0] == 0.7
    assert res[1] == 0.06
    assert res[2] == 15.0
    assert res[3] == 3000.0

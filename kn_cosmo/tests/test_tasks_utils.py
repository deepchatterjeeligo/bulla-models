"""Tests for utility functions"""
import os

from unittest.mock import patch, Mock
import pkg_resources

from .. import utils


def test_get_meta_information():
    res = utils._get_meta_information(
        'sed_cos_theta_0.7_mej_0.06_phi_15_T_3.0e+03.txt'
    )
    assert res[0] == 0.7
    assert res[1] == 0.06
    assert res[2] == 15.0
    assert res[3] == 3000.0


@patch('numpy.savetxt')
def test_snana_format_data_extraction(fake_np_savetxt):
    mock_arguments = Mock()
    mock_arguments.input = pkg_resources.resource_filename(
        __name__, "data/nph1.0e+06_mej0.01_phi15_T3.0e+03.txt")
    mock_arguments.outdir = '/tmp'
    mock_arguments.snana_sed_format = True
    mock_arguments.verbose = False

    with patch('kn_cosmo.utils._get_args_for_extract_data',
               return_value=mock_arguments):
        utils.extract_data()
    arg_list = fake_np_savetxt.call_args_list
    filename = arg_list[0][0][0]
    snana_data = arg_list[0][0][1]
    assert os.path.basename(
        filename
    ) == "sed_cos_theta_0.0_mej_0.01_phi_15_T_3.0e+03.txt"
    assert snana_data.shape == (60, 3)

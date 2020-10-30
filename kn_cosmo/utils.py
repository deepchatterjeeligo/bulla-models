"""Utility functions"""
import os
import re
from argparse import ArgumentParser

import numpy as np
import pkg_resources

from . import config


def extract_data():
    args = _get_args_for_extract_data()
    filename = pkg_resources.resource_filename(__name__, args.input)
    try:
        nph, mej, phi, temp = re.match(config.FILENAME_PATTERN,  # noqa: F821
                                       os.path.basename(filename)).groups()
    except AttributeError:
        nph, mej, phi = re.match(config.FILENAME_PATTERN_NO_T,  # noqa: F821
                                 os.path.basename(filename)).groups()
        temp = ""


    # header
    with open(args.input) as f:
        header = [next(f) for _ in range(3)]  # FIXME: assume top 3 lines
    (n_obs, *_), (n_wave, *_), (n_time, t_i, t_f, *_) = list(
        map(lambda z: z.split(' '), header)
    )
    n_obs = int(n_obs)
    n_wave = int(n_wave)
    n_time = int(n_time)
    t_i = float(t_i)
    t_f = float(t_f)

    # data
    data = np.loadtxt(args.input, skiprows=3)  # FIXME: hardcoding skiprows

    # FIXME: add command line args
    outdir = args.outdir
    if args.verbose:
        print(f"Saving SEDs to {outdir}")

    cos_thetas = np.linspace(0, 1, n_obs)
    for idx, cos_theta in enumerate(cos_thetas):
        fname = config.OUTPUT_SED_FILENAME.format(cos_theta, mej, phi, temp) if temp\
            else config.OUTPUT_SED_FILENAME_NO_T.format(cos_theta, mej, phi)
        sed_cos_theta = data[idx * n_wave: (idx + 1) * n_wave]
        if not args.snana_sed_format:
            np.savetxt(os.path.join(outdir, fname), sed_cos_theta)
            continue
        wave, *fluxes = sed_cos_theta.T
        dt = (t_f - t_i)/n_time
        phases = np.arange(t_i + 0.5*dt, t_f, dt)
        snana_data_format = list()
        for idx, phase in enumerate(phases):
            snana_data_format.append((phase * np.ones(wave.shape),
                                     wave, fluxes[idx]))
        snana_data_format = np.hstack(snana_data_format).T
        np.savetxt(os.path.join(outdir, fname), snana_data_format,
                   fmt=("%.2f", "%.2f", "%.4e"))


def _get_meta_information(filename):
    """Read filename and parse meta information"""
    cos_theta, mej, phi, temp = re.match(
        config.OUTPUT_SED_FILENAME_REGEXP,
        os.path.basename(filename)
    ).groups()
    return list(
        map(float, (cos_theta, mej, phi, temp))
    )


def _get_args_for_extract_data():
    parser = ArgumentParser(
        description="Extract data from kilonova models."
        "Assume datafiles of the form nph1.0e+06_mej0.01_phi15_T3.0e+03.txt"
    )
    parser.add_argument("-o", "--outdir", required=True,
                        help="Output directory")
    parser.add_argument("-d", "--input", required=True,
                        help="SED filename")
    parser.add_argument(
        "--snana-sed-format", action='store_true', default=False,
        help="3 column format - phase, wave, flux"
    )
    parser.add_argument("-v", "--verbose", action='store_true',
                        default=False, help="Verbosity")
    args = parser.parse_args()
    return args

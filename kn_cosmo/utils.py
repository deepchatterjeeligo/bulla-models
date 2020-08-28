"""Utility functions"""
import os
from argparse import ArgumentParser

import pkg_resources


def extract_data():
    args = _get_args()
    filename = pkg_resources.resource_filename(__name__, args.input)
    nph, mej, phi, temp = re.match(FILENAME_PATTERN,
                                   os.path.basename(filename)).groups()

def _get_args():
    parser = ArgumentParser(description="Extract seds from kilonova models")
    parser.add_argument("-d", "--input", required=True,
                        help="SED filename")
    args = parser.parse_args()
    return args

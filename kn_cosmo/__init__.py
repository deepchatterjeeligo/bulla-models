import re

from .utils import *
from . import lightcurves

FILENAME_REGEXP = "nph(.*)_mej(.*)_phi(.*)_T(.*)\.txt"
FILENAME_PATTERN = re.compile(FILENAME_REGEXP)

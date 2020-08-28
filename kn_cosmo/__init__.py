import re

from .utils import *  # noqa: F401, F403

FILENAME_REGEXP = r"nph(.*)_mej(.*)_phi(.*)_T(.*)\.txt"
FILENAME_PATTERN = re.compile(FILENAME_REGEXP)

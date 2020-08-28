import re

FILENAME_REGEXP = r"nph(.*)_mej(.*)_phi(.*)_T(.*)\.txt"
FILENAME_PATTERN = re.compile(FILENAME_REGEXP)
OUTPUT_SED_FILENAME = r"sed_cos_theta_{:.1f}_mej_{}_phi_{}_T_{}.txt"
OUTPUT_SED_FILENAME_REGEXP = r"sed_cos_theta_(.*)_mej_(.*)_phi_(.*)_T_(.*).txt"

__all__ = (
    FILENAME_REGEXP, FILENAME_PATTERN, OUTPUT_SED_FILENAME
)

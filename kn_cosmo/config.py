import re

FILENAME_REGEXP = r"nph(.*)_mej(.*)_phi(.*)_T(.*)\.txt"
FILENAME_REGEXP_NO_T = r"nph(.*)_mej(.*)_phi(.*)\.txt"
FILENAME_PATTERN = re.compile(FILENAME_REGEXP)
FILENAME_PATTERN_NO_T = re.compile(FILENAME_REGEXP_NO_T)
OUTPUT_SED_FILENAME = r"sed_cos_theta_{:.1f}_mej_{}_phi_{}_T_{}.txt"
OUTPUT_SED_FILENAME_NO_T = r"sed_cos_theta_{:.1f}_mej_{}_phi_{}.txt"
OUTPUT_SED_FILENAME_REGEXP = r"sed_cos_theta_(.*)_mej_(.*)_phi_(.*)_T_(.*).txt"
OUTPUT_SED_FILENAME_REGEXP_NO_T = r"sed_cos_theta_(.*)_mej_(.*)_phi_(.*).txt"

__all__ = (
    FILENAME_REGEXP, FILENAME_REGEXP_NO_T,
    FILENAME_PATTERN, FILENAME_PATTERN_NO_T,
    OUTPUT_SED_FILENAME, OUTPUT_SED_FILENAME_NO_T
)

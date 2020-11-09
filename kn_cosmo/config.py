import re

FILENAME_REGEXP = r"nph([0-9]+.*)_mej([0-9]+.*)_phi(.*)_T(.*)\.txt"
FILENAME_REGEXP_NO_T = r"nph([0-9]+.*)_mej([0-9]+.*)_phi(.*)\.txt"
FILENAME_REGEXP_BHNS = r"nph([0-9]+.*)_mejdyn([0-9]+.*)_mejwind([0-9]+.*)_phi(.*).txt"
FILENAME_PATTERN = re.compile(FILENAME_REGEXP)
FILENAME_PATTERN_NO_T = re.compile(FILENAME_REGEXP_NO_T)
FILENAME_PATTERN_BHNS = re.compile(FILENAME_REGEXP_BHNS)
OUTPUT_SED_FILENAME = r"sed_cos_theta_{:.1f}_mej_{}_phi_{}_T_{}.txt"
OUTPUT_SED_FILENAME_NO_T = r"sed_cos_theta_{:.1f}_mej_{}_phi_{}.txt"
OUTPUT_SED_FILENAME_BHNS = r"sed_cos_theta_{:.1f}_mejdyn_{}_mejwind_{}_phi_{}.txt"
OUTPUT_SED_FILENAME_REGEXP = r"sed_cos_theta_([0-9]+.*)_mej_(.*)_phi_(.*)_T_(.*).txt"
OUTPUT_SED_FILENAME_REGEXP_NO_T = r"sed_cos_theta_([0-9]+.*)_mej_([0-9]+.*)_phi_(.*).txt"
OUTPUT_SED_FILENAME_REGEXP_BHNS = r"sed_cos_theta_([0-9]+.*)_mejdyn_([0-9]+.*)_mejwind_([0-9]+.*)_phi_(.*).txt"

__all__ = (
    FILENAME_REGEXP, FILENAME_REGEXP_NO_T, FILENAME_REGEXP_BHNS,
    FILENAME_PATTERN, FILENAME_PATTERN_NO_T, FILENAME_PATTERN_BHNS,
    OUTPUT_SED_FILENAME, OUTPUT_SED_FILENAME_NO_T, OUTPUT_SED_FILENAME_BHNS
)

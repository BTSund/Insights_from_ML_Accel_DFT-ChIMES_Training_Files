"""

    Configuration file for the ChIMES potential energy surface generator (pes_generator.py)

	Don't forget to set PAIR CHEBYSHEV PENALTY SCALING to zero in the parameter file.

"""

CHMS_REPO  = "/g/g14/sundberg3/codes/ChCalc_Tab/"

PARAM_FILE = "/p/vast1/sundberg3/Model_Dev/Funct_test/PW91_29/params.txt"

PAIRTYPES  = [0] # Pair type index for scans, i.e. number after "PAIRTYPE PARAMS:" in parameter file
PAIRSTART  = [1.55] # Smallest distance for scan
PAIRSTOP   = [7.0] # Largest distance for scan
PAIRSTEP   = [0.001] # Step size for scan
TRIPTYPES  = [0] # Triplet type index for scans, i.e. number after "TRIPLETTYPE PARAMS:" in parameter file
TRIPSTART  = [1.55] # Smallest distance for scan:
TRIPSTOP   = [6] # Largest distance for scan
TRIPSTEP   = [0.05] # Step size for scan

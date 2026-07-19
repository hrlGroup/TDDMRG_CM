import numpy as np


#== General ==#
prefix = 'H2O'

#== System ==#
atoms = \
            '''
            O   0.000   0.000   0.107;
            H   0.000   0.785  -0.427;
            H   0.000  -0.785  -0.427;
            '''
basis = 'cc-pvdz'
symmetry = 'C2v'
charge = 0
twosz = 0
wfnsym = 0
source = 'rhf'

localize = False

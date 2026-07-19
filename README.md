

# TDDMRG_CM

TDDMRG_CM is a Python program designed to make the workflow of simulating charge migration using the time-dependent density matrix renormalization group (TDDMRG) easy and straightforward. It consists of three main functionalities: ground state DMRG, application of annihilation operator, and time evolution using TDDMRG. This program is built on top of BLOCK2 (https://github.com/block-hczhai/block2-preview) and PySCF (https://github.com/pyscf/pyscf), therefore, these two programs must already be installed before using TDDMRG_CM. 


## Installation from GitHub
After making sure that PySCF and BLOCK2 have been successfully installed, perform the following steps to install TDDMRG_CM

1. Create the directory where your local TDDMRG_CM git repository will be cloned (downloaded) to, and go to this directory.
2. Run `git clone https://github.com/iswhy/TDDMRG_CM.git`, a directory called `TDDMRG_CM` will be created.
3. Add the following lines to your `~/.bashrc` file
    ```
    export PYTHONPATH=/path/to/TDDMRG_CM:$PYTHONPATH
    export PATH=/path/to/TDDMRG_CM:$PATH
    export PATH=/path/to/TDDMRG_CM/orbs_generate:$PATH
    export PATH=/path/to/TDDMRG_CM/observables:$PATH
    ```
    where the `/path/to/TDDMRG_CM` is to be replaced with the actual path leading to the `TDDMRG_CM` directory resulting from Step 2 above.


## Running a TDDMRG_CM simulation
Once installed, the program can be run by executing `cm_dmrg input_file.py`, where `input_file.py` is a Python script containing [input parameters](#input-parameters) for your simulation. You will most likely want to run TDDMRG_CM in parallel, ***at the moment, TDDMRG_CM only supports shared memory parallel execution***.

The typical workflow of TDDMRG_CM is that first the user decides which molecule to simulate, determines its geometry, and calculates the site orbitals and save their atomic orbital (AO) coefficients (e.g. computed using PySCF) as a matrix in a numpy array file. The user runs a ground state DMRG calculation for the chosen molecule using the previously determined geometry and orbitals. The converged ground state MPS is then fed into the annihilation operator simulation to remove an electron from a particular orbital in the ground state MPS. The output MPS of the annihilation operator task will then be used as the initial state for the subsequent TDDMRG simulation.

The recognized input parameters are defined [below](#input-parameters). The input parsing environment of TDDMRG_CM has been designed so that ***input files are essentially a normal Python `*.py` file***.  This offers high flexibility for users in providing the values of input parameters to the program. Since it is an ordinary Python file, you can write the code to calculate the value of a certain input parameter right inside the input file. As an example, you want to initiate the ground state DMRG iterations from an MPS having a certain set of orbital occupancies (see `gs_occs` input definition below), and these occupancies are obtained from a separate (and less accurate) quantum chemistry calculation. Let's say that this other calculation returns a one-particle reduced density matrix (RDM) as a matrix named `rdm.npy` in the parent folder. Then, you can give a value to the `gs_occs` input parameter in the following manner inside your input file.
```python
import numpy as np
...
rdm = np.load('../rdm.npy')
gs_occs = np.diag(rdm)
...
```
The program views the variable `rdm` as an intermediate variable, and hence will not be affected by it nor aborts even though it is an unrecognized input variable. While allowing for a flexible input value determination, the downside of the above input design, however, is that any syntactical error inside the input file is not always indicated with the location where it happens.

## Orbital Generation 

The first step will be to compute the orbitals for a given molecule, the example below is for H2O. This is done with `get_orbs`. The python scipt `Path to orb gen H2O.py`, shown below, gives an example to generate orbitals using Hartree-Fock

```pyhon

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

```
Running `get_orbs H2O.py` this will create the files numpy arrays that include the orbitals, ccupations, energies and reduced density matrix that will be used in the next step of the calculation. Available electronic structure methods are restricted hartree-fock `rhf`, complete active space `casscf` and density functional theory `dft`. For CASSCF calculations, the number of CAS orbitals, core orbitals, and CAS electrons are required. For DFT the exchange correlation `xc` functional must be specified. The orbitals are generated using PySCF. 

## Ground state DMRG

This task computes the ground state energy using DMRG algorithm and optionally saves the final ground state MPS. The Python script `TDDMRG_CM/examples/H2O/H2O.py`, also shown below, demonstrates an example of a simple ground state calculation of the water molecule using TDDMRG_CM
```python

complex_MPS_type = 'hybrid'
prefix = 'H2O'
atoms = \
            '''
            O   0.000   0.000   0.107;
            H   0.000   0.785  -0.427;
            H   0.000  -0.785  -0.427;
            '''
basis = 'cc-pvdz'
group = 'C2v'
wfn_sym = 'A1'
orb_path = '/absolute/path/to/orbitals/H2O.orb.npy'

nCore = 1
nCAS = 23
nelCAS = 8
twos = 0

do_groundstate = True
if do_groundstate:
    D_gs = [100]*4 + [250]*4 + [400]
    gs_outmps_dir = './' + prefix + '.gs-mps'

do_annihilate = False
do_timeevo = False
```
Here, it is assumed that some orbitals were calculated in the previous step and are stored in a numpy file whose full path is `/absolute/path/to/orbital/H2O.orb.npy`. The output of this calculation contains a line that shows the final ground state energy
```
 Ground state energy =   -76.2393734097
```
Some of the first micro iterations in the 11-th macro iteration (denoted by `Sweep = ...`) should look like
```
Sweep =   11 | Direction = backward | Bond dimension =  400 | Noise =  0.00e+00 | Dav threshold =  1.00e-06
 <-- Site =   21-  22 .. 
     1     1     0   -24.15991433     1.47e-11
Mmps =    3 Ndav =   1 E =    -76.2393711185 Error = 0.00e+00 FLOPS = 3.41e+05 Tdav = 0.00 T = 0.01
 <-- Site =   20-  21 .. 
     1     1     0   -24.15991433     5.29e-08
Mmps =   10 Ndav =   1 E =    -76.2393711185 Error = 0.00e+00 FLOPS = 1.38e+07 Tdav = 0.00 T = 0.01
 <-- Site =   19-  20 .. 
     1     1     0   -24.15991433     5.48e-07
Mmps =   35 Ndav =   1 E =    -76.2393711185 Error = 0.00e+00 FLOPS = 2.50e+08 Tdav = 0.00 T = 0.01
 <-- Site =   18-  19 .. 
     1     1     0   -24.15991433     8.96e-07
Mmps =  118 Ndav =   1 E =    -76.2393711185 Error = 1.80e-45 FLOPS = 3.17e+09 Tdav = 0.01 T = 0.02
 <-- Site =   17-  18 .. 
     1     1     0   -24.15991433     9.64e-07
Mmps =  246 Ndav =   1 E =    -76.2393711185 Error = 8.18e-40 FLOPS = 1.09e+10 Tdav = 0.01 T = 0.03
 <-- Site =   16-  17 .. 
     1     1     0   -24.15991433     1.47e-07
Mmps =  298 Ndav =   1 E =    -76.2393711185 Error = 0.00e+00 FLOPS = 5.87e+09 Tdav = 0.07 T = 0.10
 <-- Site =   15-  16 .. 
     1     1     0   -24.15991433     1.72e-07
Mmps =  400 Ndav =   1 E =    -76.2393711185 Error = 3.80e-37 FLOPS = 8.49e+09 Tdav = 0.14 T = 0.19
 <-- Site =   14-  15 .. 
     1     1     0   -24.15991433     1.97e-06
     2     2     0   -24.15991449     2.91e-08
Mmps =  400 Ndav =   2 E =    -76.2393712705 Error = 1.18e-08 FLOPS = 9.65e+09 Tdav = 0.40 T = 0.48
 <-- Site =   13-  14 .. 
     1     1     0   -24.15991433     2.61e-05
     2     2     0   -24.15991662     6.78e-07
Mmps =  400 Ndav =   2 E =    -76.2393734097 Error = 2.03e-07 FLOPS = 9.64e+09 Tdav = 0.79 T = 0.88
 <-- Site =   12-  13 .. 
     1     1     0   -24.15991434     2.06e-05
     2     2     0   -24.15991604     3.15e-07
```
The above snippet shows a backward micro iteration since it starts from the last site, site number 22 (the number of sites, 23, is given by `nCAS`). Note that, the bond dimension (denoted by `Mmps`) is capped at 400. This is because at the shown 11-th macro iteration, the maximum bond dimension is 400. The input parameter `D_gs` is used to set the schedule for the applied maximum bond dimension as the macro iteration progresses.

At the end of the calculation, several standard quantum chemical quantities are printed, such as orbital occupancies, multipole moments, and bond orders of some significant bonds
```
  *** Molecular orbitals occupations (alpha, beta) ***
      (1: 1.000000, 1.000000)   (2: 0.991053, 0.991053)   (3: 0.981319, 0.981319)   (4: 0.983570, 0.983570)   (5: 0.985799, 0.985799)   
      (6: 0.004947, 0.004947)   (7: 0.005064, 0.005064)   (8: 0.006625, 0.006625)   (9: 0.006228, 0.006228)   (10: 0.006486, 0.006486)   
      (11: 0.008741, 0.008741)   (12: 0.003715, 0.003715)   (13: 0.001840, 0.001840)   (14: 0.002151, 0.002151)   (15: 0.001196, 0.001196)   
      (16: 0.002363, 0.002363)   (17: 0.000313, 0.000313)   (18: 0.001442, 0.001442)   (19: 0.001623, 0.001623)   (20: 0.001440, 0.001440)   
      (21: 0.001302, 0.001302)   (22: 0.001130, 0.001130)   (23: 0.000842, 0.000842)   (24: 0.000812, 0.000812)   
 
  *** Atomic Mulliken populations ***
      (O1: -0.275821)   (H2: 0.137910)   (H3: 0.137910)   
 
  *** Atomic Lowdin populations ***
      (O1: -0.065060)   (H2: 0.032530)   (H3: 0.032530)   
 
  *** Mulliken bond orders ***
     Atom A    Atom B    Bond order
          1         2      0.978000
          1         3      0.978000
   Note: Only bonds for which the bond order is larger than 0.1 are printed.
 
  *** Lowdin bond orders ***
     Atom A    Atom B    Bond order
          1         2      1.158799
          1         3      1.158799
   Note: Only bonds for which the bond order is larger than 0.1 are printed.
 
  *** Multipole moment components ***
                        x            y            z            xx           yy           zz           xy           yz           xz     
     Electronic     -0.000000     0.000000    -0.723955    -5.240511    -7.391749    -6.191456    -0.000000    -0.000000    -0.000000
     Nuclear         0.000000     0.000000     0.003779     0.000000     4.401159     1.629298     0.000000     0.000000     0.000000
     Total           0.000000     0.000000    -0.720176    -5.240511    -2.990590    -4.562158     0.000000    -0.000000     0.000000
```



## Annihilation operator
Since charge migration happens in an ionized state, an important component of TDDMRG_CM is the application of annihilation operator to the MPS of an un-ionized state to emulate ionization. The Python script below is an example of input file for annihilation operator task where the input MPS is the ground state MPS calculated above. Before creating this input file for annihilation task, make a directory under the directory of the ground state calculation previously, then create the input file under this new directory.
```python
import numpy as np
from os.path import abspath

prefix = 'H2O'
GS_PATH = '..'        # Relative path of the ground state calculation.
prev_logbook = abspath(GS_PATH + '/H2O.lb')    # Convert to an absolute path right here---another great thing of having an input file as a Pythons script.
complex_MPS_type = 'logbook'

atoms = 'logbook'
basis = 'logbook'
group = 'logbook'
wfn_sym = 'logbook'
orb_path = 'logbook'
orb_order = 'logbook:orb_order_id'

nCore = 'logbook'
nCAS = 23
nelCAS = 'logbook'
twos = 'logbook'

do_groundstate = False

do_annihilate = True
if do_annihilate:
    ann_sp = True
    ann_orb = np.zeros(nCAS)
    ann_orb[3] = ann_orb[9] = 1/np.sqrt(2)
    D_ann_fit = [100]*4 + [300]*4 + [500]*4 + [800]*4 + [600]*4 + [400]
    ann_inmps_dir = abspath(GS_PATH + '/H2O.gs-mps')
    ann_outmps_dir = abspath('./' + prefix + '.ann-mps')
    ann_out_singlet_embed = True
    ann_out_cpx = True

do_timeevo = False
```
The input file above, also available in `TDDMRG_CM/examples/H2O/H2O.annihilate-ocpx/H2O.py`, extensively utilizes the logbook file, a file generated by TDDMRG_CM with an extension `.lb`, created from the previous ground state calculation. A logbook file stores information about the value of many variables (including input parameters) generated during a job. This file serves a similar purpose as Gaussian checkpoint files or NWChem's RTDB file, and other quantum chemistry program's auxiliary files that provide transferrability of data between different simulations or simulation components. ***The use of logbook file is highly encouraged since it minimizes accidental errors in providing the correct value to some input parameters***. Among exceptions in which you cannot use a logbook to get the value of a certain input is when you want to use its value somewhere else in the input script. An example is `nCAS` in the snippet above, whose value will be used to construct `ann_orb`. During a program run, the logbook file will be created and updated at several instances, including when it is finished.

In the snippet above, the lines
```python
GS_PATH = '..'
prev_logbook = abspath(GS_PATH + '/H2O.lb)'
```
which result in the absolute path of the previous logbook file being assigned to the input parameter `prev_logbook` tells the program where to look for the logbook file to be used as a reference for several input parameters in the current input file. Once an existing logbook is specified, there are two syntaxes to extract information from it: `varname1 = 'logbook'` and `varname1 = 'logbook:varname2'`. In the first form, the program will look for a variable named `'varname1'` in the loaded logbook and assign its value to the parameter `varname1` in the current input script. While in the second form, the program will look for a variable named `'varname2'` and assign its value to `varname1`. For example, in the input snippet above `basis` and `wfn_sym` take values from the logbook using the first syntax.  They will then be assigned with `'cc-pvdz'` and `'A1'`, respectively. The second form is used to provide value for `orb_order`, which controls orbital ordering. Orbital ordering for annihilation (and [time evolution](#time-evolution)) task should be the same as the ordering in the ground state task. Had we used the first logbook syntax, the program will pull an entry named `'orb_order'` from the loaded logbook, whose value is `'genetic'`, as specified in the previous ground state task, and will prompt the program to recalculate the ordering using the genetic algorithm. This may lead to a slightly different ordering, especially if there are degenerate orbitals. In our example, we are looking for a variable named `orb_order_id` because this variable stores the ordering indices calculated during the previous simulation. The second logbook syntax obviously requires you that you know what parameter names are stored in a logbook file. TDDMRG_CM provides several utility functions to analyze or preview the content of a logbook file. See the example below.
```python
from TDDMRG_CM.utils import util_logbook
lb = util_logbook.read('H2O.lb')     # Loading a logbook given its path.
util_logbook.content(lb)             # Print the content of logbook.
```
Note that once loaded using `util_logbook.read`, a logbook is essentially a Python dictionary, so you can perform any operations defined for a dictionary on `lb`.

We highly recommend to use an absolute path rather than a relative path for any input parameters that accept a path, such as `orb_path`, `ann_inmps_dir`, and `ann_outmps_dir`, among others. This is because this parameter will be stored in the current logbook file with their value as is. If this logbook file should be referenced by another simulation located in a different directory, the relative paths will lead to wrong places.

The input parameters responsible for informing the program where to look for the input MPS for annihilation operator tasks are `ann_inmps_dir` (for the directory) and `ann_inmps_fname` (for the filename containing the information about the input MPS). The value assigned to `ann_inmps_fname` must be a file located under the directory path assigned to `ann_inmps_dir`. In the snippet above, only `ann_inmps_dir` is explicitly given, while `ann_inmps_fname` is omitted. Its omission means that the program will use its default value, `GS_MPS_INFO`, which coincides with the default value for `gs_outmps_fname`, the parameter that controls the filename of MPS info file saved by the ground state task.

In the above input for annihilation operator task, an electron is annihilated from an orbital whose coefficient in the basis of the site orbitals are given by `ann_orb`. Since it contains zeros except for the 3rd and 9th elements, which are equal to `np.sqrt(2)`, the annihilation orbital is thus an in-phase, equal-strength superposition between Hartree-Fock HOMO (index `3`) and LUMO+5 (index `9`). 

The output of annihilation operator task contains the following table in the beginning of the simulation.
```
 Occupations before annihilation:
 ---------------------------------------------------------------------------------------------------
  No.    Alpha MO occ.    Beta MO occ.    Irrep / ID    aorb coeff     Alpha natorb occ.   Beta natorb occ.
 ---------------------------------------------------------------------------------------------------
    0       0.99105259      0.99105259        A1 / 0    0.00000000            0.99196709         0.99196709
    1       0.98131860      0.98131860        B2 / 3    0.00000000            0.98580737         0.98580737
    2       0.98356961      0.98356961        A1 / 0    0.00000000            0.98276444         0.98276444
    3       0.98579937      0.98579937        B1 / 2    0.70710678            0.98139798         0.98139798
    4       0.00494665      0.00494665        A1 / 0    0.00000000            0.01348813         0.01348813
    5       0.00506351      0.00506351        B2 / 3    0.00000000            0.01291446         0.01291446
    6       0.00662521      0.00662521        B2 / 3    0.00000000            0.00884486         0.00884486
    7       0.00622765      0.00622765        A1 / 0    0.00000000            0.00618726         0.00618726
    8       0.00648558      0.00648558        A1 / 0    0.00000000            0.00308791         0.00308791
    9       0.00874101      0.00874101        B1 / 2    0.70710678            0.00303757         0.00303757
   10       0.00371483      0.00371483        B2 / 3    0.00000000            0.00273979         0.00273979
   ...
   ...
   21       0.00084233      0.00084233        A1 / 0    0.00000000            0.00003464         0.00003464
   22       0.00081188      0.00081188        B2 / 3    0.00000000            0.00002364         0.00002364
 ---------------------------------------------------------------------------------------------------
  Sum       4.00000000      4.00000000                                        4.00000000         4.00000000
 ---------------------------------------------------------------------------------------------------
```
This table lists the occupancies of the site orbitals (2nd and 3rd columns), the irrep type and index of the corresponding site orbital (4th column), orbital coefficients in the `ann_orb` (5th column), and the occupancies of natural orbitals (6th and 8th columns) in the input MPS. The last row displays the number of electrons in each spin channel, which must equal the value assigned to `nelCAS`. Toward the end of the output, you will also find a similar table 
```
 Occupations after annihilation:
 ---------------------------------------------------------------------------------------------------
  No.    Alpha MO occ.    Beta MO occ.    Irrep / ID    aorb coeff     Alpha natorb occ.   Beta natorb occ.
 ---------------------------------------------------------------------------------------------------
    0       0.99140248      0.99140248        A1 / 0    0.00000000            0.99264465         0.99264465
    1       0.98231103      0.98231103        B2 / 3    0.00000000            0.98441170         0.98441170
    2       0.98464807      0.98464807        A1 / 0    0.00000000            0.98303153         0.98303153
    3       0.49449454      0.49449454        B1 / 2    0.70710678            0.49559134         0.49559134
    4       0.00412045      0.00412045        A1 / 0    0.00000000            0.01246532         0.01246532
    5       0.00455988      0.00455988        B2 / 3    0.00000000            0.01142285         0.01142285
    6       0.00605761      0.00605761        B2 / 3    0.00000000            0.00521137         0.00521137
    7       0.00535028      0.00535028        A1 / 0    0.00000000            0.00335203         0.00335203
    8       0.00621465      0.00621465        A1 / 0    0.00000000            0.00264789         0.00264789
    9       0.00434197      0.00434197        B1 / 2    0.70710678            0.00252970         0.00252970
   10       0.00378889      0.00378889        B2 / 3    0.00000000            0.00154977         0.00154977
   ...
   ...
   21       0.00061853      0.00061853        A1 / 0    0.00000000            0.00001883         0.00001883
   22       0.00078966      0.00078966        B2 / 3    0.00000000            0.00001837         0.00001837
 ---------------------------------------------------------------------------------------------------
  Sum       3.50000000      3.50000000                                        3.50000000         3.50000000
 ---------------------------------------------------------------------------------------------------
```
except that now the occupancies are calculated with respect to the output MPS resulting from the action of the annihilation operator on the input MPS. As can be seen, the total occupancy of the 3rd site orbital (HOMO) has been reduced by about one. The total number of electrons after annihilation process is seen to be exactly equal to `nelCAS-1`.

Near the beginning of the output, you can find the information about the quantum numbers of the input and output MPSs.
```
 Quantum number information:
  - Input MPS =  < N=8 S=0 PG=0 >
  - Input MPS multiplicity =  1
  - Annihilated orbital =  < N=-1 S=1/2 PG=2 >
  - Output MPS =  < N=7 S=1/2 PG=2 >
  - Output MPS multiplicity =  2
```
`N`, `S`, and `PG` stand for the number of electros, the total spin, and irrep type of the MPS. Here, we see that the input MPS has 8 active electrons, is a singlet state, and has the $A_1$ (ID 0) irrep. The annihilated orbital is defined to have `-1` number of electrons. In particular, its irrep is equal to `2`, which corresponds to the $B_1$ irrep of the $C_{2v}$ point group. Also note that the two orbitals, HOMO and LUMO+5, making up the linear combination of the annihilated orbital, have the same symmetry. This is necessary, otherwise an error will occur. If you need to have an annihilated orbital that is a linear combination of site orbitals of different irreps, then you need to choose an appropriate point group for input parameter `group` that identifies the orbitals in the linear combination as belonging to the same point group. The output MPS has 7 electrons, a total spin of one-half, and irrep type of $B_1$. The irrep of the output MPS can be determined through the irrep direct product property.

In the input file for annihilation operator task above, the bond dimension schedule has been given values that initially increase from `100` to `800` and then decrease to the final value of `400`. The overshot to the maximum value of `800` instead of increasing and stopping at the final desired value of `400` allows the MPS fitting algorithm to search for the minimum (the solution output MPS) in a larger Hilbert space. Repeating the simulation with a bond dimension schedule that exhibits no overshot as `D_ann_fit = [100]*4 + [300]*4 + [400]` results in a less accurate output MPS as demonstrated by the final electron number of `3.49999942 * 2 = 6.99999884` that is less close to the proper value of 7 than previously. See occupancy table below.
```
 Occupations after annihilation:
 ---------------------------------------------------------------------------------------------------
  No.    Alpha MO occ.    Beta MO occ.    Irrep / ID    aorb coeff     Alpha natorb occ.   Beta natorb occ.
 ---------------------------------------------------------------------------------------------------
   ...
   ...
   21       0.00061854      0.00061854        A1 / 0    0.00000000            0.00001882         0.00001882
   22       0.00078963      0.00078963        B2 / 3    0.00000000            0.00001841         0.00001841
 ---------------------------------------------------------------------------------------------------
  Sum       3.49999942      3.49999942                                        3.49999942         3.49999942
 ---------------------------------------------------------------------------------------------------
```
The simulation in the case of bad choice of bond dimension schedule above is available in `TDDMRG_CM/examples/H2O/H2O.annihilate-bad_d/H2O.py`.


The output MPS above has a non-zero total spin (non-singlet) as necessitated by the odd number of electrons it has. In MPS framework, it is possible to represent a non-singlet MPS as a singlet MPS, this is referred to as singlet-embedding. As shown in the input script above, to convert a non-singlet output MPS of annihilation operator task, switch singlet embedding on using the `ann_out_singlet_embed` input parameter.
```
...
...
do_annihilate = True
if do_annihilate:
    ...
    ann_out_singlet_embed = True
```
Using singlet-embedded MPS for a non-singlet MPS for time evolution using TDDMRG is highly recommended as has been shown in [this paper](https://doi.org/10.1021/acs.jctc.4c01185).

As also shown in the cited publication above, using full complex MPS type in TDDMRG time evolution rather than the hybrid one is much more favorable due to the faster convergence with bond dimension. Performing ground state and annihilation operator calculations in the full complex mode where the MPSs are complex is possible by setting `complex_MPS_type = 'full'`. While this should yield exactly the same results, this is redundant since these calculations do not necessitate a complex wave function. A much more efficient way is to convert the output MPS from annihilation task run in a `'hybrid'` mode to a full complex MPS form. This is done by setting `ann_out_cpx = True`.


## Time Evolution
The MPS resulting from the annihilation operator task above is typically used as the initial state for time evolution tasks using TDDMRG. For the first example, let's simulate a time evolution with singlet-embedding on. So, first create a new directory, for example, as a subdirectory under the annihilation operator simulation using singlet-embedding. The Python script below, also available in `TDDMRG_CM/examples/H2O/H2O.annihilate-ocpx/H2O.tevo/H2O.py`, is a minimal example
```python
from os.path import abspath

prefix = 'H2O'
memory = 250.0E9
dump_inputs = True
T0_PATH = '..'
prev_logbook = abspath(T0_PATH + '/H2O.lb')
complex_MPS_type = 'full'

atoms = 'logbook'
basis = 'logbook'
group = 'logbook'
wfn_sym = 'B1'
orb_path = 'logbook'
orb_order = 'logbook:orb_order_id'

nCore = 'logbook'
nCAS = 'logbook'
nelCAS = 8
twos = 0

do_groundstate = False
do_annihilate = False

do_timeevo = True
if do_timeevo:
    te_inmps_dir = abspath(T0_PATH + '/H2O.ann-mps')
    te_max_D = 600
    te_inmps_cpx = True
    tinit = 0.0
    tmax = 20.0
    fdt = 0.04
    dt = [fdt/4]*4 + [fdt/2]*2 + [fdt]
    te_method = 'tdvp'
    krylov_size = 5
    te_sample = ('delta', 5*dt[-1])
    te_in_singlet_embed = (True, nelCAS-1)
```

The parameter `complex_MPS_type` is set to `'full'` because the initial state is in full complex representation (due to the use of `ann_out_cpx = True` in the annihilation simulation). `wfn_sym` is set to `'B1'` because $B_1$ is the symmetry of the output MPS of the annihilation simulation, this can be checked in the `Quantum number information:` section in the annihilation output. `nelCAS` is given an explicit value of `8` instead of `7`. This is because the initial state is also in singlet-embedding representation. This also affects the value assigned to `twos`, which is `0`.

Parameters for time evolution is given under the `do_timeevo` block. Since entanglement will increase with time, the bond dimension is set to `600` which is higher than that of the initial state. For this example, we chose `tdvp` as the time integrator, another option is `rk4`, which, however, is less efficient than `tdvp`, and the printing interval of time-dependent quantities (see below) is every `5 * 0.04 = 0.2` atomic unit of time. The parameter `te_in_singlet_embed` tells the program that the initial MPS is in singlet-embedding format and that the actual MPS (that is embedded in a larger singlet MPS) has `nelCAS-1 = 7` active electrons.

Similar to the case of annihilation task, the time evolution task also defines two input parameters that control the program on where to look for the initial MPS: `te_inmps_dir` (for the directory) and `te_inmps_fname` (for the MPS info file). `te_inmps_fname` is omitted in the input script above because its default value is `ANN_MPS_INFO`, which coincides with the default value for `ann_outmps_fname`, the parameter that controls the filename of output MPS info file of an annihilation task.

The first time evolution example above has singlet-embedding turned on. This greatly increases the efficiency of TDDMRG simulation without virtually affecting the accuracy (see [this paper](https://doi.org/10.1021/acs.jctc.4c01185)). If you want to see how the performance is affected by this optional parameter, you can run the same time evolution without singlet-embedding. To do this, simply create another annihilation operator directory under ground state directory. Run the annihilation task using the same input script as [the previous one](#annihilation-operator) except that `ann_out_singlet_embed` should be omitted or be given a `False`. Then, perform a time evolution simulation with the same input script as above except that `nelCAS = 7`, `twos = 1`, and `te_in_singlet_embed` omitted. You should see that the previous time evolution with singlet-embedding on runs about twice as fast as the one without singlet-embedding. The input scripts for the non-singlet-embedding simulations may be found in `examples/H2O/H2O.annihilate-ocpx-nose/H2O.py` and `examples/H2O/H2O.annihilate-ocpx-nose/H2O.tevo/H2O.py`.



### Time-dependent quantities
There are four quantities that are printed by default throughout the time evolution, they are dipole and quadrupole moments, Lowdin partial charges, autocorrelation function, and 1-particle RDM (1RDM). The 1RDM can then be used to calculate other observables not available in TDDMRG_CM which do not depend on higher order RDMs. These quantities are printed at the sampling time points, which is controlled by `te_sample` except for the autocorrelation function, which is printed at every time step. Refer to the definition of `te_sample` below for the available options and convention on which time points exactly are the above quantites printed. The dipole and quadupole moments, Lowdin partial charges, and autocorrelation functions are printed into `<prefix>.mp`, `<prefix>.<n>.low`, and `<prefix>.ac`, respectively. Here, `n` is an integer starting from 1 that signifies the part number of the Lowdin partial charge files. There can be more than one Lowdin partial charge file depending on the number of atoms in the molecule. While the RDMs are saved in `<prefix>.sample/tevo-<m>` folders where `m` is a time point number. The dipole and quadupole moments, Lowdin partial charges, and autocorrelation functions are also saved into a numpy file, named `<prefix>.mp.npy`, `<prefix>.low.npy`, and `<prefix>.ac.npy`, respectively, for easier use in further analyses.

By default, the time-dependent MPS is also saved at the time points set by `te_sample`. In the default behavior, or when `te_sample = 'overwrite'`, the MPS from the previous sampling point is overwritten by the MPS at the current sampling point (see `te_save_mps`). It is also possible to save the time-dependent MPS and 1RDM at a certain future time by using 'probe files'. Probe files must be named `probe-<n>`, here `n`n is the step number. As an example, at present, the time evolution is processing the 60-th time step, if the sampling time points coincide with, e.g. the 61st, 66th, 71st, 76th ... etc time steps (you will know which step numbers tje sampling will be carried  out when you list the content of the `<prefix>.sample` folder), and user creates a probe file under `<prefix>.sample` directory and name it `probe-66`, when the program reaches the 66-th step, it will examine the content of the probe file, and check if any recognized keywords are found. The only recognized keywords to be typed inside a probe file are `save_mps` and `save_1pdm`, which are to be assigned with true or false. For example, if `probe-66` contains
```
save_mps true
save_1pdm false
```
the program will save the MPS but not the 1pdm when it reaches the 66-th time point. The saved MPS and 1RDM are located under `<prefix>.sample/tevo-66`. Absent keywords are interpreted to have a `false` value, e.g., had we not typed the second line in the snippet above, it would have had the same effect of informing the program to save the MPS but not the 1RDM. As for the accepted values, instead of `true`, one can use `t`, `1`, `yes`, or `y`. Likewise, `f`, `0`,  `no`, and `n` have the same effect as a `false`.





### Restarting a TDDMRG simulation
Time evolution simulations using TDDMRG can take days or even weeks on ~50 cores already. For this reason, it is essential that users know how to restart a terminated TDDMRG job. Let's suppose that the TDDMRG simulation prepared with an input script above is terminated when the time reaches 4.0 atomic unit of time. You can run another TDDMRG simulation starting from the last MPS saved in a previous TDDMRG run, such as this one. To restart this simulation, make a new directory as a subdirectory of the previous TDDMRG simulation. Copy the previous TDDMRG input file into the newly created restart directory, make the following changes
```python
complex_MPS_type = 'logbook'
wfn_sym = 'logbook'
nelCAS = 'logbook'
twos = 'logbook'
te_inmps_dir = abspath(T0_PATH + '/H2O.mps_t')
te_inmps_fname = 'mps_info.bin'
te_max_D = 'logbook'
tinit = 4.0       # 'From the time information in the '../H2O.mps_t/TIME_INFO' file.'
tmax = 'logbook'
dt = [fdt]
te_method = 'logbook'
krylov_size = 'logbook'
te_sample = 'logbook'
te_in_singlet_embed = 'logbook'
```
to the existing lines containing the same input parameters, and add the following lines under the `do_timeevo` conditional block.
```python
mps_act0_dir = 'logbook'
mps_act0_fname = 'logbook'
mps_act0_cpx = 'logbook'
mps_act0_multi = 'logbook'
```
Since this simulation is to start from a previous TDDMRG, `te_inmps_dir` is set to the directory where the time-dependent MPS is saved, `<prefix>.mps_t` under the previous TDDMRG simulation directory. Unlike the time evolution starting from the annihilation output, this time, the input parameter `te_inmps_fname` is set explicitly to `mps_info.bin`. `mps_info.bin` is the filename of MPS info file of the time-dependent MPS saved during a TDDMRG simulation. Also, don't forget to set `dt` to the time step length of the previous TDDMRG simulation when it was terminated. The new four input parameters `mps_act0_*` are given in the input to let the program know which MPS is to be treated as the initial MPS for the calculation of autocorrelation function. If these parameters are not given, their default values will be assumed, and these would be equal to `te_inmps_dir`, `te_inmps_fname`, `te_inmps_cpx`, and `te_inmps_multi`, respectively. You will typically want the output MPS of the annihilation task for the autocorrelation function since the this is the actual start of the evolution, not the last MPS from the previously terminated TDDMRG simulation. Therefore, you can use the information stored in the previous logbook. `tinit` sets the initial time that is printed in the text files where time-dependent quantities are printed. It does not affect the propagation or the calculation of time-dependent quantities, it only offsets the time points to the specified value. Despite rather trivial, setting it to the last time point when the last MPS in the previous simulation was saved can save one from manually matching the time points with the last one from previous simulation in further analyses, such as for Fourier analysis. In a restart simulation, you can determine the proper value for `tinit` by looking into the content of a file named `TIME_INFO` located under the same directory as the MPS files of the MPS to restart from, and use the time point in a.u. in the line starting with `Actual sampling time`. In the example above, this file should be found under the `<prefix>.mps_t` directory.




## Tools for analyses
Apart from the main three functionalities described above, TDDMRG_CM also provides tools for analyzing the dynamics or for generating orbitals adapted to the dynamics (see [this paper](https://doi.org/10.1021/acs.jctc.4c01185)). Many of these tools accept a logbook as one of the arguments. Whenever possible, pass a logbook to be safe from the risk of supplying wrong values to the arguments of these tools.

### Hole density
The volumetric hole density at each sampling time point throughout the time evolution can be calculated using `TDDMRG_CM.observables.hole_dens.eval_volume`. See the script `TDDMRG_CM/examples/H2O/H2O.annihilate-ocpx/H2O.tevo/H2O.analysis/hole_density/H2O.py` for an example of how to use it. The volumetric hole density data (in `*.cube` file format) at each sampling time point calculated by this function will be printed into the respective sampling time `<prefix>.sample/tevo-*` directory in the current time evolution folder with an extension `.tvl.cube`. If hole density slices are desired, users should use `TDDMRG_CM.observables.hole_dens.eval_xyplane`, `TDDMRG_CM.observables.hole_dens.eval_xzplane`, or `TDDMRG_CM.observables.hole_dens.eval_yzplane` to calculate the slice on a plane parallel to the xy, xz, or yz plane, respectively. While `TDDMRG_CM.observables.hole_dens.eval_plane` is available to calculate the slices on any arbitrary plane. The slice data at each sampling time point calculated by the four aforementioned in-plane evaluator functions will be printed into the respective sampling time `<prefix>.sample/tevo-*` directory with an extension `.tpl`.

### Orbital hole occupancies
Hole occupancies of arbitrary orbitals at each sampling time point can be computed by using `TDDMRG_CM.observables.td_hocc.calc` function. See the script `TDDMRG_CM/examples/H2O/H2O.annihilate-ocpx/H2O.tevo/H2O.analysis/occupancies/H2O.py` for an example of how to use it. The time-dependent hole occupancies are printed into a file with an extension of `.thoc`. Note that the orbitals whose hole occupancies are computed must be expanded by the same AO basis as that used in the TDDMRG simulation.

### Dynamics-adapted orbitals
There are two dynamics-adapted orbitals supported by TDDMRG_CM: DM-adapted and hole-DM-adapted orbitals. These two types of orbitals are introduced in [this paper](https://doi.org/10.1021/acs.jctc.4c01185). See the script `TDDMRG_CM/examples/H2O/H2O.annihilate-ocpx/H2O.tevo/H2O.analysis/dynorb/H2O.py` for an example of how to obtain them from a previous TDDMRG simulation. 






## Input parameters
The definitions of input parameters recognized by TDDMRG_CM are listed below. Some advices to keep in mind:
<ol>												  
  <li><strong>Use logbook file as much as possible</strong>. One exception in which logbook cannot be used to get the value of a certain parameter is if this parameter is needed somewhere else in the input file.</li>
  <li><strong>Use absolute paths</strong> for input parameters recognized by TDDMRG_CM that accept a path, e.g. <code>orb_path</code>. Consider using <code>os.path.abspath</code> to help you resolve the absolute path of a relative path.</li>
  <li><strong>Don&#39t set the sampling times (through  <code>te_sample</code>) too close one after another</strong> (i.e., having too frequent printings of time-dependent quantities) if you set <code>te_save_mps</code> to <code>'overwrite'</code> (the default) or <code>'sample'</code>. As for the <code>'overwrite'</code> option, this increases the risk of corrupting the saved MPS files when the program is terminated (e.g. due to time runout) while a MPS saving process is still ongoing, a complete MPS saving process can span a few minutes. Since, the previous MPS is overwritten, if the current MPS is not successfully saved, you have basically lost ability to restart the simulation. While for <code>'sampled'</code>, too frequent MPS savings can take up a huge space.</li>
  <li>Even if you follow the previous advice about sampling time, the option <code>'overwrite'</code> is still not totally fail-proof as program termination can still happen when a MPS saving is in progress. As a general advice, <strong>if your simulation has been running for ~3 days, consider saving the time-dependent MPS at a close future (e.g. 1-2 sampling time points ahead) using a proble file</strong> to serve as a checkpoint and ensure that the MPS saving is completed by making sure that the line <code>The current MPS has been successfully saved under /path/to/probe/file/directory</code> is printed in the output. MPSs saved through probe files will not get overwritten since they are saved in their respective <code>&ltprefix&gt.sample/tevo-*</code> directory. If instead the program terminates during a MPS saving set through a probe file, the previous &#39normally&#39 saved MPS in <code>&ltprefix&gt.mps_t</code> can be used for restart since it does not get overwritten. Do this again after several days of further program run if it has not finished yet.
</ol>
These input parameters may be categorized into general input (needed by all three functionalities), ground state, annihilation operation, and time evolution.

### ATTENTION - Change in input variable names
Some older versions of TDDMRG_CM have a different naming for several input variables. These changed input parameters are

1. `inp_coordinates` --> `atoms`
2. `inp_basis` --> `basis`
3. `inp_symmetry` --> `group`
4. `inp_ecp` --> `ecp`

where the keywords on the right of the arrows are the current ones. If you find an input script for TDDMRG_CM in which the keywords on the left of the arrows appear, and want to run it using the current version of TDDMRG_CM, then change them to their new names.

### General
<details>
  <summary><code>atoms</code></summary>
  A python multiline string that specifies the cartesian coordinates of the atoms in the molecule. The format is as follows
  
  ```
  <Atom1>  <x1>  <y1>  <z1>;
  <Atom2>  <x2>  <y2>  <z2>;
  ...
  ```
	  
</details>

<details>
  <summary><code>basis</code></summary>
  The name of the Gaussian basis set.
</details>

<details>
  <summary><code>wfn_sym</code></summary>
  The irrep of the wave function associated with the chosen value for <code>group</code> input. It accepts both the literal form e.g. <code>'Ag'</code>, <code>'B1'</code>, <code>'B2'</code>, <code>"'A'"</code>, <code>'"A"'</code>, as well as the integer form in PySCF notation where the trivial irrep is equal to 0. To get the complete list of the integer index equivalence of each irrep, consult the PySCF source file <code>&ltpyscf_root&gt/pyscf/symm/param.py</code>.
</details>

<details>
  <summary><code>nCore</code></summary>
  The number of core orbitals.
</details>

<details>
  <summary><code>nCAS</code></summary>
  The number of active orbitals.
</details>

<details>
  <summary><code>nelCAS</code></summary>
  The number of active electrons occupying the active orbitals.
</details>

<details>
  <summary><code>twos</code></summary>
  The result of 2*S where S is the total spin quantum number of the wave function.
</details>

<details>
  <summary><code>scratch</code> (optional)</summary>
  <strong>Default</strong>: <code>'&ltprefix&gt.tmp'</code> where <code>&ltprefix&gt</code> is the value given to the <code>prefix</code> parameter.
  <br>
  The path to the scratch directory. Scratch directories are used to store intermediate quantities such as MPS and MPO tensor elements, etc. If not given in the input file, the program will first check if an environment variable named `ITDDMRG_TMPDIR` has been set to the desired scratch directory path. Otherwise, the program will use the default value defined above.
</details>

<details>
  <summary><code>prev_logbook</code> (optional)</summary>
  <strong>Default</strong>: <code>None</code>
  <br>
  The path to an existing logbook. This is used when you want to use the values of several input parameters from another simulation.
</details>

<details>
  <summary><code>complex_MPS_type</code> (optional)</summary>
  <strong>Default</strong>: <code>'hybrid'</code>
  <br>
  The complex type of MPS in the calculation. The possible options are <code>'hybrid'</code> and <code>'full'</code>. For ground state and annihilation tasks, the choice of complex type should not matter. If they differ, then at least one of the simulations has not converged yet. For time evolution, the results will differ depending on the bond dimension. The two complex types should give identical time evolution dynamics when the bond dimension reaches convergence.
</details>

<details>
  <summary><code>dump_inputs</code> (optional)</summary>
  <strong>Default</strong>: <code>False</code>
  <br>
  If True, then the values of the input parameters will be printed to the output.
</details>

<details>
  <summary><code>memory</code> (optional)</summary>
  <strong>Default</strong>: <code>1E9</code>
  <br>
  Memory allocation in bytes for the entire run of the program.
</details>

<details>
  <summary><code>prefix</code> (optional)</summary>
  <strong>Default</strong>: The prefix of the input file if it has a <code>.py</code> extension, otherwise, the full name of the input file.
  <br>
  The prefix of files and folders created during simulation.
</details>

<details>
  <summary><code>verbose_lvl</code> (optional)</summary>
  <strong>Default</strong>: 4
  <br>
  An integer that controls the verbosity level of the output.
</details>

<details>
  <summary><code>ecp</code> (optional)</summary>
  <strong>Default</strong>: <code>None</code>
  <br>
  The effective core potential (ECP) on each atom. The format follows pyscf format for ECP. If not specified, no ECP will be used.
</details>

<details>
  <summary><code>group</code> (optional)</summary>
  <strong>Default</strong>: <code>'C1'</code>
  <br>
  A string that specifies the point group symmetry of the molecule.
</details>

<details>
  <summary><code>orb_path</code> (optional)</summary>
  <strong>Default</strong>: Hartee-Fock canonical orbitals using the chosen AO basis set and geometry.
  <br>
  Specifies the site orbitals. It accepts the path to a <code>*.npy</code> file that stores a 2D array (matrix) of the AO coefficients of the orbitals, where the rows refer to the AO index and the columns refer to the orbital index. The AO used to expand the orbitals should be the same as the AO chosen for the <code>basis</code> parameter. It also accepts <code>None</code>, for which case the program will treat it as if <code>orb_path</code> is not present (hence, will fall back to the default value).
</details>

<details>
  <summary><code>orb_order</code> (optional)</summary>
  <strong>Default</strong>: <code>'genetic'</code>
  <br>
  Specifies orbital ordering. The choices are as follows:
  <ol>
    <li>A string that specifies the path of a <code>*.npy</code> file containig a 1D array (vector) of integers representing the orbital index. These indices are 0-based.</li>
    <li>A list of 0-based integers. This is basically the hard-coded version of the first option above.</li>
    <li>A dictionary of the form
      <ol type="i">
	  <li><code>{'type':'linear', 'direction':(x, y, z)}</code>, or</li>
	  <li><code>{'type':'circular', 'plane':&lt3x3 matrix&gt}</code></li>
      </ol>
      The i format is for ordering based on a line in 3D space. In this ordering, the orbitals are ordered according to the projection of their dipole moments in the direction specified by the <code>'direction'</code> key. <code>x</code>, <code>y</code>, and <code>z</code> specifies the direction vector for the projection. The i format is best used for molecules whose one of the dimenions is clearly longer than the other. The ii format is for circular ordering, best for molecules exhibiting some form of circularity in shape, e.g. aromatic molecules. The value for <code>'plane'</code> is a 3x3 numpy matrix. This matrix specifies the coordinates of three points in space through which the plane of the circular ordering is defined (a plane can be uniquely defined by three points that do not all lie in a line). The rows of this matrix correspond to the three points, while the columns correrspond to their <code>x</code>, <code>y</code>, and <code>z</code> Cartesian components.
    </li>
    <li>A string 'genetic', the genetic algorithm.</li>
    <li>A string 'fiedler', the Fiedler algorithm.</li>
  </ol>
</details>

<details>
  <summary><code>mrci</code> (optional)</summary>
  <strong>Default</strong>: <code>None</code>
  <br>
  If given the format-conforming value, it prompts an MRCI calculation using MPS. The format is a dictionary with two entries, <code>'nactive2'</code> and <code>'order'</code>. <code>'nactive2'</code> specifies the number of the excitation orbitals. <code>'nactive2':10</code> means that the last 10 orbitals of the nCAS active orbitals are considered to be the excitation orbitals. <code>'order'</code> specifies the excitation order. Currently, the available options for <code>'order'</code> are 1, 2, and 3, representing single, single-double, and single-double-triple excitations, respectively.
</details>



### Ground state

<details>
  <summary><code>do_groundstate</code></summary>
  True or False. If True, a groundstate DMRG calculation will be performed.
</details>

<details>
  <summary><code>D_gs</code></summary>
  A list containing the schedule of the bond dimensions during DMRG iterations. For example, <code>[100]*2 + [200*4] + [300]</code>, means that the first two iterations use a max bond dimension of 100, the next four use 200 max bond dimension, and beyond that it uses the max bond dimension of 300 until convergence or maximum iteration number is reached, whichever is earlier.
</details>

<details>
  <summary><code>gs_inmps_dir</code> (optional)</summary>
  <strong>Default</strong>: <code>None</code>
  <br>
  One of the three ways to construct a guess MPS for macro iterations. If it is set to a valid directory path, then the guess MPS is constructed using MPS files located under this directory. The default of the three ways is a randomly generated MPS having the prescribed maximum bond dimension.
</details>

<details>
  <summary><code>gs_inmps_fname</code> (optional)</summary>
  <strong>Default</strong>: <code>'mps_info.bin'</code>
  <br>
  The file name of the info file of the MPS to be used to start the ground state DMRG iterations. This file should be inside the folder specified through gs_inmps_dir. This input must be present if gs_inmps_dir is present.
</details>

<details>
  <summary><code>gs_noise</code> (optional)</summary>
  <strong>Default</strong>: <code>[1E-3]*4 + [1E-4]*4 + [0.0]</code>
  <br>
  A list containing the schedule of the noise applied during ground state iterations. A nonzero noise can be used to prevent the MPS from getting trapped in a local minimum. Its format follows the same convention as D_gs.
</details>

<details>
  <summary><code>gs_dav_tols</code> (optional)</summary>
  <strong>Default</strong>: <code>[1E-2]*2 + [1E-3]*2 + [1E-6]*500</code>
  <br>
  A list containing the schedule of the tolerances to terminate the Davidson/micro iterations for diagonlizing the effective Hamiltonian. Typically, it starts from a large value such as 0.01 and decrease until e.g. 1E-7. Its format follows the same convention as D_gs.
</details>

<details>
  <summary><code>gs_steps</code> (optional)</summary>
  <strong>Default</strong>: <code>50</code>
  <br>
  The maximum number of macro iterations in the ground state calculation. Use this or gs_conv_tol to determine when to terminate the macro iteration.
</details>

<details>
  <summary><code>gs_conv_tol</code> (optional)</summary>
  <strong>Default</strong>: <code>1E-6</code>
  <br>
  The energy difference tolerance when the macro iterations should stop. Use this or gs_steps to determine when to terminate the macro iteration.
</details>

<details>
  <summary><code>gs_cutoff</code> (optional)</summary>
  <strong>Default</strong>: <code>1E-14</code>
  <br>
  States with eigenvalue below this number will be discarded, even when the bond dimension is large enough to keep this state.
</details>

<details>
  <summary><code>gs_occs</code> (optional)</summary>
  <strong>Default</strong>: <code>None</code>
  <br>
  One of the three ways to construct a guess MPS for macro iterations. If it is set, then the guess MPS is constructed in such a way that its orbital occupancies are equal to gs_occs. It is a vector of nCAS floating point numbers. gs_occs is meaningless if gs_inmps_dir is set.
</details>

<details>
  <summary><code>gs_bias</code> (optional)</summary>
  <strong>Default</strong>: <code>1.0</code>
  <br>
  A floating point number used to shift/bias the occupancies of active orbitals used to construct the guess MPS for macro iterations. If gs_bias is set, the given initial occupancies will be modified so that high occupancies are reduce by an gs_bias while low occupancies are increased by gs_bias. Only meaningful when gs_occs is given.
</details>

<details>
  <summary><code>gs_outmps_dir</code> (optional)</summary>
  <strong>Default</strong>: scratch directory
  <br>
  The path to the directory in which the MPS files of the final ground state MPS will be saved for future use.
</details>

<details>
  <summary><code>gs_outmps_fname</code> (optional)</summary>
  <strong>Default</strong>: <code>'GS_MPS_INFO'</code>
  <br>
  The file name of the info file of the final ground state MPS This input must be present if gs_outmps_dir is present.
</details>

<details>
  <summary><code>save_gs_1pdm</code> (optional)</summary>
  <strong>Default</strong>: <code>False</code>
  <br>
  True or False. If True, the one-particle RDM of the final ground state MPS will be saved under gs_outmps_dir with a filename GS_1pdm.npy.
</details>

<details>
  <summary><code>flip_spectrum</code> (optional)</summary>
  <strong>Default</strong>: <code>False</code>
  <br>
  True or False. If True, the macro iterations will seek the highest energy of the Hamiltonian. It is implemented by running the same iterations as when this input is False but with a -1 multiplied into the Hamiltonian.
</details>

<details>
  <summary><code>gs_out_cpx</code> (optional)</summary>
  <strong>Default</strong>: <code>False</code>
  <br>
  True or False. If True, the final ground state MPS will be converted to a full complex MPS where the tensor elements are purely real complex numbers. If True and complex_MPS_type is 'full', the program will be aborted.
</details>



### Annihilation operation
<details>
  <summary><code>do_annihilate</code></summary>
  True or False. If True, the program will calculate the annihilation of an electron from an orbital in the given input MPS.
</details>

<details>
  <summary><code>ann_sp</code></summary>
  True or False. The spin projection of the annihilated electron, True means alpha electron, otherwise, beta electron.
</details>

<details>
  <summary><code>ann_orb</code></summary>
  Specifies which orbital from which an electron is annihilated. It accepts an integer ranging from 0 to nCAS-1 and a nCAS-long vector. If it is given an integer, the program annihilates electron from the (ann_orb+1)-th orbital of the site. For example, ann_orb=2 means that the an electron will be annihilated from the third active orbital. If ann_orb is given a vector, the program will annihilate an electron from the orbital represented by the linear combination of the site orbitals where the expansion coefficients are contained in ann_orb. Note that small elements of ann_orb vector can cause execution error, therefore user should set small elements of ann_orb vector to exactly zero before running the program. Usually the threshold is 1E-5, that is, in this case do <code>ann_orb[np.abs(ann_orb) &lt 1.0E-5] = 0.0</code>. The final ann_orb vector must be normalized. When ann_orb is a vector, the irrep of orbitals with large expansion coefficients must be the same. If classification between large and small coefficients is not possible (e.g. due to low contrast of these coefficients), then set group to a point group with less symmetries. Ultimately, <code>group = 'C1'</code> should cover <code>ann_orb</code> vector of no symmetry.
</details>

<details>
  <summary><code>D_ann_fit</code></summary>
  A list containing the schedule of the bond dimensions during the fitting iterations. Its format follows the same convention as D_gs.
</details>

<details>
  <summary><code>ann_inmps_dir</code> (optional)</summary>
  <strong>Default</strong>: scratch directory.
  <br>
  The path to the directory containing the MPS files of the input MPS on which the annihilation operator will be applied.
</details>

<details>
  <summary><code>ann_inmps_fname</code> (optional)</summary>
  <strong>Default</strong>: <code>'GS_MPS_INFO'</code>
  <br>
  The file name of the info file of the input MPS on which the annihilation operator will be applied. ann_inmps_fname must be located under ann_inmps_dir.
</details>

<details>
  <summary><code>ann_outmps_dir</code> (optional)</summary>
  <strong>Default</strong>: scratch directory.
  <br>
  The path to the directory containing the MPS files of the output MPS.
</details>

<details>
  <summary><code>ann_outmps_fname</code> (optional)</summary>
  <strong>Default</strong>: <code>'ANN_MPS_INFO'</code>
  <br>
  The file name of the info file of the output MPS. ann_outmps_fname must be located under ann_outmps_dir.
</details>

<details>
  <summary><code>ann_orb_thr</code> (optional)</summary>
  <strong>Default</strong>: <code>1.0E-12</code>
  <br>
  The threshold for determining the irrep of the orbital represented by ann_orb in vector form. The irrep of the annihilated orbital is equal to the irreps of orbitals whose absolute value of coefficient is higher than ann_orb_thr. This implies that the irrep of these large-coefficient orbitals must all be the same.
</details>

<details>
  <summary><code>ann_fit_noise</code> (optional)</summary>
  <strong>Default</strong>: <code>[1e-5]*4 + [1E-6]*4 + [0.0]</code>
  <br>
  A list containing the schedule of the noise applied during fitting iterations. A nonzero noise can be used to prevent the MPS from getting trapped in a local minimum. Its format follows the same convention as D_gs.
</details>

<details>
  <summary><code>ann_fit_tol</code> (optional)</summary>
  <strong>Default</strong>: <code>1E-7</code>
  <br>
  A threshold to determine when fitting iterations should stop.
</details>

<details>
  <summary><code>ann_fit_steps</code> (optional)</summary>
  <strong>Default</strong>: <code>50</code>
  <br>
  The maximum number of iteration for the fitting iterations.
</details>

<details>
  <summary><code>ann_fit_cutoff</code> (optional)</summary>
  <strong>Default</strong>: <code>1E-14</code>
  <br>
  States with eigenvalue below this number will be discarded, even when the bond dimension is large enough to keep this state.
</details>

<details>
  <summary><code>ann_fit_occs</code> (optional)</summary>
  <strong>Default</strong>: <code>None</code>
  <br>
  If it is set, the guess MPS for fitting iterations is constructed in such a way that its orbital occupancies are equal to ann_fit_occs. It is a vector of nCAS floating point numbers.
</details>

<details>
  <summary><code>ann_fit_bias</code> (optional)</summary>
  <strong>Default</strong>: <code>1.0</code>
  <br>
  A floating point number used to shift/bias the occupancies of active orbitals used to construct the guess MPS for fitting iterations. If ann_fit_bias is set, the given initial occupancies will be modified so that high occupancies are reduce by an ann_fit_bias while low occupancies are increased by ann_fit_bias. Only meaningful when ann_fit_occs is given.
</details>

<details>
  <summary><code>normalize_annout</code> (optional)</summary>
  <strong>Default</strong>: <code>True</code>
  <br>
  True or False. If True, the output MPS after annihilation is normalized.
</details>

<details>
  <summary><code>save_ann_1pdm</code> (optional)</summary>
  <strong>Default</strong>: <code>False</code>
  <br>
  True or False. If True, the one-particle RDM of the output MPS will be saved under ann_outmps_dir with a filename ANN_1pdm.npy.
</details>

<details>
  <summary><code>ann_out_singlet_embed</code> (optional)</summary>
  <strong>Default</strong>: <code>False</code>
  <br>
  True or False. If True, the output MPS will be converted to a singlet- embedding representation.
</details>

<details>
  <summary><code>ann_out_cpx</code> (optional)</summary>
  <strong>Default</strong>: <code>False</code>
  <br>
  True or False. If True, the final output MPS will be converted to a full complex MPS where the tensor elements are purely real complex numbers. If True and complex_MPS_type is 'full', the program will be aborted.
</details>





### Time evolution

<details>
  <summary><code>do_timeevo</code></summary>
  True or False. If True, time evolution simulation using TDDMRG will be performed.
</details>

<details>
  <summary><code>te_max_D</code></summary>
  The maximum bond dimension of the time-evolving MPS in the TDDMRG simulation.
</details>

<details>
  <summary><code>tmax</code></summary>
  The maximum time up to which the time evolution is run.
</details>

<details>
  <summary><code>dt</code></summary>
  The time step for time evolution in atomic unit of time.
</details>

<details>
  <summary><code>tinit</code> (optional)</summary>
  <strong>Default</strong>: <code>0.0</code>
  <br>
  The initial time at which the time evolution starts. It only affects the time points printed at which observables are calculated and printed. It does not affect the simulation.
</details>

<details>
  <summary><code>te_inmps_dir</code> (optional)</summary>
  <strong>Default</strong>: scratch directory.
  <br>
  The path to the directory containing the MPS files of the initial MPS from which the time evolution starts.
</details>

<details>
  <summary><code>te_inmps_fname</code> (optional)</summary>
  <strong>Default</strong>: <code>'ANN_MPS_INFO'</code>
  <br>
  The file name of the info file of the initial MPS from which the time evolution starts. te_inmps_fname must be located under te_inmps_dir.
</details>

<details>
  <summary><code>te_inmps_cpx</code> (optional)</summary>
  <strong>Default</strong>: <code>False</code>
  <br>
  True or False. Set it to True if the initial MPS is complex, and False if the initial MPS is real. When restarting a TDDMRG simulation, regardless of the value of complex_MPS_type, this input must be set to True since the last MPS from the previous TDDMRG is complex. This input must also be set to True if the initial MPS is not from a previous TDDMRG simulation but complex_MPS_type is 'full', e.g. from an annihilation calculation with complex_MPS_type = 'full'.
</details>

<details>
  <summary><code>te_inmps_multi</code> (optional)</summary>
  <strong>Default</strong>: <code>False</code>
  <br>
  True or False. Set it to True if the initial MPS is in state-average format, for example, when restarting from a previous TDDMRG simulation where complex_MPS_type = 'hybrid'. Set it to False otherwise.
</details>

<details>
  <summary><code>mps_act0_dir</code> (optional)</summary>
  <strong>Default</strong>: the value of <code>te_inmps_dir</code>.
  <br>
  The path to the directory containing the MPS files of the MPS used as the state at t=0 for the computation of autocorrelation function.
</details>

<details>
  <summary><code>mps_act0_fname</code> (optional)</summary>
  <strong>Default</strong>: the value of <code>te_inmps_fname</code>.
  <br>
  The file name of the info file of the MPS used as the state at t=0 for the computation of autocorrelation function. This file must be located under the mps_act0_dir directory.
</details>

<details>
  <summary><code>mps_act0_cpx</code> (optional)</summary>
  <strong>Default</strong>: the value of <code>te_inmps_cpx</code>.
  <br>
  True or False. It has the same meaning as te_inmps_cpx except for the MPS used as the state at t=0 for the computation of autocorrelation function.
</details>

<details>
  <summary><code>mps_act0_multi</code> (optional)</summary>
  <strong>Default</strong>: the value of <code>te_inmps_multi</code>.
  <br>
  True or False. It has the same meaning as te_inmps_multi except for the MPS used as the state at t=0 for the computation of autocorrelation function.
</details>

<details>
  <summary><code>te_method</code> (optional)</summary>
  <strong>Default</strong>: <code>'tdvp'</code>
  <br>
  The time propagation method. The available options are <code>'rk4'</code> and <code>'tdvp'</code>. <code>'rk4'</code> stands for the time-step targeting (TST) method, while <code>'tdvp'</code> stands for the time-dependent variational principle method (TDVP).
</details>

<details>
  <summary><code>te_cutoff</code> (optional)</summary>
  <strong>Default</strong>: <code>0</code>
  <br>
  States with eigenvalue below this number will be discarded, even when the bond dimension is large enough to keep this state.
</details>

<details>
  <summary><code>krylov_size</code> (optional)</summary>
  <strong>Default</strong>: <code>20</code>
  <br>
  The size of Krylov subspace used to approximate the action of a matrix exponential on a vector in TDVP propagation. Meaningless if <code>te_method = 'rk4'</code>.
</details>

<details>
  <summary><code>krylov_tol</code> (optional)</summary>
  <strong>Default</strong>: <code>5.0E-6</code>
  <br>
  A threshold used to set the accuracy of the Krylov subspace method in approximating the action of a matrix exponential on a vector in TDVP propagation.
</details>

<details>
  <summary><code>n_sub_sweeps</code> (optional)</summary>
  <strong>Default</strong>: <code>2</code>
  <br>
  The number of sweeps in a TST propagation used to improve the renormalized basis in each time step.
</details>

<details>
  <summary><code>n_sub_sweeps_init</code> (optional)</summary>
  <strong>Default</strong>: <code>4</code>
  <br>
  The number of sweeps in the first time step of a TST propagation used to improve the renormalized basis in each time step.
</details>

<details>
  <summary><code>te_normalize</code> (optional)</summary>
  <strong>Default</strong>: <code>False</code>
  <br>
  True or False. If True, the MPS will be normalized after every time step.
</details>

<details>
  <summary><code>te_sample</code> (optional)</summary>
  <strong>Default</strong>: <code>None</code>
  <br>
  The sampling time points around which the observables will be calculated and printed. It accepts three formats: a numpy vector of monotonically increasing time points, a tuple of the form <code>('steps', n)</code> with <code>n</code> an integer, and a tuple of the form <code>('delta', d)</code> with <code>d</code> a float. The <code>('steps', n)</code> format is used to choose sampling time points using a fixed interval <code>n</code>. <code>n = 1</code> means that the observables are calculated and printed exactly every time step. <code>n = 2</code> means that the observables are calculated and printed at every second time step. The <code>('delta', d)</code> format is used to choose sampling time points at a fixed time interval. <code>d = 0.01</code> means that the sampling time points are separated by 0.01 a.u. of time. Note that sampling times only tell the program approximately around which time points should observables be calculated. The actual time points when the observables are printed are those determined by dt which are the closest to a particular te_sample. For example, if the only sampling time point is 12.6 and two propagation time points around it is 12.0 and 13.0, then the observables will be printed at t = 13.0. This means that the <code>('steps', n)</code> format produces sampling  time points that are exactly a subset of the propagation time points. If <code>dt</code> contains non-uniform time steps, however, the <code>('steps', n)</code> format will produce sampling time points which are not uniformly spaced (uniform spacing might desired for Fourier transform). To exact subset of the propagation time points which are not uniformly ensure uniformly spaced sampling points that are also the spaced (as is usually true because the first few time steps should typically be really short compared to at the later times), one can do
  
  ```python
  dt = [DT/m]*m + [DT/n]*n + [DT]
  te_sample = ('delta', p*dt[-1])
  ```
  
  where <code>m</code>, <code>n</code>, and <code>p</code> are integers, while <code>DT</code> is a floating point.
</details>

<details>
  <summary><code>te_save_mps</code> (optional)</summary>
  <strong>Default</strong>: <code>'overwrite'</code>
  <br>
  Determines how often the instantaneous MPS should be saved. The available options are:
  <ol>
    <li><code>'overwrite'</code>. MPS files are saved at the sampling time points under the folder <code>&ltprefix&gt.mps_t</code> where <code>&ltprefix&gt</code> is the value of <code>prefix</code> input. These MPS files overwrite the MPS files saved in the previous sampling time point.</li>
    <li><code>'sampled'</code>. MPS files are saved at every sampling time points. This option can lead to a huge space taken up by the MPS files. This option is usually used if you want to use these instantaneous MPS for later analyses that are not available already in this program and for which the use of 1RDM alone is not enough. If that is not your plan, using <code>'overwrite\'</code> is recommended.</li>
    <li><code>'no'</code>. MPS files will not be saved.</li>
  </ol>
  Regardless of the value of <code>te_save_mps</code>, the instantaneous MPS can be saved 'on-demand' by using probe files.
</details>

<details>
  <summary><code>te_save_1pdm</code> (optional)</summary>
  <strong>Default</strong>: <code>True</code>
  <br>
  True or False. If True, the 1-electron RDM is saved at every sampling time points under the folder <code>&ltprefix&gt.sample</code> where <code>&ltprefix&gt</code> is the value of <code>prefix</code> input.
</details>

<details>
  <summary><code>te_in_singlet_embed</code> (optional)</summary>
  <strong>Default</strong>: <code>(False, None)</code>
  <br>
  A 2-entry tuple with the first entry being True or False, while the second one is an integer. Specify this input with the first entry set to True if the initial MPS is in singlet-embedding format, and the second entry set to the actual number of active electrons in the system. Due to the singlet-embedded form, the number of electrons in the initial MPS is adjusted so that the total spin can be zero.
</details>

<details>
  <summary><code>bo_pairs</code> (optional)</summary>
  <strong>Default</strong>: <code>None</code>
  <br>
  Lowdin bond order.
</details>



import sys
from os.path import exists
import numpy as np
import defvals


#######################################################
def get_inputs(inp_file):
    '''
    This function returns a dictionary containing the input parameters and their values
    as key-value pairs.

    To define a new input parameters, first decide whether this new input parameter is 
    mandatory or optional parameter. If it is a mandatory input, then simply add the 
    following line after the 'inputs = {}' below
       inputs['new_input'] = new_input
    where new_input is to be replaced with the intended name of the new input. On the
    other hand, if the new input is optional, do the following steps.
       1) If the default value of this optional input does not depend on any other 
          parameters, then add the following line anywhere after the 'inputs = {}' line 
          below
             try:
                 inputs['new_input'] = new_input
             except NameError:
                 inputs['new_input'] = defvals.def_new_input
          Then, add this line inside defvals.py
             def_new_input = <value>
          where def_new_input is to be replaced with the intended name of the variable that
          holds the default value for this optional input, and <value> is the default value.
       2) If the default value depends on some parameters and can be determined here (e.g. 
          the input prefix below, whose default value depends on the input file name), then 
          replace the inputs['new_input'] = defvals.def_new_input line in point 1) 
          above with the appropriate line(s) that involve the dependency parameters.
          The addition of the corresponding default parameter inside defvals.py is 
          unnecessary in this case since the default value has been calculated here.
       3) If the default value depends on some parameters and can only be determined later
          in the program, then replace the right-hand side of the 
          inputs['new_input'] = defvals.def_new_input line in point 1) above with the string
          'DEFINE_LATER'. And later in the code when this input is about to be used for the 
          first time, do the assignment in the following way:
             if inputs['new_input'] == 'DEFINE_LATER':
                 <the appropriate lines to determine the value of inputs['new_input']>
    
    The newly defined input parameter can then be referred to by invoking inputs['new_input'] 
    inside cm_dmrg assuming that the output of this function is stored in a variable called 
    inputs. 
    
    It is strongly encouraged that any newly defined inputs are added such that all 
    mandatory inputs are defined before all optional inputs in their approppriate section 
    (marked by a comment line such as #=== abcde ===# below).
    '''
    
    exec(open(inp_file).read(), globals())

    inputs = {}

    #==== General parameters ====#
    inputs['atoms'] = atoms

    # basis:
    #   A library that specifies the atomic orbitals (AO) basis on each atom. The format
    #   follows pyscf format format for AO basis.
    inputs['basis'] = basis

    # wfn_sym:
    #   The irrep of the wave function associated with the chosen value for 'group'
    #   input. It accepts both the literal form, e.g. Ag, B1, B2, A', A", as well as the
    #   integer form in PySCF notation where the trivial irrep is equal to 0. To get the
    #   complete list of the integer index equivalence of each irrep, consult the PySCF
    #   source file <pyscf_root>/pyscf/symm/param.py.
    inputs['wfn_sym'] = wfn_sym

    # scratch:
    try:
        inputs['scratch'] = scratch
    except NameError:
        inputs['scratch'] = 'DEFINE_LATER'
    
    # prev_logbook:
    #   The path to an existing logbook. This is used when you want to use the values of
    #   several input parameters from another simulation.
    try:
        inputs['prev_logbook'] = prev_logbook
    except NameError:
        inputs['prev_logbook'] = defvals.def_prev_logbook
    
    # complex_MPS_type (optional):
    #   The complex type of MPS in the calculation. The possible options are 'hybrid'
    #   and 'full' with default being 'hybird', which is faster than 'full'.
    #   For ground state and annihilation tasks, the choice of complex type should not
    #   matter. If they differ, then at least one of the simulations has not converged
    #   yet. For time evolution, the results will differ depending on the bond
    #   dimension. The two complex types should give identical time evolution dynamics
    #   when the bond dimension reaches convergence.
    try:
        inputs['complex_MPS_type'] = complex_MPS_type
    except NameError:
        inputs['complex_MPS_type'] = defvals.def_complex_MPS_type

    # dump_inputs (optional):
    #   If True, then the values of the input parameters will be printed to the output.
    #   The default is False.
    try:
        inputs['dump_inputs'] = dump_inputs
    except NameError:
        inputs['dump_inputs'] = defvals.def_dump_inputs

    # memory (optional):
    #   Memory in bytes. The default is 1E9 (1 GB).
    try:
        inputs['memory'] = memory
    except NameError:
        inputs['memory'] = defvals.def_memory

    # prefix (optional):
    #   The prefix of files and folders created during simulation. The default is the
    #   prefix of the input file if it has a '.py' extension, otherwise it uses the
    #   full name of the input file as prefix.
    try:
        inputs['prefix'] = prefix
    except NameError:
        if inp_file[len(inp_file)-3:len(inp_file)] == '.py':
            inputs['prefix'] = inp_file[0:len(inp_file)-3]
        else:
            inputs['prefix'] = inp_file

    # verbose_lvl (optional):
    #   An integer that controls the verbosity level of the output. The default is 4.
    try:
        inputs['verbose_lvl'] = verbose_lvl
    except NameError:
        inputs['verbose_lvl'] = defvals.def_verbose_lvl

    # ecp (optional):
    #   The effective core potential (ECP) on each atom. The format follows pyscf
    #   format for ECP. The default is None, which means that no ECP will be used.
    try:
        inputs['ecp'] = ecp
    except NameError:
        inputs['ecp'] = defvals.def_ecp

    # group (optional):
    #   A string to specifies the point group symmetry of the molecule. The default is
    #   'c1'.
    try:
        inputs['group'] = group
    except NameError:
        inputs['group'] = defvals.def_group

    # orb_path (optional):
    #   A string to specify the path of the orbitals stored as a *.npy file that is
    #   used to represent the site of the MPS. The *.npy file should contain a 2D
    #   array (matrix) of the AO coefficients of the orbitals, where the rows refer to
    #   the AO index and the columns refer to the orbital index. The AO used to expand
    #   the orbitals should be the same as the AO chosen for the basis parameter.
    #   When ignored, the orbitals will be calculated from the canonical Hartree-Fock
    #   orbitals of the molecule using the chosen AO basis and geometry.
    try:
        inputs['orb_path'] = orb_path
    except NameError:
        inputs['orb_path'] = defvals.def_orb_path

    # orb_order (optional):
    #   Specifies the orbital ordering. The choices are the following:
    #    1) A string that specifies the path of a *.npy file containig a 1D array
    #       (vector) of integers representing the orbital index. These indices
    #       is 0-based.
    #    2) A list of 0-based integers. This is basically the hard-coded version of
    #       option one above.
    #    3) A library of the form
    #         a) {'type':'linear', 'direction':(x, y, z)}, or
    #         b) {'type':'circular', 'plane':<3x3 matrix>}
    #       The a) format is for ordering based on a line in 3D space. In this ordering,
    #       the orbitals are ordered according to the projection of their dipole moments
    #       in the direction specified by the 'direction' key. x, y, and z specifies the
    #       direction vector for the projection. The a) format is best used for molecules
    #       whose one of the dimenions is clearly longer than the other.
    #       The b) format is for circular ordering, best for molecules exhibiting some
    #       form of circularity in shape, e.g. aromatic molecules. The value for 'plane'
    #       is a 3x3 numpy matrix. This matrix specifies the coordinates of three points
    #       in space with which the plane of the circular ordering is defined. The rows
    #       of this matrix correspond to the three points, while the columns
    #       correrspond to their x, y, and z Cartesian components.
    #    4) A string 'genetic', the genetic algorithm, which is also the default.
    #    5) A string 'fiedler', the Fiedler algorithm.
    try:
        inputs['orb_order'] = orb_order
    except NameError:
        inputs['orb_order'] = defvals.def_orb_order
        
    #==== CAS parameters ====#
    # nCore:
    #   The number of core orbitals.
    inputs['nCore'] = nCore

    # nCAS:
    #   The number of active orbitals.
    inputs['nCAS'] = nCAS

    # nelCAS:
    #   The number of active electrons occupying the active orbitals.
    inputs['nelCAS'] = nelCAS

    # twos:
    #   The result of 2*S where S is the total spin quantum number of the wave function.
    inputs['twos'] = twos

    # mrci:
    #  If given the format-conforming value, then it prompts an MRCI calculation using
    #  MPS. The format is a library with two entries, 'nactive2' and 'order'. 'nactive2'
    #  specifies the number of the excitation orbitals. 'nactive2':10 means that the
    #  last 10 orbitals of the nCAS active orbitals are considered to be the excitation
    #  orbitals. 'order' specifies the excitation order. Currently, the available options
    #  for 'order' is 1, 2, and 3, representing single, single-double, and single-double-
    #  triple excitations, respectively.
    try:
        inputs['mrci'] = mrci
    except:
        inputs['mrci'] = defvals.def_mrci

    #==== Ground state parameters ====#
    # do_groundstate:
    #   True or False. If True, a groundstate DMRG calculation will be performed.
    inputs['do_groundstate'] = do_groundstate

    if inputs['do_groundstate'] == True:
        # D_gs:
        #   A list containing the schedule of the bond dimensions during DMRG
        #   iterations. For example, [100]*2 + [200*4] + [300], means that the first two
        #   iterations use a max bond dimension of 100, the next four use 200 max bond
        #   dimension, and beyond that it uses the max bond dimension of 300 until
        #   convergence or maximum iteration number is reached, whichever is earlier.
        inputs['D_gs'] = D_gs

        # gs_inmps_dir:
        #   One of the three ways to construct a guess MPS for macro iterations. If it is set to
        #   a valid directory path, then the guess MPS is constructed using MPS files located under
        #   this directory. The default of the three ways is a randomly generated MPS having the
        #   prescribed maximum bond dimension.
        try:
            inputs['gs_inmps_dir'] = gs_inmps_dir
        except NameError:
            inputs['gs_inmps_dir'] = defvals.def_gs_inmps_dir

        # gs_inmps_fname:
        #   The file name of the info file of the MPS to be used to start the ground state DMRG
        #   iterations. This file should be inside the folder specified through gs_inmps_dir.
        #   This input must be present if gs_inmps_dir is present.
        try:
            inputs['gs_inmps_fname'] = gs_inmps_fname
        except NameError:
            inputs['gs_inmps_fname'] = defvals.def_gs_inmps_fname

        # gs_noise:
        #   A list containing the schedule of the noise applied during ground state iterations.
        #   A nonzero noise can be used to prevent the MPS from getting trapped in a local
        #   minimum. Its format follows the same convention as D_gs.
        try:
            inputs['gs_noise'] = gs_noise
        except NameError:
            inputs['gs_noise'] = defvals.def_gs_noise

        # gs_dav_tols:
        #   A list containing the schedule of the tolerances to terminate the Davidson/micro
        #   iterations for diagonlizing the effective Hamiltonian. Typically, it starts from a
        #   large value such as 0.01 and decrease until e.g. 1E-7. Its format follows the same
        #   convention as D_gs.
        try:
            inputs['gs_dav_tols'] = gs_dav_tols
        except NameError:
            inputs['gs_dav_tols'] = defvals.def_gs_dav_tols

        # gs_steps:
        #   The maximum number of macro iterations in the ground state calculation. Use this
        #   or gs_conv_tol to determine when to terminate the macro iteration.
        try:
            inputs['gs_steps'] = gs_steps       # Maximum number of iteration steps
        except NameError:
            inputs['gs_steps'] = defvals.def_gs_steps

        # gs_conv_tol:
        #   The energy difference tolerance when the macro iterations should stop. Use this
        #   or gs_steps to determine when to terminate the macro iteration.
        try:
            inputs['gs_conv_tol'] = gs_conv_tol
        except NameError:
            inputs['gs_conv_tol'] = defvals.def_gs_conv_tol

        # gs_cutoff:
        #   States with eigenvalue below this number will be discarded, even when
        #   the bond dimension is large enough to keep this state.
        try:
            inputs['gs_cutoff'] = gs_cutoff
        except NameError:
            inputs['gs_cutoff'] = defvals.def_gs_cutoff

        # gs_occs:
        #   One of the three ways to construct a guess MPS for macro iterations. If it is set,
        #   then the guess MPS is constructed in such a way that its orbital occupancies are
        #   equal to gs_occs. It is a vector of nCAS floating point numbers. gs_occs is
        #   meaningless if gs_inmps_dir is set.
        try:
            inputs['gs_occs'] = gs_occs
        except NameError:
            inputs['gs_occs'] = defvals.def_gs_occs

        # gs_bias:
        #   A floating point number used to shift/bias the occupancies of active orbitals
        #   used to construct the guess MPS for macro iterations. If gs_bias is set, the
        #   given initial occupancies will be modified so that high occupancies are
        #   reduce by an gs_bias while low occupancies are increased by gs_bias. Only
        #   meaningful when gs_occs is given.
        try:
            inputs['gs_bias'] = gs_bias
        except NameError:
            inputs['gs_bias'] = defvals.def_gs_bias

        # gs_outmps_dir:
        #   The path to the directory in which the MPS files of the final ground state
        #   MPS will be saved for future use.
        try:
            inputs['gs_outmps_dir'] = gs_outmps_dir
        except NameError:
            inputs['gs_outmps_dir'] = 'DEFINE_LATER'

        # gs_outmps_fname:
        #   The file name of the info file of the final ground state MPS This input must
        #   be present if gs_outmps_dir is present.
        try:
            inputs['gs_outmps_fname'] = gs_outmps_fname
        except NameError:
            inputs['gs_outmps_fname'] = defvals.def_gs_outmps_fname

        # save_gs_1pdm:
        #   True or False. If True, the one-particle RDM of the final ground state MPS
        #   will be saved under gs_outmps_dir with a filename GS_1pdm.npy.
        try:
            inputs['save_gs_1pdm'] = save_gs_1pdm
        except NameError:
            inputs['save_gs_1pdm'] = defvals.def_save_gs_1pdm

        # flip_spectrum:
        #   True or False. If True, the macro iterations will seek the highest energy
        #   of the Hamiltonian. It is implemented by running the same iterations as when
        #   this input is False but with a -1 multiplied into the Hamiltonian.
        try:
            inputs['flip_spectrum'] = flip_spectrum
        except NameError:
            inputs['flip_spectrum'] = defvals.def_flip_spectrum

        # gs_out_cpx:
        #   True or False. If True, the final ground state MPS will be converted to a
        #   full complex MPS where the tensor elements are purely real complex numbers.
        #   If True and complex_MPS_type is 'full', the program will be aborted.
        try:
            inputs['gs_out_cpx'] = gs_out_cpx
        except NameError:
            inputs['gs_out_cpx'] = defvals.def_gs_out_cpx
    
    #==== Annihilation operation parameters ====#
    # do_annihilate:
    #   True or False. If True, the program will calculate the annihilation of an electron
    #   from an orbital in the given input MPS.
    inputs['do_annihilate'] = do_annihilate

    if inputs['do_annihilate'] == True:
        # ann_sp:
        #   True or False. The spin projection of the annihilated electron, True means alpha
        #   electron, otherwise, beta electron.
        inputs['ann_sp'] = ann_sp

        # ann_orb:
        #   Specifies which orbital from which an electron is annihilated. It accepts an
        #   integer ranging from 0 to nCAS-1 and a nCAS-long vector. If it is given an
        #   integer, the program annihilates electron from the (ann_orb+1)-th orbital of
        #   the site. For example, ann_orb=2 means that the an electron will be annihilated
        #   from the third active orbital. If ann_orb is given a vector, the program will
        #   annihilate an electron from the orbital represented by the linear combination
        #   of the site orbitals where the expansion coefficients are contained in ann_orb.
        #   Note that small elements of ann_orb vector can cause execution error, therefore
        #   user should set small elements of ann_orb vector to exactly zero before running
        #   the program. Usually the threshold is 1E-5, that is, in this case do
        #          ann_orb[np.abs(ann_orb) < 1.0E-5] = 0.0
        #   The final ann_orb vector must be normalized. When ann_orb is a vector, the
        #   irrep of orbitals with large expansion coefficients must be the same. If
        #   classification between large and small coefficients is not possible (e.g. due
        #   to low contrast of these coefficients), then set group to a point group
        #   with less symmetries. Ultimately, group = 'C1' should cover
        #   ann_orb vector of no symmetry.
        inputs['ann_orb'] = ann_orb

        # D_ann_fit:
        #   A list containing the schedule of the bond dimensions during the fitting
        #   iterations. Its format follows the same convention as D_gs.
        inputs['D_ann_fit'] = D_ann_fit

        # ann_inmps_dir:
        #   The path to the directory containing the MPS files of the input MPS on
        #   which the annihilation operator will be applied.
        try:
            inputs['ann_inmps_dir'] = ann_inmps_dir
        except NameError:
            inputs['ann_inmps_dir'] = 'DEFINE_LATER'

        # ann_inmps_fname:
        #   The file name of the info file of the input MPS on which the annihilation
        #   operator will be applied. ann_inmps_fname must be located under
        #   ann_inmps_dir.
        try:
            inputs['ann_inmps_fname'] = ann_inmps_fname
        except NameError:
            inputs['ann_inmps_fname'] = defvals.def_ann_inmps_fname

        # ann_outmps_dir:
        #   The path to the directory containing the MPS files of the output MPS.
        try:
            inputs['ann_outmps_dir'] = ann_outmps_dir
        except NameError:
            inputs['ann_outmps_dir'] = 'DEFINE_LATER'

        # ann_outmps_fname:
        #   The file name of the info file of the output MPS. ann_outmps_fname must
        #   be located under ann_outmps_dir.
        try:
            inputs['ann_outmps_fname'] = ann_outmps_fname
        except NameError:
            inputs['ann_outmps_fname'] = defvals.def_ann_outmps_fname

        # ann_orb_thr:
        #   The threshold for determining the irrep of the orbital represented by
        #   ann_orb in vector form. The irrep of the annihilated orbital is
        #   equal to the irreps of orbitals whose absolute value of coefficient
        #   is higher than ann_orb_thr. This implies that the irrep of these
        #   large-coefficient orbitals must all be the same.
        try:
            inputs['ann_orb_thr'] = ann_orb_thr
        except NameError:
            inputs['ann_orb_thr'] = defvals.def_ann_orb_thr
            
        #OLD try:
        #OLD     inputs['ann_fit_margin'] = ann_fit_margin
        #OLD except NameError:
        #OLD     inputs['ann_fit_margin'] = defvals.def_ann_fit_margin

        # ann_fit_noise:
        #   A list containing the schedule of the noise applied during fitting iterations.
        #   A nonzero noise can be used to prevent the MPS from getting trapped in a local
        #   minimum. Its format follows the same convention as D_gs.
        try:
            inputs['ann_fit_noise'] = ann_fit_noise
        except NameError:
            inputs['ann_fit_noise'] = defvals.def_ann_fit_noise

        # ann_fit_tol:
        #   A threshold to determine when fitting iterations should stop.
        try:
            inputs['ann_fit_tol'] = ann_fit_tol
        except NameError:
            inputs['ann_fit_tol'] = defvals.def_ann_fit_tol

        # ann_fit_steps:
        #   The maximum number of iteration for the fitting iterations.
        try:
            inputs['ann_fit_steps'] = ann_fit_steps
        except NameError:
            inputs['ann_fit_steps'] = defvals.def_ann_fit_steps

        # ann_fit_cutoff:
        #   States with eigenvalue below this number will be discarded, even when
        #   the bond dimension is large enough to keep this state.
        try:
            inputs['ann_fit_cutoff'] = ann_fit_cutoff
        except NameError:
            inputs['ann_fit_cutoff'] = defvals.def_ann_fit_cutoff

        # ann_fit_occs:
        #   If it is set, the guess MPS for fitting iterations is constructed in such a way
        #   that its orbital occupancies are equal to ann_fit_occs. It is a vector of nCAS
        #   floating point numbers.
        try:
            inputs['ann_fit_occs'] = ann_fit_occs
        except NameError:
            inputs['ann_fit_occs'] = defvals.def_ann_fit_occs

        # ann_fit_bias:
        #   A floating point number used to shift/bias the occupancies of active orbitals
        #   used to construct the guess MPS for fitting iterations. If ann_fit_bias is set,
        #   the given initial occupancies will be modified so that high occupancies are
        #   reduce by an ann_fit_bias while low occupancies are increased by ann_fit_bias.
        #   Only meaningful when ann_fit_occs is given.
        try:
            inputs['ann_fit_bias'] = ann_fit_bias
        except NameError:
            inputs['ann_fit_bias'] = defvals.def_ann_fit_bias

        # normalize_annout:
        #   True or False. If True, the output MPS after annihilation is normalized.
        try:
            inputs['normalize_annout'] = normalize_annout
        except NameError:
            inputs['normalize_annout'] = defvals.def_normalize_annout

        # save_ann_1pdm:
        #   True or False. If True, the one-particle RDM of the output MPS will be saved
        #   under ann_outmps_dir with a filename ANN_1pdm.npy.
        try:
            inputs['save_ann_1pdm'] = save_ann_1pdm
        except NameError:
            inputs['save_ann_1pdm'] = defvals.def_save_ann_1pdm

        # ann_out_singlet_embed:
        #   True or False. If True, the output MPS will be converted to a singlet-
        #   embedding representation.
        try:
            inputs['ann_out_singlet_embed'] = ann_out_singlet_embed
        except NameError:
            inputs['ann_out_singlet_embed'] = defvals.def_ann_out_singlet_embed

        # ann_out_cpx:
        #   True or False. If True, the final output MPS will be converted to a full
        #   complex MPS where the tensor elements are purely real complex numbers.
        #   If True and complex_MPS_type is 'full', the program will be aborted.
        try:
            inputs['ann_out_cpx'] = ann_out_cpx
        except NameError:
            inputs['ann_out_cpx'] = defvals.def_ann_out_cpx


    #==== Delta kick operation parameters ====#
    try:
        inputs['do_delta_kick'] = do_delta_kick
    except NameError:
        inputs['do_delta_kick'] = False

    if inputs['do_delta_kick'] == True:
        inputs["delta_kick"] = delta_kick
        inputs['D_delta_kick_fit'] = D_delta_kick_fit

        try:
            inputs['delta_kick_inmps_dir'] = delta_kick_inmps_dir
        except NameError:
            inputs['delta_kick_inmps_dir'] = 'DEFINE_LATER'

        try:
            inputs['delta_kick_inmps_fname'] = delta_kick_inmps_fname
        except NameError:
            inputs['delta_kick_inmps_fname'] = defvals.def_delta_kick_inmps_fname

        try:
            inputs['delta_kick_inmps_cpx'] = delta_kick_inmps_cpx
        except NameError:
            inputs['delta_kick_inmps_cpx'] = defvals.def_delta_kick_inmps_cpx

        try:
            inputs['delta_kick_inmps_multi'] = delta_kick_inmps_multi
        except NameError:
            inputs['delta_kick_inmps_multi'] = defvals.def_delta_kick_inmps_multi

        try:
            inputs['delta_kick_outmps_dir'] = delta_kick_outmps_dir
        except NameError:
            inputs['delta_kick_outmps_dir'] = 'DEFINE_LATER'

        try:
            inputs['delta_kick_outmps_fname'] = delta_kick_outmps_fname
        except NameError:
            inputs['delta_kick_outmps_fname'] = defvals.def_delta_kick_outmps_fname

        try:
            inputs['delta_kick_fit_noise'] = delta_kick_fit_noise
        except NameError:
            inputs['delta_kick_fit_noise'] = defvals.def_delta_kick_fit_noise

        try:
            inputs['delta_kick_fit_tol'] = delta_kick_fit_tol
        except NameError:
            inputs['delta_kick_fit_tol'] = defvals.def_delta_kick_fit_tol

        try:
            inputs['delta_kick_fit_steps'] = delta_kick_fit_steps
        except NameError:
            inputs['delta_kick_fit_steps'] = defvals.def_delta_kick_fit_steps

        try:
            inputs['delta_kick_fit_cutoff'] = delta_kick_fit_cutoff
        except NameError:
            inputs['delta_kick_fit_cutoff'] = defvals.def_delta_kick_fit_cutoff

        try:
            inputs['delta_kick_fit_occs'] = delta_kick_fit_occs
        except NameError:
            inputs['delta_kick_fit_occs'] = defvals.def_delta_kick_fit_occs

        try:
            inputs['delta_kick_fit_bias'] = delta_kick_fit_bias
        except NameError:
            inputs['delta_kick_fit_bias'] = defvals.def_delta_kick_fit_bias

        try:
            inputs['normalize_delta_kickout'] = normalize_delta_kickout
        except NameError:
            inputs['normalize_delta_kickout'] = defvals.def_normalize_delta_kickout

        try:
            inputs['save_delta_kick_1pdm'] = save_delta_kick_1pdm
        except NameError:
            inputs['save_delta_kick_1pdm'] = defvals.def_save_delta_kick_1pdm


    #==== Add a static electric field to the Hamiltonian====#
    try:
        inputs["static_electric_field"] = static_electric_field
    except NameError:
        inputs["static_electric_field"] = None

    if not inputs['do_delta_kick']:
        inputs["delta_kick"] = None

    try:
        inputs["field_origin"] = field_origin
    except NameError:
        inputs["field_origin"] = (0.0, 0.0, 0.0)

    try:
        inputs["include_core_field_energy"] = include_core_field_energy
    except NameError:
        inputs["include_core_field_energy"] = True

    #==== Time evolution parameters ====#
    # do_timeevo:
    #   True or False. If True, time evolution simulation using TDDMRG will be
    #   performed.
    inputs['do_timeevo'] = do_timeevo
    
    if inputs['do_timeevo'] == True:
        # te_max_D:
        #   The maximum bond dimension of the time-evolving MPS in the TDDMRG
        #   simulation.
        inputs['te_max_D'] = te_max_D

        # tmax:
        #   The maximum time up to which the time evolution is run.
        inputs['tmax'] = tmax

        # dt:
        #   The time step for time evolution in atomic unit of time.
        inputs['dt'] = dt

        # tinit:
        #   The initial time at which the time evolution starts. It only affects
        #   the time points printed at which observables are calculated and printed.
        #   It does not affect the simulation.
        try:
            inputs['tinit'] = tinit
        except NameError:
            inputs['tinit'] = defvals.def_tinit

        # te_inmps_dir:
        #   The path to the directory containing the MPS files of the initial MPS
        #   from which the time evolution starts.
        try:
            inputs['te_inmps_dir'] = te_inmps_dir
        except NameError:
            inputs['te_inmps_dir'] = 'DEFINE_LATER'

        # te_inmps_fname:
        #   The file name of the info file of the initial MPS from which the time
        #   evolution starts. te_inmps_fname must be located under te_inmps_dir.
        try:
            inputs['te_inmps_fname'] = te_inmps_fname
        except NameError:
            inputs['te_inmps_fname'] = defvals.def_te_inmps_fname

        # te_inmps_cpx:
        #   True or False. Set it to True if the initial MPS is complex, and
        #   False if the initial MPS is real. When restarting a TDDMRG simulation,
        #   regardless of the value of complex_MPS_type, this input must be set to
        #   True since the last MPS from the previous TDDMRG is complex. This
        #   input must also be set to True if the initial MPS is not from a
        #   previous TDDMRG simulation but complex_MPS_type is 'full', e.g. from
        #   an annihilation calculation with complex_MPS_type = 'full'.
        try:
            inputs['te_inmps_cpx'] = te_inmps_cpx
        except NameError:
            inputs['te_inmps_cpx'] = defvals.def_te_inmps_cpx

        # te_inmps_multi:
        #   True or False. Set it to True if the initial MPS is in state-average
        #   format, for example, when restarting from a previous TDDMRG simulation
        #   where complex_MPS_type = 'hybrid'. Set it to False otherwise.
        try:
            inputs['te_inmps_multi'] = te_inmps_multi
        except NameError:
            inputs['te_inmps_multi'] = defvals.def_te_inmps_multi

        # mps_act0_dir:
        #   The path to the directory containing the MPS files of the MPS used as
        #   the state at t=0 for the computation of autocorrelation function.
        try:
            inputs['mps_act0_dir'] = mps_act0_dir
        except NameError:
            inputs['mps_act0_dir'] = 'DEFINE_LATER'

        # mps_act0_fname:
        #   The file name of the info file of the MPS used as the state at t=0
        #   for the computation of autocorrelation function. This file must be
        #   located under the mps_act0_dir directory.
        try:
            inputs['mps_act0_fname'] = mps_act0_fname
        except NameError:
            inputs['mps_act0_fname'] = 'DEFINE_LATER'

        # mps_act0_cpx:
        #   True or False. It has the same meaning as te_inmps_cpx except for
        #   the MPS used as the state at t=0 for the computation of autocorrelation
        #   function.
        try:
            inputs['mps_act0_cpx'] = mps_act0_cpx
        except NameError:
            inputs['mps_act0_cpx'] = 'DEFINE_LATER'

        # mps_act0_multi:
        #   True or False. It has the same meaning as te_inmps_multi except for
        #   the MPS used as the state at t=0 for the computation of autocorrelation
        #   function.
        try:
            inputs['mps_act0_multi'] = mps_act0_multi
        except NameError:
            inputs['mps_act0_multi'] = 'DEFINE_LATER'

        # te_method:
        #   The time propagation method. The available options are 'rk4' and 'tdvp'.
        #   'rk4' is stands for the time-step targeting (TST) method, while 'tdvp'
        #   stands for the time-dependent variational principle method (TDVP).
        try:
            inputs['te_method'] = te_method
        except NameError:
            inputs['te_method'] = defvals.def_te_method

        # exp_tol:
        try:
            inputs['exp_tol'] = exp_tol
        except NameError:
            inputs['exp_tol'] = defvals.def_exp_tol

        # te_cutoff:
        #   States with eigenvalue below this number will be discarded, even when
        #   the bond dimension is large enough to keep this state.
        try:
            inputs['te_cutoff'] = te_cutoff
        except NameError:
            inputs['te_cutoff'] = defvals.def_te_cutoff

        # krylov_size:
        #   The size of Krylov subspace used to approximate the action of a matrix
        #   exponential on a vector in TDVP propagation. Meaningless if
        #   te_method = 'rk4'.
        try:
            inputs['krylov_size'] = krylov_size
        except NameError:
            inputs['krylov_size'] = defvals.def_krylov_size

        # krylov_tol:
        #   A threshold used to set the accuracy of the Krylov subspace method in
        #   approximating the action of a matrix exponential on a vector in TDVP
        #   propagation.
        try:
            inputs['krylov_tol'] = krylov_tol
        except NameError:
            inputs['krylov_tol'] = defvals.def_krylov_tol

        # n_sub_sweeps:
        #   The number of sweeps in a TST propagation used to improve the
        #   renormalized basis in each time step.
        try:
            inputs['n_sub_sweeps'] = n_sub_sweeps
        except NameError:
            inputs['n_sub_sweeps'] = defvals.def_n_sub_sweeps

        # n_sub_sweeps_init:
        #   The number of sweeps in the first time step of a TST propagation used
        #   to improve the renormalized basis in each time step.
        try:
            inputs['n_sub_sweeps_init'] = n_sub_sweeps_init
        except NameError:
            inputs['n_sub_sweeps_init'] = defvals.def_n_sub_sweeps_init

        # te_normalize:
        #   True or False. If True, the MPS will be normalized after every time
        #   step.
        try:
            inputs['te_normalize'] = te_normalize
        except NameError:
            inputs['te_normalize'] = defvals.def_te_normalize

        # te_sample:
        #   The sampling time points around which the observables will be
        #   calculated and printed. It accepts three formats: a numpy vector of
        #   monotonically increasing time points, a tuple of the form
        #   ('steps', n) with n an integer, and a tuple of the form ('delta', d)
        #   with d a float. The ('steps', n) format is used to choose sampling 
        #   time points using a fixed interval n. n = 1 means that the observables
        #   are calculated and printed exactly every time step. n = 2 means that
        #   the observables are calculated and printed at every second time step.
        #   The ('delta', d) format is used to choose sampling time points at a
        #   fixed time interval. d = 0.01 means that the sampling time points are
        #   separated by 0.01 a.u. of time.
        #   Note that sampling times only tell the program approximately around
        #   which time points should observables be calculated. The actual time
        #   points when the observables are printed are those determined by dt
        #   which are the the closest to a particular te_sample. For example, if
        #   the only sampling time point is 12.6 and two propagation time points
        #   around it is 12.0 and 13.0, then the observables will be printed at
        #   t = 13.0. This means that the ('steps', n) format produces sampling 
        #   time points that are exactly a subset of the propagation time points.
        #   If dt contains non-uniform time steps, however, the ('steps', n)
        #   format will produce sampling time points which are not uniformly
        #   spaced (uniform spacing might desired for Fourier transform). To
        #   exact subset of the propagation time points which are not uniformly
        #   ensure uniformly spaced sampling points that are also the spaced (as
        #   is usually true because the first few time steps should typically be
        #   really short compared to at the later times), one can do
        #     dt = [DT/m]*m + [DT/n]*n + [DT]
        #     te_sample = ('delta', p*dt[-1])
        #   where m, n, and p are integers, while DT is a floating point.
        try:
            inputs['te_sample'] = te_sample
        except NameError:
            inputs['te_sample'] = defvals.def_te_sample

        # te_save_mps:
        #   Determines how often the instantaneous MPS should be saved. The
        #   available options are:
        #     1) 'overwrite'. MPS files are saved at the sampling time points
        #        under the folder <prefix>.mps_t where <prefix> is the value of
        #        prefix input. These MPS files overwrite the MPS files saved in
        #        the previous sampling time point.
        #     2) 'sampled'. MPS files are saved at every sampling time points.
        #        This option can lead to a huge space taken up by the MPS files.
        #        This option is usually used if you want to use these
        #        instantaneous MPS for later analyses that are not available
        #        already in this program and for which the use of 1RDM alone is
        #        not enough. If that is not your plan, using 'overwrite\' is 
        #        recommended.
        #     3) 'no'. MPS files will not be saved.
        #   Regardless of the value of te_save_mps, the instantaneous MPS can be
        #   saved 'on-demand' by using probe files.
        try:
            inputs['te_save_mps'] = te_save_mps
        except NameError:
            inputs['te_save_mps'] = defvals.def_te_save_mps

        # te_save_1pdm:
        #   True or False. If True, the 1-electron RDM is saved at every
        #   sampling time points under the folder <prefix>.sample where <prefix>
        #   is the value of prefix input.
        try:
            inputs['te_save_1pdm'] = te_save_1pdm
        except NameError:
            inputs['te_save_1pdm'] = defvals.def_te_save_1pdm

        # te_save_2pdm:
        try:
            inputs['te_save_2pdm'] = te_save_2pdm
        except NameError:
            inputs['te_save_2pdm'] = defvals.def_te_save_2pdm

        # save_txt:
        try:
            inputs['save_txt'] = save_txt
        except NameError:
            inputs['save_txt'] = defvals.def_save_txt

        # save_npy:
        try:
            inputs['save_npy'] = save_npy
        except NameError:
            inputs['save_npy'] = defvals.def_save_npy

        # te_in_singlet_embed:
        #   A 2-entry tuple of the form (True|False, n). Specify this input
        #   with the first entry set to True if the initial MPS is in singlet-
        #   embedding format, and n (second entry) set to the actual number of
        #   active electrons in the system. Due to the singlet-embedded form,
        #   the number of electrons in the initial MPS is adjusted so that the
        #   total spin can be zero.
        try:
            inputs['te_in_singlet_embed'] = te_in_singlet_embed
        except NameError:
            inputs['te_in_singlet_embed'] = defvals.def_te_in_singlet_embed

        # bo_pairs:
        #   Lowdin bond order.
        try:
            inputs['bo_pairs'] = bo_pairs
        except NameError:
            inputs['bo_pairs'] = defvals.def_bo_pairs

    return inputs
#######################################################

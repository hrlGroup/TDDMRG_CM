
def_memory = 1E9
def_verbose_lvl = 4
def_prev_logbook = None
def_complex_MPS_type = 'hybrid'
def_dump_inputs = False
def_orb_path = None
def_orb_order = 'genetic'
def_ecp = None
def_group = 'c1'
def_mrci = None

def_gs_inmps_fname = 'mps_info.bin'
def_gs_inmps_dir = None
def_gs_steps = 50
def_gs_noise = [1E-3]*4 + [1E-4]*4 + [0.0]
def_gs_dav_tols = [1E-2]*2 + [1E-3]*2 + [1E-6]*500
def_gs_conv_tol = 1E-6
def_gs_cutoff = 1E-14
def_gs_occs = None
def_gs_bias = 1.0
def_gs_outmps_fname = 'GS_MPS_INFO'
def_save_gs_1pdm = False
def_flip_spectrum = False
def_gs_out_cpx = False

def_ann_orb_thr = 1.0E-12
def_ann_inmps_fname = 'GS_MPS_INFO'
def_ann_outmps_fname = 'ANN_MPS_INFO'
#OLD def_ann_fit_margin = 150
def_ann_fit_noise = [1e-5]*4 + [1E-6]*4 + [0.0]
def_ann_fit_tol = 1E-7
def_ann_fit_steps = 50
def_ann_fit_cutoff = 1E-14
def_ann_fit_occs = None
def_ann_fit_bias = 1.0
def_normalize_annout = True
def_save_ann_1pdm = False
def_ann_out_singlet_embed = False
def_ann_out_cpx = False

def_delta_kick_inmps_fname = 'GS_MPS_INFO'
def_delta_kick_outmps_fname = 'DK_MPS_INFO'
def_delta_kick_fit_noise = None 
def_delta_kick_fit_tol = 1E-7
def_delta_kick_fit_steps = 50
def_delta_kick_fit_cutoff = 1E-14
def_delta_kick_fit_occs = None
def_delta_kick_fit_bias = 1.0
def_normalize_delta_kickout = True
def_save_delta_kick_1pdm = False
def_delta_kick_inmps_cpx = False
def_delta_kick_inmps_multi = False

def_te_inmps_fname = 'ANN_MPS_INFO'
def_te_method = 'tdvp'
def_tinit = 0.0
def_te_inmps_cpx = False
def_te_inmps_multi = False
def_exp_tol = 1.0E-6
def_te_cutoff = 0
def_te_normalize = False

def_krylov_size = 20
def_krylov_tol = 5.0E-6
def_n_sub_sweeps = 2
def_n_sub_sweeps_init = 4

def_te_sample = None
def_te_save_mps = 'overwrite'
def_te_save_1pdm = True
def_te_save_2pdm = False
def_save_txt = True
def_save_npy = True
def_te_in_singlet_embed = (False, None)
def_bo_pairs = None

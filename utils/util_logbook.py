import pickle
from TDDMRG_CM.utils import util_print as uprint



########################################################
def parse(inputs0):
    inputs = inputs0.copy()

    for key in inputs:
        if inputs[key] == 'logbook':
            assert inputs['prev_logbook'] is not None, f"The input '{key}' is using " + \
                'the value of the same input from a logbook but no logbook location is ' + \
                'specified in the input file. Provide the path to a logbook using ' + \
                '\'prev_logbook\' input keyword.'
            with open(inputs['prev_logbook'], 'rb') as f:
                logbook = pickle.load(f)
            break

    for key in inputs:
        if isinstance(inputs[key], str):
            key0 = None
            if inputs[key] == 'logbook':
                key0 = key
            elif inputs[key][0:8] == 'logbook:':
                key0 = inputs[key][8:]
            else:
                pass

            if key0 is not None:
                assert key0 in logbook, f"The keyword '{key0}' cannot be found in the " + \
                    'specified previous logbook. Check your previous logbook again.'
                inputs[key] = logbook[key0]
        else:
            pass
    return inputs
########################################################


########################################################
def read(path):
    '''
    Load a logbook from a logbook file.
    '''
    with open(path, 'rb') as f:
        logbook = pickle.load(f)
    return logbook
########################################################


########################################################
def content(lb):
    uprint.print_section('Content of logbook')
    for kw in lb:
        uprint.print_i2(kw, ' = ', lb[kw])
########################################################


########################################################
def save(logbook, fname, terminate=False, verbose=4):
    if verbose >= 2:
        print('Saving logbook file \'' + fname + '\' into the current directory.')
        
    with open(fname, 'wb') as f:
        try:
            pickle.dump(logbook, f)
        except TypeError:
            for key in logbook:
                print(key, type(logbook[key]))
            if terminate:
                raise TypeError('The types of the above keys are not compatible with pickle.')
            else:
                uprint.print_warning('The above keys are not saved in the logbook because ' +
                                     'their types are not compatible with pickle.')
########################################################

__doc__ = """
Information management for inferring synaptic connections

Nicholas Turner <nturner@cs.princeton.edu>, 2018
"""
import operator

import numpy as np
import pandas as pd

SCORE_TYPES = ["sum", "average", "mix"]
RECORD_SCHEMA = [("presyn_segid", np.uint64), ("postsyn_segid", np.uint64),
                 ("presyn_wt", np.float32), ("postsyn_wt", np.float32),
                 ("presyn_sz", np.uint16), ("postsyn_sz", np.uint16),
                 ("presyn_x", np.uint32), ("presyn_y", np.uint32),
                 ("presyn_z", np.uint32),
                 ("postsyn_x", np.uint32), ("postsyn_y", np.uint32),
                 ("postsyn_z", np.uint32),
                 ("presyn_basin", np.uint64), ("postsyn_basin", np.uint64)]
NULL_VALUES = {np.uint64:0, np.uint32:0, np.uint16:0, np.float32:np.nan}


def empty_dataframe():
    """ Creates an empty dataframe with the necessary schema """
    names = list(map(operator.itemgetter(0), RECORD_SCHEMA))
    types = list(map(operator.itemgetter(1), RECORD_SCHEMA))

    series = {name: pd.Series(dtype=dt) for (name, dt) in zip(names, types)}
    return pd.DataFrame(series)


def empty_record():
    names = list(map(operator.itemgetter(0), RECORD_SCHEMA))
    types = list(map(operator.itemgetter(1), RECORD_SCHEMA))

    return dict((name,NULL_VALUES[dt]) for (name,dt) in zip(names,types))


def compute_info(outputs, score_type):
    record = empty_record()

    


def merge_info(old_info, new_info, score_type):
    pass


def make_assignment(cleft_info, score_type):
    pass

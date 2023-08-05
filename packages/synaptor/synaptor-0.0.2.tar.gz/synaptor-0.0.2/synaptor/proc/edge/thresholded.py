#!/usr/bin/env python

from . import asynet


def infer_edges_w_threshs(net, img, cleft, seg, offset, patchsz, wshed=None,
                          samples_per_cleft=2, dil_param=5, cleft_ids=None,
                          thresh=None, presyn_thresh=None, postsyn_thresh=None):

    edge_dframe = asynet.infer_edges(net, img, cleft, seg, offset, patchsz,
                                     wshed=wshed, dil_param=dil_param,
                                     samples_per_cleft=samples_per_cleft,
                                     cleft_ids=cleft_ids)

    if thresh is not None:
        presyn_thresh = thresh
        postsyn_thresh = thresh

    return threshold_dframe(edge_dframe, presyn_thresh, postsyn_thresh)


def threshold_dframe(df, presyn_thresh, postsyn_thresh):

    assert "presyn_wt" in asynet.RECORD_SCHEMA, "record schema out of sync"
    assert "postsyn_wt" in asynet.RECORD_SCHEMA, "record schema out of sync"

    df = df[df["presyn_wt"] >= presyn_thresh]
    df = df[df["postsyn_wt"] >= postsyn_thresh]

    return df

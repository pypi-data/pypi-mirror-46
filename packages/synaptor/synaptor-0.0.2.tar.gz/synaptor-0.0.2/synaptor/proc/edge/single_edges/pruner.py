#!/usr/bin/env python

from ... import candidate
from .. import pruner
from .... import seg_utils
from ....types import bbox


def infer_edge_in_patches(cleft_id, net, patchsz,
                          img_p, seg_p, clf_p, prx_p=None):

    cands = candidate.extract_label_candidates(clf_p, seg_p, dil_param=3,
                                               overlap_thresh=0)

    cands = list(filter(lambda c: c[0] == cleft_id, cands))

    preds = pruner.max_candidates(net, img_p, seg_p,
                                  patchsz, cands, prox=prx_p,
                                  cleft=clf_p, loc_type="vol_center")

    return preds[0]

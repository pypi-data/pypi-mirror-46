#!/usr/bin/env python3


from .... import types
from .... import io


def make_local_window(point, patchsz):
    begin = point - types.Vec3d(patchsz) // 2
    end = begin + patchsz

    return types.BBox3d(begin, end)


def pull_local_window(cvname, point, patchsz,
                      resolution=(4, 4, 40), parallel=1,
                      progress=True):

    bbox = make_local_window(point, patchsz)

    return io.read_cloud_volume_chunk(cvname, bbox, mip=resolution,
                                      parallel=parallel, progress=progress)


def pull_inf_windows(point, patchsz,
                     img_cvname, seg_cvname, clf_cvname,
                     resolution=(4, 4, 40), parallel=1,
                     progress=True):

    img_p = pull_local_window(img_cvname, point, patchsz, progress=progress,
                              resolution=resolution, parallel=parallel)
    seg_p = pull_local_window(seg_cvname, point, patchsz, progress=progress,
                              resolution=resolution, parallel=parallel)
    clf_p = pull_local_window(clf_cvname, point, patchsz, progress=progress,
                              resolution=resolution, parallel=parallel)


    return img_p, seg_p, clf_p

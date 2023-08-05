import numpy as np
from torch.utils.data import Dataset


class AsynetDataset(Dataset):

    def __init__(self, img, seg, clf, cleft_ids,
                 patchsz, samples_per_cleft=2):

        assert img.shape == seg.shape == clf.shape, "mismatched data"

        self.img = img
        self.seg = seg
        self.clf = clf

        self.cleft_ids = cleft_ids
        self.locs = self.pick_cleft_locs(clf, cleft_ids, samples_per_cleft)

    def __len__(self):
        return sum(map(len,self.locs))

    def __getitem__(self, idx):
        pass

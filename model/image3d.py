import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import thresholding as th
from skimage import morphology, segmentation


class Image3d:

    def __init__(self):
        self.images = None
        self.layers = None
        self.imsize = None
        self.images_modified = None

    def load_data(self, data: np.array):
        self.images = data
        self.images_modified = None
        self.layers = len(data)
        self.imsize = data[0].shape

    def binarize(self, threshold_name):

        names = {
            'otsu': th.threshold_otsu,
            'li': th.threshold_li,
            'mean': th.threshold_mean,
            'yen': th.threshold_yen,
            'None': None
        }
        if threshold_name == 'None':
            self.images_modified = None
        elif self.images_modified is not None:
            thresh = names[threshold_name](self.images_modified)
            self.images_modified = self.images_modified > thresh
        elif self.images is not None:
            thresh = names[threshold_name](self.images)
            self.images_modified = self.images > thresh

    def morph(self, func):

        names = {
            'skeletonize': morphology.skeletonize_3d,
            'open': morphology.opening,
            'close': morphology.closing,
            'dilation': morphology.dilation,
            'erosion': morphology.erosion,
            'watershed': segmentation.watershed,
        }
        if self.images_modified is not None:
            new_images = names[func](self.images_modified)
            self.images_modified = new_images
        elif self.images is not None:
            new_images = names[func](self.images)
            self.images_modified = new_images

    def apply(self):
        if self.images_modified is not None:
            self.images = np.array(self.images_modified)
            self.images_modified = None

    def revert(self):
        self.images_modified = None

import matplotlib.pyplot as plt
import numpy as np
from skimage import util
from skimage.data import cells3d
from skimage.filters import thresholding as th
from skimage import morphology

data = util.img_as_float(cells3d()[:, 1, :, :])


class Image3d:

    def __init__(self, data: np.array):
        self.images = data
        self.images_modified = None
        self.layers = len(data)
        self.imsize = data[0].shape

    def binarize(self, threshold_name):

        names = {
            'otsu': th.threshold_otsu,
            'li': th.threshold_li,
            'mean': th.threshold_mean,
            'yen': th.threshold_yen
        }

        thresh = names[threshold_name](self.images)
        self.images_modified = self.images > thresh

    def morph(self, func):
        new_images = []
        for image in self.images:
            new_images.append(func(image))
        self.images_modified = new_images

    def apply(self):
        self.images = np.array(self.images_modified)
        self.images_modified = None


def display(im3d, cmap="gray", step=2):
    _, axes = plt.subplots(nrows=5, ncols=6, figsize=(16, 14))

    for ax, image in zip(axes.flatten(), im3d[::step]):
        ax.imshow(image, cmap=cmap)
        ax.set_xticks([])
        ax.set_yticks([])



im = Image3d(data)
im.binarize('otsu')
im.apply()
display(im.images)
im.morph(morphology.binary_erosion)
display(im.images_modified)
plt.show()

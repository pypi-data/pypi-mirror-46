# -*- coding: utf-8 -*-

import numpy as np
from skimage import morphology
from skimage import measure


__all__ = ['remove_weak_connection',
           ]


def remove_weak_connection(bin_img):
    """ Remove weak connection in binary image.

    Parameters
    ----------
    bin_img: np.array
        numpy binary image.

    Returns
    -------
    refine_img : np.array
        weak boundary removed binary image

    """

    refine_img = np.zeros_like(bin_img, dtype=bool)
    all_labels = measure.label(bin_img)
    region_num = len(np.unique(all_labels))

    for r in np.arange(1, region_num):
        cur_region = (all_labels == r)
        open_region = morphology.opening(cur_region, morphology.square(5))
        region_num = len(np.unique(measure.label(open_region))) - 1
        if region_num > 1:
            refine_img += open_region
            diff = cur_region ^ open_region
            diff_labels = measure.label(diff)
            diff_num = len(np.unique(diff_labels))
            for d in np.arange(1, diff_num):
                cur_diff = diff_labels == d
                diff_add = open_region + cur_diff
                cur_region_num = len(np.unique(measure.label(diff_add))) - 1
                if  cur_region_num == region_num:
                    refine_img += cur_diff
        else:
            refine_img += cur_region

    return refine_img

# -*- coding: utf-8 -*-

import numpy as np

__all__ = ['crop_center',
           ]

def crop_center(img, crop_h, crop_w):
    """ Crop center part of image.

    Parameters
    ----------
    img: np.array
        numpy image
    crop_h: int
        height of cropped image
    crop_w: int
        width of cropped image

    Returns
    -------
    crop_img: np.array
        center cropped image

    """

    img_h, img_w = img.shape[0], img.shape[1]
    if crop_h > img_h or crop_w > img_w:
        raise AssertionError("Cropped image shape too large")

    start_h = int(np.floor((img_h - crop_h) / 2))
    start_w = int(np.floor((img_w - crop_w) / 2))

    crop_img = img[start_h:start_h+crop_h, start_w:start_w+crop_w]

    return crop_img

# -*- coding: utf-8 -*-

import numpy as np


__all__ = ['blend_images',
           ]


def blend_images(img1, img2, alpha=0.5):
    """ Blend two images with alpha as ratio

    """

    if alpha < 0.0 or alpha > 1.0:
        raise AssertionError("alpha value should be between 0 to 1")
    if img1.shape != img2.shape:
        raise AssertionError("Two image should be of same shape")

    if np.amax(img1) > 1: # if value of img1 is 0-255
        img1 = img1 / 255.0
    if np.amax(img2) > 1:
        img2 = img2 / 255.0

    combine = img1 * alpha + img2 * (1.0 - alpha)
    combine = (combine * 255.0).astype(np.uint8)

    return combine

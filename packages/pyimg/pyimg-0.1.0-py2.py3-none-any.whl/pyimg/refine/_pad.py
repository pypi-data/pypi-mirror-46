# -*- coding: utf-8 -*-

import numpy as np

__all__ = ['pad_image',
           ]

def pad_image(img, ttl_h, ttl_w):
    """ Pad image to be with fixed-size.

    Parameters
    ----------
    img: np.array
        numpy image
    ttl_h: int
        height of the padded image
    ttl_w: int
        width of the padded image

    Returns
    -------
    pad_img: np.array
        padded image

    """

    pad_img = None

    if len(img.shape) == 2:
        pad_img = np.zeros((ttl_h, ttl_w), dtype=np.uint8)
    elif len(img.shape) ==3 and img.shape[2] == 3:
        pad_img = np.zeros((ttl_h, ttl_w, 3), dtype=np.uint8)
    else:
        raise AssertionError("Unknon image shape")

    img_h, img_w = img.shape[0], img.shape[1]
    start_h = int(np.floor(ttl_h - img_h)/2.0)
    start_w = int(np.floor(ttl_w - img_w)/2.0)
    pad_img[start_h:start_h+img_h, start_w:start_w+img_w] = img

    return pad_img

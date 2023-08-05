# -*- coding: utf-8 -*-

from skimage import io


__all__ = ['Img',
           ]


class Img(object):
    def __init__(self, np_arr):
        self.data = np_arr
        self.type = self.data.dtype
        self.shape = np_arr.shape
        self._height = self.shape[0]
        self._width = self.shape[1]
        if len(self.shape) == 3:
            self._channel = self.shape[2]
        else:
            self._channel = 0

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def channel(self):
        return self._channel

    def save(self, img_path):
        io.imsave(img_path, self.data)

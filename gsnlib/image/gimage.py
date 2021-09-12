#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Iterable, Literal, Optional
from PIL import Image as PILImage
from PIL import ImageDraw as PILImageDraw

import numpy as np
import scipy.ndimage


class Image:
    width: int
    height: int
    pixels: Optional[Iterable[int]]

    def __init__(self,
                 width: int,
                 height: int,
                 data: Optional[Iterable[int]],
                 mode: str = 'RGBA'):
        self.width = width
        self.height = height
        self.pixels = data
        self.mode = mode
        self.draw = None

        if self.pixels is None:
            if len(self.mode) > 1:
                self.pixels = np.zeros((self.height, self.width, len(mode)),
                                       dtype=np.uint8)
            else:
                self.pixels = np.zeros((self.height, self.width),
                                       dtype=np.uint8)

    def resize(self, w: int, h: int, glitch: bool = False):
        sx = None
        sy = None

        # We don't scale to 0! Return nothing!
        if w == 0 and h == 0:
            return None

        if w != 0:
            sx = float(w) / float(self.width)

        if h != 0:
            sy = float(h) / float(self.height)

        if h == 0:
            sy = sx

        if w == 0:
            sx = sy

        if glitch:
            # NOTE: This gave an interesting glitchy scale
            pixels = self.pixels.reshape(self.width,
                                         self.height,
                                         len(self.mode))
            pixels = scipy.ndimage.zoom(pixels, (sx, sy, 1))

            width = pixels.shape[0]
            height = pixels.shape[1]

        else:
            pixels = self.pixels.reshape(self.height,
                                         self.width,
                                         len(self.mode))
            pixels = scipy.ndimage.zoom(pixels, (sy, sx, 1))

            width = pixels.shape[1]
            height = pixels.shape[0]

        #pixels.shape = (-1, len(self.mode))

        return self.create(width, height, pixels, mode=self.mode)
        # print(self.pixels.shape)

    def save(self, filename: str):
        """
        if len(self.mode) > 1:
            data = self.pixels.reshape(self.height, self.width, len(self.mode))
        else:
            data = self.pixels.reshape(self.height, self.width)
        #print(data.shape)

        img = PILImage.fromarray(data)

        if len(self.mode) > 1:
            data = img.tostring('raw', 'BGRA')
            data = np.fromstring(data, dtype=np.uint8)
            data.shape = (self.height, self.width, len(self.mode))
            img = PILImage.fromarray(data)
        """
        img = PILImage.fromarray(self.pixels)
        img.save(filename)

    def premultiply_alpha(self):
        s = self.pixels.astype(float)
        alpha = s[:, :, 3] / 255.0
        s[:, :, 0] *= alpha
        s[:, :, 1] *= alpha
        s[:, :, 2] *= alpha

        s[s < 0] = 0
        s[s > 255] = 255

        self.pixels = s.astype(np.uint8)

    def add_alpha(self, alpha):
        # Add an image channel as alpha

        # print(self.pixels.shape)
        self.pixels[:, :, 3] = alpha.pixels

    def channel_copy(self, dch: int, sch: int, invert: bool = False):
        # Copies one channel into another
        if invert:
            self.pixels[:, :, dch] = 255 - self.pixels[:, :, sch]
        else:
            self.pixels[:, :, dch] = self.pixels[:, :, sch]

    def get_2d_data(self):
        if len(self.mode) > 1:
            data = self.pixels.reshape(self.height, self.width, len(self.mode))
        else:
            data = self.pixels.reshape(self.height, self.width)

        return data

    def get_pil(self):
        #print("Get pil")
        # return PILImage.fromarray(self.get_2d_data())
        # print(type(self.pixels))
        # print(self.pixels.shape)
        # print(self.pixels.shape)
        return PILImage.fromarray(self.pixels)

    def get_float(self):
        out = self.pixels.astype(float)
        out /= 255.0
        return out

    def get_array(self):
        return np.array(self.pixels)

    @classmethod
    def fromarray(cls, data, mode=None, premult=False):
        return cls.from_pil(PILImage.fromarray(data), mode=mode)

    @classmethod
    def from_pil(cls, img, mode='RGBA', premult=False):
        if mode is not None and img.mode != mode:
            img = img.convert(mode)

        out = cls(img.size[0], img.size[1], np.array(img), mode=img.mode)
        """
        if len(mode) > 1:
            s = img.tostring('raw', 'BGRA')
            s = np.fromstring(s, dtype=np.uint8)
            s.shape = (-1, len(mode))
        else:
            s = img.tostring('raw', mode)
            s = np.fromstring(s, dtype=np.uint8)
            s.shape = (-1)

        out = cls(img.size[0], img.size[1], s, mode=mode)

        if premult:
            if len(mode) == 2 or len(mode) == 4:
                out.premultiply_alpha()

        """
        return out

    @classmethod
    def create(cls, width, height, data, mode='RGBA'):
        out = cls(width, height, data, mode=mode)

        return out

    @classmethod
    def open(cls, filename: str, mode: str = 'RGBA', premult: bool = False):
        try:
            img = PILImage.open(filename)
            return cls.from_pil(img, mode, premult)
        except Exception:
            print("Could not open ", filename)
            raise Exception

    def crop(self, x0, y0, x1, y1):
        assert x0 < x1
        assert y0 < y1

        assert x0 != x1
        assert y0 != y1

        assert x0 >= 0
        assert y0 >= 0
        assert x1 > 1
        assert y1 > 1

        data = self.pixels

        data = data[y0:y1, x0:x1]

        self.pixels = data
        self.width = x1 - x0
        self.height = y1 - y0

    def copy(self, x0: int, y0: int, x1: int, y1: int):
        data = self.pixels[y0:y1, x0:x1]
        return self.fromarray(data)

    def crop_to_channel(self, ch=3):
        # Convert pixels to array
        #data = self.get_2d_data()
        data = self.pixels

        if len(self.mode) > 1:
            c = data[:, :, ch]
        else:
            c = data[:, :]

        t = np.where(c > 0)

        minx: float = t[1].min()
        maxx: float = t[1].max()

        miny: float = t[0].min()
        maxy: float = t[0].max()

        if len(self.mode) > 1:
            data = data[miny:maxy, minx:maxx, :]
            #self.pixels = data.reshape(-1, len(self.mode))

        else:
            data = data[miny:maxy, minx:maxx]
            #self.pixels = data.reshape(-1)
        self.pixels = data
        self.width = (maxx - minx)
        self.height = (maxy - miny)

    ######
    # Get in different data formats
    ######

    def get_pixels_cairo(self, mode=None):
        if mode is None:
            mode = self.mode

        img = self.get_pil()

        if img.mode != 'RGBA':
            img.convert('RGBA')

        s = img.tostring('raw', 'RGBA')
        s = np.fromstring(s, dtype=np.uint8)
        s.shape = (-1, len(mode))

        return s

    ######
    # Primitive draw functions through PIL
    ######
    def beginDraw(self):
        if self.draw is None:
            self.img = self.get_pil()
            self.draw = PILImageDraw.Draw(self.img)

    def endDraw(self):
        if self.draw is not None:
            del self.draw
            self.draw = None

        out = self.from_pil(self.img, self.img.mode, premult=False)
        return out

    def draw_polygon(self, xy, fill=None, outline=None):
        if self.draw is None:
            raise Exception("Not in drawing mode")

        self.draw.polygon(xy, fill=fill, outline=outline)

    ######
    # Filters
    #####

    def blur(self, sigma=5, channel=None, mode='constant', cval=0.0):
        if channel is None:
            return self.fromarray(
                scipy.ndimage.gaussian_filter(self.pixels,
                                              sigma=sigma,
                                              mode=mode,
                                              cval=cval), mode=self.mode)

        else:
            data = self.pixels.copy()
            ch = data[:, :, channel]
            ch = scipy.ndimage.gaussian_filter(ch, sigma=sigma,
                                               mode=mode, cval=cval)
            data[:, :, channel] = ch
            return self.fromarray(data)

    def vignette(self, radius: float = 0.3, inner_radius: float = 0.3, channel: Literal[0, 1, 2, 3] = 3):
        center = (0.5, 0.5)
        aspect_correction = (1.0, 1.0)

        if self.width > self.height:
            aspect_correction = (float(self.width) / float(self.height), 1.0)
        else:
            aspect_correction = (1.0, float(self.height) / float(self.width))

        pihalf_div_radius = 0.5 * np.pi / radius
        pihalf = np.pi * 0.5

        #yoffset = self.height / 2.0
        #xoffset = self.width / 2.0

        indices = np.indices(self.pixels.shape[0:2]).astype(float)
        indices[0] /= float(self.height)
        indices[0] -= center[1]
        indices[0] *= aspect_correction[0]

        indices[1] /= float(self.width)
        #indices[1] -= xoffset
        indices[1] -= center[0]
        indices[1] *= aspect_correction[1]

        dist = (np.sqrt(np.power(
            indices[0], 2) + np.power(indices[1], 2)) - inner_radius) * pihalf_div_radius
        dist = np.clip(dist, 0, pihalf)
        falloff = np.cos(dist) * np.cos(dist)
        self.pixels[:, :, channel] *= falloff

    def vignette2(self, amount: float = 0.1, sigma: int = 5):
        edge = np.ceil(min(self.width, self.height) * amount).astype(int)

        alpha = np.ones((self.height, self.width)).astype(float)

        alpha[-edge:, :] = 0.0
        alpha[:edge, :] = 0.0
        alpha[:, :edge] = 0.0
        alpha[:, -edge:] = 0.0
        alpha = scipy.ndimage.gaussian_filter(alpha, sigma=sigma,
                                              mode='constant', cval=0.0)
        t = self.pixels[:, :, 3] * alpha
        return t.astype(int)

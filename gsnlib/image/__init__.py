#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from typing import Any, Dict, Literal, Optional, Tuple, Union

from PIL import Image
from PIL import ImageDraw
import numpy as np
from scipy import ndimage

from ..utils import file_hash, offsetter


class GSNImage(object):
    filename: Union[Path, None]
    img: Union[Image.Image, None]

    def __init__(self,
                 filename: Optional[Path] = None,
                 checksum: bool = False):
        self.info: Dict[str, Any] = {}
        self.img = None
        self.filename = None
        self.pixels = None
        self.draw = None

        if filename is not None:
            self.filename = filename

            if checksum is True:
                self.info['hash'] = file_hash(filename)

    # , infofile=None):
    def open(self, filename: Optional[Path] = None, checksum: bool = True):
        if filename is not None:
            self.filename = self.info['filename'] = filename

        # if infofile is not None:
        #    self.infofile = infofile

        if self.filename is None or not self.filename.is_file():
            raise IOError

        if checksum:
            self.info['hash'] = file_hash(self.filename)

        try:
            self.img = Image.open(self.filename)
        except IOError:
            raise IOError

        self.img.load()

        # if infofile is not None:
        #    self.open_info(infofile)

    def save(self, filename: Path):
        self.filename = filename
        if self.img is not None:
            self.img.save(self.filename)

    def get_thumb(self,
                  size: Tuple[int, int],
                  resample: Literal[0, 1, 2, 3, 4, 5] = 0,
                  mode: str = 'RGB'):
        """
            Returns a PIL Image copy of this image
        """
        out = None
        if self.img is None and self.filename is not None:
            try:
                out = Image.open(self.filename)
            except IOError:
                raise IOError
        elif self.img is not None:
            out = self.img.copy()

        if out is not None:
            if out.mode != mode:
                out = out.convert(mode)
            out.thumbnail(size, resample=resample)
        return out

    def get_data(self):
        """
            Returns the array of the pixel data of this image
        """
        self.pixels = np.array(self.img)
        return self.pixels

    def get(self):
        return GSNImage.fromarray(self.get_data())

    def update_data(self):
        self.img = Image.fromarray(self.pixels)
        self.pixels = None

    @staticmethod
    def fromarray(arr):
        """
            Creates a GSNImage from an array
        """
        newimg = GSNImage(checksum=False)
        newimg.img = Image.fromarray(arr)
        return newimg

    @staticmethod
    def save_from_array(array, filename: Path):
        """
            SAves an image based on a numpy array
        """
        result = Image.fromarray(array)
        result.save(filename)

    """
        Manipulation functions
    """

    def add_alpha(self,
                  value: Union[int, Image.Image] = 255,
                  mask: Optional['GSNImage'] = None):
        """
            Adds an alpha channel to the image,
            and sets it to the value specified.
            Function modifies object
        """
        if mask is not None and mask.img is not None:
            value = mask.img

        if self.img:
            self.img.putalpha(value)

    def rotate(self,
               angle: float,
               offset: Optional[Tuple[int, int]] = None,
               center: Optional[Tuple[int, int]] = None):
        """
            Rotate image <angle> degrees
        """
        d = self.get_data()
        if center is not None:

            nh = (abs(d.shape[0] / 2 - center[1]) + d.shape[0] / 2) * 2
            nw = (abs(d.shape[1] / 2 - center[0]) + d.shape[1] / 2) * 2

            dd = np.zeros((nh, nw, d.shape[2]), dtype=d.dtype)
            print(" ")
            print(nh, nw)
            print(" ")
            np.copyto(dd[nh / 2 - center[1]:nh - center[1] + d.shape[0],
                         nw / 2 - center[0]:nw - center[0] + d.shape[1]], d)

            d = dd

        if offset is not None:
            dd = np.zeros((d.shape[0] + abs(offset[1]),
                           d.shape[1] + abs(offset[0]),
                          d.shape[2]), dtype=d.dtype)
            if offset[0] < 0:
                xo = 0
            else:
                xo = offset[0]
            if offset[1] < 0:
                yo = 0
            else:
                yo = offset[1]

            np.copyto(dd[yo:yo + d.shape[0], xo:xo + d.shape[1]], d)
            d = dd
        return self.fromarray(ndimage.interpolation.rotate(d, angle))

    def add(self,
            data,
            offset: Tuple[int, int] = (0, 0),
            mode: str = 'center'):
        """
            Add image <data> to this image,
            offset at <offset>
            Will expand image if needed
            Returns GSNImage

        """
        d = self.get_data()
        if isinstance(data, self.__class__):
            data = data.get_data()

        nw, dxo, dataxo = offsetter(d.shape[1], data.shape[1], offset[0], mode)
        nh, dyo, datayo = offsetter(d.shape[0], data.shape[0], offset[1], mode)

        print("New shape", nw, nh)
        print("Source offset", dxo, dyo)
        print("Added offset", dataxo, datayo)

        out = np.zeros((nh, nw, d.shape[2]), dtype=d.dtype)

        out[dyo:d.shape[0] + dyo, dxo:d.shape[1] + dxo] = d

        t = out[datayo:data.shape[0] + datayo, dataxo:data.shape[1] + dataxo]
        a = Image.fromarray(t)
        b = Image.fromarray(data)
        t = np.array(Image.composite(b, a, b))
        out[datayo:data.shape[0] + datayo, dataxo:data.shape[1] + dataxo] = t
        return self.fromarray(out)

    def scale(self, w: int, h: int):
        """
            Scales image to a certain size
        """
        return self.fromarray(np.array(self.img.resize(
            (w, h), Image.ANTIALIAS
        )))

    def scale_perc(self, perc: float):
        """
            Scales an image by a certain percentage
            Keeps aspect ratio
        """
        oldsize = self.img.size
        arr = np.array(self.img)
        pil_img = self.img.resize(
            (int(oldsize[0] * perc / 100.0),
             int(oldsize[1] * perc / 100.0)),
            Image.ANTIALIAS)
        arr = np.array(pil_img)
        return GSNImage.fromarray(arr)

    def fit_in(self, w: int, h: int):
        return self.scale_perc(
            min(float(w) / float(self.width),
                float(h) / float(self.height)) * 100.0
        )

    def fill_in(self, w: int, h: int):
        return self.scale_perc(
            max(float(w) / float(self.width),
                float(h) / float(self.height)) * 100.0
        )

    def crop_by_channel(self, channel: int = 3):
        data = self.get_data()
        if data.shape[2] < channel:
            return None

        c = data[:, :, channel]

        t = np.where(c > 0)
        minx: float = t[0].min()
        maxx: float = t[0].max()

        miny: float = t[1].min()
        maxy: float = t[1].max()

        return self.fromarray(data[minx:maxx, miny:maxy, :])

    @staticmethod
    def create_image(width: int, height: int, channels: int = 1, format=np.uint8):
        """
            Creates a new empty image/canvas
        """
        data = np.zeros(shape=(height, width), dtype=format)
        # print data.shape
        if channels > 1:
            data.resize((data.shape[0], data.shape[1], 1))
            data = np.repeat(data, channels, 2)

        newimg = GSNImage(checksum=False)
        newimg.img = Image.fromarray(data)

        return newimg

    def get_width(self):
        if self.img:
            return self.img.size[0]

    width = property(get_width, None, None, "Width of image")

    def get_height(self):
        if self.img:
            return self.img.size[1]

    height = property(get_height, None, None, "Height of image")

    """
    Info functions
    """

    def get_info(self, name: str):
        """
            Gets info based on name.
            Splits up name string
            and digs into the info dictionary
        """
        path = name.split('__')
        out = self.info
        for p in path:
            if p not in out:
                return None
            out = out[p]
        return out

    def open_info(self, filename=None):
        if filename is None:
            filename = self.filename + '.json'

        if os.path.exists(filename):
            with open(filename, 'r') as f:
                ind = json.load(f)

            if ind['hash'] == self.info['hash']:
                self.info.update(ind)
                return

        self.analyze()
        self.save_info()

    def save_info(self, filename: Optional[Path] = None):
        print("Saving info")
        if filename is None and self.filename is not None:
            filename = self.filename.with_suffix('json')

            # print json.dumps(self.info, indent=4)
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.info, f, indent=4)
            # print self.info

    def feather(self, level: int):
        self.feather_snow(level)

    @staticmethod
    def snow_pixel(value: float, cur_level: float, step: float):
        if value < cur_level:
            cur_level -= step
        else:
            cur_level = 0
        return cur_level

    def feather_snow(self, level: int):
        step = 256.0

        if level != 0:
            step = 256.0 / level

        data = self.get_data()
        for y in range(self.height):
            # Snow left
            cur_level = 0
            for x in range(self.width):
                v = data[y, x]
                cur_level = self.snow_pixel(v, cur_level, step)
                data[y, x] = cur_level

            # Snow right
            cur_level = 0
            for x in range(self.width):
                v = data[y, self.width - x - 1]
                cur_level = self.snow_pixel(v, cur_level, step)
                data[y, self.width - x - 1] = cur_level

        for x in range(self.width):
            # Snow left
            cur_level = 0
            for y in range(self.height):
                v = data[y, x]
                cur_level = self.snow_pixel(v, cur_level, step)
                data[y, x] = cur_level

            # Snow right
            cur_level = 0
            for y in range(self.height):
                v = data[self.height - y - 1, x]
                cur_level = self.snow_pixel(v, cur_level, step)
                data[self.height - y - 1, x] = cur_level

        self.update_data()

    """
        Drawing functions
        Destructive!
        Will modify image in place
    """

    def begin_draw(self):
        if self.draw is None and self.img is not None:
            self.draw = ImageDraw.Draw(self.img)

    def end_draw(self):
        if self.draw is not None:
            del self.draw
            self.draw = None

    def draw_polygon(self,
                     xy: Tuple[int, int],
                     fill: Union[str, int, Tuple[int, int, int], None] = None,
                     outline: Union[str, int, Tuple[int, int, int], None] = None):
        if self.draw is None:
            raise Exception("Not in drawing mode")

        self.draw.polygon(xy, fill=fill, outline=outline)

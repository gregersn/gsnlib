#!/usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import hashlib

from os import listdir
from os.path import isfile, join


def file_hash(filename, chunk_size=2 ** 8):
    h = hashlib.md5()
    with open(filename) as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            h.update(data)

    return h.hexdigest()


def find_duplicates(folder):
    """
    Returns a list of tuples of duplicate files in a folder, based on
    file hash
    """

    dupes = []
    hashes = {}

    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

    for f in onlyfiles:
        h = file_hash(join(folder, f), chunk_size=256)
        if h in hashes:
            hashes[h].append(f)
        else:
            hashes[h] = [f, ]

    for k in hashes.keys():
        if len(hashes[k]) > 1:
            dupes.append(hashes[k])

    return dupes


def offsetter(aw, bw, offset, mode='center'):
    """
        Calculates a new "width" two room a and b, when b is offset
        Used to calculate each dimension when two images are
        added to each other, with an offset

        Returns tuple with new width, a-offset, b-offset

        modes: 'center', 'corner'

    """

    nw = max(aw, bw)
    ao = 0
    bo = offset

    if mode == 'center':
        if aw >= bw:
            if abs(offset) > (aw / 2.0 - bw / 2.0):
                nw = aw + abs(offset) - ((aw - bw) / 2.0)
        else:
            if abs(offset) > (bw / 2.0 - aw / 2.0):
                nw = bw + abs(offset) - ((bw - aw) / 2.0)

        ao = nw / 2.0
        bo = nw / 2.0

        bo += offset

        ao += (nw / 2.0 - aw / 2.0)
        bo += (nw / 2.0 - bw / 2.0)

        fix = min(ao, bo)

        ao -= fix
        bo -= fix

    elif mode == 'corner':
        if offset > 0:
            nw = max(aw, bw + offset)
        else:
            nw = abs(offset) + max(aw, bw)
            ao = abs(offset)
            bo = 0

    return (int(nw), int(ao), int(bo))

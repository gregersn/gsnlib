import numpy as np
from gsnlib.coordinates import Coordinates

class Vector(object):
    def __init__(self, x, y, z=0):
        self.v = np.array([x, y, z])
    
    def translate(self, x, y):
        pass
    
    def rotate(self, a):
        pass

    @property
    def x(self):
        return self.v[0]
    
    @property
    def y(self):
        return self.v[1]

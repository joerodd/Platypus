# Copyright 2015-2016 David Hadka
#
# This file is part of Platypus, a Python module for designing and using
# evolutionary algorithms (EAs) and multiobjective evolutionary algorithms
# (MOEAs).
#
# Platypus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Platypus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Platypus.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import, division, print_function

import copy
import math
import random
import numpy as np
from abc import ABCMeta, abstractmethod
from .tools import bin2gray, bin2int, int2bin, gray2bin

class Type(object):
    
    __metaclass__ = ABCMeta
    
    def __init__(self):
        super(Type, self).__init__()
        
    @abstractmethod
    def rand(self):
        raise NotImplementedError("method not implemented")
    
    def encode(self, value):
        return value
    
    def decode(self, value):
        return value
        
class Real(Type):
    
    def __init__(self, min_value, max_value):
        super(Real, self).__init__()
        self.min_value = float(min_value)
        self.max_value = float(max_value)
        
    def rand(self):
        return random.uniform(self.min_value, self.max_value)
        
    def __str__(self):
        return "Real(%f, %f)" % (self.min_value, self.max_value)


class Real_Normal(Type):
    def __init__(self, min_value, max_value, default_value, spread=5, clamp = None):
        super(Real_Normal, self).__init__()
        self.min_value = float(min_value)
        self.max_value = float(max_value)
        self.default_value = float(default_value)
        self.spread = spread
        self.clamp = clamp

    def rand(self):
        if self.spread > 0 and not self.clamp[0]:
            value = float(np.random.normal(self.default_value, self.spread, 1))
            value = max([value, self.min_value])
            value = min([value, self.max_value])
        else:
            value = self.default_value
        return value

    def __str__(self):
        return "Real_Normal(%f, %f, %f, %f)" % (self.min_value, self.max_value, self.default_value, self.spread)


class Real_T(Type):
    def __init__(self, min_value, max_value, default_value):
        super(Real_T, self).__init__()
        self.min_value = float(min_value)
        self.max_value = float(max_value)
        self.default_value = float(default_value)

    def rand(self):
        value = np.random.standard_t(df=5) + self.default_value
        value = max([value, self.min_value])
        value = min([value, self.max_value])
        return value

    def __str__(self):
        return "Real_T(%f, %f)" % (self.min_value, self.max_value, self.default_value)


class Binary(Type):
    
    def __init__(self, nbits):
        super(Binary, self).__init__()
        self.nbits = nbits
        
    def rand(self):
        return [random.choice([False, True]) for _ in range(self.nbits)]
        
    def __str__(self):
        return "Binary(%d)" % self.nbits
    
class Integer(Binary):
    
    def __init__(self, min_value, max_value):
        super(Integer, self).__init__(int(math.log(int(max_value)-int(min_value), 2)) + 1)
        self.min_value = int(min_value)
        self.max_value = int(max_value)
        
    def rand(self):
        return self.encode(random.randint(self.min_value, self.max_value))
        
    def encode(self, value):
        return bin2gray(int2bin(value-self.min_value, self.nbits))
    
    def decode(self, value):
        value = bin2int(gray2bin(value))
        
        if value > self.max_value-self.min_value:
            value -= self.max_value-self.min_value
            
        return self.min_value + value
    
    def __str__(self):
        return "Integer(%d, %d)" % (self.min_value, self.max_value)
    
class Permutation(Type):
    
    def __init__(self, elements):
        super(Permutation, self).__init__()
        self.elements = list(elements)
        
    def rand(self):
        elements = copy.deepcopy(self.elements)
        random.shuffle(elements)
        return elements
        
    def __str__(self):
        return "Permutation(%d)" % len(self.elements)
    
class Subset(Type):
    
    def __init__(self, elements, size):
        super(Subset, self).__init__()
        self.elements = list(elements)
        self.size = size
        
    def rand(self):
        indices = list(range(1, len(self.elements)))
        random.shuffle(indices)
        return [self.elements[i] for i in indices[:self.size]]
    
    def __str__(self):
        return "Subset(%d, %d)" % (len(self.elements), self.size)
        
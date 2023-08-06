'''
Author: Dr. Mohamed A. Bouhlel <mbouhlel@umich.edu>

This package is distributed under New BSD license.
'''

from __future__ import division
import warnings
import numpy as np

from smt.surrogate_models.krg_based import KrgBased
from smt.utils.kriging_utils import componentwise_distance

"""
The kriging class.
"""

class KRG(KrgBased):

    def _initialize(self):
        super(KRG, self)._initialize()
        declare = self.options.declare
        declare('theta0', None, types=(list, np.ndarray), desc='Initial hyperparameters')
        self.name = 'Kriging'

    def _componentwise_distance(self,dx,opt=0):
        d = componentwise_distance(dx,self.options['corr'].__name__,
                                   self.nx)
        return d

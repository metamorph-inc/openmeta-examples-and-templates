#!/usr/bin/python
""" OpenMDAO component generating two random 3-D vectors
    bounded by the unit cube scaled by 's'"""

from __future__ import print_function

import math
import numpy as np
from random import random

from openmdao.api import IndepVarComp, Component, Problem, Group


class TwoRandomVectors(Component):

    def __init__(self):
        super(TwoRandomVectors, self).__init__()

        # TODO: verify the default values
        self.add_param('s', val=1.0)

        self.add_output('v1', val=np.array([1,0,0]), pass_by_obj=True)
        self.add_output('v2', val=np.array([0,1,0]), pass_by_obj=True)

    def solve_nonlinear(self, params, unknowns, resids):
        scale = params["s"]

        (vector1, vector2) = self._TwoRandomVectors(scale)

        unknowns['v1'] = vector1
        unknowns['v2'] = vector2

    def _TwoRandomVectors(self, s):
        v1 = s * np.array([random(), random(), random()])
        v2 = s * np.array([random(), random(), random()])
        return (v1, v2)

if __name__ == "__main__":

    top = Problem()

    root = top.root = Group()

    root.add('Input', IndepVarComp('s', 5.0))
    root.add('Generator', TwoRandomVectors())
    root.connect('Input.s', 'Generator.s')

    top.setup()
    top.run()

    print('Vector 1:', root.Generator.unknowns['v1'])
    print('Vector 2:', root.Generator.unknowns['v2'])
    

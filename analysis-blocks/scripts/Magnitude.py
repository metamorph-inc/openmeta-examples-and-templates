#!/usr/bin/python
""" OpenMDAO component generating two random 3-D vectors
    bounded by the unit cube scaled by 's'"""

from __future__ import print_function

import math
import numpy as np

from openmdao.api import IndepVarComp, Component, Problem, Group


class Magnitude(Component):

    def __init__(self):
        super(Magnitude, self).__init__()

        self.add_param('v', val=np.array([1,0,0]), pass_by_obj=True)
        self.add_output('m', val=1.0)

    def solve_nonlinear(self, params, unknowns, resids):
        unknowns["m"] = np.linalg.norm(params["v"])

if __name__ == "__main__":

    top = Problem()

    root = top.root = Group()

    root.add('Input', IndepVarComp('v', np.array([1.0, 1.0, 1.0]), pass_by_obj=True))
    root.add('Magnitude', Magnitude())
    root.connect('Input.v', 'Magnitude.v')

    top.setup()
    top.run()

    print('Magnitude:', root.Magnitude.unknowns['m'])
    

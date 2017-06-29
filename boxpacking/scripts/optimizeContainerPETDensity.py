#!/usr/bin/python
""" OpenMDAO component for optimal packing calculations."""

# ~/GitHub/mdaolab/venv/bin/python optimalPackingPET.py

from __future__ import print_function

import math

from openmdao.api import IndepVarComp, Component, Problem, Group


class Optimize_Container(Component):

    def __init__(self):
        super(Optimize_Container, self).__init__()

        # TODO: verify the default values
        self.add_param('L1', val=0.0, units='m')
        self.add_param('W1', val=0.0, units='m')
        self.add_param('H1', val=0.0, units='m')
        self.add_param('D1', val=0.0, units='kg/m**3')
        self.add_param('L2', val=0.0, units='m')
        self.add_param('W2', val=0.0, units='m')
        self.add_param('H2', val=0.0, units='m')
        self.add_param('D2', val=0.0, units='kg/m**3')

        self.add_output('Length', val=0.0, units='m')
        self.add_output('Width', val=0.0, units='m')
        self.add_output('Height', val=0.0, units='m')
        self.add_output('Volume', val=0.0, units='m^3')
        self.add_output('Mass', val=0.0, units="kg")

    def solve_nonlinear(self, params, unknowns, resids):
        (Length, Width, Height, Volume, Mass) = self._optimizeContainer(
            float(params['L1']),
            float(params['W1']),
            float(params['H1']),
            float(params['D1']),
            float(params['L2']),
            float(params['W2']),
            float(params['H2']),
            float(params['D2']))

        unknowns['Length'] = Length
        unknowns['Width'] = Width
        unknowns['Height'] = Height
        unknowns['Volume'] = Volume
        unknowns['Mass'] = Mass

    def _optimizeContainer(self, L1, W1, H1, D1, L2, W2, H2, D2):
        Length = L1 + L2
        Width = W1 + W2
        Height = H1 + H2
        Volume = Length * Width * Height
        Mass = L1*W1*H1*D1 + L2*W2*H2*D2
        return (Length, Width, Height, Volume, Mass)

if __name__ == "__main__":

    top = Problem()

    root = top.root = Group()

    # TODO: Add reasonable input values for testing purposes
    root.add('L1', IndepVarComp('y', 1.0))
    root.add('W1', IndepVarComp('y', 2.0))
    root.add('H1', IndepVarComp('y', 3.0))
    root.add('L2', IndepVarComp('y', 4.0))
    root.add('W2', IndepVarComp('y', 5.0))
    root.add('H2', IndepVarComp('y', 6.0))

    root.add('Optimize_Container', Optimize_Container())

    root.connect('L1.y', 'Optimize_Container.L1')
    root.connect('W1.y', 'Optimize_Container.W1')
    root.connect('H1.y', 'Optimize_Container.H1')
    root.connect('L2.y', 'Optimize_Container.L2')
    root.connect('W2.y', 'Optimize_Container.W2')
    root.connect('H2.y', 'Optimize_Container.H2')

    top.setup()
    top.run()

    print('Length', root.Optimize_Container.unknowns['Length'])
    print('Width', root.Optimize_Container.unknowns['Width'])
    print('Height', root.Optimize_Container.unknowns['Height'])
    print('Volume', root.Optimize_Container.unknowns['Volume'])

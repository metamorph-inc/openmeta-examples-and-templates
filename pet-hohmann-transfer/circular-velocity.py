from openmdao.api import Component
import numpy as np

class VCircComp(Component):
    """
    Computes the circular orbit velocity given a radius and gravitational
    parameter.
    """
    def __init__(self):
        super(VCircComp, self).__init__()

        self.add_param('r',
                       val=1.0,
                       desc='Radius from central body',
                       units='km')

        self.add_param('mu',
                       val=1.0,
                       desc='Gravitational parameter of central body',
                       units='km**3/s**2')

        self.add_output('vcirc',
                        val=1.0,
                        desc='Circular orbit velocity at given radius '
                             'and gravitational parameter',
                        units='km/s')

    def solve_nonlinear(self, params, unknowns, resids):
        r = params['r']
        mu = params['mu']

        if r == 0:
          unknowns['vcirc'] = float('inf')
        else:
          unknowns['vcirc'] = np.sqrt(mu / r)
        
from openmdao.api import Component
import numpy as np

class DeltaVComp(Component):
    """
    Compute the delta-V performed given the magnitude of two velocities
    and the angle between them.
    """
    def __init__(self):
        super(DeltaVComp, self).__init__()

        self.add_param('v1', val=1.0, desc='Initial velocity', units='km/s')
        self.add_param('v2', val=1.0, desc='Final velocity', units='km/s')
        self.add_param('dinc', val=1.0, desc='Plane change', units='rad')

        # Note:  We're going to use trigonometric functions on dinc.  The
        # automatic unit conversion in OpenMDAO comes in handy here.

        self.add_output('delta_v', val=0.0, desc='Delta-V', units='km/s')

    def solve_nonlinear(self, params, unknowns, resids):
        v1 = params['v1']
        v2 = params['v2']
        dinc = params['dinc']

        unknowns['delta_v'] = np.sqrt(v1 ** 2 + v2 ** 2 - 2.0 * v1 * v2 * np.cos(dinc))

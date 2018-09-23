from openmdao.api import Component
import numpy as np

class TransferOrbit(Component):
    def __init__(self):
        super(TransferOrbit, self).__init__()
        
        self.add_param('mu',
                       val=398600.4418,
                       desc='Gravitational parameter of central body',
                       units='km**3/s**2')
        self.add_param('rp', val=7000.0, desc='periapsis radius', units='km')
        self.add_param('ra', val=42164.0, desc='apoapsis radius', units='km')

        self.add_output('vp', val=0.0, desc='periapsis velocity', units='km/s')
        self.add_output('va', val=0.0, desc='apoapsis velocity', units='km/s')

    def solve_nonlinear(self, params, unknowns, resids):
        mu = params['mu']
        rp = params['rp']
        ra = params['ra']

        a = (ra + rp) / 2.0
        e = (a - rp) / a
        p = a * (1.0 - e ** 2)
        h = np.sqrt(mu * p)

        unknowns['vp'] = h / rp
        unknowns['va'] = h / ra
        
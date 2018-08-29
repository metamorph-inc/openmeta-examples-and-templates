from __future__ import print_function
import collections

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np


class AreaVolume(Component):
    def __init__(self):
        super(AreaVolume, self).__init__()

        self.add_param("x", val=0.0)
        self.add_param("y", val=0.0)
        self.add_param("z", val=0.0)
        self.add_output("volume", val=0.0)
        self.add_output("area", val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        unknowns["volume"] = params["x"] * params["y"] * params["z"]
        unknowns["area"] = 2 * ( params["x"] * params["y"] + \
                                 params["y"] * params["z"] + \
                                 params["z"] * params["x"] )

def main():
    top = Problem()

    root = top.root = Group()

    root.add('Input', IndepVarComp([('x', 1.0), ('y', 2.0), ('z', 3.0)]))
    root.add('p', AreaVolume())
    root.connect('Input.x', 'p.x')
    root.connect('Input.y', 'p.y')
    root.connect('Input.z', 'p.z')

    top.setup()
    top.run()
    
    print('area =', root.p.unknowns['area'])
    print('volume =', root.p.unknowns['volume'])

if __name__ == "__main__":
    main()
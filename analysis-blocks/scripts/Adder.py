from __future__ import print_function
import collections

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np


class Adder(Component):
    def __init__(self):
        super(Adder, self).__init__()

        self.add_param("x", val=0.0)
        self.add_param("y", val=0.0)
        self.add_output("z", val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        unknowns["z"] = params["x"] + params["y"]

def main():
    top = Problem()

    root = top.root = Group()

    root.add('Input', IndepVarComp([('x', 1.0), ('y', 2.0)]))
    root.add('p', Adder())
    root.connect('Input.x', 'p.y')
    root.connect('Input.x', 'p.y')

    top.setup()
    top.run()
    
    print('z =', root.p.unknowns['z'])

if __name__ == "__main__":
    main()
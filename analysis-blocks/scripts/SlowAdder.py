from __future__ import print_function

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np
import time


class SlowAdder(Component):
    def __init__(self):
        super(SlowAdder, self).__init__()

        self.add_param("x", val=0.0)
        self.add_param("y", val=0.0)
        self.add_output("z", val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        time.sleep(10)
        unknowns["z"] = params["x"] + params["y"]

def main():
    top = Problem()

    root = top.root = Group()

    root.add('Input', IndepVarComp([('x', 1.0), ('y', 2.0)]))
    root.add('p', SlowAdder())
    root.connect('Input.x', 'p.x')
    root.connect('Input.y', 'p.y')

    top.setup()
    top.run()
    
    print('z =', root.p.unknowns['z'])

if __name__ == "__main__":
    main()
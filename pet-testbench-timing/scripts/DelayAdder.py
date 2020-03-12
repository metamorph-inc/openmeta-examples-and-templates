from __future__ import print_function
import collections
import time

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np


class DelayAdder(Component):
    def __init__(self):
        super(DelayAdder, self).__init__()

        self.add_param("a", val=0.0)
        self.add_param("b", val=0.0)
        self.add_param("delay", val=3.0)
        self.add_output("x", val=0.0)
        self.add_output("y", val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        time.sleep(params["delay"])
        unknowns["x"] = params["a"] + params["b"]
        unknowns["y"] = (params["a"] + params["b"]) * 0.1

def main():
    top = Problem()

    root = top.root = Group()

    root.add('p', DelayAdder())

    top.setup()
    top.run()

if __name__ == "__main__":
    main()

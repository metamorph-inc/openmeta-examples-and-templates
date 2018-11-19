from __future__ import print_function
import collections

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef, AnalysisError
import numpy as np


class ExceptionAdder(Component):
    def __init__(self):
        super(ExceptionAdder, self).__init__()

        self.add_param("a", val=0.0)
        self.add_param("b", val=0.0)
        self.add_output("x", val=0.0)
        self.add_output("y", val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        print("Ran ExceptionAdder {}, {}".format(params["a"], params["b"]))
        if params["a"] >= 2 and params["a"] <= 4:
            print("Threw exception")
            raise AnalysisError("Invalid Parameters")

        unknowns["x"] = params["a"] + params["b"]
        unknowns["y"] = (params["a"] + params["b"]) * 0.1

def main():
    top = Problem()

    root = top.root = Group()

    root.add('p', ExceptionAdder())

    top.setup()
    top.run()

if __name__ == "__main__":
    main()

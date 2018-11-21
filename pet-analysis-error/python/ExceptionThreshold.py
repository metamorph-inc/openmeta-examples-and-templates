from __future__ import print_function
import collections

from openmdao.api import Component, Problem, Group, AnalysisError
import numpy as np


class ExceptionAdder(Component):
    def __init__(self):
        super(ExceptionAdder, self).__init__()

        self.add_param("MustBe0", val=0.0)
        self.add_param("MustBeAbove0", val=1.0)
        self.add_output("Zero", val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        if not np.isclose(params["MustBe0"], 0):
            raise AnalysisError("MustBe0 was not 0. It was {}".format(params["MustBe0"]))
        if not params["MustBeAbove0"] > 0:
            raise AnalysisError("MustBeAbove0 was not above 0. It was {}".format(params["MustBeAbove0"]))
            

def main():
    top = Problem()

    root = top.root = Group()

    root.add('p', ExceptionAdder())

    top.setup()
    top.run()

if __name__ == "__main__":
    main()

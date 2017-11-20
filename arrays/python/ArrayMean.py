from __future__ import print_function
import collections

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np


DIMENSION = 10


class ArrayMean(Component):
    def __init__(self):
        super(ArrayMean, self).__init__()

        self.add_param("array", val=np.zeros(DIMENSION), pass_by_obj=True)
        self.add_output("mean", val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        unknowns["mean"] = np.mean(params["array"])

def main():
    top = Problem()

    root = top.root = Group()

    root.add("array", IndepVarComp("array", np.full(DIMENSION, 5.0), pass_by_obj=True))

    root.add('ArrayMean', ArrayMean())

    root.connect("array.array", "ArrayMean.array")

    top.setup()
    top.run()

    print(top["ArrayMean.mean"])

if __name__ == "__main__":
    main()

from __future__ import print_function
import collections

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np


DIMENSION = 10


class ArraySum(Component):
    def __init__(self):
        super(ArraySum, self).__init__()

        self.add_param("array1", val=np.zeros(DIMENSION), pass_by_obj=True)
        self.add_param("array2", val=np.zeros(DIMENSION), pass_by_obj=True)
        self.add_output("sumArray", val=np.zeros(DIMENSION), pass_by_obj=True)

    def solve_nonlinear(self, params, unknowns, resids):
        unknowns["sumArray"] = params["array1"] + params["array2"]

def main():
    top = Problem()

    root = top.root = Group()

    root.add("array1", IndepVarComp("array1", np.full(DIMENSION, 5.0), pass_by_obj=True))
    root.add("array2", IndepVarComp("array2", np.full(DIMENSION, 10.0), pass_by_obj=True))

    root.add('ArraySum', ArraySum())

    root.connect("array1.array1", "ArraySum.array1")
    root.connect("array2.array2", "ArraySum.array2")

    top.setup()
    top.run()

    print(top["ArraySum.sumArray"])

if __name__ == "__main__":
    main()

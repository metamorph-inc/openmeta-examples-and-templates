from __future__ import print_function
import collections

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np


DIMENSION = 10


class ScalarToArray(Component):
    def __init__(self):
        super(ScalarToArray, self).__init__()

        self.add_param("value", val=0.0)
        self.add_param("increment", val=0.0)
        self.add_output("array", val=np.zeros(DIMENSION), pass_by_obj=True)

    def solve_nonlinear(self, params, unknowns, resids):
        arr = np.full(DIMENSION, params["value"]) + np.linspace(0, (DIMENSION - 1) * params["increment"], num=DIMENSION)
        unknowns["array"] = arr

def main():
    top = Problem()

    root = top.root = Group()

    root.add("value", IndepVarComp("value", 3.0))
    root.add("increment", IndepVarComp("increment", 1.0))

    root.add('ScalarToArray', ScalarToArray())

    root.connect("value.value", "ScalarToArray.value")
    root.connect("increment.increment", "ScalarToArray.increment")

    top.setup()
    top.run()

    print(top["ScalarToArray.array"])

if __name__ == "__main__":
    main()

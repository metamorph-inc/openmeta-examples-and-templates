from __future__ import print_function

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np
import time
from random import choice

class CompareStringSelectScalar(Component):
    def __init__(self):
        super(CompareStringSelectScalar, self).__init__()

        self.add_param("string1", val=u"True", pass_by_obj=True)
        self.add_param("string2", val=u"True", pass_by_obj=True)
        self.add_param("value_same", val=0.0)
        self.add_param("value_different", val=0.0)
        self.add_output("output", val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        if params["string1"] == params["string2"]:
            unknowns["output"] = params["value_same"]
        else:
            unknowns["output"] = params["value_different"]

def main():
    top = Problem()

    root = top.root = Group()

    root.add('Input', IndepVarComp([('string1', choice([u"True", u"False"]), {"pass_by_obj": True}),
                                    ('x', 1.0),
                                    ('y', 2.0)]))
    root.add('select', CompareStringSelectScalar())
    root.connect('Input.string1', 'select.string1')
    root.connect('Input.x', 'select.value_same')
    root.connect('Input.y', 'select.value_different')

    top.setup()
    top.run()
    
    print('string1 =', root.select.params['string1'])
    print('output =', root.select.unknowns['output'])

if __name__ == "__main__":
    main()
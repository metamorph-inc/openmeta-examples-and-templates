from __future__ import print_function
import collections

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np


class GenerateAssortedData(Component):
    def __init__(self):
        super(GenerateAssortedData, self).__init__()

        self.add_param("m", val=1.0)
        self.add_param("n", val=1.0)
        self.add_output("scalar_out", val=0.0)
        self.add_output("scalararray_out", val=[0.0, 0.0], pass_by_obj=True)
        self.add_output("npscalararray_out", val=np.array([[0.0, 0.0], [0.0, 0.0]]), pass_by_obj=True)
        self.add_output("string_out", val=u"None", pass_by_obj=True)
        self.add_output("stringarray_out", val=[u"", u""], pass_by_obj=True)
        self.add_output("npstringarray_out", val=np.array([u"", u""]), pass_by_obj=True)
        self.add_output("bool_out", val=True, pass_by_obj=True)
        self.add_output("dict_homo_out", val={'apples': 3, 'oranges': 2, 'bananas': 1}, pass_by_obj=True)
        self.add_output("dict_hetero_out", val={'name': 'alice', 'age': 50, 'children': ['bob', 'caleb']}, pass_by_obj=True)

    def solve_nonlinear(self, params, unknowns, resids):
        m = max(int(params["m"]), 1)
        n = max(int(params["n"]), 1)
        unknowns["scalar_out"] = m * n
        unknowns["scalararray_out"] = [[y for y in xrange(x * n, x * n + n)] for x in xrange(m)]
        unknowns["npscalararray_out"] = np.array(xrange(m * n)).reshape(m, n) 
        unknowns["string_out"] = "m = " + str(m) + "; n = " + str(n)
        unknowns["stringarray_out"] = [str(m), str(n)]
        unknowns["npstringarray_out"] = np.array([str(m), str(n)])
        unknowns["bool_out"] = m > n
        unknowns["dict_homo_out"]["apples"], unknowns["dict_homo_out"]["oranges"] = m, n
        unknowns["dict_hetero_out"]["children"] = ['bob', 'caleb']
        for name in ["other_child_{0}".format(num+1) for num in xrange(min(m+n,10))]:
            unknowns["dict_hetero_out"]["children"].append(name)

def main():
    top = Problem()

    root = top.root = Group()

    root.add('Input', IndepVarComp([('m', 2.0),
                                    ('n', 3.0)]))
    root.add('Generator', GenerateAssortedData())
    root.connect('Input.m', 'Generator.m')
    root.connect('Input.n', 'Generator.n')

    top.setup()
    top.run()
    
    print('scalar_out =', root.Generator.unknowns['scalar_out'])
    print('scalararray_out =', root.Generator.unknowns['scalararray_out'])
    print('npscalararray_out =', root.Generator.unknowns['npscalararray_out'])
    print('string_out =', root.Generator.unknowns['string_out'])
    print('stringarray_out =', root.Generator.unknowns['stringarray_out'])
    print('npstringarray_out =', root.Generator.unknowns['npstringarray_out'])
    print('bool_out =', root.Generator.unknowns['bool_out'])
    print('dict_homo_out =', root.Generator.unknowns['dict_homo_out'])
    print('dict_hetero_out =', root.Generator.unknowns['dict_hetero_out'])

if __name__ == "__main__":
    main()
# coding=utf-8
from __future__ import print_function
import collections

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np


class GenerateAssortedData(Component):
    def __init__(self):
        super(GenerateAssortedData, self).__init__()

        self.add_param("m", val=1.0)
        self.add_param("n", val=1.0)
        self.add_output("float_out", val=0.0)
        self.add_output("floatarray_out", val=[0.0, 0.0], pass_by_obj=True)
        self.add_output("npfloatarray_out", val=np.array([[0.0, 0.0], [0.0, 0.0]]), pass_by_obj=True)
        self.add_output("int_out", val=0)
        self.add_output("intarray_out", val=[0, 0], pass_by_obj=True)
        self.add_output("npintarray_out", val=np.array([[0, 0], [0, 0]]), pass_by_obj=True)
        self.add_output("string_out", val="String", pass_by_obj=True)
        self.add_output("stringarray_out", val=["String 1", "String 2"], pass_by_obj=True)
        self.add_output("npstringarray_out", val=np.array(["String 1", "String 2"]), pass_by_obj=True)
        self.add_output("unicode_out", val=u"Unicøde", pass_by_obj=True)
        self.add_output("unicodearray_out", val=[u"Unicøde 1", u"Unicøde 2"], pass_by_obj=True)
        self.add_output("npunicodearray_out", val=np.array([u"Unicøde 1", u"Unicøde 2"]), pass_by_obj=True)
        self.add_output("bool_out", val=True, pass_by_obj=True)
        self.add_output("dict_strkey_homo_out", val={'apples': 3, 'oranges': 2, 'bananas': 1}, pass_by_obj=True)
        self.add_output("dict_unikey_homo_out", val={u'apples': 3, u'oranges': 2, u'bananas': 1, u'crêpes': 0}, pass_by_obj=True)
        self.add_output("dict_hetero_out", val={'name': 'alice', 'age': 50, 'children': ['bob', 'caleb']}, pass_by_obj=True)

    def solve_nonlinear(self, params, unknowns, resids):
        m = max(int(params["m"]), 1)
        n = max(int(params["n"]), 1)
        unknowns["float_out"] = float(m * n)
        unknowns["floatarray_out"] = [[float(y) for y in xrange(x * n, x * n + n)] for x in xrange(m)]
        unknowns["npfloatarray_out"] = np.array(xrange(m * n), dtype=np.float).reshape(m, n)
        unknowns["int_out"] = int(m * n)
        unknowns["intarray_out"] = [[int(y) for y in xrange(x * n, x * n + n)] for x in xrange(m)]
        unknowns["npintarray_out"] = np.array(xrange(m * n)).reshape(m, n)
        unknowns["string_out"] = "m = " + str(m) + "; n = " + str(n)
        unknowns["stringarray_out"] = [str(m), str(n)]
        unknowns["npstringarray_out"] = np.array([str(m), str(n)])
        unknowns["unicode_out"] = unicode(m) + u" bÿ " + unicode(n) + u" 😂"
        unknowns["unicodearray_out"] = [unicode(m) + u"ï", unicode(n) + u"😂"]
        unknowns["npunicodearray_out"] = np.array([unicode(m) + u"ï", unicode(n) + u"😂"])
        unknowns["bool_out"] = m > n
        unknowns["dict_strkey_homo_out"]["apples"], unknowns["dict_strkey_homo_out"]["oranges"] = m, n
        unknowns["dict_unikey_homo_out"]["apples"], unknowns["dict_unikey_homo_out"][u"crêpes"] = m, n
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
    
    print('float_out =', root.Generator.unknowns['float_out'])
    print('floatarray_out =', root.Generator.unknowns['floatarray_out'])
    print('npfloatarray_out =', root.Generator.unknowns['npfloatarray_out'])
    print('int_out =', root.Generator.unknowns['int_out'])
    print('intarray_out =', root.Generator.unknowns['intarray_out'])
    print('npintarray_out =', root.Generator.unknowns['npintarray_out'])
    print('string_out =', root.Generator.unknowns['string_out'])
    print('stringarray_out =', root.Generator.unknowns['stringarray_out'])
    print('npstringarray_out =', root.Generator.unknowns['npstringarray_out'])
    print('unicode_out =', root.Generator.unknowns['unicode_out'])
    print('unicodearray_out =', root.Generator.unknowns['unicodearray_out'])
    print('npunicodearray_out =', root.Generator.unknowns['npunicodearray_out'])
    print('bool_out =', root.Generator.unknowns['bool_out'])
    print('dict_strkey_homo_out =', root.Generator.unknowns['dict_strkey_homo_out'])
    print('dict_unikey_homo_out =', root.Generator.unknowns['dict_unikey_homo_out'])
    print('dict_hetero_out =', root.Generator.unknowns['dict_hetero_out'])

if __name__ == "__main__":
    main()
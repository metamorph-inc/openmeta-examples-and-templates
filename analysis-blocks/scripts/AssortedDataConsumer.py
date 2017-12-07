# coding=utf-8
from __future__ import print_function
import collections

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np


class AssortedDataConsumer(Component):
    def __init__(self):
        super(AssortedDataConsumer, self).__init__()

        self.add_param("float_in", val=0.0)
        self.add_param("floatarray_in", val=[0.0, 0.0], pass_by_obj=True)
        self.add_param("npfloatarray_in", val=np.array([[0.0, 0.0], [0.0, 0.0]]), pass_by_obj=True)
        self.add_param("int_in", val=0, pass_by_obj=True)
        self.add_param("intarray_in", val=[0, 0], pass_by_obj=True)
        self.add_param("npintarray_in", val=np.array([[0, 0], [0, 0]]), pass_by_obj=True)
        self.add_param("string_in", val="", pass_by_obj=True)
        self.add_param("stringarray_in", val=["", ""], pass_by_obj=True)
        self.add_param("npstringarray_in", val=np.array(["", ""]), pass_by_obj=True)
        self.add_param("unicode_in", val=u"", pass_by_obj=True)
        self.add_param("unicodearray_in", val=[u"", u""], pass_by_obj=True)
        self.add_param("npunicodearray_in", val=np.array([u"", u""]), pass_by_obj=True)
        self.add_param("bool_in", val=True, pass_by_obj=True)
        self.add_param("dict_strkey_intval_homo_out", val={'apples': 3, 'oranges': 2, 'bananas': 1}, pass_by_obj=True)
        self.add_param("dict_unikey_intval_homo_out", val={u'apples': 3, u'oranges': 2, u'bananas': 1, u'crêpes': 0}, pass_by_obj=True)
        self.add_param("dict_strkey_strval_homo_out", val={'Chief Executive Officer': 'Ralph', 'Company Secretary': 'Lenny'}, pass_by_obj=True)
        self.add_param("dict_strkey_unival_homo_out", val={'Chief Executive Officer': u'Raphaël', 'Company Secretary': u'Léo'}, pass_by_obj=True)
        self.add_param("dict_unikey_unival_homo_out", val={u'Président Directeur Général': u'Raphaël', u'Secrétaire Général': u'Léo'}, pass_by_obj=True)
        self.add_param("dict_hetero_in", val={'name': 'alice', 'age': 50, 'children': ['bob', 'caleb']}, pass_by_obj=True)

    def solve_nonlinear(self, params, unknowns, resids):
        with open("consumerpython.txt", "w") as fout:
            for key in params:
                print("{} = {}".format(key, repr(params[key])))
                fout.write("{} = {}\n".format(key, repr(params[key])))
        

def main():
    top = Problem()

    root = top.root = Group()

    root.add('Input', IndepVarComp([('float_in', 2.0),
                                    ('floatarray_in', [2.0, 3.0], {"pass_by_obj": True}),
                                    ('npfloatarray_in', np.array([[1.0, 2.0], [3.0, 4.0]]), {"pass_by_obj": True}),
                                    ('int_in', 3, {"pass_by_obj": True}),
                                    ('intarray_in', [3, 4, 5], {"pass_by_obj": True}),
                                    ('npintarray_in', np.array([1, 3, 5]), {"pass_by_obj": True}),
                                    ('string_in', "Test", {"pass_by_obj": True}),
                                    ('stringarray_in', ["Two", "Tests"], {"pass_by_obj": True}),
                                    ('npstringarray_in', np.array(["Two", "Tests"]), {"pass_by_obj": True}),
                                    ('unicode_in', u"Test", {"pass_by_obj": True}),
                                    ('unicodearray_in', [u"Two", u"Tests"], {"pass_by_obj": True}),
                                    ('npunicodearray_in', np.array([u"Two", u"Tests"]), {"pass_by_obj": True}),
                                    ('bool_in', True, {"pass_by_obj": True}),
                                    ('dict_strkey_intval_homo_out', {"Hearts": 2, "Spades": 3, "Diamonds": 5, "Clubs": 0}, {"pass_by_obj": True}),
                                    ('dict_unikey_intval_homo_out', {u"Hearts": 2, u"Spades": 3, u"Diamonds": 5, u"Clubs": 0}, {"pass_by_obj": True}),
                                    ('dict_strkey_strval_homo_out', {'Chief Executive Officer': 'Leah', 'Company Secretary': 'Chloe'}, {"pass_by_obj": True}),
                                    ('dict_strkey_unival_homo_out', {'Chief Executive Officer': 'Léa', 'Company Secretary': 'Chloé'}, {"pass_by_obj": True}),
                                    ('dict_unikey_unival_homo_out', {'Président Directeur Général': 'Léa', 'Secrétaire Général': 'Chloé'}, {"pass_by_obj": True}),
                                    ('dict_hetero_in', {'name': 'bob', 'age': 25, 'children': ['catherine', 'david']}, {"pass_by_obj": True})]))
    root.add('Consumer', AssortedDataConsumer())
    root.connect('Input.float_in', 'Consumer.float_in')
    root.connect('Input.floatarray_in', 'Consumer.floatarray_in')
    root.connect('Input.npfloatarray_in', 'Consumer.npfloatarray_in')
    root.connect('Input.int_in', 'Consumer.int_in')
    root.connect('Input.intarray_in', 'Consumer.intarray_in')
    root.connect('Input.npintarray_in', 'Consumer.npintarray_in')
    root.connect('Input.string_in', 'Consumer.string_in')
    root.connect('Input.stringarray_in', 'Consumer.stringarray_in')
    root.connect('Input.npstringarray_in', 'Consumer.npstringarray_in')
    root.connect('Input.unicode_in', 'Consumer.unicode_in')
    root.connect('Input.unicodearray_in', 'Consumer.unicodearray_in')
    root.connect('Input.npunicodearray_in', 'Consumer.npunicodearray_in')
    root.connect('Input.bool_in', 'Consumer.bool_in')
    root.connect('Input.dict_strkey_intval_homo_out', 'Consumer.dict_strkey_intval_homo_out')
    root.connect('Input.dict_unikey_intval_homo_out', 'Consumer.dict_unikey_intval_homo_out')
    root.connect('Input.dict_strkey_strval_homo_out', 'Consumer.dict_strkey_strval_homo_out')
    root.connect('Input.dict_strkey_unival_homo_out', 'Consumer.dict_strkey_unival_homo_out')
    root.connect('Input.dict_unikey_unival_homo_out', 'Consumer.dict_unikey_unival_homo_out')
    root.connect('Input.dict_hetero_in', 'Consumer.dict_hetero_in')

    top.setup()
    top.run()

if __name__ == "__main__":
    main()
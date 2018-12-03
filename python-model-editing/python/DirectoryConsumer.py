from __future__ import print_function
import collections
import os
import os.path

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef, AnalysisError
import numpy as np

from DirectoryProducer import DirectoryProducer


class DirectoryConsumer(Component):
    def __init__(self):
        super(DirectoryConsumer, self).__init__()

        self.add_param("input_directory_path", val=".", pass_by_obj=True)
        self.add_output("addition", val=0.0)
        self.add_output("subtraction", val=0.0)
        self.add_output("multiplication", val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        input_dir_path = params["input_directory_path"]

        unknowns["addition"] = self.read_single_value_from_file(os.path.join(input_dir_path, "addition.txt"))
        unknowns["subtraction"] = self.read_single_value_from_file(os.path.join(input_dir_path, "subtraction.txt"))
        unknowns["multiplication"] = self.read_single_value_from_file(os.path.join(input_dir_path, "subdirectory", "multiplication.txt"))

    @staticmethod
    def read_single_value_from_file(file_name):
        with open(file_name, "r") as file:
            lines = file.readlines()
            if len(lines) != 1:
                raise AnalysisError("Invalid file format in " + file_name)
            return float(lines[0].strip())

def main():
    top = Problem()

    root = top.root = Group()

    root.add('p', DirectoryProducer())
    root.add('c', DirectoryConsumer())

    root.connect('p.output_directory_path', 'c.input_directory_path')

    top.setup()
    top.run()

if __name__ == "__main__":
    main()

from __future__ import print_function
import collections
import os
import os.path
import zipfile

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef, AnalysisError
import numpy as np

from ZipProducer import ZipProducer


class ZipConsumer(Component):
    def __init__(self):
        super(ZipConsumer, self).__init__()

        self.add_param("input_directory_zip", val=FileRef("input_dir.zip"), pass_by_obj=True, binary=True)
        self.add_output("addition", val=0.0)
        self.add_output("subtraction", val=0.0)
        self.add_output("multiplication", val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        input_dir_path = self.find_next_dirname() # Autogenerate a new target directory name to extract ZIP to

        # Extract ZIP file
        with params["input_directory_zip"].open("r") as zip_fp:
            self.extract_zip_to_directory(zip_fp, input_dir_path)

        # Perform analysis using files extracted from ZIP file (you could also pass the extracted
        # directory name to an external tool here)
        unknowns["addition"] = self.read_single_value_from_file(os.path.join(input_dir_path, "addition.txt"))
        unknowns["subtraction"] = self.read_single_value_from_file(os.path.join(input_dir_path, "subtraction.txt"))
        unknowns["multiplication"] = self.read_single_value_from_file(os.path.join(input_dir_path, "subdirectory", "multiplication.txt"))

    @staticmethod
    def extract_zip_to_directory(zip_fp, dir_name):
        with zipfile.ZipFile(zip_fp, "r") as zip_file:
            zip_file.extractall(dir_name)

    @staticmethod
    def find_next_dirname():
        template = "ZC_{}"
        found = list()
        for root, dirs, files in os.walk(os.getcwd()):
            for dir in dirs:
                found.append(dir)

        idx = 0
        finished = False
        candidate_name = '.'
        while idx < 10000000 and not finished:
            candidate_name = template.format(idx)
            if candidate_name in found:
                idx += 1
            else:
                finished = True

        # claim it
        os.makedirs(candidate_name)
        return candidate_name

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

    root.add('p', ZipProducer())
    root.add('c', ZipConsumer())

    root.connect('p.output_directory_zip', 'c.input_directory_zip')

    top.setup()
    top.run()

if __name__ == "__main__":
    main()

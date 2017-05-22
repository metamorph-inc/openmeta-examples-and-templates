from __future__ import print_function
import collections
import os.path
import zipfile

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np


class DirectoryProducer(Component):
    def __init__(self):
        super(DirectoryProducer, self).__init__()

        self.add_param("a", val=3.0)
        self.add_param("b", val=2.0)
        self.add_output("output_directory_path", val="", pass_by_obj=True)
        self.add_output("output_directory_zip", val=FileRef("output_dir.zip"), pass_by_obj=True, binary=True)

    def solve_nonlinear(self, params, unknowns, resids):
        # Create new output directory
        output_dir_name = self.find_next_dirname()

        # Create some files in it
        with open(os.path.join(output_dir_name, "addition.txt"), "w") as addition_file:
            addition_file.write(str(params["a"] + params["b"]))

        with open(os.path.join(output_dir_name, "subtraction.txt"), "w") as subtraction_file:
            subtraction_file.write(str(params["a"] - params["b"]))

        # Create a subdirectory with a file in it, just to show we can
        os.makedirs(os.path.join(output_dir_name, "subdirectory"))
        with open(os.path.join(output_dir_name, "subdirectory", "multiplication.txt"), "w") as multiplication_file:
            multiplication_file.write(str(params["a"] * params["b"]))

        # Set output_directory_path to absolute path of the directory we just created
        unknowns["output_directory_path"] = os.path.abspath(output_dir_name)

        # Zip up our output directory, so it can be archived by the artifact archiver
        with unknowns["output_directory_zip"].open('w') as zip_fp:
            self.zip_directory(output_dir_name, zip_fp)

    @staticmethod
    def find_next_dirname():
        template = "DP_{}"
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
    def zip_directory(directory_path, zip_fp):
        dir_basename = os.path.basename(directory_path)
        
        with zipfile.ZipFile(zip_fp, 'w') as output_zip:
            for directory_tuple in os.walk(directory_path):
                for file in directory_tuple[2]:
                    real_path = os.path.join(directory_tuple[0], file)
                    archive_path = os.path.join(dir_basename, os.path.relpath(real_path, directory_path))
                    print("Archiving", real_path, "to", archive_path)
                    output_zip.write(real_path, archive_path)


def main():
    top = Problem()

    root = top.root = Group()

    root.add('p', DirectoryProducer())

    top.setup()
    top.run()

if __name__ == "__main__":
    main()

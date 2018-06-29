from __future__ import print_function
import collections

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np


class Launch(Component):
    def __init__(self):
        super(Launch, self).__init__()

        self.add_param("Altitude", val=10000.0)
        self.add_param("VehicleMass", val=10000.0)
        self.add_param("Thrust", val=10000.0)
        self.add_param("BurnRate", val=0.01)
        self.add_output("FuelBurn", val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
    
        acceleration = 0
        time = 0
        
        unknowns["FuelBurn"] = params["Altitude"]*params["VehicleMass"]*params["BurnRate"]/params["Thrust"]
                                       
        
def main():
    top = Problem()

    root = top.root = Group()

    root.add('p', Launch())

    top.setup()
    top.run()

if __name__ == "__main__":
    main()

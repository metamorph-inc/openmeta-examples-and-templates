from __future__ import print_function
import collections
import datetime
import json

import dateutil.parser

from openmdao.api import IndepVarComp, Component, Problem, Group, FileRef
import numpy as np


class TestbenchTiming(Component):
    def __init__(self):
        super(TestbenchTiming, self).__init__()

        self.add_param("manifest", val=FileRef("manifest.json"), binary=True, pass_by_obj=True)
        self.add_output("timing_info", val="[]", pass_by_obj=True)
        self.add_output("total_time", val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        with params['manifest'].open('r') as f:
            manifest = json.load(f)

        result = []
        first_time = None
        last_time = None
        for step in manifest["Steps"]:
            start_time = dateutil.parser.parse(step["ExecutionStartTimestamp"])
            stop_time = dateutil.parser.parse(step["ExecutionCompletionTimestamp"])

            if first_time is None:
                first_time = start_time

            last_time = stop_time

            run_timedelta = stop_time - start_time
            result.append({
                "Invocation": step["Invocation"],
                "Description": step["Description"],
                "RuntimeSeconds": run_timedelta.total_seconds()
            })

        unknowns["timing_info"] = json.dumps(result)
        unknowns["total_time"] = (last_time - first_time).total_seconds()

def main():
    top = Problem()

    root = top.root = Group()

    root.add('p', TestbenchTiming())

    top.setup()
    top.run()

if __name__ == "__main__":
    main()

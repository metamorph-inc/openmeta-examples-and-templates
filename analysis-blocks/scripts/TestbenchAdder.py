import json

def read_testbench_manifest_parameters(testbench_manifest):
    parameters_dict = dict()
    print("Reading parameters from testbench_manifest.json...")
    print()
    for parameter in testbench_manifest['Parameters']:
        parameters_dict[parameter['Name']] = parameter['Value']
        print(parameter['Name'] + ": " + str(parameter['Value']))
    print()
    return parameters_dict

if __name__ == '__main__':
    print("Running " + str(__file__) + "...")

    #Obtain testbench configuration
    with open('testbench_manifest.json', 'r') as f_in:
        testbench_manifest = json.load(f_in)

    params = read_testbench_manifest_parameters(testbench_manifest)
    
    x = float(params["x"])
    y = float(params["y"])
    
    z = x + y

    #Add metrics
    print("Saving Metrics to testbench_manifest.json...")
    for metric in testbench_manifest["Metrics"]:
        if str(metric["Name"])=="z":
            metric["Value"]=z
    
    #Save the testbench_manifest
    with open('testbench_manifest.json', 'w') as f_out:
        json.dump(testbench_manifest, f_out, indent=2)

    print("Done.")

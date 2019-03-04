import sys
import os
import numpy as np
import shutil
from common import PostProcess, update_metrics_in_report_json
from common import read_limits, check_limits_and_add_to_report_json
#from common import VirtualVehicleMakeMetrics as VVM

def main():
    print "in main....."
    sampleRate = 0.10
    startAnalysisTime = 50
    
    f = open('rawdata.csv', 'w')
    mat_file_name = sys.argv[1]
    print "Mat file name is "+mat_file_name
    if not os.path.exists(mat_file_name):
        print "Given result file does not exist: ",mat_file_name
        raise IOError('Given result file does not exist: {0}'.format(sys.argv[1]))
    else:
        print "line 10....",os.getcwd()
        dstpath = os.path.join(os.getcwd(), 'matfiles')
        print "dstPath is ",dstpath
        if not os.path.isdir(dstpath):
            os.makedirs(dstpath)
        numFiles = len(os.listdir(dstpath))
        dstname = '_' + str(numFiles) + mat_file_name
        print  "dstname ",dstname
        #shutil.copyfile(mat_file_name, os.path.join(dstpath, dstname))
        print "line30"


    print "Line 24: Opened "+mat_file_name
    ## First limit part
    #limit_dict, filter = read_limits()
    print "done limits"
    filter = []
    ## End of first limit part

    ## Post processing part
    #--------accelerations-----------------------------------------------

    #---------------------------------------------------------------------------------
    #                  Processing
    #---------------------------------------------------------------------------------
    # loads results with the filtered out variables (and 'time' which is default)
    filter = []
    pp = PostProcess(mat_file_name, filter)
    vars_available = pp.get_names()
    dumpList = []
    print vars_available[1]
    endings = ["SpacecraftBehavior.angleMeas", "SpacecraftBehavior.setpoint", "SpacecraftBehavior.vSys", "Frame.temp", "Gyroscope.temp", "Gyroscope.current", "Battery.temp", "transmitting.active", "onOrbit.active"]
    for vv in vars_available:
        for ending in endings:
            if vv.endswith(ending):
                print "add to dumpList: "+vv
                dumpList.append(vv)
                break;

    pp.print_time()
    print "Last time is "+str(pp.get_max_time()) 
    sampData = []    
    for vv in dumpList:
        ndat = pp.resample_data(vv,sampleRate)
        print "got ndat size=",len(ndat)
        sampData.append(ndat)
        print 'sampdata=',len(sampData),'cols',len(sampData[0]),'rows'

        
    i = 0
    print "dumping raw data headers"
    for c,vv in enumerate(dumpList):
        print vv,c
        f.write( vv+',')
    f.write( "\n")
    print "dump data"
    print len(sampData),'cols',len(sampData[0])
    while i < len(sampData[0]):
        if i % 1000 == 0:
            print "line ",i
        for c,vv in enumerate(dumpList):
            f.write(str(sampData[c][i])+',')
        f.write( "\n")
        i = i + 1
    f.close() 
    actAngleIdx = -1
    setAngleIdx = -1
    voltBusIdx = -1
    currGyroIdx  = -1
    gyroTempIdx = -1
    baseTempIdx = -1
    transmittingIdx = -1
    onOrbitIdx = -1

    
    for c,vv in enumerate(dumpList):
        if vv.endswith("SpacecraftBehavior.setpoint"):
            setAngleIdx = c
        if vv.endswith("SpacecraftBehavior.angleMeas"):
            actAngleIdx = c
        if vv.endswith("SpacecraftBehavior.vSys"):
            voltBusIdx = c
        if vv.endswith("Gyroscope.current"):
            currGyroIdx = c
            print "gyro idx ",currGyroIdx
        if vv.endswith("Gyroscope.temp"):
            gyroTempIdx = c
        if vv.endswith("Frame.temp"):
            baseTempIdx = c
        if vv.endswith("transmitting.active"):
            transmittingIdx = c
        if vv.endswith("onOrbit.active"):
            onOrbitIdx = c
                       
    maxErr = 0
    sumErr = 0
    avgErr = 0  
    maxBusV = -1
    minBusV = 100
    minBattCap = 100
    maxGyroCurr = 0
    maxTemp = 0
    maxGyroTemp = 0
    transmittingPercentage = -1
    
    if actAngleIdx != -1 and setAngleIdx != -1:
        i = int(startAnalysisTime/sampleRate)
        first = i       
        print "scanning angles from ",i," to " ,len(sampData[setAngleIdx])
        while i < len(sampData[setAngleIdx]):
            angErr = abs(sampData[setAngleIdx][i] - sampData[actAngleIdx][i])
            if angErr > maxErr:
                maxErr = angErr
            sumErr = sumErr + angErr
            i = i + 1
        avgErr = sumErr / (i - first + 1)
 
        
    if voltBusIdx != -1:
        i = int(startAnalysisTime/sampleRate)     
        while i < len(sampData[voltBusIdx]):
            vts = abs(sampData[voltBusIdx][i])
            if vts > maxBusV:
                maxBusV = vts
            if vts < minBusV:
                minBusV = vts
            i = i + 1
 
    if currGyroIdx != -1:
        i = int(startAnalysisTime/sampleRate)  
        print "scanning Gyro currents from ",i," to " ,len(sampData[currGyroIdx])        
        while i < len(sampData[currGyroIdx]):
            vts = abs(sampData[currGyroIdx][i])        
            if vts > maxGyroCurr:
                maxGyroCurr = vts
                print vts
            i = i + 1
 
    if baseTempIdx != -1:
        i = int(startAnalysisTime/sampleRate)     
        while i < len(sampData[baseTempIdx]):
            vts = abs(sampData[baseTempIdx][i])
            if vts > maxTemp:
                maxTemp = vts
            i = i + 1
 
    if gyroTempIdx != -1:
        i = int(startAnalysisTime/sampleRate)     
        while i < len(sampData[gyroTempIdx]):
            vts = abs(sampData[gyroTempIdx][i])
            if vts > maxGyroTemp:
                maxGyroTemp = vts
            i = i + 1
 
    transmittingSteps = 0
    onOrbitSteps = 0
    if transmittingIdx != -1 and onOrbitIdx != -1:
        i = int(startAnalysisTime/sampleRate)
        first = i       
        print "scanning angles from ",i," to " ,len(sampData[transmittingIdx])
        while i < len(sampData[transmittingIdx]):
            if sampData[transmittingIdx][i] == 1:
                transmittingSteps += 1
            if sampData[onOrbitIdx][i] == 1:
                onOrbitSteps += 1
            i += 1
        if onOrbitSteps > 0:
            transmittingPercentage = 100.0 * transmittingSteps / onOrbitSteps
 
    # Rough calculation of deepest discharge for capacitor model:
    minBattCap = 100 * ( minBusV/maxBusV ) ** 2
 
    output_dir = "../"
    json_filename = os.path.join(output_dir, 'testbench_manifest.json')
	 
    import json
    
    json_data = {}

    if os.path.isfile(json_filename):
        with open(json_filename, "r") as json_file:
            print "reading json"
            json_data = json.load(json_file)

    print "json_data is....."
    print json_data
    
    for metric in json_data['Metrics']: 
        if metric["Name"] == "angleMaxError": 
            metric["Value"] = str(maxErr)
        if metric["Name"] == "angleAvgError": 
            metric["Value"] = str(avgErr)
        if metric["Name"] == "minBusVoltage": 
            metric["Value"] = str(minBusV)
        if metric["Name"] == "maxBusVoltage": 
            metric["Value"] = str(maxBusV)
        if metric["Name"] == "minBattCapacity": 
            metric["Value"] = str(minBattCap)            
        if metric["Name"] == "maxGyroCurrent": 
            metric["Value"] = str(maxGyroCurr)     
        if metric["Name"] == "maxTemp": 
            metric["Value"] = str(maxTemp)                 
        if metric["Name"] == "maxGyroTemp": 
            metric["Value"] = str(maxGyroTemp)            
        if metric["Name"] == "transmittingPercentage": 
            metric["Value"] = str(transmittingPercentage)              
    print "dumping to ",json_filename
    print json_data    
    with open(json_filename, "w") as json_file:
        json.dump(json_data, json_file, indent=4)


    
    # #---------------------------------------------------------------------------------
    # #                  Potential_Design
    # #---------------------------------------------------------------------------------
    # Potential_Design = 0
    # followTime = pp.get_data_by_index(followTime_uri, -1)
    # if (SettlingTime == -1 or riseTime == -1 or minDistance < .1*minDistanceVelocity*followTime):
        # Potential_Design = -1
    # else: Potential_Design = 1

    # print "Potential_Design: %d" %Potential_Design

    # #---------------------------------------------------------------------------------
    # #                  Metrics
    # #---------------------------------------------------------------------------------
    # metrics = {}
    # metrics.update({'vehicleMass':{'value': vehicleMass, 'unit':'kg'},
                    # 'distanceTraveled':{'value': distanceTraveled, 'unit': 'm'},
                    # 'minDistance': {'value': minDistance, 'unit': 'm'},
                    # 'finalVelocity':{'value': Vf, 'unit': 'm/s'},
                    # 'requiredTorque':{'value': requiredTorque, 'unit':'N-m'},
                    # 'riseTime':{'value': np.amax(riseTime), 'unit' :''},
                    # 'Overshoot':{'value': np.amax(Overshoot), 'unit' :''},
                    # 'settlingTime':{'value': np.amax(SettlingTime), 'unit' :''},
                    # 'rms_error':{'value': RMS_error, 'unit' : ''},
                    # 'numSetpointCrossings':{'value':numSetPointCrossings, 'unit': ''},
                    # 'averageA': {'value': maxAccel, 'unit': 'm/s2'},
                    # 'averageJ': {'value': maxJerk, 'unit': 'm/s3'},
                    # 'Potential_Design': {'value': Potential_Design, 'unit': ''},





                    # #'chassisType':{'value': chassisType, 'unit' :''},
                    # })
    #print metrics
    cwd = os.getcwd()
    os.chdir('..')
    # print 'Plot saved to : {0}'.format(pp.save_as_svg(vehicle_speed,
                                                      # pp.global_abs_max(vehicle_speed),
                                                      # 'VehicleSpeed',
                                                      # 'max(FTP_Driver.driver_bus.vehicle_speed)',
                                                      # 'kph'))


    #pp.store_data_to_csv(jerk_uri, '{0}.csv'.format(jerk_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(a_uri, '{0}.csv'.format(a_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(pp.time_array, '{0}.csv'.format(pp.time_array), 0, time_inc, numSamples)
    #pp.store_data_to_csv(boomCylLength_uri, '{0}.csv'.format(boomCylLength_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(armCylLength_uri, '{0}.csv'.format(armCylLength_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(bucketCylLength_uri, '{0}.csv'.format(bucketCylLength_uri), 0, time_inc, numSamples)
    #pp.store_data_to_csv(boomCylRPressure_uri, '{0}.csv'.format(boomCylRPressure_uri), 0, 0.1, dur)
    #pp.store_data_to_csv(arm_ang_vel_uri, '{0}.csv'.format(arm_ang_vel_uri), 0, 0.1, dur)
    #pp.store_data_to_csv(max_Y_uri, '{0}.csv'.format(max_Y_uri), 0, 0.1, dur)
    #pp.store_data_to_csv(max_reach_uri, '{0}.csv'.format(max_reach_uri), 0, 0.1, dur)
    #pp.store_data_to_csv(State_uri, '{0}.csv'.format(State_uri), 0, 0.1, dur)
    ## end of postprocessing part

    ## Second limit part
    #check_limits_and_add_to_report_json(pp, limit_dict)
    #update_metrics_in_report_json(metrics)
    ## end of Second limit part
    os.chdir(cwd)
    print "done main"

if __name__ == '__main__':
    root_dir = os.getcwd()
    
    print "Starting in "+root_dir
    try:
        print "Starting Main...."
        main()
    except:
        print "exception occurred..."
        os.chdir(root_dir)
        import traceback
        trace = traceback.format_exc()
        # Generate this file on failed executions, https://github.com/scipy/scipy/issues/1840
        with open(os.path.join('..', '_POST_PROCESSING_FAILED.txt'), 'wb') as f_out:
            f_out.write(trace)

import sys
import os
import numpy as np
import shutil
from common import PostProcess, update_metrics_in_report_json
from common import read_limits, check_limits_and_add_to_report_json
from common import VirtualVehicleMakeMetrics as VVM

def main():
    mat_file_name = sys.argv[1]
    if not os.path.exists(mat_file_name):
        raise IOError('Given result file does not exist: {0}'.format(sys.argv[1]))
    else:
        dstpath = os.path.join(os.getcwd(), 'matfiles')
        if not os.path.isdir(dstpath):
            os.makedirs(dstpath)
        numFiles = len(os.listdir(dstpath))
        dstname = '_' + str(numFiles) + mat_file_name
        shutil.copyfile(mat_file_name, os.path.join(dstpath, dstname))



    ## First limit part
    limit_dict, filter = read_limits()
    ## End of first limit part

    ## Post processing part
    #--------accelerations-----------------------------------------------
    pos_uri = 'DriveTrain.r'
    filter.append(pos_uri)
    currentDistance_uri = 'DriveTrain.ACC.currentDistance'
    filter.append(currentDistance_uri)
    targetDistance_uri = 'DriveTrain.ACC.TargetDistance.y'
    filter.append(targetDistance_uri)

    vel_uri = 'DriveTrain.vel'
    filter.append(vel_uri)
    #desired_uri = 'DriveTrain.ACC.differenceTargetAndCurrentSpeed.u2' #This is the general setpoint. It takes velocity or a distance that has been converted to a velocity
    v_desired_uri = 'DriveTrain.targetSpeed'
    filter.append(v_desired_uri)
    #LeaderTargetVelocity_uri = 'LeaderTargetVelocity'
    LeaderTargetVelocity_uri = 'vehicleAhead.Velocity'
    filter.append(LeaderTargetVelocity_uri)

    a_uri = 'DriveTrain.a'
    filter.append(a_uri)

    jerk_uri = 'DriveTrain.j'
    filter.append(jerk_uri)

    gear_uri = "DriveTrain.current_gear"
    filter.append(gear_uri)

    followTime_uri = 'DriveTrain.followTime'
    filter.append(followTime_uri)
    FCC_uri = 'FOLLOWER_CRUISE_CONTROL'
    filter.append(FCC_uri)

    #--- Force, torque and rolling radius for front and rear tires. The two front wheels are the same so we only pull one of them
    # To find the vehicle weight the value needs to multiplied by two.
    wheelF_Force_uri = 'DriveTrain.wheelF_Force'
    wheelR_Force_uri = 'DriveTrain.wheelR_Force'
    wheelF_Torque_uri = 'DriveTrain.wheelF_Torque'
    wheelR_Torque_uri = 'DriveTrain.wheelR_Torque'
    wheelF_RollRadius_uri = 'DriveTrain.wheelF_RollRadius'
    wheelR_RollRadius_uri = 'DriveTrain.wheelR_RollRadius'
    filter.extend((wheelF_Force_uri, wheelR_Force_uri, wheelF_RollRadius_uri, wheelR_RollRadius_uri))
    #chassis_type_uri = 'DriveTrain.chassisType'
    #---------------------------------------------------------------------------------
    #                  Processing
    #---------------------------------------------------------------------------------
    # loads results with the filtered out variables (and 'time' which is default)
    pp = VVM(mat_file_name, filter)
    #---------------------------------------------------------------------------------
    #                  SETUP
    #---------------------------------------------------------------------------------
    start_time = 5 #time from which we start averaging
    endTime = pp.time[-1] #last time in data sequence
    startIndex = pp.get_index_from_time(start_time) #ignore data while system falls into place.
    time_inc = .1 #step size for rolling average
    a_bar = 0
    jerk_bar = 0
    tolerance = 0.01 # controls when set point detection occurs
    rise_tol = .1 # rise time set at 100*(1- rise_tol) of set point
    settle_tol = 0.1 # settle time within 100*(1- settle_tol) of set point.

    #---------------------------------------------------------------------------------
    #                  vehicleMass
    #---------------------------------------------------------------------------------
    wheelF_Force = pp.get_data_by_index(wheelF_Force_uri, -1)
    print("Front wheel load: %d" %wheelF_Force)
    wheelR_Force = pp.get_data_by_index(wheelR_Force_uri, -1)
    print("Rear wheel load: %d" %wheelR_Force)
    vehicleMass = 2*( wheelF_Force + wheelR_Force)/9.81
    #---------------------------------------------------------------------------------
    #                 Distance traveled
    #---------------------------------------------------------------------------------
    distanceTraveled = pp.get_data_by_index(pos_uri, -1)
    print("Distance traveled: %d" %distanceTraveled)
    #---------------------------------------------------------------------------------
    #                  minumum following distance
    #---------------------------------------------------------------------------------
    minDistance = pp.get_local_min(currentDistance_uri, startIndex, -1)
    print("minDistance is : %f" %minDistance)
    minDistanceIndex = pp.get_local_min_index(currentDistance_uri, startIndex, -1)
    #print "minDistanceIndex is: %d" %minDistanceIndex
    minDistanceVelocity = pp.get_data_by_index(vel_uri, minDistanceIndex)
    #---------------------------------------------------------------------------------
    #                 initial and final velocity
    #---------------------------------------------------------------------------------
    V0 = pp.get_data_by_index(vel_uri, 0)
    print("initial velocity: %f" %V0)
    Vf = pp.get_data_by_index(vel_uri, -1)
    print("final velocity: %f" %Vf)
    #---------------------------------------------------------------------------------
    #                  requiredTorque
    #---------------------------------------------------------------------------------
    forceExerted = vehicleMass*(Vf**2-V0**2)/(2*distanceTraveled) # Fd = (1/2)m(V^2) Work formula solve for force
    print("forece Exerted if uniform: %d" %forceExerted)
    requiredTorque = forceExerted*(.5*(pp.get_data_by_index(wheelF_RollRadius_uri, -1) + pp.get_data_by_index(wheelR_RollRadius_uri, -1)))
    print("requiredTorque if uniform: %d" %requiredTorque)
    #---------------------------------------------------------------------------------
    #                  Rise time, Overshoot, Settling time, RMS Error
    #                  Setpoint Crossings for REGULAR CRUISE CONTROL
    #---------------------------------------------------------------------------------
    SETPOINT = ''
    CURRENT =''
    #print type(desired_uri)
    if (pp.get_data_by_index(FCC_uri, -1) == 1 and pp.get_data_by_index(currentDistance_uri, -1)<=150):
        #print "HERE"
        #SETPOINT = targetDistance_uri #this data set varies if there is a vehicle ahead based on primary vehicles speed
        #CURRENT = currentDistance_uri
        SETPOINT = LeaderTargetVelocity_uri
        CURRENT = vel_uri
        #print SETPOINT
    else:
        SETPOINT = v_desired_uri # this data is constant
        CURRENT = vel_uri

    print(SETPOINT)
    #--the negative 1 gets the last/only value in the array.--
    riseTime =pp.calculate_rise_time(CURRENT, SETPOINT, start_time, tolerance, rise_tol)[-1]
    #calculate_rise_time(self, actual_name, setpoint_name, start_time = 0, tolerance = 0.01, rise_tol = 0.05, changes_allowed = 100, num_index = 1)
    print("rise time: %d" %riseTime)
    #--the zero gets the first value in the array.--
    Overshoot = (100*pp.calculate_overshoot(CURRENT, SETPOINT, start_time)[-1])
    print("Percent Overshoot: %f" %Overshoot)
    SettlingTime = pp.calculate_settling_time(CURRENT, SETPOINT, start_time, tolerance, settle_tol)[-1]
    #calculate_settling_time(self, actual_name, setpoint_name, start_time = 0, tolerance = 0.01, settle_tol = 0.05, changes_allowed = 100, num_index = 2):
    print("SettlingTime: %f" %SettlingTime)
    RMS_error = pp.calculate_rmse(CURRENT, SETPOINT,startIndex)
    print("RMS_error: %d" %RMS_error)
    #numSetPointCrossings = pp.calculate_settling_crossing(CURRENT, SETPOINT, start_time)[-1]
    #print "numSetPointCrossings: %d" %numSetPointCrossings
    # don't know what this function was doing but it wasn't what i was after.

    #--------------SETPOINT CROSSINGS--------------------------
    TargetArray = pp.short_array(SETPOINT, startIndex, -1)
    #print TargetArray
    #print TargetArray[0]
    #print TargetArray[-1]
    CurrentArray = pp.short_array(CURRENT, startIndex, -1)
    numSetPointCrossings = 0
    sign = 1
    index = 0
    if CurrentArray[0] < TargetArray[0]:
        sign = -1

    for i in xrange(len(CurrentArray)):
        diff = CurrentArray[i] -TargetArray[i]

        if(TargetArray[i] != TargetArray[i-1]):
            #print "Set point change, adjust sign."
            #print "sign: %d" %sign
            if CurrentArray[i] < TargetArray[i]:
                sign = -1
            else: sign = 1
            #print "sign: %d" %sign

        if (diff * sign < 0):
            sign = -sign
            #print "sign"
            #print i
            #print TargetArray[i]
            #print CurrentArray[i]
            numSetPointCrossings += 1

    print("numSetPointCrossings: %d" %numSetPointCrossings)
    #distance_desired = pp.short_array(distance_targetDistance_uri, start_time, -1)
    #---------------------------------------------------------------------------------
    #                  Rolling average Acceleration and Jerk
    #---------------------------------------------------------------------------------
    a_roll_int = 2
    j_roll = 1
    #print 'endTime:{0}'.format(endTime)

    #shiftIndex=[]
    #k = 0
    #shift_skip = 0.3
    #Gear = pp.get_data_by_index(gear_uri, initIndex)
    #print "Gear is %d" %Gear
    #Gear_Array = pp.short_array(gear_uri, initIndex, -1)
    #Gear = Gear_Array[0]
    #print "Gear is now: %d" %Gear
    #Gear_Array = Gear_Array[Gear:-1]
    #print len(Gear_Array)
    #print type(Gear_Array) #check to make sure I actually have a numpy array.
#    it = np.nditer(Gear_Array, flags=['f_index'])
#    for i in it:
#            shiftIndex.append(it.index)
#            Gear = i
#    print shiftIndex
    #-------------SETUP----------------------------------
    print('Measure Acceleration')
    time_array = pp.time_array()
    #print type(time_array)
    #print "time is: %d " %time_array[100]
    time_iter = np.nditer(time_array, flags=['f_index'])

    accel_array = pp.data_array(a_uri)
    clean_accel_array = []
    sumAccel = 0
    #print type(accel_array)
    jerk_array = pp.data_array(jerk_uri)
    clean_jerk_array = []
    sumJerk = 0
    #print type(jerk_array)
    avg_Accel = []
    avg_Jerk = []

    #-------------Iterate----------------------------------
    next_time = start_time
    past_time = 0
    accelStep = int(a_roll_int/time_inc)
    #print accelStep
    for i in time_iter:
        if i > next_time:
            next_time = i + time_inc
            clean_accel_array.append(accel_array[time_iter.index])
            clean_jerk_array.append(jerk_array[time_iter.index])

    #print "clean: %d" %len(clean_accel_array)
    for i in xrange(len(clean_accel_array)):
        sumAccel = sumAccel + clean_accel_array[i]
        sumJerk = sumJerk + clean_jerk_array[i]
        if i > a_roll_int/time_inc:
            sumAccel = sumAccel - clean_accel_array[i - int(a_roll_int/time_inc)]
            avg_Accel.append(sumAccel/int(a_roll_int/time_inc))
        if i > j_roll/time_inc:
            sumJerk = sumJerk - clean_jerk_array[i-int(j_roll/time_inc)]
            avg_Jerk.append(sumJerk/int(j_roll/time_inc))

    maxAccel = np.amax(avg_Accel)
    maxJerk = np.amax(avg_Jerk)
    #print type(maxAccel) # added this because I had the wrong type for the print statement.
    print("Max average acceleration: %f" %maxAccel)
    print("Max average Jerk: %f" %maxJerk)

            #print "next time is: %d" %next_time
#    time = start_time
#    while time < (endTime-a_roll_int):
#        #print 'time:{0}'.format(t)
#        start = pp.get_index_from_time(time)
#        end = pp.get_index_from_time(time+a_roll_int)
#        if k<len(shiftIndex) and pp.time[shiftIndex[k]]<pp.time[start]+a_roll_int:
#            print 'here'
#            start = pp.get_index_from_time(pp.time[shiftIndex[k]]+shift_skip)
#            end = pp.get_index_from_time(pp.time[shiftIndex[k]]+shift_skip+a_roll_int)
#            time = pp.time[start]
#            k = k+1
#        print 'time:{0}'.format(pp.time[start])
#        a = pp.short_array(a_uri, start, end)
#        #print abs(numpy.mean(a))
#        if(numpy.mean(a) > a_bar):
#                a_bar = numpy.mean(a)
#                print a_bar
#                #print 'time:{0}'.format(t)
#        time = time + time_inc
#
#    time = start_time # restart
#    k = 0
#    print 'Measure Jerk'
#    while time < (endTime-j_roll):
#        #print 'time:{0}'.format(t)
#        start = pp.get_index_from_time(time)
#        end = pp.get_index_from_time(time+j_roll)
#        if k<len(shiftIndex) and pp.time[shiftIndex[k]]<pp.time[start]+j_roll:
#            print 'here'
#            start = pp.get_index_from_time(pp.time[shiftIndex[k]]+shift_skip)
#            end = pp.get_index_from_time(pp.time[shiftIndex[k]]+shift_skip+j_roll)
#            time = pp.time[start]
#            k = k+1
#        jerk = pp.short_array(jerk_uri, start, end)
#        print 'time:{0}'.format(pp.time[start])
#        absjerk = []
#        #print absjerk
#        for i in jerk:
#            absjerk.append(abs(i))
#        if(numpy.mean(absjerk) > jerk_bar):
#                jerk_bar = numpy.mean(absjerk)
#                print jerk_bar
#                #print 'time:{0}'.format(t)
#        time = time + time_inc
#        #print "done"
    #---------------------------------------------------------------------------------
    #                  Potential_Design
    #---------------------------------------------------------------------------------
    Potential_Design = 0
    followTime = pp.get_data_by_index(followTime_uri, -1)
    if (SettlingTime == -1 or riseTime == -1 or minDistance < .1*minDistanceVelocity*followTime):
        Potential_Design = -1
    else: Potential_Design = 1

    print("Potential_Design: %d" %Potential_Design)

    #---------------------------------------------------------------------------------
    #                  Metrics
    #---------------------------------------------------------------------------------
    metrics = {}
    metrics.update({'vehicleMass':{'value': vehicleMass, 'unit':'kg'},
                    'distanceTraveled':{'value': distanceTraveled, 'unit': 'm'},
                    'minDistance': {'value': minDistance, 'unit': 'm'},
                    'finalVelocity':{'value': Vf, 'unit': 'm/s'},
                    'requiredTorque':{'value': requiredTorque, 'unit':'N-m'},
                    'riseTime':{'value': np.amax(riseTime), 'unit' :''},
                    'Overshoot':{'value': np.amax(Overshoot), 'unit' :''},
                    'settlingTime':{'value': np.amax(SettlingTime), 'unit' :''},
                    'rms_error':{'value': RMS_error, 'unit' : ''},
                    'numSetpointCrossings':{'value':numSetPointCrossings, 'unit': ''},
                    'averageA': {'value': maxAccel, 'unit': 'm/s2'},
                    'averageJ': {'value': maxJerk, 'unit': 'm/s3'},
                    'Potential_Design': {'value': Potential_Design, 'unit': ''},





                    #'chassisType':{'value': chassisType, 'unit' :''},
                    })
    print(metrics)
    cwd = os.getcwd()
    os.chdir('..')
    # print 'Plot saved to : {0}'.format(pp.save_as_svg(vehicle_speed,
                                                      # pp.global_abs_max(vehicle_speed),
                                                      # 'VehicleSpeed',
                                                      # 'max(FTP_Driver.driver_bus.vehicle_speed)',
                                                      # 'kph'))

    numSamples = int(endTime/time_inc)
    print(numSamples)
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
    check_limits_and_add_to_report_json(pp, limit_dict)
    update_metrics_in_report_json(metrics)
    ## end of Second limit part
    os.chdir(cwd)

if __name__ == '__main__':
    root_dir = os.getcwd()
    try:
        main()
    except:
        os.chdir(root_dir)
        import traceback
        trace = traceback.format_exc()
        # Generate this file on failed executions, https://github.com/scipy/scipy/issues/1840
        with open(os.path.join('..', '_POST_PROCESSING_FAILED.txt'), 'wb') as f_out:
            f_out.write(trace)

import sys
import os
from common import PostProcess, update_metrics_in_report_json
from common import read_limits, check_limits_and_add_to_report_json
import numpy as np

if __name__ == '__main__':
    try:
        mat_file_name = sys.argv[1]
        if not os.path.exists(mat_file_name):
            print 'Given result file does not exist: {0}'.format(sys.argv[1])
            os._exit(3)

        ## First limit part
        limit_dict, filter = read_limits()
        ## End of first limit part
        
        ## Post processing part
        filter.append('design.tank_level')
        filter.append('design.FuelTankVolume')
        filter.append('design.engine_heat_port.T')
        filter.append('driver_Land_Profile.driver_control.error_current.u2')

        # loads results with the filtered out variables (and 'time' which is default)
        pp = PostProcess(mat_file_name, filter)
        metrics = {}
        
        start_fraction = pp.get_data_by_time('design.tank_level', 0.01)[0]
        end_fraction = pp.last_value('design.tank_level')
        tank_volume = pp.last_value('design.FuelTankVolume')
        distance_covered_m = pp.integrate('driver_Land_Profile.driver_control.error_current.u2')
        
        print "start_fraction     : {0}".format(start_fraction)
        print "end_fraction       : {0}".format(end_fraction)
        print "tank_volume        : {0}".format(tank_volume)
        print "distance_covered_m : {0}".format(distance_covered_m)
        print "end_time           : {0}".format(pp.time[-1])
        
        metrics.update({'FuelConsumed': {'value': (start_fraction - end_fraction) * tank_volume, 'unit': 'L'}})
        metrics.update({'DistanceCovered': {'value': distance_covered_m, 'unit': 'm'}})
        metrics.update({'AverageSpeed': {'value': (distance_covered_m / pp.time[-1]) * 3.6, 'unit': 'kph'}})
        #metrics.update({'EngineTemperature': {'value': pp.last_value('design.engine_heat_port.T') - 273.15, 'unit': 'C'}})

        cwd = os.getcwd()
        os.chdir('..')        
        update_metrics_in_report_json(metrics)
        ## end of postprocessing part

        ## Second limit part
        check_limits_and_add_to_report_json(pp, limit_dict)
        ## end of Second limit part

        os.chdir(cwd)
    except Exception as err:
        print err.message
        if os.name == 'nt':
            import win32api
            win32api.TerminateProcess(win32api.GetCurrentProcess(), 1)
        else:
            sys.exit(1)

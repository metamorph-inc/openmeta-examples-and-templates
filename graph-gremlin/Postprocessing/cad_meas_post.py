import sys
import os
from common import PostProcess, update_metrics_in_report_json
from common import read_limits, check_limits_and_add_to_report_json
import math
import numpy as np
from scipy.io import loadmat

class postprocess:

    def __init__(self):
        self.stuff = {}

# gets array of data wanted
# parameters: result_mat[0], string of the data name
# returns the data in an array
    def data_array(self, result, name):
        data = result[name]
        #data_arr = np.array(data)
        return data
    
# prints array of data wanted
# parameters: result_mat[0], string of the data name
# returns the data in an array
    def print_data(self, result, name):
        data = self.data_array(result, name)
        print('name of data: ')
        print(name)
        print('here is the data: (with index)')
        print('[', end=' ')
        for i in xrange(data.size-1):
            print(str(i) + ':', str(data[i]) + ',', end=' ')
        print(str(i+1) + ':', str(data[i+1]) + ']')
        return data
    
# gets array of time
# parameter: result_mat[0]
# returns the time/time intervals in an array
    def time_array(self, result):
        time = result['time']
        
        return time 
    
# prints array of time
# parameter: result_mat[0]
# returns the time/time intervals in an array
    def print_time(self, result):
        time = time_array(self, result)
        print('here are time intervals:', time)
    
        return time 

# get an array between 2 values
# parameters: result_mat[0], name of the data, 2 values
# returns the "shortened" array
    def short_array(self, result, name, val1, val2):
        array = []
        data = result[name]
        for i in range(val1, val2):
            array.append(data[i])
        new_array = np.array(array)
        return new_array
        
# plot of data and time
# parameters: result_mat[0], string of the data name
# returns the data and time in an array
    def plot(self, result, name):
        data = self.data_array(self, result, name)
        time = self.time_array(self, result)

        return data, time

# get data based on time value
# parameters: time value, name of data, time data, result_mat[0]
# returns the data and the index of the data
    def get_data(self, time_val, name, time, result):
        i = 0
        while time[i] < time_val and i in xrange(time.size-1):
            i += 1
        data_arr = self.data_array(result, name)   
        if time[i-1] != time_val:
            cur = data_arr[i-1]
            next = data_arr[i]
            data = time[i-1] / ((time[i-1]+time[i])/2) * (next-cur) + cur
        else:
            data = data_arr[i-1]
        
        return data, i
                
# get time based on data value
    def get_time(self, data):
        pass
        
# last value
# parameter: result_mat[0]
# returns the last value
    def last_value(self, data):
        result = data[-1]
    
        return result

# maximum
# parameters: data array
# returns the result in an array
    def global_max(self, data):
        result = data.max()
    
        return result
    
# time of max
# parameters: data array
# returns the time at where the max is
    def global_max_time(self, data, time_arr):
        index = data.argmax()
        time = time_arr[index]  
    
        return time
    
# minimum
# parameters: data array
# returns the result in an array
    def global_min(self, data):
        result = data.min()
    
        return result
    
# time of min
# parameters: data array, time array
# returns the time at where the min is
    def global_min_time(self, data, time_arr):
        index = data.argmin()
        time = time_arr[index]   
    
        return time

# standard deviation
# parameters: data array
# returns the standard deviation of data
    def std_dev(self, data):
        stddev = data.std()
    
        return stddev

# variance
# parameters: data array
# returns the variance of data
    def variance(self, data):
        variance = data.var()
    
        return variance
    
# sum
# parameters: data array
# returns the sum of data
    def sum_value(self, data):
        result = data.sum()
    
        return result
    
# mean
# parameters: data array
# returns the mean of data
    def mean(self, data):
        result = np.mean(data, dtype=np.float64)
    
        return result
 
# integral
# parameters: data array, time array
# returns the area under the curve of data
    def integrate(self, data, time):
        sum = 0
        next = data[0]
        next_t = time[0]
        for i in xrange(data.size):
            cur = next
            next = data[i]
            cur_t = next_t
            next_t = time[i]
            height = (next + cur) / 2
            interval = next_t - cur_t
            sum = sum + (height * interval)
    
        return sum

# minimums
# parameters: data array
# returns the minimums of data
    def minimums(self, data):
        min = []
        prev = 0
        cur = 0
        next = data[0]
        for i in xrange(data.size):
            if cur < prev and cur <= next:
                min.append(cur)     
            prev = cur
            cur = next
            next = data[++i]
        minimum = np.array(min)
        
        return minimum
        
# maximums
# parameters: data array
# returns the maximums of data
    def maximums(self, data):
        max = []
        prev = 0
        cur = 0
        next = data[0]
        for i in xrange(data.size):
            if cur >= prev and cur > next:
                max.append(cur)        
            prev = cur
            cur = next
            next = data[++i]  
        maximum = np.array(max)
        
        return maximum

# time of positive to negative roots
# parameters: data array, time array
# returns time of the roots from positive to negative of data
    def pos_neg(self, data, time_arr):
        time = []
        tolerance = 0.00000015
        next = -1
        for i in xrange(data.size):
            cur = next
            next = data[i]
            if cur > 0+tolerance and next <= 0+tolerance:
                if cur != 0:
                    cur_t = time_arr[i-1]
                    next_t = time_arr[i]
                    time.append((cur / (cur+next)/2) * (next_t-cur_t) + cur_t)
                else:
                    time.append(time_arr[i-1])
        timing = np.array(time)
        
        return timing

# time of negative to positive roots
# parameters: data array, time array
# returns time of the roots from negative to positive of data
    def neg_pos(self, data, time_arr):
        time = [] 
        tolerance = 0.00000015
        next = 1
        for i in xrange(data.size):
            cur = next
            next = data[i]
            if cur <= 0+tolerance and next > 0+tolerance:
                if cur != 0:
                    cur_t = time_arr[i-1]
                    next_t = time_arr[i]
                    time.append(cur / ((cur+next)/2) * (next_t-cur_t) + cur_t)
                else:
                    time.append(time_arr[i-1])
        timing = np.array(time) 
        
        return timing
    
# time from a number to zero 
# (use index from print_data() function)
# parameters: data array, time array, index of value
# returns the time of the zero
    def to_zero(self, data, time_arr, value_index):
        i = value_index + 1
        cur = data[value_index]
        next = data[i]
        tolerance = 0.00000015
        if data[value_index] >= 0:
            while next >= 0+tolerance and i in xrange(data.size-1):
                i += 1
                cur = next
                next = data[i]
            if next >=0+tolerance:
                return -1
        else:
            while next <= 0+tolerance and i in xrange(data.size-1):
                i += 1
                cur = next
                next = data[i]
            if next <= 0+tolerance:
                return -1
        if cur != 0:
            cur_t = time_arr[i-1]
            next_t = time_arr[i]
            time = cur / ((cur+next)/2) * (next_t-cur_t) + cur_t
        else:
            time = time_arr[i-1]
        
        return time
        
# time from a number to zero 
# (use index from print_data() function)
# parameters: data array, time array, index of value
# returns the time of the zero
    def from_zero(self, data, time_arr, value_index):
        i = value_index - 1
        cur = data[value_index]
        next = data[i]
        tolerance = 0.00000015
        if data[value_index - 1] >= 0:
            while next >= 0+tolerance and i in xrange(data.size):
                i -= 1
                cur = next
                next = data[i]
            if next >= 0+tolerance:
                return -1
        else:
            while next <= 0+tolerance and i in xrange(data.size):
                i -= 1
                cur = next
                next = data[i]
            if next <= 0+tolerance:
                return -1
        if cur != 0:
            cur_t = time_arr[i+1]
            next_t = time_arr[i]
            time = cur / ((cur+next)/2) * (next_t-cur_t) + cur_t
        else:
            time = time_arr[i+1]
        
        return time
        
# find zeros
# parameters: data array, time array
# returns the time of the zero
    def zeros(self, data_array, time):
        data = [[],[]]
        data[0].append(self.pos_neg(data_array, time))
        data[1].append(self.neg_pos(data_array, time))
        data_arr = np.array(data)
    
        return data_arr
    
# compare two components
# parameters: 2 strings of data
# returns bool of whether they are the same
    def compare(self, str1, str2):
        data1 = self.data_array(str1)
        data2 = self.data_array(str2)
        for i in xrange(data1.size):
            if data1[i] != data2[i]:
                return False

        return True

# finding the difference between 2 times        
    def time_total(self, val1, val2):
        time = abs(val2 - val1)
        
        return time
    
def load_mat(datafile, expand_param_data=True):
	data = loadmat(datafile, matlab_compatible=True)
	
	names = data['name'].transpose()
	descrips = data['description'].transpose()
	
	data_loc = data['dataInfo'][0]
	data_sign = np.sign(data['dataInfo'][1])
	data_col = np.abs(data['dataInfo'][1]) - 1
	
	num_time_pts = data['data_2'][0].shape[0]
	
	data_dict = {}
	desc_dict = {}
	
	for i in xrange(names.shape[0]):
		
		name = ''.join([str(e) for e in names[i]]).rstrip()
		
		if name == 'Time':
			name = 'time'
		
		descrip = ''.join([str(e) for e in descrips[i]]).rstrip()
		
		desc_dict[name] = descrip
		
		if data_loc[i] == 1:
			if expand_param_data:
				data_dict[name] = (np.ones(num_time_pts) * 
								   data['data_1'][data_col[i]][0] * data_sign[i])  # memory runs out here
			else:
				data_dict[name] = data['data_1'][data_col[i]] * data_sign[i]
		else:
			data_dict[name] = data['data_2'][data_col[i]] * data_sign[i]
	
	return data_dict, desc_dict

	
	
if __name__ == '__main__':


	
    ##############################################################
    # update results in   tb manifest and/or summary (or both!)
    ##############################################################

    output_dir = ""
    json_filename = os.path.join(output_dir, 'testbench_manifest.json')
	 
    import json
    json_data = {}
    coords =[ [] ,[] ]
    if os.path.isfile(json_filename):
        with open(json_filename, "r") as json_file:
            json_data = json.load(json_file)
    tags = ["CG","F0_ILE", "F0_ITE" ,"F0_OLE" ,"F0_OTE" ,"C0_ILE" ,"C0_ITE" ,"C0_OLE" ,"C0_OTE","dome_tip","tail_exit","tail_base","tail_exit_internal","bnose_pt","dnose_pt"]
    for ss in tags :
        coords.append([])
    for metric in json_data['Metrics']: 
        for ss in tags: 
            #print ss
            if metric["Name"] == ss:
                idx = tags.index(ss)
                tmp = metric["Value"]
                for x in tmp.split(";") :
                    coords[idx].append(float(x))
                #print ss
                #print coords[idx]
    for ss in tags: 
        print(ss)
        idx = tags.index(ss)
        print(coords[idx])
    # coordinate system  [2] = tip to tail ; [0] = top to bottom;  [1] = left to right       
    fin_chord0 = coords[tags.index("F0_ILE")][2] - coords[tags.index("F0_ITE")][2]
    fin_chord1 = coords[tags.index("F0_OLE")][2] - coords[tags.index("F0_OTE")][2]
    fin_len = coords[tags.index('F0_OLE')][0] - coords[tags.index('F0_ILE')][0]    
    fin_trailing = coords[tags.index("F0_ILE")][2] - coords[tags.index("F0_OLE")][2]   
    fin_sweep = 180 * math.atan(abs(fin_trailing / fin_len)) / 3.14159  
    fin_type = "HEX"    
    
    canard_chord0 = abs(coords[tags.index("C0_ILE")][2] - coords[tags.index("C0_ITE")][2])
    canard_chord1 = abs(coords[tags.index('C0_OLE')][2] - coords[tags.index('C0_OTE')][2])
    canard_len =  abs(coords[tags.index('C0_OLE')][0] - coords[tags.index('C0_ILE')][0])
    canard_trailing = abs(coords[tags.index("C0_ILE")][2] - coords[tags.index("C0_OLE")][2])
    canard_sweep = 180 * math.atan(abs(canard_trailing / canard_len)) / 3.14159
    canard_type = "HEX"
    
    aft_len = abs(coords[tags.index('tail_base')][2] - coords[tags.index('tail_exit')][2])
    xx = 2*abs(coords[tags.index('dome_tip')][1] - coords[tags.index('tail_exit')][1])
    yy = 2*abs(coords[tags.index('dome_tip')][0] - coords[tags.index('tail_exit')][0])
    aft_diameter = math.sqrt(xx*xx+yy*yy)
    xx = 2*abs(coords[tags.index('dome_tip')][1] - coords[tags.index('tail_exit_internal')][1])
    yy = 2*abs(coords[tags.index('dome_tip')][0] - coords[tags.index('tail_exit_internal')][0])
    aft_exitdiameter = math.sqrt(xx*xx+yy*yy)
    xx = 2*abs(coords[tags.index('dome_tip')][1] - coords[tags.index('tail_base')][1])
    yy = 2*abs(coords[tags.index('dome_tip')][0] - coords[tags.index('tail_base')][0])
    missile_diameter = math.sqrt(xx*xx+yy*yy)
    missile_length = abs(coords[tags.index('dome_tip')][2] - coords[tags.index('tail_exit')][2])
    fin_station = abs(coords[tags.index('dome_tip')][2] - coords[tags.index('F0_ILE')][2])
    canard_station = abs(coords[tags.index('dome_tip')][2] - coords[tags.index('C0_ILE')][2])  

    dnose = 2*abs(coords[tags.index('dome_tip')][1] - coords[tags.index('dnose_pt')][1])
    bnose = abs(coords[tags.index('dome_tip')][1] - coords[tags.index('bnose_pt')][1])
    lnose = abs(coords[tags.index('dome_tip')][2] - coords[tags.index('dnose_pt')][2])
   
    missile_cg = [0,0,0]
    for i in [0,1,2]:
        missile_cg[i] = abs(coords[tags.index('dome_tip')][i] - coords[tags.index('CG')][i])
    
    print("Fin Chord Base   = " + str(fin_chord0))
    print("Fin Chord Tip    = " + str(fin_chord1))
    print("Fin Length       = " + str(fin_len))
    print("Fin sweep        = " + str(fin_sweep))          
    print("Canard Chord Base= " + str(canard_chord0))
    print("Canard Chord Tip = " + str(canard_chord1))
    print("Canard Length    = " + str(canard_len))   
    print("Canard sweep     = " + str(canard_sweep))
    print("aft length       = " + str(aft_len)) 
    print("aft diameter     = " + str(aft_diameter))
    print("aft exitdiameter = " + str(aft_exitdiameter))
    print("Missile_diameter     = " + str(missile_diameter))    
    print("Missile_length     = " + str(missile_length))
    print("Missile_cg         = " + str(missile_cg))
    print("bnose              = " + str(bnose))
    print("dnose              = " + str(dnose))
    print("lnose              = " + str(lnose))    
    for metric in json_data['Metrics']: 
        if metric["Name"] == "fin_chordroot": 
            metric["Value"] = str(fin_chord0)
        if metric["Name"] == "fin_chordtip": 
            metric["Value"] = str(fin_chord1)
        if metric["Name"] == "fin_sweep": 
            metric["Value"] = str(fin_sweep) 
        if metric["Name"] == "fin_span": 
            metric["Value"] = str(fin_len)  
        if metric["Name"] == "fin_station": 
            metric["Value"] = str(fin_station) 
        if metric["Name"] == "fin_type": 
            metric["Value"] = fin_type             
        if metric["Name"] == "canard_chordroot": 
            metric["Value"] = str(canard_chord0)
        if metric["Name"] == "canard_chordtip": 
            metric["Value"] = str(canard_chord1)            
        if metric["Name"] == "canard_sweep": 
            metric["Value"] = str(canard_sweep) 
        if metric["Name"] == "canard_span": 
            metric["Value"] = str(canard_len)   
        if metric["Name"] == "canard_station": 
            metric["Value"] = str(canard_station)   
        if metric["Name"] == "canard_type": 
            metric["Value"] = canard_type               
        if metric["Name"] == "aft_len": 
            metric["Value"] = str(aft_len) 
        if metric["Name"] == "aft_diameter": 
            metric["Value"] = str(aft_diameter) 
        if metric["Name"] == "aft_exitdiameter": 
            metric["Value"] = str(aft_exitdiameter) 
        if metric["Name"] == "missile_length": 
            metric["Value"] = str(missile_length) 
        if metric["Name"] == "missile_diameter": 
            metric["Value"] = str(missile_diameter)             
        if metric["Name"] == "missile_cg": 
            metric["Value"] = str(missile_cg[2]) 
        if metric["Name"] == "dome_type": 
            metric["Value"] = "OGIVE"
        if metric["Name"] == "dnose": 
            metric["Value"] = str(dnose)   
        if metric["Name"] == "bnose": 
            metric["Value"] = str(bnose)   
        if metric["Name"] == "lnose": 
            metric["Value"] = str(lnose)   

            
    cleanup = False
    
    mmass_kg = 60.0
    for metric in json_data['Metrics']: 
        if metric["Name"] == "missile_mass": 
            mmass_kg = float(metric["Value"])
            
    for metric in json_data['Metrics']: 
        if metric["Name"] == "missile_mass_lbs": 
            metric["Value"] = str(mmass_kg*2.20462)

    for param in json_data['Parameters']: 
            if param["Name"] == "Clean":
                print("CLEANING UP CAD FILES!!!!")
                cleanup = True
                dir = "."
                files = os.listdir(dir)
                for file in files:
                    print("Check :"+file)
                    if file.find(".prt.")!= -1 or file.find(".PRT.")!= -1 or file.find(".asm")!= -1 or file.find(".ASM")!= -1 or file.find("trail")!= -1:
                        print("Zapping "+os.path.join(dir,file))
                        try: 
                            os.remove(os.path.join(dir,file))
                        except : 
                            print("Failed to zap:"+os.path.join(dir,file))
                dir = "log"                        
                print("CLEANING UP LOG FILES!!!!")
                files = os.listdir(dir)
                for file in files:
                    print("Zapping "+os.path.join(dir,file))
                    try: 
                        os.remove(os.path.join(dir,file))
                    except : 
                        print("Failed to zap:"+os.path.join(dir,file))
                dir = "AP203_E2_SEPARATE_PART_FILES"                        
                print("CLEANING UP AP203 STEP FILES!!!!")
                try: 
                    files = os.listdir(dir)
                    for file in files:
                        print("Zapping "+os.path.join(dir,file))
                        os.remove(os.path.join(dir,file))
                except : 
                    print("Failed to zap:"+os.path.join(dir,file))
                dir = "AP203_E2_SINGLE_FILE"                        
                print("CLEANING UP AP203 STEP FILES!!!!")
                try: 
                    files = os.listdir(dir)
                    for file in files:
                        print("Zapping "+os.path.join(dir,file))
                        os.remove(os.path.join(dir,file))
                except : 
                    print("Failed to zap:"+os.path.join(dir,file))
            
    with open(json_filename, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

    try:
        fbat = open('my_output.txt', 'w')
    except Exception as e:
        log("Could not open  {0}: {1}".format(outputfilename_bat_path, str(e)))
    #fbat.write('set ERROR_CODE=0\n')    	
    #fbat.write('{0}\n'. format(str(result_mat)) )    	
    #fbat.write(' my outputs!!\n')    	
    #fbat.write('\n')    	
    #fbat.write('{0}\n'. format(float(result_mat['fov'])))    	
    #fbat.write('{0}\n'. format(str(result_mat['fov'])))    	
    #fbat.write('exit /b %ERROR_CODE%\n')    	
    #fbat.close()
    #sys.exit(0)
			
    try:

        cwd = os.getcwd()

    except Exception as err:
        print(err.message)
        if os.name == 'nt':
            import win32api
            win32api.TerminateProcess(win32api.GetCurrentProcess(), 1)
        else:
            sys.exit(1)
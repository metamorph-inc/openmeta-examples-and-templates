import sys
import os
from common import PostProcess, update_metrics_in_report_json
from common import read_limits, check_limits_and_add_to_report_json
import math
import numpy as np
from scipy.io import loadmat
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

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
	
    import xml.etree.ElementTree as ET
    from xml.etree import ElementTree
    from xml.etree.ElementTree import Element
    from xml.etree.ElementTree import SubElement


    t = ET.parse('CADAssembly_metrics.xml')
    r = t.getroot()
    robot = ET.Element('model')

    for mes in r.iter('MetricComponents'):
        for me in mes:
            print(me.tag,me.get('Name'),me.get('Type'))
            lnk = ET.SubElement(robot,"link",name=me.get('Name'))
            #lnk.set("name",me.get('Name'))
            if me.get('Type') == "PART":
                for cg in me.iter('CG'):
                    cgloc = cg.get('X')+" "+cg.get('Y')+" "+cg.get('Z')
                    print("CG=",cgloc)
                orig =  ET.SubElement(lnk,'origin')
                orig.text = cgloc
                #orig.value= cgloc
                myMass = "0.0001"
                for scalars in me.iter('Scalars'):
                    for scalar in scalars.iter("Scalar"):
                        if scalar.get("Name") == "Mass" :
                            myMass = scalar.get('Value')
                print("Mass: "+myMass)

                for it in me.iter('InertiaTensor'):
                    if it.get('At') == 'CENTER_OF_GRAVITY':
                        inert = ET.SubElement(lnk,"intertial")
                        mas = ET.SubElement(inert,"mass")
                        mas.text = myMass
                        #mas.set("value","123")

                        ine = ET.SubElement(inert,"inertia")
                        matrix = [[0 for i in xrange(3)] for i in xrange(3)]
                        inertArray =[[]]
                        for rowz in it.iter('Rows'):
                            y = 0
                            for row in rowz.iter('Row'):
                                rl = []
                                x= 0
                                for vv in row.iter('Column'):
                                    #print rl
                                    print("VALUE",vv.get("Value"))
                                    matrix[x][y] = vv.get("Value")
                                    rl.append(vv.get('Value'))
                                    x = x + 1
                                print("RL=",rl)
                                #row.set('value',str(rl))
                                inertArray.append(rl)
                                y = y + 1
                        print("InertArray: ",inertArray)
                        aa= ET.SubElement(ine,"ixx")
                        aa.text = str(matrix[0][0])
                        #aa.set("value",matrix[0][0])
                        aa = ET.SubElement(ine,"ixy")
                        aa.text = str(matrix[0][1])
                        #//aa.set("value",matrix[0][1])
                        aa = ET.SubElement(ine,"ixz")
                        aa.text = str(matrix[0][2])
                        #//aa.set("value",matrix[0][2])
                        aa = ET.SubElement(ine,"iyy")
                        aa.text = str(matrix[1][1])
                        #//aa.set("value",matrix[1][1])
                        aa = ET.SubElement(ine,"iyz")
                        aa.text = str(matrix[1][2])
                        #//aa.set("value",matrix[1][2])
                        aa = ET.SubElement(ine,"izz")
                        aa.text = str(matrix[2][2])
                        #//aa.set("value",matrix[2][2])

    t = ET.parse('ComputedValues.xml')
    r = t.getroot()
    for comps in r.iter('Components'):
        print(comps.tag)
        for comp in comps:
            print(comp.tag)
            for mets in comp:
                for me in mets:
                    mename = me.get('MetricName')
                    metype = me.get('Type')
                    meval = me.get('ArrayValue')
                    print(me.tag,mename,metype,meval)
                    if mename != None:
                        if mename.find('Joint') >= 0:
                            jpt =  ET.SubElement(lnk,'JointPoint')
                            jpt.set(mename,meval)
 
	
    output_file = open( 'links.xml', 'w' )
    output_file.write( '<?xml version="1.0"?>' )
    output_file.write( ET.tostring( robot) ) 
    output_file.close()
    print("robot stuff here.....")
    print(robot)
    #ET.dump(robot)
    for xx in robot:
        print("<1>",xx,xx.get('name'))
        for oo in xx:
            print("<2>",oo,oo.get("text"))
            for dd in oo:
                print("<3>",dd,dd.get("text"))
                for ee in dd:
                    print("<4>",ee,ee.text)

    ET.dump(robot)

# coding: utf-8
import sys
import os
import os.path
import json
import collections
import imp
# taken from CyPhyPython:
#  pythoncom.py calls LoadLibrary("pythoncom27.dll"), which will load via %PATH%
#  Anaconda's pythoncom27.dll (for one) doesn't include the correct SxS activation info, so trying to load it results in "An application has made an attempt to load the C runtime library incorrectly."
#  load our pythoncom27.dll (which we know works) with an explicit path
import os.path
# FIXME: would this be better : pkg_resources.resource_filename('win32api', 'pythoncom27.dll')
import pythoncom
# sys.path.append(r"C:\Program Files\ISIS\Udm\bin")
# if os.environ.has_key("UDM_PATH"):
#     sys.path.append(os.path.join(os.environ["UDM_PATH"], "bin"))
import _winreg as winreg
import pywintypes
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\META") as software_meta:
    meta_path, _ = winreg.QueryValueEx(software_meta, "META_PATH")
sys.path.append(os.path.join(meta_path, 'bin'))
import udm


from win32com.client import DispatchEx
Dispatch = DispatchEx
import win32com.client.dynamic
import win32com.server.util
from pywintypes import com_error
import json
# with open(sys.argv[1]) as input_json:

path_project_xme = os.path.abspath("PETDirectoryPassing.xme")
path_project_mga = os.path.abspath("PETDirectoryPassing_original.mga")

parser = win32com.client.DispatchEx("Mga.MgaParser")
parser.ParseProject(project, lib_xme)

print(path_project)
project = Dispatch("Mga.MgaProject")
project.Open("MGA=" + path_project)

project.BeginTransactionInNewTerr()
try:
    path_dv = "/@Testing/ParametricExploration/ParametricExploration/ParameterStudy/a"
    dv = project.RootFolder.GetObjectByPathDisp(path_dv)
    if dv is None:
        raise ValueError("Couldn't find DV '{}'".format(path_dv))

    # Manipulate the name
    print ('dv org Name: {}'.format(dv.Name))
    dv.Name = 'a_2'
    print ('dv new Name: {}'.format(dv.Name))

    # Name has changed so update our path
    path_dv = path_dv + "_2"
    dv = project.RootFolder.GetObjectByPathDisp(path_dv)

    # Change the range attribute
    print ('dv org Range: {}'.format(dv.GetStrAttrByNameDisp("Range")))
    dv.SetStrAttrByNameDisp("Range", "0.0,12.0")
    print ('dv new Range: {}'.format(dv.GetStrAttrByNameDisp("Range")))

finally:
    project.CommitTransaction()

project.Save(project.ProjectConnStr.replace(".mga", "_altered.mga"), True)
try:
    project.Close(False)
except pywintypes.com_error as e:
    if 'Access is denied' in repr(e):
        print('Could not save "{}". Is it open in GME?'.format(project.ProjectConnStr[4:]))
    else:
        raise


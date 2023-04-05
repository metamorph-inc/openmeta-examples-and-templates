# coding: utf-8
import sys
import os
import os.path
import json
import collections
import imp
import os.path
# FIXME: would this be better : pkg_resources.resource_filename('win32api', 'pythoncom27.dll')
# sys.path.append(r"C:\Program Files\ISIS\Udm\bin")
# if os.environ.has_key("UDM_PATH"):
#     sys.path.append(os.path.join(os.environ["UDM_PATH"], "bin"))
import six.moves.winreg as winreg
import pywintypes
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\META") as software_meta:
    meta_path, _ = winreg.QueryValueEx(software_meta, "META_PATH")
sys.path.append(os.path.join(meta_path, 'bin'))
import udm


from win32com.client import DispatchEx
import win32com.client.dynamic
Dispatch = win32com.client.dynamic.Dispatch
import win32com.server.util
from pywintypes import com_error
import json
# with open(sys.argv[1]) as input_json:

path_project_xme = os.path.abspath("PETDirectoryPassing.xme")
path_project_mga = os.path.abspath("PETDirectoryPassing_original.mga")

project = Dispatch("Mga.MgaProject")
project.Create("MGA=" + path_project_mga, "CyPhyML")

parser = Dispatch("Mga.MgaParser")
resolver = Dispatch("Mga.MgaResolver")
resolver.IsInteractive = False
parser.Resolver = resolver
parser.ParseProject(project, path_project_xme)
project.Save(project.ProjectConnStr, False)

print(path_project_mga)

project.BeginTransactionInNewTerr()
try:
    path_dv = "/@Testing/ParametricExploration/ParametricExploration/ParameterStudy/a"
    dv = project.RootFolder.GetObjectByPathDisp(path_dv)
    if dv is None:
        raise ValueError("Couldn't find DV '{}'".format(path_dv))

    # Manipulate the name
    print('dv org Name: {}'.format(dv.Name))
    dv.Name = 'a_2'
    print('dv new Name: {}'.format(dv.Name))

    # Name has changed so update our path
    path_dv = path_dv + "_2"

    # Change the range attribute
    print('dv org Range: {}'.format(dv.GetStrAttrByNameDisp("Range")))
    dv.SetStrAttrByNameDisp("Range", "0.0,12.0")
    print('dv new Range: {}'.format(dv.GetStrAttrByNameDisp("Range")))

    parameterStudy = dv.ParentModel
    pet = dv.ParentModel.ParentModel
    directoryProducer = pet.ObjectByPath('/@DirectoryProducer')
    directoryProducer_a = directoryProducer.ObjectByPath('/@a')
    connectionRole = pet.Meta.GetRoleByNameDisp("VariableSweep")
    connection = pet.CreateSimpleConnDisp(connectionRole, dv, directoryProducer_a, None, None)
    connection.Name = connectionRole.Name

finally:
    project.CommitTransaction()

project.Save(project.ProjectConnStr.replace("_original.mga", "_altered.mga"), False)
project.Close(True)


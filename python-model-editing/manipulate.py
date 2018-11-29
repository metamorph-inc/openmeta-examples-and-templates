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
import afxres
# FIXME: would this be better : pkg_resources.resource_filename('win32api', 'pythoncom27.dll')
imp.load_dynamic('pythoncom', os.path.join(os.path.dirname(afxres.__file__), 'pythoncom%d%d.dll' % sys.version_info[0:2]))
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


def log(s):
    print s


def log_formatted(s):
    print s
try:
    import CyPhyPython  # will fail if not running under CyPhyPython
    import cgi

    def log_formatted(s):
        CyPhyPython.log(s)

    def log(s):
        CyPhyPython.log(cgi.escape(s))
except ImportError:
    pass


def start_pdb():
    """Start pdb, the Python debugger, in a console window."""
    import ctypes
    ctypes.windll.kernel32.AllocConsole()
    import sys
    sys.stdout = open('CONOUT$', 'wt')
    sys.stdin = open('CONIN$', 'rt')
    import pdb
    pdb.set_trace()


# This is the entry point
def invoke(focusObject, rootObject, componentParameters, udmProject, **kwargs):
    pass


# Allow calling this script with a .mga file as an argument
if __name__ == '__main__':
    def run():
        import argparse

        parser = argparse.ArgumentParser(description='Re-run a PET with updated parameters.')
        parser.add_argument('--project')
        parser.add_argument('--pet-name')
        parser.add_argument('--log-file')
        parser.add_argument('--output-file')
        command_line_args = parser.parse_args()

        from win32com.client import DispatchEx
        Dispatch = DispatchEx
        import win32com.client.dynamic
        import win32com.server.util
        from pywintypes import com_error
        import json
        # with open(sys.argv[1]) as input_json:
        project = Dispatch("Mga.MgaProject")
        project.Open("MGA=" + os.path.abspath(command_line_args.project))

        project.BeginTransactionInNewTerr()
        try:
            pet = project.RootFolder.GetObjectByPathDisp(command_line_args.pet_name.replace("/", "/@"))
            if pet is None:
                raise ValueError("Couldn't find PET '{}'".format(args["PETName"]))
        finally:
            project.CommitTransaction()

        cyPhyPython = Dispatch("Mga.Interpreter.CyPhyPython")

        project.BeginTransactionInNewTerr()
        try:
            newPET = pet
            newPETID = pet.ID
            tbs = [tb for tb in newPET.ChildFCOs if tb.MetaBase.Name == 'TestBenchRef' and tb.Referred is not None]
            if not tbs:
                config_ids = [newPET.ID]
            else:
                tb = tbs[0]
                suts = [sut for sut in tb.Referred.ChildFCOs if sut.MetaRole.Name == 'TopLevelSystemUnderTest']
                if len(suts) == 0:
                    raise ValueError('Error: TestBench "{}" has no TopLevelSystemUnderTest'.format(tb.Name))
                if len(suts) > 1:
                    raise ValueError('Error: TestBench "{}" has more than one TopLevelSystemUnderTest'.format(tb.Name))
                sut = suts[0]
                if sut.Referred.MetaBase.Name == 'ComponentAssembly':
                    config_ids = [sut.Referred.ID]
                else:
                    configurations = [config for config in sut.Referred.ChildFCOs if config.MetaBase.Name == 'Configurations']
                    if not configurations:
                        raise ValueError('Error: design has no Configurations model "{}"'.format(args["GeneratedConfigurationModel"]))
                    configurations = configurations[0]
                    cwcs = [cwc for cwc in configurations.ChildFCOs if cwc.MetaBase.Name == 'CWC']
                    config_ids = [cwc.ID for cwc in cwcs]
        finally:
            project.CommitTransaction()

        config_light = Dispatch("CyPhyMasterInterpreter.ConfigurationSelectionLight")

        # GME id, or guid, or abs path or path to Test bench or SoT or PET
        config_light.ContextId = newPETID

        config_light.SetSelectedConfigurationIds(config_ids)

        # config_light.KeepTemporaryModels = True
        config_light.PostToJobManager = False

        class StatusCallback(object):
            _public_methods_ = ['SingleConfigurationProgress', 'MultipleConfigurationProgress']

            def __init__(self, log):
                self.log = log

            def SingleConfigurationProgress(self, args):
                # args = win32com.client.dynamic.Dispatch(args)
                # print (args.Context or '') + ' ' + (args.Configuration or '') + ' ' + args.Title
                pass

            def MultipleConfigurationProgress(self, args):
                args = win32com.client.dynamic.Dispatch(args)
                # print (args.Context or '') + ' ' + (args.Configuration or '') + ' ' + args.Title
                self.log.write(args.Title + '\n')
                self.log.flush()

        master = Dispatch("CyPhyMasterInterpreter.CyPhyMasterInterpreterAPI")
        master.Initialize(project)
        logfile = None
        if command_line_args.log_file:
            logfile = open(command_line_args.log_file, 'wb')
            cb = win32com.client.dynamic.Dispatch(win32com.server.util.wrap(StatusCallback(logfile)))
            master.AddProgressCallback(cb)
        # master.Initialize(project._oleobj_.QueryInterface(pythoncom.IID_IUnknown))
        results = master.RunInTransactionWithConfigLight(config_light)
        if logfile:
            logfile.close()

        print(results)

        if command_line_args.output_file:
            with open(command_line_args.output_file, "w") as out:
                for mi_result in results:
                    result_obj = {
                        "success": mi_result.Success,
                        "message": mi_result.Message,
                        "exception": mi_result.Exception,
                        "output_directory": mi_result.OutputDirectory
                    }
                    out.write(json.dumps(result_obj))
                    out.write("\r\n")

        project.Save(project.ProjectConnStr + "_PET_debug.mga", True)
        try:
            project.Close(False)
        except pywintypes.com_error as e:
            if 'Access is denied' in repr(e):
                print('Could not save "{}". Is it open in GME?'.format(project.ProjectConnStr[4:]))
            else:
                raise

        # print(cyPhyPython.ComponentParameter())

    run()
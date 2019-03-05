from __future__ import print_function, unicode_literals

import sys
import os
#sys.path.append(r"C:\Program Files\ISIS\Udm\bin")
#if os.environ.has_key("UDM_PATH"):
#    sys.path.append(os.path.join(os.environ["UDM_PATH"], "bin"))
import _winreg as winreg
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\META") as software_meta:
    meta_path, _ = winreg.QueryValueEx(software_meta, "META_PATH")
sys.path.append(os.path.join(meta_path, 'bin'))

import datetime
import os.path
import pprint
import shutil
from cStringIO import StringIO

import udm
import six
import csv

from gremlin_python import statics
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
from gremlin_python.process.traversal import Order
from gremlin_python.process.traversal import Cardinality
from gremlin_python.process.traversal import Column
from gremlin_python.process.traversal import Direction
from gremlin_python.process.traversal import Operator
from gremlin_python.process.traversal import P
from gremlin_python.process.traversal import Pop
from gremlin_python.process.traversal import Scope
from gremlin_python.process.traversal import Barrier
from gremlin_python.process.traversal import Bindings
from gremlin_python.process.traversal import WithOptions

uml_diagram = udm.uml_diagram()
Uml = udm.map_uml_names(uml_diagram)

# This is the entry point
def invoke(focusObject, rootObject, componentParameters, **kwargs):
    log("Running elaborator")
    elaborate(focusObject)

    log(pprint.pformat(componentParameters))

    g = make_graph(focusObject)

    # Find the top 10 objects in the graph by degree centrality
    # Derived from Tinkerpop example: http://tinkerpop.apache.org/docs/current/recipes/#degree-centrality
    degrees = (g.V().project("v", "name","degree").by().by("name").
        by(__.bothE().count()).order().by(__.select("degree"), Order.desc)
        .limit(10).toList())

    log(pprint.pformat(degrees))

    with open(os.path.join(componentParameters["output_dir"], "centrality.csv"), "wb") as output_file:
        writer = csv.DictWriter(output_file, ["name", "degree"], extrasaction="ignore")

        writer.writeheader()
        writer.writerows(degrees)

    componentParameters["runCommand"] = "cmd.exe /c echo"


def make_graph(focusObject):
    g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))

    # Make sure this graph is empty (real code should probably create a graph
    # here or something)
    g.V().drop().iterate()

    def visit_and_make_nodes(gme_node, parent_gremlin_node = None):
        if not is_object_association(gme_node):
            node_type = gme_node.type.name
            node_id = gme_node.id
            node_name = gme_node.name

            new_node_traversal = g.addV(node_type).property('id', node_id)

            for (attribute_name, attribute_value) in six.iteritems(list_object_attributes(gme_node)):
                new_node_traversal = new_node_traversal.property(attribute_name, attribute_value)

            new_node = new_node_traversal.next()

            if(parent_gremlin_node != None):
                g.V(parent_gremlin_node).addE('contains').to(new_node).iterate()

            for child in gme_node.children():
                visit_and_make_nodes(child, new_node)

            # log("{0}: {1}".format(node_name, node_type))
            # log(str(list_object_attributes(gme_node)))

    visit_and_make_nodes(focusObject)

    def visit_and_make_connections(gme_node):
        if is_object_association(gme_node):
            node_type = gme_node.type.name
            node_id = gme_node.id
            node_name = gme_node.name

            # log("{0}: {1}".format(node_name, node_type))

            (src_obj, dst_obj) = get_association_ends(gme_node)

            src_node = g.V().has("id", src_obj.id).next();
            dst_node = g.V().has("id", dst_obj.id).next();

            new_edge_traversal = g.V(src_node).addE(node_type)

            for (attribute_name, attribute_value) in six.iteritems(list_object_attributes(gme_node)):
                new_edge_traversal = new_edge_traversal.property(attribute_name, attribute_value)

            new_edge = new_edge_traversal.to(dst_node).iterate()

            # log("  {0} ({1}) => {2} ({3})".format(src_obj.id, src_obj.name, dst_obj.id, dst_obj.name))

        for child in gme_node.children():
            visit_and_make_connections(child)

    visit_and_make_connections(focusObject)

    return g

def is_object_association(o):
    if o.type.association:
        return True
    else:
        return False

def get_association_ends(o):
    src_obj = getattr(o, o.type.association.children()[0].name)
    dst_obj = getattr(o, o.type.association.children()[1].name)

    return (src_obj, dst_obj)

def list_object_attributes(o):
    def list_class_attributes(class_):
        attributes_set = set()
        attributes = class_.children(child_type=Uml.Attribute)
        if attributes:
            for attribute in attributes:
                attributes_set.add(attribute.name)

        if class_.baseTypes:
            for base_type in class_.baseTypes:
                attributes_set |= list_class_attributes(base_type)

        return attributes_set

    attribute_values = {}

    for attribute_name in list_class_attributes(o.type):
        attribute_values[attribute_name] = o.attr(str(attribute_name))
    return attribute_values


#CyPhyPython boilerplate stuff
def log(s):
    print( s)
try:
    import CyPhyPython # will fail if not running under CyPhyPython
    import cgi
    def log(s):
        CyPhyPython.log(cgi.escape(s))
except ImportError:
    pass

def log_formatted(s):
    print( s)
try:
    import CyPhyPython # will fail if not running under CyPhyPython
    import cgi
    def log(s):
        CyPhyPython.log(s)
except ImportError:
    pass

def elaborate(focusObject):
    import win32com.client.dynamic
    elaborate = win32com.client.dynamic.Dispatch("MGA.Interpreter.CyPhyElaborateCS")
    succeeded = elaborate.RunInTransaction(focusObject.convert_udm2gme().Project, focusObject.convert_udm2gme(), win32com.client.dynamic.Dispatch("Mga.MgaFCOs"), 128)
    if not succeeded:
        raise RuntimeError("Elaborator failed")

def start_pdb():
    ''' Starts pdb, the Python debugger, in a console window
    '''
    import ctypes
    ctypes.windll.kernel32.AllocConsole()
    import sys
    sys.stdout = open('CONOUT$', 'wt')
    sys.stdin = open('CONIN$', 'rt')
    import pdb; pdb.set_trace()

# Debugging helper methods
def log_object(o, indent=0):
    # if o.type.name == "GenericDomainModel":
    #     log("{2}{0} - {1} - {3} - {4} -> {5}".format(o.name, o.type.name, '  '*indent, o.Domain, o.Type, get_adjacent_object_names(o)))
    # elif o.type.name == "GenericDomainModelParameter":
    #     log("{2}{0} - {1} - {3}".format(o.name, o.type.name, '  '*indent, SimulinkBlock.get_adjacent_param_value(o)))
    # elif o.type.name == "GenericDomainModelPort":
    #     log("{2}{0} - {1} -> {3}".format(o.name, o.type.name, '  '*indent, get_adjacent_object_names(o)))
    # else:
    log("{2}{0} - {1}".format(o.name, o.type.name, '  '*indent))

    for child in o.children():
        log_object(child, indent + 1)

def get_adjacent_object_names(o):
    adjacent = o.adjacent()
    return [get_full_path(a) for a in adjacent]

def get_full_path(o):
    path = []
    intermediate = o
    while intermediate != udm.null:
        path.insert(0, (intermediate.name, intermediate.type.name))
        intermediate = intermediate.parent

    return '/'.join(["{0} ({1})".format(name, typeName) for (name, typeName) in path])

if __name__ == "__main__":
    import _winreg as winreg
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\META") as software_meta:
        meta_path, _ = winreg.QueryValueEx(software_meta, "META_PATH")

    # need to open meta DN since it isn't compiled in
    uml_diagram = udm.uml_diagram()
    meta_dn = udm.SmartDataNetwork(uml_diagram)
    import os.path
    CyPhyML_udm = os.path.join(meta_path, r"generated\CyPhyML\models\CyPhyML_udm.xml")
    if not os.path.isfile(CyPhyML_udm):
        CyPhyML_udm = os.path.join(meta_path, r"meta\CyPhyML_udm.xml")
    meta_dn.open(CyPhyML_udm, "")

    dn = udm.SmartDataNetwork(meta_dn.root)
    dn.open(sys.argv[1], "")
    # TODO: what should focusObject be
    # invoke(None, dn.root);
    dn.close_no_update()
    meta_dn.close_no_update()

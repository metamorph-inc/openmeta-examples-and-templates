OpenMETA Gremlin Graph Example
==============================

This example demonstrates how to bring an OpenMETA model into a graph database
and run graph algorithms on it, using Gremlin's Python bindings.  The included
`openmeta_to_gremlin.py` script will, when run against a component assembly
within a test bench, generate a graph corresponding to the component assembly
using Gremlin, then use that graph to determine the top 10 objects in the
graph by degree centrality (this can be easily replaced with your own graph
traversal code).

Prerequisites
-------------

  * Install Gremlin's Python bindings into OpenMETA's Python:

        "C:\Program Files (x86)\META\bin\Python311\python.exe" -m pip install --user gremlinpython futures

  * Download and extract [Gremlin Server][tinkerpop-web].  The Gremlin server
    can be configured to access any graph database supported by Tinkerpop, but
    this example expects a single GraphTraversalSource attached to an empty
    graph labeled `g`--  the default Gremlin Server configuration included with
    the 3.4.0 distribution is acceptable (it uses an empty, in-memory
    TinkerGraph database by default).  See the [Gremlin Server Documentation][gremlin-server-docs]
    for more details on configuration.

    **Note:**  This script will remove and replace the contents of the
    connected graph database with its own data; don't use a database with
    contents that you care about.

[tinkerpop-web]: https://tinkerpop.apache.org/
[gremlin-server-docs]: http://tinkerpop.apache.org/docs/3.4.0/reference/#gremlin-server

Using
-----

The `openmeta_to_gremlin.py` script is designed to work with OpenMETA's
CyPhyPython interpreter--  in `Spacecraft.xme`, there is an example testbench
(at "Testing/GraphTB") that will run the `openmeta_to_gremlin` script.  Open
the test bench in OpenMETA and run the Master Interpreter to run the test bench;
the script's output will be placed in the test bench's results folder.

To apply the script to your own models, you'll need to create a test bench and
workflow that runs the `openmeta_to_gremlin.py` script in your model.  See the
[OpenMETA Documentation][openmeta-tb-tutorial] for a walkthrough.

[openmeta-tb-tutorial]: http://docs.metamorphsoftware.com/doc/tutorials/hello_world/hello_world_analyzing_our_company.html

Results
-------

The top ten elements in the MorphSat_v3 component assembly by degree centrality,
as computed using Gremlin:

    [{u'degree': 40L, u'name': u'MorphSat_V3', u'v': v[170057]},
     {u'degree': 36L, u'name': u'Base_Module_Frame', u'v': v[170070]},
     {u'degree': 26L, u'name': u'Shelf1', u'v': v[172580]},
     {u'degree': 26L, u'name': u'Shelf3', u'v': v[174951]},
     {u'degree': 26L, u'name': u'Shelf2', u'v': v[173348]},
     {u'degree': 26L, u'name': u'Computer', u'v': v[175719]},
     {u'degree': 24L, u'name': u'CADModel', u'v': v[172720]},
     {u'degree': 24L, u'name': u'CADModel', u'v': v[175091]},
     {u'degree': 24L, u'name': u'CADModel', u'v': v[173488]},
     {u'degree': 23L, u'name': u'Battery', u'v': v[170931]}]

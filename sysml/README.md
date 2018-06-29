# sysml

This set of OpenMETA and Cameo projects shows how OpenMETA PETs can be exposed within Cameo Systems Modeler as Constraint Blocks and Activity Diagrams.

## Requirements

These project require the No Magic's Cameo Systems Modeler and "OpenMETA Plugin":

* Cameo Systems Modeler 18.5
* OpenMETA v0.18.5 or higher
* OpenMETA Plugin v2.1.0 or higher

OpenMETA can be downloaded from the product website: http://openmeta.metamorphsoftware.com/
The OpenMETA Plugin is available only by request. Please feel free to contact us at support@metamorphsoftware.com.

Once you've installed the OpenMETA Plugin, you can access its documentation through the Cameo Help menu.
![MasterInterpreter](/path-to-cameo-plugin-docs.png "Opening the OpenMETA Plugin User Guide from within Cameo")

## Projects

### python

This set of projects demonstrates the ability to execute an OpenMETA PET with a Python analysis block from within Cameo by executing an instance table.

To give it a try yourself:

1. Open the `python/spacecraft.mdxml` project.
2. Open the `00_Operational::MissionInstanceTable`.
3. Click the *Run* button at the end of the diagram window toolbar.

### cad

This set of projects demonstrates the ability to execute an OpenMETA PET with CAD Model Assembly from within Cameo by executing an instance table using the System Structure of Cameo to build a new OpenMETA Component Assembly to use as the Top-Level System Under Test.

To give it a try yourself:

1. Open the `cad/spacecraft_composition.mdxml` project.
2. Open the `01-Spacecraft::Instances::Instance Table`.
3. Click the *Run* button at the end of the diagram window toolbar.


# Hohmann Transfer Example
This example is based on the Hohmann Transfer orbital mechanics example from NASA's OpenMDAO team. The example is detailed in their documentation:
http://openmdao.org/twodocs/versions/2.2.0/examples/hohmann_transfer/hohmann_transfer.html

This OpenMETA model includes a PET with an optimizer, and uses a combination of Python scripts and Excel spreadsheets to accomplish the calculation. The optimizer works to minimize the total Delta-V.

## More Documentation on OpenMETA Features
Comprehensive documentation for the Parametric Exploration capability is available in the OpenMETA Documentation:
http://docs.metamorphsoftware.com/doc/reference_modeling/pet/pet.html

It includes details on how to use specific integrations such as Python, MATLAB, and Excel.

## How to Run It
1. Double-click on `hohmann-transfer.xme` to load the project. OpenMETA will ask you to save an MGA file. Choose the same folder you loaded the XME from. The MGA file is the "working copy" of your project.
2. In the *GME Browser* at the right, navigate to `RootFolder -> Analysis -> ParametricExploration -> HohmannTransfer_Complete`

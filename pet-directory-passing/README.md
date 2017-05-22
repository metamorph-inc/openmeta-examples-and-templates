PET Directory Passing Example
=============================

This example illustrates passing a directory between components, as well as archiving the contents of the directory as an artifact by saving its contents as a ZIP file.

Contents
--------

  * `PETDirectoryPassing.xme` - OpenMETA model containing a PET that incorporates the DirectoryProducer and DirectoryConsumer OpenMDAO components.
  * `python\DirectoryProducer.py` - OpenMDAO component that takes in two numbers, and outputs several files within a single directory.  Outputs the directory's path as a string, and also outputs the contents of the directory as a ZIP file pointed to by a FileRef.
  * `python\DirectoryConsumer.py` - OpenMDAO component that takes in a directory name (passed as a string), and outputs statistics about that directory.

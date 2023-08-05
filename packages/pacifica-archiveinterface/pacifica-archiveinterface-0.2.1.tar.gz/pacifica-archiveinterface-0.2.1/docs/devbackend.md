# Extending Supported Backends

## Create a backend directory

Under `pacifica/archiveinterface/backends` add a
directory for the new backend type

## Create Classes that Implement the Abstract Backend Class methods

Abstract backend classses can ge found under:
`pacifica/archiveinterface/backends/abstract`
Descriptions of all the methods that need to be abstracted exists in the
comments above the class.

## Update Backend Factory

Update the archive backend factory found here:
`pacifica/archiveinterface/backends/factory.py`
In this file is a `load_backend_archive()` method.  This method needs to have
its logic extended to support the new backend type.  This also entails loading
the appropriate files for this backend using import

## Update Interface Server

Update the `main()` method to support the new backend choice.
File located: `pacifica/archiveinterface/__main__.py`
In this file the type argument is defined with its supported types.  Need to
extend that array to include the new backend type

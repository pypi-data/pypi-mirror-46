==========
CHANGE LOG
==========

*1.2.0* 
- Changes to object model

1.3.1
- Implements startLocalQIS
- Packs QIS v1.6 - fixes the bugs with QIS >v1.6 and multiple modules
- Updates quarchPPM (connection_specific)
- Compatible with x6 PPM QIS stream.

1.3.2
- Bug Fix running QIS locally

1.3.3
- Implements isQisRunning
- Implements qisInterface
- Changes startLocalQIS to startLocalQis
- Fixes a bug in QIS interface listDevices that didn't allow it to work with Python 3

1.3.4
- Implemented resampling and a better way to launch QIS from the script.

1.4
- Integration with QPS
- supports Iometer testing
- Additional fixes for wait times

1.4.1
- Fixed the wmi error when importing quarchpy.

1.5
- Integration with FIO 
- Additional QPS functionality
- Added device search timeout

1.5.1
- Additional Bug Fixes

1.5.2
- Bug Fix - Case sensitivity issue with devices 

1.5.4
- Updating README and LICENSE

1.6.0
- custom $scan IP
- fixes QIS detection
- implements custom separator for stream files
- Bug fix - QIS Load

1.6.1
- Updating USB Scan
- Adding functionality to specify OS bit architecture (windows)

1.7
- Improved compatability with Windows and Ubuntu 

1.7.1
- Updated FIO for use with Linux and to allow arguments without values 
- Fixes path problem on Linux
- Fixes FIO on Linux

1.7.2
- Bug fixing timings for QIS (LINUX + WINDOWS)

1.7.3
- Additional Bug Fixes

1.7.4
- Updated to QPS 1.08

1.7.5
- Fixed USB DLL Compatibility 
- Fixed potential path issues with Qis and Qps open

1.7.6
- Fixes bug with usb connection

1.8
- Tab to white space convert
- Updated __init__ file to co-allign with python practices
- Updated project structure 
- Added documents for changes and Script Locations
- Disk selection update
- Compatibility with Python 3 and Linux Improved!

2.0
- Major folder restructure
- Added test center support
- detected streaming devices
- added latest qps1.09 and qis
- minor bug fixes
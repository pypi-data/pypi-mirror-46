# STKHelper

STKHelper is a Python package for creating and running STK Simulations using their interface.

## Installation

STKHelper is on the [Python Packaging Index](https://pypi.org/project/stkhelper/). Thus, use [pip](https://pip.pypa.io/en/stable/) to install STKHelper.

```bash
pip install stkhelper
```

## Prerequisites

STKHelper currently only work on Windows platforms. Along with this, you will need [STK](https://agi.com/products) downloaded and running on your computer using a purchased license. This will not work with the free version of STK because the free version does not have access to the Interface.

## Modules

STKHelper currently offers three different modules to aid in calculations.

### application.py

```python
from stkhelper import application

app = application.Application()
```

This module contains the `Application` class, which is the class used to create applications and scenarios in STK. It stores all area target and satellite information for the scenario while also manages the current running application, scenario, and root.

### processing.py

```python
from stkhelper import processing

processing.Processing.PrintSatellites(satelliteArray)
```
```bash
Satellite:		15
Satellite Name:		ISS
Satellite Pointer:	<pointerToObject>
```

This module contains the `Processing` class, which is a static class containing static methods used for processing data, problem solving, or clear display.

### tle_manager.py

```python
from stkhelper import tle_manager

parsedTLE = tle_manager.TLE_Manager.ParseTLE('TestTLE.txt')
```

This module contains the `TLE_Manager` class, which is a static class containing static methods used for handling, processing, retrieving, and parsing TLE files. Currently, the module only supports parsing a TLE, but will eventually be able to retrieve a TLE from STK's server.

## Usage

```python
from stkhelper import application

app = application.Application()
app.AddScenario('Test Scenario','+24hr')

app.CloseScenario()
app.CloseApplication()
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

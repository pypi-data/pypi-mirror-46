"""

Provides the Application class to create an STK11 object.

The purpose of this code is to add simplicity to STK integration with
the Python programming language.

"""

from win32api import GetSystemMetrics
from comtypes.client import CreateObject
from comtypes.gen import STKObjects
from comtypes import COMError
import sys

#Inner-package imports
from tle_manager import TLE_Manager
from processing import Processing

__author__ = "W. Conor McFerren"
__maintainer__ = "W. Conor McFerren"
__email__ = "cnmcferren@gmail.com"

class Application:
    """
    
    Application object that holds the STK11 application
    
    """

#%% init Function
    
    def __init__(self):
        
        """
        
        Initialization function for the Application class. Creates a new
        application of STK11 and sets visibility and user control to true.
        Also initializes the list of area targets, the list of satellites,
        and the list of cameras.
        
        """
        
        assert ('win32' in sys.platform), 'This code can only be run on Windows'
        
        self.uiApplication = CreateObject("STK11.Application")
        self.uiApplication.Visible = True
        self.uiApplication.UserControl = True
        
        self.root = self.uiApplication.Personality2
        
        self.areaTargetList = []    # [name, satellite]
        self.satelliteList = []     # [areaTarget, name, patterns]
        self.cameraList = []        # [camera, cameraGeneral]

#%% Methods to add objects
        
    def AddScenario(self, name, timePeriod):
        
        """
        
        Adds a scenario to the STK11 application (uiApplication) and
        creates the root.
        
        Parameters:
            name (str): Name of the new scenario
            timePeriod (str): Time period for the scenario to continue
            to. Written in the form "+24hr"
            
        Returns:
            The pointer to the scenario created.
            
        """
        
        self.root.NewScenario(name.replace(' ','_'))
        self.scenario = self.root.CurrentScenario
        self.scenario = self.scenario.QueryInterface(STKObjects.IAgScenario)
        try:
            self.scenario.SetTimePeriod('Today',str(timePeriod))
        except COMError:
            raise ValueError, "Time period not properly formatted"
        
        return self.scenario

    def AddSatellite(self, name, tleFile):
        
        """
        
        Adds satellite to the current scenario of the application.
        
        Parameters:
            name (str): Name of the satellite to be displayed in program.
            tleFile (str): Name of the TLE file to be used.
            
        Returns:
            The pointer to the satellite created.
            
        """
    
        tle = TLE_Manager.ParseTLE(tleFile)
        self.scenario = self.scenario.QueryInterface(STKObjects.IAgScenario)
        try:
            satellite = self.root.CurrentScenario.Children.New(STKObjects.eSatellite, name)
        except COMError:
            raise (RuntimeError,'\nIncorrect name format or name already taken for satellite.' + 
                  ' Please do not use spaces or reuse satellite names.')
        try:
            self.root.ExecuteCommand('SetState */Satellite/' + name + ' TLE "' +
                                     tle[0] + '" "' + tle[1] +
                                     '" TimePeriod "' +
                                     self.scenario.StartTime + '" "' +
                                     self.scenario.StopTime + '"')
        except COMError:
            raise (RuntimeError, "Failure to add satellite. Check formatting of TLE.")
        
        self.satelliteList.append([name, satellite])
        
        return satellite
        
    def AddCamera(self, name, hostSat, fovWidth, fovLength):
        
        """
        
        Adds a camera to a host satellite with a certain rectangular
        field of view.
        
        Parameters:
            name (str): Name of camera to be displayed in program.
            hostSat (STKObjects.eSatellite): Satellite to hold the camera.
            fovWidth (float): Width of field of view (in degrees).
            fovLength (float): Length of field of view (in degrees).
            
        Returns:
            The pointer to the camera created.
            
        """
        
        if not ((type(fovWidth) == int or type(fovWidth) == float) and
                (type(fovLength) == int or type(fovLength) == float)):
            raise TypeError, "Field of View parameters of invalid type."
            
        self.root.BeginUpdate()
        
        cameraGeneral = hostSat.Children.New(20, name)
        camera = cameraGeneral.QueryInterface(STKObjects.IAgSensor)
        camera.CommonTasks.SetPatternRectangular(fovWidth, fovLength)
        
        self.root.EndUpdate()
        
        self.cameraList.append([camera,cameraGeneral])
        
        return camera
        
    def AddAreaTarget(self, parsedLine):
        
        """
        
        Adds area target to the scenario of the application
        
        Parameters:
            name (str): Name of area target to be displayed in program.
            coordPoints (list): List of tuples containing coordinate 
            representing coordinate pairs.
            
        Returns:
            The pointer to the area target created.
            
        """
        
        self.root.BeginUpdate()
        
        ID = parsedLine[1]
        startLat = parsedLine[8]
        startLon = parsedLine[9]
        endLat = parsedLine[10]
        endLon = parsedLine[11]
        
        print("Adding: " + ID)

        areaTarget = self.root.CurrentScenario.Children.New(STKObjects.eAreaTarget,ID)
        areaTarget = areaTarget.QueryInterface(STKObjects.IAgAreaTarget)
        areaTarget.AreaType = STKObjects.ePattern
        patterns = areaTarget.AreaTypeData
        patterns = patterns.QueryInterface(STKObjects.IAgAreaTypePatternCollection)
        
        patterns.Add(startLat,startLon)
        patterns.Add(startLat,endLon)
        patterns.Add(endLat,endLon)
        patterns.Add(endLat,startLon)
        areaTarget.AutoCentroid = True

        self.areaTargetList.append([ID,areaTarget])
        
        self.root.EndUpdate()
        
        return areaTarget


#%% Access Functions
        
    def ComputeAccess(self, cameraArray, areaTargetArray):
        
        """
        
        Computes access between a camera and an area target and saves access
        to file with area targets name in the local directory.
        
        Parameters:
            cameraArray (list): List of camera and info from cameraList.
            areaTargetArray (list): List of area target and info from 
            areaTargetList.
        
        """
        
        self.root.BeginUpdate()
        
        access = cameraArray[1].GetAccessToObject(areaTargetArray[0])
        access.ComputeAccess()
        intervalCollection = access.ComputedAccessIntervalTimes
        try:
            computedIntervals = intervalCollection.ToArray(0,-1)
            filename = areaTargetArray[1] + '.txt'
            Processing.ArrayToFile(computedIntervals,filename)
        except Exception:
            filename = areaTargetArray[1] + '.txt'
            blankFile = open(filename,'w')
            blankFile.close()
            
        self.root.EndUpdate()
    
    def ComputeAllAccess(self, cameraArray):
        for i in range(len(self.areaTargetList)):
            self.ComputeAccess(cameraArray,self.areaTargetList[i])

    def ComputeLifetime(self, satArray):

        """

        Computes the lifetime of the satellite provided.

        Parameters:
            satArray (list): List that contains the satellite used for computation.

        """

        ##TODO TESTING REQUIRED
        name = satArray[1]
        self.root.ExecuteCommand("Lifetime */Satellite/" + str(name))
    
    def ComputeKeplerians(self, satArray, timeInstant):

	"""

	Computes the keplerian parameters for a satellite at a time instant.

	Parameters:
		satArray (list): Array containing the name and the satellite object.
		timeInstant (str): String containing the time instant.

	Returns:
		arr (list): Array containing the keplererian parameters.

	"""
        
        sat = satArray[1]
        
        satDPSingle = sat.DataProviders.Item('Classical Elements')
        satDPSingle = satDPSingle.QueryInterface(STKObjects.IAgDataProviderGroup)
        ceicrf = satDPSingle.Group.Item('ICRF')
        ceicrf = ceicrf.QueryInterface(STKObjects.IAgDataPrvTimeVar)
        
        result = ceicrf.ExecSingle(timeInstant)
        
        time = result.DataSets.GetDataSetByName('Time').GetValues()
        sma = result.DataSets.GetDataSetByName('Semi-major Axis').GetValues()
        ecc = result.DataSets.GetDataSetByName('Eccentricity').GetValues()
        inc = result.DataSets.GetDataSetByName('Inclination').GetValues()
        raan = result.DataSets.GetDataSetByName('RAAN').GetValues()
        aop = result.DataSets.GetDataSetByName('Arg of Perigee').GetValues()
        trueAnomaly = result.DataSets.GetDataSetByName('True Anomaly').GetValues()
        
        arr = [time,sma,ecc,inc,raan,aop,trueAnomaly]
        
        return arr

#%% Setter Functions
        
    def SetTimePeriod(self, elapseTime):
        
        """
        
        Sets the time period of the scenario/
        
        Parameters:
            elapseTime (str): Time for scenario to run in the form "+24hr".
            
        """
        
        self.scenario.SetTimePeriod('Today',str(elapseTime))
        
#%% Getter Functions 
        
    def GetRoot(self):
        
        """
        
        Returns the root of the application.
        
        Returns:
            self.root: Root of the application.
            
        """
        
        return self.root
    
    def GetScenario(self):
        
        """
        
        Returns the scenario of the application.
        
        Returns:
            self.root: The scenario of the application.
            
        """
        
        return self.scenario
    
    def GetAreaTargets(self):
        
        """
        
        Returns the list of all area targets in the scenario.
        
        Returns:
            self.areaTargetList: List of area targets.
            
        """
        
        return self.areaTargetList
    
    def GetSatellites(self):
        
        """
        
        Returns the list of all satellites in the scenario.
        
        Returns:
            self.satelliteList: List of satellites.
            
        """
        
        return self.satelliteList
    
    def GetCameras(self):
        
        """
        
        Returns the list of all cameras in the scenario
        
        Returns:
            self.cameraList: List of all cameras
            
        """
        
        return self.cameraList

#%% STK Functions
        
    def CloseScenario(self):
        
        """
        
        Closes the current scenario.
        
        """
        
        self.root.CloseScenario()
    
    def SaveScenario(self):
        
        """
        
        INCOMPLETE
        
        """
        
        ##TODO Add code to save scenario when AGI Interface is back online.
        return 0
    
    def CloseApplication(self):
        
        """
        
        Close STK
        
        """
        
        self.uiApplication.Quit()
    
    

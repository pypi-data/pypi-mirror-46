"""

Used  to manage and handle TLE files for the purpose of using them in STK.

"""

import os

__author__ = "W. Conor McFerren"
__maintainer__ = "W. Conor McFerren"
__email__ = "cnmcferren@gmail.com"


class TLE_Manager:
    
    """
    
    Class containing only static methods for processing TLE files.
    
    """
    
    @staticmethod
    def ParseTLE(filename):
    
        """
        
        Parses a TLE file of the given file name.
        
        Parameters:
            filename (str): Name of the TLE file.
            
        """
    
        #Create array for return value
        outputArray = []
    
        #Open TLE file
        tle = open(filename,'r')
    
        #Saves first and second lines to variables
        firstLine = tle.readline()
        secondLine = tle.readline()
    
        #Adds line to output array
        outputArray.append(firstLine)
        outputArray.append(secondLine)
    
        #Close tle file
        tle.close()
    
        return outputArray

    @staticmethod
    def GenerateTLE(application, sscNumber):
    
        """
    
        TESTING REQUIRED

        Retrieves TLE file for a satellite with a given SSC Number

        Parameters:
            application (uiApplication): Application object that holds the scenario.
            sscNumber (str || int): SSC Number of the satellite to retrieve TLE file from.
    
        """
        
        sscNumber = str(sscNumber)
        application.GetRoot().ExecuteCommand("CreateTLEFile * AGIServer " +
                os.getcwd() + "\\" + sscNumber + ".tle" + 
                " SSCNumber " + sscNumber)

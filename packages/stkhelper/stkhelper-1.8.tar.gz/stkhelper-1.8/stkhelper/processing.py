"""

Exists for the purpose of processing data from STK applications and holds 
miscellaneous methods to support in STK computation and testing.

Contains only static methods.

"""

__author__ = "W. Conor McFerren"
__maintainer__ = "W. Conor McFerren"
__email__ = "cnmcferren@gmail.com"

class Processing:
    
    """
    
    Class containing only static methods for processing and testing.
    
    """
    
    @staticmethod
    def ArrayToFile(array, filename):
    
        """
        
        Takes array of computed access intervals and writes them to a .txt file.
        
        Parameters:
            array (list): List of computed access intervals.
            filename (str): Filename for access intervals to be written to.
            
            """
    
        newFile = open(filename,'w')
        for x in range(len(array)):
            newFile.write(array[x][0] + ',' + array[x][1] + '\n')
            newFile.close()
            
    @staticmethod        
    def PrintCameras(cameraArray):
    
        """
    
        Prints camera array from the Application class.
        
        Parameters:
            cameraArray (list): The list of cameras from an Application object.
        
        """
    
        for i in range(len(cameraArray) - 1):
            print("Camera " + str(i))
            print("\tCamera Pointer:\t" + str(cameraArray[i][0]))
            print("\tGeneral Camera Pointer:\t" + str(cameraArray[i][1]) + "\n")
    
    @staticmethod    
    def PrintAreaTargets(atArray):
            
        """
    
        Prints area targets array from the Application class.
    
        Parameters:
            atArray (list): The list of area targets from an Application object.
        
        """
    
        for i in range(len(atArray) - 1):
            print("Area Target " + str(i))
            print("\tArea Target Pointer:\t" + str(atArray[0]))
            print("\tArea Target Name:\t" + str(atArray[1]))
            print("\tArea Target Pattern:\t" + str(atArray[2]))
    
    @staticmethod    
    def PrintSatellites(satArray):
        
        """
        
        Prints satellites array from the Application class.
        
        Parameters:
            satArray (list): The list of satellites from an Application object.
            
        """
            
        for i in range(len(satArray) - 1):
            print("Satellite " + str(i))
            print("\tSatellite Name:\t" + satArray[0])
            print("\tSatellite Pointer:\t"  + satArray[1])

    @staticmethod
    def ComputeCenterTarget(parsedLine):
        
        """
        
        Computes the coordinates for the center of an area target.
        
        Parameters:
            parsedLine (str): Line parsed from target list csv.
            
        Returns:
            midPoint (list): List containing name and coordinates of the middle of the area target.
            
        """
        
        name = parsedLine[0]
        startLat = parsedLine[8]
        startLon = parsedLine[9]
        endLat = parsedLine[10]
        endLon = parsedLine[11]
        
        midLat = (startLat + endLat)/2
        midLon = (startLon + endLon)/2
        
        return [name, (midLat,midLon)]
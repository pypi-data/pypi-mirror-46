"""

Exists for the purpose of processing data from STK applications and holds 
miscellaneous methods to support in STK computation and testing.

Contains only static methods.

"""

__author__ = "W. Conor McFerren"
__maintainer__ = "W. Conor McFerren"
__email__ = "cnmcferren@gmail.com"

import datetime

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
        
        midLat = (float(startLat) + float(endLat))/2.0
        midLon = (float(startLon) + float(endLon))/2.0
        
        return [name, (midLat,midLon)]
    
    @staticmethod
    def GetTimeDelta(timeArray):
        
        """
        
        Computes the time difference between to time instances from STK.
        
        Parameters:
            timeArray (list): A list containting two time instances from STK.
            Each instance is in format: 'DD MM YYYY HH:mm:SS.sss'
            
        Returns:
            deltat (float): Time elapsed in seconds between the two instants.
            
        """
        
        monthDict = {"Jan": 1,
                     "Feb": 2,
                     "Mar": 3,
                     "Apr": 4,
                     "May": 5,
                     "Jun": 6,
                     "Jul": 7,
                     "Aug": 8,
                     "Sep": 9,
                     "Oct": 10,
                     "Nov": 11,
                     "Dec": 12}
        
        time1 = str(timeArray[0])
        
        splitTime1 = time1.split(' ')
        day1 = splitTime1[0]
        month1 = monthDict[splitTime1[1]]
        year1 = splitTime1[2]
        
        clockTime1 = splitTime1[3]
        
        splitClockTime1 = clockTime1.split(':')
        hours1 = splitClockTime1[0]
        minutes1 = splitClockTime1[1]
        seconds1 = splitClockTime1[2].split('.')[0]
        microseconds1 = splitClockTime1[2].split('.')[1]
        
        timeObj1 = datetime.datetime(
                int(year1),
                int(month1),
                int(day1),
                hour=int(hours1),
                minute=int(minutes1),
                second=int(seconds1),
                microsecond=int(microseconds1))
        
        time2 = str(timeArray[1])
        
        splitTime2 = time2.split(' ')
        day2 = splitTime2[0]
        month2 = monthDict[splitTime2[1]]
        year2 = splitTime2[2]
        
        clockTime2 = splitTime2[3]
        
        splitClockTime2 = clockTime2.split(':')
        hours2 = splitClockTime2[0]
        minutes2 = splitClockTime2[1]
        seconds2 = splitClockTime2[2].split('.')[0]
        microseconds2 = splitClockTime2[2].split('.')[1]
        
        timeObj2 = datetime.datetime(
                int(year2),
                int(month2),
                int(day2),
                hour=int(hours2),
                minute=int(minutes2),
                second=int(seconds2),
                microsecond=int(microseconds2))
        
        timeDiff = timeObj2 - timeObj1
        print(timeDiff.days,timeDiff.seconds, timeDiff.microseconds)
        deltat = float(timeDiff.days*86400.0) + \
        float(timeDiff.seconds) + \
        (0.001*float(timeDiff.microseconds))
                    
        return deltat
        
import numpy as np
hour = 11

hours = np.array(range(8,18))
latDegrees = 41.117842
longDegrees = -112.056938
hourAngle = getHourAngle(hour)
timezone = 'USMountain'

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def getDialAngle(hour,latDegrees,longDegrees,timezone):
    def Hour2Angle(hour):
        return(np.radians(15*(hour-12)))
    
    def getLongCorrection(longDegrees,timezone):
        meridians = {'USPacific':-120,'USMountain':-105,'USCentral':-90,
             'USEastern':-75,'Atlantic':-60,'Greenwich':0,
             'MiddleEurope':15,'EasternEurope':30}
        return(np.deg2rad(longDegrees-meridians.get(timezone)))
    
    hourAngle = Hour2Angle(hour)+getLongCorrection(longDegrees,timezone)
    latRad = np.deg2rad(latDegrees)
    dialHour = np.arctan(np.tan(hourAngle)*np.sin(latRad))
    return(np.rad2deg(dialHour))

DialAngles = getDialAngle(hours,latDegrees,longDegrees,timezone)+90

xPoint = np.cos(np.radians(DialAngles))
yPoint = np.sin(np.radians(DialAngles))

def add_zeros_between_elements(arr):
    # Calculate the number of zeros to insert
    num_zeros = len(arr) - 1

    # Create an array of zeros
    zeros_arr = np.zeros(num_zeros)

    # Use numpy insert to add zeros between each element
    result = np.insert(arr, np.arange(1, len(arr)), zeros_arr)

    return result


import matplotlib.pyplot as plt


plt.plot(add_zeros_between_elements(xPoint),add_zeros_between_elements(yPoint))
plt.show()
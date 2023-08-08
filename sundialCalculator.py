import numpy as np
hour = 11

hours = np.array(range(6,20))
latDegrees = 41.117842
longDegrees = -112.056938
timezone = 'USMountain'
gnomonHeight = 10

days = np.append(np.array(range(1,365)),1)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def Hour2Angle(hour):
        return(np.radians(15*(hour-12)))

def getDialAngle(hour,latDegrees,longDegrees,timezone):
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

plt.close()
plt.plot(add_zeros_between_elements(xPoint),add_zeros_between_elements(yPoint))
plt.show()

def get_declination_degrees(day):
    rad = np.sin(np.radians(-23.44))*np.cos(np.radians((360/365.25)*(day+10)+(360/np.pi)*0.0167*np.sin(np.radians((360/365.24)*(day-2)))))
    
    declination_degrees = np.degrees(np.arcsin(rad))
    return(declination_degrees)

def get_solar_altitude(decDegrees,latDegrees,hourDegrees):
        latRad = np.radians(latDegrees)
        decRad = np.radians(decDegrees)
        hourRad = np.radians(hourDegrees)
        
        a = np.sin(latRad)*np.sin(decRad)+np.cos(latRad)*np.cos(decRad)*np.cos(hourRad)
        return(np.arcsin(a))



HourDegree = getDialAngle(12,latDegrees,longDegrees,timezone)
DecDegrees = get_declination_degrees(days)

altitude = get_solar_altitude(DecDegrees,latDegrees,HourDegree)



def getShadowLength(hour,gnomonHeight,day,latDegrees,longDegrees,timezone):
    HourDegree = getDialAngle(hour,latDegrees,longDegrees,timezone)
    DecDegrees = get_declination_degrees(day)
    altitude = get_solar_altitude(DecDegrees,latDegrees,HourDegree)
    shadowLen = gnomonHeight/np.tan(altitude)
    return(shadowLen)

plt.plot(days,getShadowLength(12,gnomonHeight,days,latDegrees,longDegrees,timezone))
plt.show()


def equation_of_time(day):
    B = 360*(day-81)/365
    EoT = 9.87*np.sin(np.radians(2*B))-7.67*np.sin(np.radians(B+78.7))
    return(EoT)

def eot_adjustment_degrees(day):
    eot = equation_of_time(day)
    return(np.degrees(Hour2Angle(eot/60))+180)

plt.plot(days,eot_adjustment_degrees(days))
plt.show()

def get_true_angle(day,hour,latDegrees,longDegrees,timezone):
    longCorrectedAngle = getDialAngle(hour,latDegrees,longDegrees,timezone)
    EoTAdjustment = eot_adjustment_degrees(day)
    
    TrueAngle = longCorrectedAngle+EoTAdjustment
    return(TrueAngle)

TrueAngles = get_true_angle(days,12,latDegrees,longDegrees,timezone)

plt.plot(days,TrueAngles)
plt.show()

def getDial(day,hour,gnomonHeight,latDegrees,longDegrees,timezone):
    r = getShadowLength(hour,gnomonHeight,day,latDegrees,longDegrees,timezone)
    angle = get_true_angle(day,hour,latDegrees,longDegrees,timezone)+90
    
    x = r*np.cos(np.radians(angle))
    y = r*np.sin(np.radians(angle))
    
    dial = {'x': x,'y': y}
    return(dial)
    
plt.close()
for hour in range(8,18):
    dial = getDial(days,hour,gnomonHeight,latDegrees,longDegrees,timezone)
    plt.plot(dial['x'],dial['y'])
plt.show()

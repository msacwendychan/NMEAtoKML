# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 20:39:07 2018

@IFN702 - SBAS Data Converter (NMEA to KML format)
@author: Wai Wing Chan n9781463
@date: 15/04/2018

"""

import os, string, sys

# Use nmeagram.py
import nmeagram

# KML file template
KML_TEMPLATE = \
"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <ScreenOverlay id="Septentrio logo">
      <name>Spetentrio Logo</name>
      <Icon><href>http://www.septentrio.com/gfx/logo180x60_v1.gif</href></Icon>
      <overlayXY x="0.0" y="1.0" xunits="fraction" yunits="fraction"/>
      <screenXY x="0.0" y="1.0" xunits="fraction" yunits="fraction"/>
      <rotation>0.0</rotation>
      <size x="0" y="0" xunits="pixels" yunits="pixels"/>
  </ScreenOverlay>
  <name> NMEA to KML: %s</name>     
  <Placemark>
      <name>Start Point</name>
          <Point>
              <coordinates>%s</coordinates>
              <altitudeMode>relativeToGround</altitudeMode>
          </Point>
  </Placemark>
  <Placemark>    
      <name> %s </name>
          <Style>
              <LineStyle>
                  <color>0xFFFFFFFF</color>
              </LineStyle>
		    </Style>
              <MultiGeometry>
                  <LineString>
                      <coordinates>%s</coordinates>
                      <altitudeMode>relativeToGround</altitudeMode>
                      <tessellate>1</tessellate>
                  </LineString>
              </MultiGeometry>
  </Placemark>
</Document>
</kml>"""

KML_EXT = ".kml"

# Read raw file in, one each time
datafile = open ("D:\IFN702\Data\SBAS_Data.Processing\Trial1\sol\septenrio\SBAS06_NMEA\sept0210.181", "r")

# Gets start point coordinate 
def getStartPoint(datafile):
    
    startPoint = []
    firstLine = datafile.readline()
    nmeagram.parseLine(firstLine)
    startPoint.append(str(nmeagram.getField("Longitude")))
    startPoint.append(",")
    startPoint.append(str(nmeagram.getField("Latitude")))
    
    return string.join (startPoint)

'''
def getEndPoint(datafile):
    
    endPoint = []
    finalLine = datafile.readlines()[-1]
    nmeagram.parseLine(finalLine)
    endPoint.append(str(nmeagram.getField("Longitude")))
    endPoint.append(",")
    endPoint.append(str(nmeagram.getField("Latitude")))
    
    return string.join (endPoint)
'''

# Gets the rest of the coordinates (within 8500 volumn)
def getCoordFirstHalf(datafile):
    
    coordData = []
    firstCoordData = []
    
    #Reads a NMEA file by lines and returns lat and long coordinates
    for line in datafile:      
        if line [:6] in ("$GPGGA"):
            nmeagram.parseLine(line)
            coordData.append(str(nmeagram.getField("Longitude")))
            coordData.append(',')
            coordData.append(str(nmeagram.getField("Latitude")))
            coordData.append(' ') 
            ''.join(coordData)
    
    # half = len(coordData)/2       
    firstCoordData = coordData[:8500]
    return ''.join (firstCoordData)

    
    
'''def getCoordSecondHalf(datafile):
    #Read a NMEA file and return lat and long coordinates.
    coordData = []
    secondCoordData = []
    
    for line in datafile:      
        if line [:6] in ("$GPGGA"):
            nmeagram.parseLine(line)
            coordData.append(str(nmeagram.getField("Longitude")))
            coordData.append(',')
            coordData.append(str(nmeagram.getField("Latitude")))
            coordData.append(' ') 
            ''.join(coordData)
            
    #half = len(coordData)/2       
    secondCoordData = coordData[8001:]
    return ''.join (secondCoordData)

'''
   
def main():
    

    if len(sys.argv) == 1:
        fn = ".\SBAS06_sept0210"
        fo = open (fn + KML_EXT, 'w')
        fo.write(KML_TEMPLATE % (fn, getStartPoint(datafile), fn, getCoordFirstHalf(datafile)))
        fo.close()
        

    elif len(sys.argv) == 2:
        fn = sys.argv[1]
        assert os.path.exists(fn)     
        fo = open(fn + KML_EXT, 'w')
        fo.write(KML_TEMPLATE % (fn, getStartPoint(datafile), fn, getCoordFirstHalf(datafile)))
        fn.close() 

    else:
        sys.stderr.write(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
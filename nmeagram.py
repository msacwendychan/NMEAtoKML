# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 19:16:33 2018

"""

#! /usr/bin/env python
"""
This module parses these 6 common NMEA sentence types:
- GPGGA Global positioning system fixed data
- GPGLL Geographic position- latitude/longitude
- GPGSA GNSS DOP and active satellites
- GPGSV GNSS satellites in view
- GPRMC Recommended minimum specific GNSS data
- GPVTG Course over ground and ground speed
"""


import string


# A dictionary container to hold the global parsed data
data = {}


def toDecimalDegrees(ddmm):
    """
    Converts string ddmm.mmmm or dddmm.mmmm format to float dd.dddddd format
    """    
    splitat = string.find(ddmm, '.') - 2
    return toFloat(ddmm[:splitat]) + toFloat(ddmm[splitat:]) / 60.0
    

def toFloat(s):
    """
    Returns the float value of string s (satellite used value) if it exists, or else displys empty string
    """
    if s:
        return float(s)
    else:
        return None


def toInt(s):
    """
    Returns the int value of string s if it exists, or None if s is an empty string.
    """
    if s:
        return int(s)
    else:
        return None


def calcCheckSum(line):
    """
    Returns the checksum as an integer value. The checksum is the XOR of everything between '$' and '*'.
    """
    s = 0
    for c in line[1:-3]:
        s = s ^ ord(c)
    return s


def parseGGA(fields):
    """
    Parses the GPGGA sentence fields.
    Stores the results in the global data dict.
    """
    
    # GGA has 15 fields
    assert len(fields) == 15
    
    if not fields [2]:
        print 0
    else: 
    # MsgId = fields[0]
        data['UtcTime'] = fields[1]
        data['Latitude'] = toDecimalDegrees(fields[2])
        data['NsIndicator'] = fields[3]
        data['Longitude'] = toDecimalDegrees(fields[4])
        data['EwIndicator'] = fields[5]
        data['PositionFix'] = fields[6]
        data['SatellitesUsed'] = toInt(fields[7])
        data['HorizontalDilutionOfPrecision'] = toFloat(fields[8])
        data['MslAltitude'] = toFloat(fields[9])
        data['MslAltitudeUnits'] = fields[10]
        data['GeoidSeparation'] = toFloat(fields[11])
        data['GeoidSeparationUnits'] = fields[12]
        data['AgeOfDiffCorr'] = toFloat(fields[13])
        data['DiffRefStationId'] = fields[14]

    # Attend to lat/lon plus/minus signs
    if data['NsIndicator'] == 'S':
        data['Latitude'] *= -1.0
    if data['EwIndicator'] == 'W':
        data['Longitude'] *= -1.0


def parseGLL(fields):
    """
    Parses the GPGLL sentence fields.
    Stores the results in the global data dict.
    """

    # GLL has 8 fields
    assert len(fields) == 7

    # MsgId = fields[0]
    data['Latitude'] = toDecimalDegrees(fields[1])
    data['NsIndicator'] = fields[2]
    data['Longitude'] = toDecimalDegrees(fields[3])
    data['EwIndicator'] = fields[4]
    data['UtcTime'] = fields[5]
    data['GllStatus'] = fields[6]

    # Attend to lat/lon plus/minus signs
    if data['NsIndicator'] == 'S':
        data['Latitude'] *= -1.0
    if data['EwIndicator'] == 'W':
        data['Longitude'] *= -1.0


def parseGSA(fields):
    """
    Parses the GPGSA sentence fields.
    Stores the results in the global data dict.
    """

    # GSA has 18 fields
    assert len(fields) == 18

    # MsgId = fields[0]
    data['Mode1'] = fields[1]
    data['Mode2'] = toInt(fields[2])
    data['SatCh1'] = toInt(fields[3])
    data['SatCh2'] = toInt(fields[4])
    data['SatCh3'] = toInt(fields[5])
    data['SatCh4'] = toInt(fields[6])
    data['SatCh5'] = toInt(fields[7])
    data['SatCh6'] = toInt(fields[8])
    data['SatCh7'] = toInt(fields[9])
    data['SatCh8'] = toInt(fields[10])
    data['SatCh9'] = toInt(fields[11])
    data['SatCh10'] = toInt(fields[12])
    data['SatCh11'] = toInt(fields[13])
    data['SatCh12'] = toInt(fields[14])
    data['PDOP'] = toFloat(fields[15])
    data['HDOP'] = toFloat(fields[16])
    data['VDOP'] = toFloat(fields[17])


def parseGSV(fields):
    """
    Parses the GPGSV sentence fields.
    Stores the results in the global data dict.
    """

    # GSV has a variable number of fields
    numfields = len(fields)
    assert numfields in (8, 12, 16, 20)

    # MsgId = fields[0]
    data['NumMsgs'] = toInt(fields[1])
    data['MsgNum'] = toInt(fields[2])
    data['SatsInView'] = fields[3]

    # Create struct (only needed first time this is called)
    if 'SatelliteId' not in data.keys():
        data['SatelliteId'] = {}
        data['Elevation'] = {}
        data['Azimuth'] = {}
        data['Snr'] = {}

    # Calculate index offset
    n = 4 * (int(fields[2]) - 1)

    data['SatelliteId'][n] = toInt(fields[4])
    data['Elevation'][n] = toInt(fields[5])
    data['Azimuth'][n] = toInt(fields[6])
    data['Snr'][n] = toInt(fields[7])

    if numfields >= 12:
        nn = n + 1
        data['SatelliteId'][nn] = toInt(fields[8])
        data['Elevation'][nn] = toInt(fields[9])
        data['Azimuth'][nn] = toInt(fields[10])
        data['Snr'][nn] = toInt(fields[11])

    if numfields >= 16:
        nn = n + 2
        data['SatelliteId'][nn] = toInt(fields[12])
        data['Elevation'][nn] = toInt(fields[13])
        data['Azimuth'][nn] = toInt(fields[14])
        data['Snr'][nn] = toInt(fields[15])

    if numfields == 20:
        nn = n + 3
        data['SatelliteId'][nn] = toInt(fields[16])
        data['Elevation'][nn] = toInt(fields[17])
        data['Azimuth'][nn] = toInt(fields[18])
        data['Snr'][nn] = toInt(fields[19])

    # If this is the last GSV sentence in this series,
    # erase old fields when fewer satellites are received than last series
    if fields[1] == fields[2]:
        while nn < len(data['SatelliteId']):
            del data['SatelliteId'][nn]
            del data['Elevation'][nn]
            del data['Azimuth'][nn]
            del data['Snr'][nn]
            nn += 1


def parseRMC(fields):
    """
    Parses the GPRMC sentence fields.
    Stores the results in the global data dict.

    """

    # RMC has 13 fields
    assert len(fields) == 13

    # MsgId = fields[0]
    data['UtcTime'] = fields[1]
    data['RmcStatus'] = fields[2]
    data['Latitude'] = toDecimalDegrees(fields[3])
    data['NsIndicator'] = fields[4]
    data['Longitude'] = toDecimalDegrees(fields[5])
    data['EwIndicator'] = fields[6]
    data['SpeedOverGround'] = toFloat(fields[7])
    data['CourseOverGround'] = toFloat(fields[8])
    data['Date'] = fields[9]
    data['MagneticVariation'] = fields[10]
    data['UnknownEmptyField'] = fields[11]
    data['RmcMode'] = fields[12]

    # Attend to lat/lon plus/minus signs
    if data['NsIndicator'] == 'S':
        data['Latitude'] *= -1.0
    if data['EwIndicator'] == 'W':
        data['Longitude'] *= -1.0


def parseVTG(fields):
    """
    Parses the GPVTG sentence fields.
    Stores the results in the global data dict.
    """

    # VTG has 10 fields
    assert len(fields) == 10

    # MsgId = fields[0]
    data['Course0'] = toFloat(fields[1])
    data['Reference0'] = fields[2]
    data['Course1'] = toFloat(fields[3])
    data['Reference1'] = fields[4]
    data['Speed0'] = toFloat(fields[5])
    data['Units0'] = fields[6]
    data['Speed1'] = toFloat(fields[7])
    data['Units1'] = fields[8]
    data['VtgMode'] = fields[9]


def parseLine(line):
    """
    Parses an NMEA sentence, sets fields in the global structure.
    Raises an AssertionError if the checksum does not validate.
    Returns the type of sentence and assigns the dedicated parsing function.
    """

    # Strips \r\n if there is any
    line = line.rstrip()

    # Asserts the validation of the sentence, at least 16 fields
    assert calcCheckSum(line) == int(line[-2:], 16)

    # Assigns the corresponding functions to the sentence read in 
    # by checking the string header 
    parseFunc = {
        "$GPGGA": parseGGA,
        "$GPGLL": parseGLL,
        "$GPGSA": parseGSA,
        "$GPGSV": parseGSV,
        "$GPRMC": parseRMC,
        "$GPVTG": parseVTG,
        }[line[:6]]

    # Gets rid of the unecessary tails and splits fields by comma
    parseFunc(line[:-3].split(','))
    
    # Returns the type of sentence
    return line[3:6]


def getField(fieldname):
    """
    Returns field name
    """
    return data[fieldname]
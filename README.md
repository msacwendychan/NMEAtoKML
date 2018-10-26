# SBAS GPS to KML

This development project aimed to contribute to the collaborative project of Queensland University of Technology (QUT), Geoscience Australia and Wenco International Mining System for testing the new generation Satellite-based Augmentation System (SBAS) in Australia. The SBAS devices (Septentrio receivers) were attached on two haul trucks in a mine site for 15 days to track the vehicles’ movements. A large dataset containing over 70,000 data points in raw GPS data format was involved in this project. By developing a GPS data extraction, processing and visualization tool, this project aids the performance evaluation of the SBAS solutions.  Python 2.7 and Keyhole Markup Language 2.2 are adopted to build the tool and Google Map is used to display the geographical data. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Users are recommended to have Python 2.7 or above / Spyder 3, Google Earth Pro (desktop) and Notepad++ installed as these are the development tools used. 

## Built With

* [Python 2.7](https://www.python.org/) - Used to create the program
* [Anaconda2 (64 bits)](https://www.anaconda.com/) - Distribution of Python and Spyder 
* [Notepad++](https://notepad-plus-plus.org/download/v7.5.8.html) - Used to read raw GPS data in NMEA format
* [Google Earth Pro](https://www.google.com/earth/download/gep/agree.html) - Used to visualize the final data tracks

## Features

* GPS data parser (nmeagram.py) – reads and parses raw GPS data (NMEA sentences)
* NMEA to KML converter (GPStoKML.py) – converts NMEA sentences or other formats of GPS data to KML format 
* KML data visualization (the output .kml files) – displays the data in tracks on Google Map Pro desktop.

## Screenshot
This is how the numerous data points displayed on Google Earth Pro, showing the operation route of one of the trucks in a period. 
![](https://github.com/msacwendychan/NMEAtoKML/blob/master/Visualize%20on%20Google%20Map_SBAS06_sept0310.jpg)

## Contributing

Pull requests and improvement are welcome. :) Please make sure to include commit comments for each change made. 

## Credits

Dr. Charles Wang – my academic supervisor from QUT

## Acknowledgments

The design of the NMEA parser was inspired by Dean Hall (2007).


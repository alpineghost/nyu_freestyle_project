

import json
import urllib
from urllib.request import urlopen
import os
import sys

import pandas as pd


#Set variables
#MTAkey = sys.argv[1]
#busLine = sys.argv[2]
MTAkey = 'bbecb0d4-3937-4fd7-a4bd-4892b317c4f3'
busLine = 'B63'

url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=%s&VehicleMonitoringDetailLevel=calls&LineRef=%s"%(MTAkey,busLine)

response = urlopen(url)
data = response.read().decode("utf-8")

dataDict = json.loads(data)

vehicleInformation = dataDict['Siri']['ServiceDelivery']['VehicleMonitoringDelivery']
numberOfBuses = len(vehicleInformation[0]['VehicleActivity'])

columns = ['Latitude','Longitude','Stop Name','Stop Status']

df = pd.DataFrame(columns=columns)

for i in range (0,numberOfBuses):

    df.loc[i,'Latitude'] = \
    vehicleInformation[0]['VehicleActivity'][i]['MonitoredVehicleJourney']['VehicleLocation']['Latitude']

    df.loc[i,'Longitude'] = \
    vehicleInformation[0]['VehicleActivity'][i]['MonitoredVehicleJourney']['VehicleLocation']['Longitude']

    onwardCallsDict = vehicleInformation[0]['VehicleActivity'][i]['MonitoredVehicleJourney']['OnwardCalls']

    if (onwardCallsDict != {}):

        df.loc[i,'Stop Name'] =vehicleInformation[0]['VehicleActivity'][i]['MonitoredVehicleJourney']\
        ['OnwardCalls']['OnwardCall'][0]['StopPointName']

        df.loc[i,'Stop Status'] =vehicleInformation[0]['VehicleActivity'][i]['MonitoredVehicleJourney']\
        ['OnwardCalls']['OnwardCall'][0]['Extensions']['Distances']['PresentableDistance']

    else:

        df.loc[i, 'Stop Name'] = 'N/A'
        df.loc[i, 'Stop Status'] = 'N/A'

print (df)

#if not len(sys.argv) == 4:
#    print("Invalid number of arguments. Run as: python aPythonScriptThatWritesToCSV.py mycvs.csv")
#    sys.exit()

#df.to_csv(sys.argv[3], index=False)

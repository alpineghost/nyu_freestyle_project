

import json
import urllib
from urllib.request import urlopen

import pandas as pd

menu = """

    Welcome to the MTA bus app.

    This app will provide you the location of all buses on the line.

    You will need an API key from the MTA.

    Please enter your API key.

    """

MTAkey = input(menu)

busLine = input("Please select a bus line: ")

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

print (df[['Stop Name','Stop Status']])

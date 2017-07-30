
import json
import urllib2
import sys


#Set variables
MTAkey = sys.argv[1]
busLine = sys.argv[2]

url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=%s&VehicleMonitoringDetailLevel=calls&LineRef=%s"%(MTAkey,busLine)

response = urllib2.urlopen(url)
data = response.read().decode("utf-8")

dataDict = json.loads(data)

vehicleInformation = dataDict['Siri']['ServiceDelivery']['VehicleMonitoringDelivery']
numberOfBuses = len(vehicleInformation[0]['VehicleActivity'])

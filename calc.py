from api import *
import sys
import re

stations = [103052, 102082, 105082, 200004, 200005, 200003, 200002, 200001, 104082, 101021, 101042, 101054, 101077, 101008, 200205, 200206, 200209, 200210, 123082];


def getCrimeData(stationID):
	smart = api("pdx")
	stationX = 0;
	stationY = 0;
	stationLocationString = "";
	stationList = smart.data("Powell Travel Time Stations", {"limit": 10})
	for i in xrange(0, len(stationList)):
		if stationList[i]["stationid"] == stationID:
			stationLocationString = stationList[i]["latlon"]
	stationLocationArray = stationLocationString.split(",")
	stationX = float(re.sub("\(|\)","",stationLocationArray[0]))
	stationY = float(re.sub("\(|\)","",stationLocationArray[1]))

	results = []
	initial = smart.data("PDX Crime Data 2013", {"limit": 1000000})
	print stationX
	print stationY
	for i in xrange(0, len(initial)):
		#print stationX - 0.015, " ", stationX + 0.015 ," ", initial[i]["X Coordinate"]
		if initial[i]["X Coordinate"] >= stationX - 0.015 and initial[i]["X Coordinate"] <= stationX + 0.015 and \
		   initial[i]["Y Coordinate"] >= stationY - 0.02  and initial[i]["Y Coordinate"] <= stationY + 0.02:
			results.append(initial[i])
	count = 0;
	morningV = 0;
	morningNV = 0;
	afternoonV = 0;
	afternoonNV = 0;
	nightV = 0;
	nightNV = 0;
	for i in xrange(0, len(results)):
		#if results[i]["X Coordinate"] <= 42.996 and results[i]["X Coordinate"] >= 42.796 and results[i]["Y Coordinate"] >= -122.236 and results[i]["Y Coordinate"] <= -122.036:
		count += 1;
		if "Assault" in results[i]["Major Offense Type"] or \
			"Homicide" in results[i]["Major Offense Type"] or \
			"Rape" in results[i]["Major Offense Type"] or \
			"Kidnap" in results[i]["Major Offense Type"] or \
			"Robbery" in results[i]["Major Offense Type"] or \
			"Arson" in results[i]["Major Offense Type"]:
			if int(results[i]["Report Time"][:2]) < 8 or int(results[i]["Report Time"][:2]) >= 19:
				nightV += 1
			if int(results[i]["Report Time"][:2]) <= 12 and int(results[i]["Report Time"][:2]) >= 8:
				morningV += 1;
			if int(results[i]["Report Time"][:2]) < 19 and int(results[i]["Report Time"][:2]) > 12:
				afternoonV += 1;
		else:
			if int(results[i]["Report Time"][:2]) < 8 or int(results[i]["Report Time"][:2]) >= 19:
				nightNV += 1
			if int(results[i]["Report Time"][:2]) <= 12 and int(results[i]["Report Time"][:2]) >= 8:
				morningNV += 1;
			if int(results[i]["Report Time"][:2]) < 19 and int(results[i]["Report Time"][:2]) > 12:
				afternoonNV += 1;
		#print results[i]["Report Time"]
	print "total:    ", count
	print "           V - NV"
	print "morning:  ", morningV, " ", morningNV
	print "afternoon:", afternoonV, " ", afternoonNV
	print "night:    ", nightV, " ", nightNV
	result = [morningV, morningNV, afternoonV, afternoonNV, nightV, nightNV];
	return result;


def crime(location, time):
	stationID = stations[int(location) % 19];
	results = getCrimeData(stationID);
	return {
		"morning" : {
			"violent": results[0],
			"nonviolent": results[1]
			},
		"afternoon" : {
			"violent" : results[2],
			"nonviolent" : results[3]
			},
		"night": {
			"violent" : results[4],
			"nonviolent" : results[5]
			}
		} #score

def stations():
	smart = api("pdx")
	stationList = smart.data("Air Quality", {"limit": 10000})
	for i in xrange(0, len(stationList)):
		if stationList[i]["epa_station_key"] == 410510080:
			print stationList[i]["wind_speed"], " ", stationList[i]["_updated_at"]


def main():
	crime(1, 0)

if __name__ == '__main__':
	main()
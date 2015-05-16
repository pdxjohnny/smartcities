from api import *
import sys


def getCrimeData():
	smart = api("pdx")
	results = smart.data("PDX Crime Data 2013", {"limit": 100})
	print len(results)
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


def crime(station, time):
	results = getCrimeData();
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

def main():
	getCrimeData();

if __name__ == '__main__':
	main()
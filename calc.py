from api import *
import sys


def getCrimeData():
	smart = api("pdx")
	results = smart.data("PDX Crime Data 2013", {"limit": 100})
	print len(results)
	count = 0;
	morning = 0;
	afternoon = 0;
	night = 0;
	violent = 0;
	for i in xrange(0, len(results)):
		#if results[i]["X Coordinate"] <= 42.996 and results[i]["X Coordinate"] >= 42.796 and results[i]["Y Coordinate"] >= -122.236 and results[i]["Y Coordinate"] <= -122.036:
		count += 1;
		if int(results[i]["Report Time"][:2]) < 8 or int(results[i]["Report Time"][:2]) >= 19:
			night += 1;
		if int(results[i]["Report Time"][:2]) <= 12 and int(results[i]["Report Time"][:2]) >= 8:
			morning += 1;
		if int(results[i]["Report Time"][:2]) < 19 and int(results[i]["Report Time"][:2]) > 12:
			afternoon += 1;
		#print results[i]["Report Time"]
		if "Assault" in results[i]["Major Offense Type"] or \
			"Homicide" in results[i]["Major Offense Type"] or \
			"Rape" in results[i]["Major Offense Type"] or \
			"Kidnap" in results[i]["Major Offense Type"] or \
			"Robbery" in results[i]["Major Offense Type"] or \
			"Arson" in results[i]["Major Offense Type"]:
			violent += 1;
	print "total:", count
	print "morning:", morning
	print "afternoon:", afternoon
	print "night:", night
	print "violent:", violent


def crime(station, time):
	value = 0;
	return {"score":value} #score

def main():
	getCrimeData();

if __name__ == '__main__':
	main()
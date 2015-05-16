from api import *


def main():
    smart = api("pdx")
    results = smart.data("Traffic Travel Time Combined", {"limit": 10})
    for i in xrange(0, len(results)):
        print "traveltime:", results[i]["traveltime"]

if __name__ == '__main__':
    main()


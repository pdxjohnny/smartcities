import urllib2
import urllib
import json

class api(object):
    """docstring for api"""
    def __init__(self, sub_domain="pdx"):
        super(api, self).__init__()
        self.sub_domain = sub_domain
        self.protocol = "http"
        self.domain = "datadash.io"
        self.sub_domain = sub_domain
        self.origin = self.update_origin()
        self.data_ids = self.data_set()

    def data_set(self):
        data = {}
        if self.sub_domain == "pdx":
            data = {
                "DEQ Export": "552d2900d838c1a200fa6925",
                "DEQ Stations": "552d2910d838c1a200fa6927",
                "Daily Averages": "552d29ccd838c1a200fa692b",
                "Average Wind Speed": "552d2a96d838c1a200fa692f",
                "Powell Stations": "552d2b60d838c1a200fa6931",
                "Emissions By Hour": "552d2ff7515c31c300715f13",
                "Emissions By Station": "552d3029515c31c300715f15",
                "Air Quality": "55353d09abadd8b7001497c4",
                "Powell Travel Time Data": "55561bae2d1c07a100b750b6",
                "Powell Travel Time Stations": "55561bc42d1c07a100b750b9",
                "PDX Crime Data 2013": "555620542d1c07a100b750c3",
                "PDX Business Licenses": "555622c42d1c07a100b750c6",
                "DEQ Air Quality Combined": "55561c662d1c07a100b750bc",
                "PDX Parks with Locations": "55561ff92d1c07a100b750c0",
                "Traffic Travel Time Combined": "555769ffaf93c4a200776b09"
            }
        self.data_ids = data
        return data

    def set_domain(self, sub_domain):
        self.sub_domain = sub_domain
        self.update_origin()

    def update_origin(self):
        self.origin = self.protocol + "://" + self.sub_domain + "." + self.domain + "/api/data/"
        return self.origin

    def getJSON(self, url, query={"limit": 100}):
        url_values = urllib.urlencode(query)
        full_url = self.origin + url + '?' + url_values
        response = urllib2.urlopen(full_url)
        headers = response.info()
        page = response.read()
        return json.loads(page)

    def data(self, set_name, query={}):
        url = self.data_ids[set_name]
        return self.getJSON(url, query)

def main():
    smart = api("pdx")
    results = smart.data("Traffic Travel Time Combined", {"limit": 10})
    for data_point in results:
        print "traveltime:", data_point["traveltime"]

if __name__ == '__main__':
    main()


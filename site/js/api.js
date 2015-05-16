var sc_api = function sc_api (sub_domain, js_type)
{
    this.protocol = "http";
    this.domain = "datadash.io";
    // Defualt sub_domain is pdx
    if ( typeof sub_domain === "undefined" )
    {
        sub_domain = "pdx";
    }
    this.sub_domain = sub_domain;
    this.origin = this.update_origin();
    if ( typeof js_type === "undefined" )
    {
        js_type = "normal";
    }
    if ( js_type === "normal" )
    {
        this._get = this._normal_get;
    }
    else
    {
        this.url = require('url');
        this.http = require('http');
        this._get = this._node_get;
    }
    this.data_ids = this.data_set();
}

sc_api.prototype.data_set = function()
{
    var set = {};
    if ( this.sub_domain === "pdx" )
    {
        set = {
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
        };
    }
    this.data_ids = set;
    return set;
}

sc_api.prototype.set_domain = function(sub_domain)
{
    this.sub_domain = sub_domain;
    this.update_origin();
}

sc_api.prototype.update_origin = function()
{
    this.origin = this.protocol + "://" + this.sub_domain + "." + this.domain + "/api/data/";
    return this.origin;
}

sc_api.prototype._node_get = function(url, callback)
{
    parsed_url = this.url.parse(url);
    return this.http.get({
        host: parsed_url.host,
        path: parsed_url.path
    }, function(response) {
        // Continuously update stream with data
        var body = '';
        response.on('data', function(d) {
            body += d;
        });
        response.on('end', function() {
            callback(body);
        });
    });
}

sc_api.prototype._normal_get = function(url, callback)
{
    // So jquery doesn't have to be included
    // http://stackoverflow.com/questions/8567114/how-to-make-an-ajax-call-without-jquery
    var xmlhttp;
    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    }
    else
    {
        // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function()
    {
        if ( xmlhttp.readyState == XMLHttpRequest.DONE )
        {
            if ( xmlhttp.status == 200 )
            {
                callback( xmlhttp.responseText );
            }
            else if ( xmlhttp.status == 400 )
            {
                console.log('AJAX ERROR: There was an error 400')
            }
            else
            {
                console.log('AJAX ERROR: something else other than 200 was returned')
            }
        }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

sc_api.prototype.get = function(url, callback)
{
    var get_callback = function (data)
    {
        callback( data );
    }
    this._get(this.origin + url, get_callback);
}

sc_api.prototype.getJSON = function(url, callback)
{
    var json_callback = function (un_parsed)
    {
        callback( JSON.parse( un_parsed ) );
    }
    this.get(url, json_callback);
}

sc_api.prototype.raw_data = function(set_name, callback, query)
{
    var url = this.data_ids[set_name] + this.get_query_string(query);
    this.getJSON(url, callback);
}

sc_api.prototype.data = function(score, time, station, callback)
{
    var query = {
        "score": score,
        "time": time,
        "station": station
    };
    var url = "/api/" + this.get_query_string(query);
    var json_callback = function (un_parsed)
    {
        callback( JSON.parse( un_parsed ) );
    }
    this._get(url, json_callback);
}

sc_api.prototype.get_query_string = function(obj)
{
    var str = "";
    if ( typeof obj !== "undefined" )
    {
        str = "?";
        for (var key in obj) {
            if (str != "?") {
                str += "&";
            }
            str += key + "=" + encodeURIComponent(obj[key]);
        }
    }
    return str;
}

// var api = new sc_api("pdx")
// api.raw_data("DEQ Export", function (data) { console.log(data); }, {"limit": 100} );
// api.data("crime", false, false, function (data) { console.log(data); } );


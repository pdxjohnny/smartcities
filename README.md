<h1>GuardJog</h1>
---

Server
---

To install / run server

Make sure you have Python >= 2.7.6
If on windows not "sudo -HE"

Make sure you have pip
download: https://bootstrap.pypa.io/get-pip.py
run: sudo -HE python /path/to/get-pip.py

Make sure you have tornado: sudo -HE pip install tornado

Run the server: sudo python server.py --port 80

Go to localhost to access the webserver

JS API
---

Include the api.js file
```html
<script src="js/api.js"></script>
```
Create the api object
```javascript
var api = new sc_api("pdx");
```
Get data from the master server.

```javascript
api.raw_data(dataset name, callback function which with be passed the object, query params as object );
api.raw_data("DEQ Export", function (data) { console.log(data); }, {"limit": 100} );
```
Get processed data from our server.

```javascript
api.data(score type: (crime air, park), time: (morning, afternoon, ngiht), station id, callback function which with be passed the object );
api.data("crime", false, false, function (data) { console.log(data); } );
```

The result from our server will look like:

```json
{
    "OK": true,
    "morning": {
        "nonviolent": 18,
        "violent": 0
        },
    "afternoon": {
        "nonviolent": 31,
        "violent": 3
    },
    "night": {
        "nonviolent": 42,
        "violent": 6
    }
}
```

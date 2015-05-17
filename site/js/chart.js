// Dear Google, please load the chart package.
google.load('visualization', '1', {packages: ['corechart', 'bar']});


// Once the chart package has successfully been loaded, dear page, please
// draw a chart based on the crime report scores.
google.setOnLoadCallback(drawTrendLines);

function drawTrendLines() {

    var r = new sc_api("pdx");

    // Ask the server for the crime report.
    var obj = r.data("crime", false, false, function (data) {    
        console.log(data);              

        // Make a chart.
        var data = new google.visualization.arrayToDataTable([
            ['Crime Type', 'Non-Violent','Violent', { role: 'annotation' }],
            ['Morning', data.morning.nonviolent, data.morning.violent, ''],
            ['Afternoon', data.afternoon.nonviolent, data.afternoon.violent, ''],
            ['Night', data.night.nonviolent, data.night.violent, '']
          ]);

          var options = {
            legend: { position: 'top', maxLines: 2 },
            bar: { groupwidth: '75%' },  
            isStacked: true
          };

          var chart = new google.visualization.ColumnChart(document.getElementById('chart'));
        
          // Draw the chart created above with the simple options.
          chart.draw(data, options);
    });
}
    
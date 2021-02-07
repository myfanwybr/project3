d3.json("/api/visualize").then(function(data) {
    
    var data = data;
    start_hour = [];
    count_hour = [];

    Object.entries(data).forEach(([key, value]) => {
        console.log(key, value);
        count_hour.push(value.hourly_trip_count);
        start_hour.push(value.start_hour);
    });

    console.log(start_hour);
    console.log(count_hour);

    var dataX = [{
        x: start_hour,
        y: count_hour,
        text: start_hour,
        mode: "markers",
        marker: {
            color: count_hour,
            size: count_hour,
            colorscale: "Jet"
        }
    }];

    var layout1 = {
        xaxis: {title: "Time of Day"},
        hovermode: "closest",
        showlegend: false
    };

    Plotly.newPlot("bubble-time", dataX, layout1);

});



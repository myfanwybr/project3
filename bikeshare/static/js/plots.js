d3.json("/api/visualize").then(function(data) {
    
    var data = data;
    start_hour = [];
    count_hour = [];
    sizes = []

    Object.entries(data).forEach(([key, value]) => {
        console.log(key, value);
        count_hour.push(value.hourly_trip_count);
        start_hour.push(value.start_hour);
        sizes.push(value.hourly_trip_count * 0.1)
    });

    console.log(start_hour);
    console.log(count_hour);

    var dataX = [{
        x: start_hour,
        y: count_hour,
        text: start_hour.map(String),
        mode: 'markers',
        marker: {
            color: count_hour,
            colorscale: "Jet"
        },
        type: 'bar'
    }];

    var layout1 = {
        title: {
            text: 'Popular Time of Day'
        },
        xaxis: {title: "Time of Day",
            tickmode: 'array',
            tickvals: [0, 3, 6, 9, 12, 15, 18, 21],
            ticktext: ['12mn', '3am', '6am', '9am', '12nn', '3pm', '6pm', '9pm']
        },
        yaxis: {title: "Number of Trips"},
        hovermode: "closest",
        showlegend: false
    };

    Plotly.newPlot("bubble-time", dataX, layout1, {responsive: true});

});



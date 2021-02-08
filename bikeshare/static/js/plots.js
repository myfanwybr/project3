
// busiest time of day
var url_time = "/api/visualize/time";
var url_hw = "/api/visualize/weather";
d3.json(url_time).then(function(data) {
    
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
            text: 'Busiest Time of Day'
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

// weather and trip count
d3.json(url_hw).then(function(weather) {
    console.log(weather);
    var startDates = [];
    var trip_count = [];
    var sizes = [];
    var texts = [];
    var maxtemp = [];

    Object.entries(weather).forEach(([key, value]) => {
        console.log(value.maxTempC);
        maxtemp.push(value.maxTempC);
        // sizes.push(value.trips * 0.1);
        sizes.push(value.maxTempC + 10);
        texts.push("High: " + value.maxTempC.toString() + " C");
        var d = new Date(value.startDate).toLocaleDateString();
        startDates.push(d);
        trip_count.push(value.trips);
        console.log(value.trips);

    });

    console.log(startDates);
    console.log(sizes);
    console.log(trip_count);
    
    var trace1 = {
        x: startDates,
        y: maxtemp,
        mode: 'markers',
        type: 'scatter',
        text: texts,
        marker: {
            size: sizes,
            color: sizes,
            colorscale: "Jet"
        },
        type: 'scatter'
    };

    var data_hw = [trace1];

    var layout_hw = {
        title: 'Temperature and Trips',
        xaxis: {
            autotick: false,
            ticks: 'outside',
            tickmode: "auto",
            nticks: 10,
            rangemode: "normal"
        },
        showlegend: false
    };     
    Plotly.newPlot("bar-weather", data_hw, layout_hw, {responsive: true});    
});

// popular destination
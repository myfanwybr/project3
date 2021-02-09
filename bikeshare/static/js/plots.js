

initPage();
function initPage() {
    var startDate = '20190101'
    var endDate = '20191231'
    buildPlots(startDate, endDate);
};

function handleSubmit() {
    d3.event.preventDefault();

    var startDate = d3.select("#start-date").node().value;
    var endDate = d3.select("#end-date").property("value");

    console.log(startDate);
    console.log(endDate);
        
    buildPlots(startDate, endDate);

};

function buildPlots(startDate, endDate) {

    var url_time = "/api/visualize/time/" + startDate + "/" + endDate;
    var url_hw = "/api/visualize/weather/" + startDate + "/" + endDate;
    var url_stops = "/api/visualize/destinations/" + startDate + "/" + endDate;
    // console.log(url_stops);
    // busiest time of day
    d3.json(url_time).then(function(data) {

        console.log(data);
    
        var data = data;
        start_hour = [];
        count_hour = [];
        sizes = []
    
        Object.entries(data).forEach(([key, value]) => {
            // console.log(key, value);
            count_hour.push(value.hourly_trip_count);
            start_hour.push(value.start_hour);
            sizes.push(value.hourly_trip_count * 0.1)
        });
    
        // console.log(start_hour);
        // console.log(count_hour);
    
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
                text: 'Busiest Time of Day',
                font: {
                    size: 16,
                    color: 'blue'
                }
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
        // console.log(weather);
        var startDates = [];
        var trip_count = [];
        var sizes = [];
        var texts = [];
        var maxtemp = [];
    
        Object.entries(weather).forEach(([key, value]) => {
            // console.log(value.maxTempC);
            maxtemp.push(value.maxTempC);
            // sizes.push(value.trips * 0.1);
            sizes.push(value.maxTempC + 10);
            texts.push("High: " + value.maxTempC.toString() + " C");
            var d = new Date(value.startDate).toLocaleDateString();
            startDates.push(d);
            trip_count.push(value.trips);
            // console.log(value.trips);
    
        });
    
        // console.log(startDates);
        // console.log(sizes);
        // console.log(trip_count);
        
        var trace1 = {
            x: startDates,
            y: trip_count,
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
            title: { 
                text: 'Temperature and Trips',
                font: {
                    size: 16,
                    color : 'blue'
                }
            },
            xaxis: {
                autotick: false,
                ticks: 'outside',
                tickmode: "auto",
                nticks: 12,
                rangemode: "normal"
            },
            showlegend: false
        };     
        Plotly.newPlot("bar-weather", data_hw, layout_hw, {responsive: true});    
    });
    
    // top 5 destination
    d3.json(url_stops).then((stops) => {
        // console.log(stops);
    
        var daysofweek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    
        var dayofweek = [];
    
        var station1 = [];
        var station2 = [];
        var station3 = [];
        var station4 = [];
        var station5 = [];
    
    
        var station_name = [];
    
        var current_stn = 0;
        var current_wk = 1
    
        Object.entries(stops).forEach(([key, value]) => {
            console.log(value.trip_count);
            console.log(value.station_name);
            console.log(value.weekday);
    
            current_stn += 1;
            if (value.weekday != current_wk) {
                current_stn = 1;
                current_wk = value.weekday;
            };
    
            if ( current_stn == 1 ) {
                station1.push(value.trip_count);
            } else if ( current_stn == 2 ) {
                station2.push(value.trip_count);
            } else if ( current_stn == 3 ) {
                station3.push(value.trip_count);
            } else if ( current_stn == 4 ) {
                station4.push(value.trip_count);
            } else if ( current_stn == 5 ) {
                station5.push(value.trip_count);
            };
    
            if (value.weekday == 1) {
                station_name.push(value.station_name);
            }
            
        });
    
    
        var trace1 = {
            x: daysofweek,
            y: station1,
            text: daysofweek,
            name: station_name[0],
            type: "bar"
        };
    
        
        var trace2 = {
            x: daysofweek,
            y: station2,
            text: daysofweek,
            name: station_name[1],
            type: "bar"
        };
    
        var trace3 = {
            x: daysofweek,
            y: station3,
            text: dayofweek,
            name: station_name[2],
            type: "bar"
        };
    
        var trace4 = {
            x: daysofweek,
            y: station4,
            text: dayofweek,
            name: station_name[3],
            type: "bar"
        };
    
        var trace5 = {
            x: daysofweek,
            y: station5,
            text: daysofweek,
            name: station_name[4],
            type: "bar"
        };
    
    
        var traceData = [trace1, trace2, trace3, trace4, trace5];
    
        var layoutXY = {
            title: {
                text: "Top 5 Destinations",
                font: {
                    size: 16,
                    color: 'blue'
                }
            },
            barmode: "group"
        };
    
        Plotly.newPlot("bar-station", traceData, layoutXY, {responsive: true});
    
    });
    
}


d3.select("#filter-button").on("click", handleSubmit);
console.log("this is for the home page");
var startDate = "20190101";
var endDate = "20191231";
var locationID = 1;
var option=d3.select("option")
var select=d3.select("select")


//load button on page load
window.addEventListener("load", buildButton);

//Build drop down of ID's
function buildButton(){
    option.html("")
    d3.json("/api/locations").then(data=>{
        console.log(data)

        Object.entries(data).forEach(function([key, value]){
                var row=select.append("option")
                row.text(value.city)
    })}) };

  
createTopFive(locationID, startDate, endDate );

function createTopFive(locationID, startDate, endDate) {
    // top 5 destination
    var url_stops = "/api/visualize/destinations/" + locationID + "/" + startDate + "/" + endDate;
    console.log(url_stops);
    // console.log(url_stops);    
    
  

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
            // console.log(value.trip_count);
            // console.log(value.station_name);
            // console.log(value.weekday);
    
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
            // text: station1,
            name: station_name[0],
            type: "bar"
        };
    
        
        var trace2 = {
            x: daysofweek,
            y: station2,
            // text: station2,
            name: station_name[1],
            type: "bar"
        };
    
        var trace3 = {
            x: daysofweek,
            y: station3,
            // text: station3,
            name: station_name[2],
            type: "bar"
        };
    
        var trace4 = {
            x: daysofweek,
            y: station4,
            // text: station4,
            name: station_name[3],
            type: "bar"
        };
    
        var trace5 = {
            x: daysofweek,
            y: station5,
            // text: station5,
            name: station_name[4],
            type: "bar"
        };
    
    
        var traceData = [trace1, trace2, trace3, trace4, trace5];
    
        var layoutXY = {
            title: {
                text: "Top 5 Destinations",
                yref: "paper",
                y: 1,
                yanchor: "bottom",
                font: {
                    size: 16,
                    color: 'blue'                    
                }
            },
            barmode: "group",
            legend: {
                x: 0.0,
                y: 1.8
            }
        };
    
        Plotly.newPlot("tor-destinations", traceData, layoutXY, {responsive: true});
    
    });
    
}
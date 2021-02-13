
function get_url() {
    // get value for current city
    var current_url = location.href;
    var locationID = current_url.split('=')[1];
    console.log(location.href);
    console.log(locationID);

    if (typeof locationID !== 'undefined') {
        var url_weather = '/api/weather' + "/" + locationID;
    }
    else {
        var url_weather = '/api/weather';
    }

    return url_weather;
}
var url_weather = get_url();
showData(url_weather);

// select filter button using ID
var filterbutton = d3.select("#filter-btn");

// select dates from form using form ID
var filterdata = d3.select("#form");

// create event handlers
filterbutton.on("click", runSubmit);
filterdata.on("submit", runSubmit);

function runSubmit() {
    var defaultStartDate = '1/1/2019';
    var defaultEndDate = '12/31/2019';
    d3.event.preventDefault();
    // get the value of the input dates
    var startDate = d3.select("#start-date");
    var inputStartDate = startDate.property("value");

    var endDate = d3.select("#end-date");
    var inputEndDate = endDate.property("value");

    if (inputStartDate) {
        console.log("not empty date");
    } else {
        console.log("empty empty");
        inputStartDate = defaultStartDate;
    }

    if (inputEndDate) {
        console.log("not empty date");
    } else {
        console.log("empty empty");
        inputEndDate = defaultEndDate;
    }

    console.log(inputStartDate);
    console.log(inputEndDate);

    var yr1 = inputStartDate.split("/")[2];
    var yr2 = inputEndDate.split("/")[2];

    var startDate = yr1.concat(inputStartDate.split("/")[0], inputStartDate.split("/")[1])
    var endDate = yr2.concat(inputEndDate.split("/")[0], inputEndDate.split("/")[1])

    console.log(startDate);
    console.log(endDate);

    var url_weather = get_url() + "/" + startDate + "/" + endDate;

    console.log(url_weather);

    showData(url_weather);

}

function showData(url_weather) {
    console.log("show Data");

    var tbody = d3.select("tbody");
    tbody.html("");
    
    d3.json(url_weather).then(function(data)
    {
        console.log(data)
        
        data.forEach(function(forecast){
            var row=tbody.append("tr");
            
            //select objects using . Entries
            Object.entries(forecast).forEach(function([key, value]){
                if (key == "forecast_date") {
                    value = new Intl.DateTimeFormat('en-US', {
                        timeZone: 'Australia/Sydney'
                      }).format(value);
                }
                if (key == "location_id") {
                    switch (value) {
                        case 1:
                            value = 'Toronto';
                            break;
                        case 2:
                            value = 'Vancouver';
                            break;
                        case 3:
                            value = 'Boston';
                            break;
                        case 4:
                            value = 'New York City'
                            break;
                        default:
                            value = value;
                    }
                }
                var cell=row.append("td")
                cell.text(value)
            })
        })
    })
    
    var tbody= d3.select("tbody")
    
}


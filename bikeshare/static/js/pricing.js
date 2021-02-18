console.log("for pricing.html");

//location api call
function get_url() {
    // get value for current city
    var current_url = location.href;
    var locationID = current_url.split('=')[1];
    console.log(location.href);
    console.log(locationID);

    if (typeof locationID !== 'undefined') {
        var url_pricing = '/api/pricing' + "/" + locationID;
    }
    else {
        var url_pricing = '/api/pricing';
    }

    return url_pricing;
}

var url_pricing = get_url();

// data from GCP
d3.json(url_pricing).then((data) => {
    console.log(data);
    // build table
    // variable declaration
    var pricetable  = d3.select("#price-index");
    // Clear exiting data
    pricetable.html("");
    // declare heading
    pricetable = pricetable.append("div")
                .attr("class", "card-deck")
                .append("div")
                .attr("class", "col-md-12")
                .append("div")
                .attr("class", "row")

    //loop through for data
    data.forEach((dataRow) => {
                
        var value = "";
        var colmd = "";
        console.log(dataRow.location_id)
        switch (dataRow.location_id) {
            case 1:
                value = 'Toronto';
                colmd = "col-md-3";
                break;
            case 2:
                value = 'Vancouver';
                colmd = "col-md-3";
                break;
            case 3:
                value = 'Boston';
                colmd = "col-md-4";
                break;
            case 4:
                value = 'New York City'
                colmd = "col-md-4";
                break;
            default:
                value = value;
        }

        // append divs
        var cityname = pricetable.append("div")
                        .attr('class', colmd)
                        .append("div")
                        .attr("class","card-header")
                        .append("h3")
                        .text(value);
                        
        var row = cityname.append("div")
                 .attr("class", "card-body")
                 .attr("id", "card-1")
                 .append("h5")
                 .text(dataRow.plan)
                 .append("h3")
                 .text("$"+dataRow.amount);
    })
})

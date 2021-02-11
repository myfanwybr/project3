// get value for current city
var current_url = location.href;
var locationID = current_url.split('=')[1];
console.log(location.href);
console.log(locationID);

if (typeof locationID !== 'undefined') {
    var url_weather = '/api/weather' + "/" + locationID
}
else {
    var url_weather = '/api/weather'
}

console.log(url_weather);

d3.json(url_weather).then(function(data)
{
    
    var data=data
    console.log(data)
    data.forEach(function(aliens){
        var row=tbody.append("tr")
    
        //select objects using . Entries
        Object.entries(aliens).forEach(function([key, value]){
            var cell=row.append("td")
            cell.text(value)
        })
    })
})

var tbody= d3.select("tbody")


// get value for current city
var current_url = location.href;
var locationID = current_url.split('=')[1];
console.log(location.href);
console.log(locationID);

if (typeof locationID !== 'undefined') {
    var url_stations = '/api/stations' + "/" + locationID
    var url_map = '/api/citymap' + "/" + locationID
}
else {
    var url_stations = '/api/stations'
    var url_map = '/api/citymap'
}
    
console.log(url_stations);
console.log(url_map);

d3.json(url_stations).then((data) => {
    console.log(data);
});

d3.json(url_map).then((data) => {
    console.log(data);
});


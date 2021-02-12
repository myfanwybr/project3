// Get value for current city
var current_url = location.href;
var locationID = current_url.split('=')[1];
console.log(location.href);
console.log(locationID);

var center_toronto = [43.645609, -79.380386];
var center_boston = [42.361145, -71.057083];
var center_vancouver = [49.24966 -123.11934];
var center_newyork = [40.730610, -73.935242];
var center_center = [41.4925, -99.9018];

if (locationID === 1) {
  center = center_toronto;
  var zoomx = 12;
} else if (locationID === 2) {
  center = center_vancouver;
  var zoomx = 12;
} else if (locationID === 3) {
  center = center_boston;
  var zoomx = 12;
} else if (locationID === 4) {
    center = center_newyork;
    var zoomx = 12;
} else {
  center = center_center;
  var zoomx = 4;
}

if (typeof locationID !== 'undefined') {
    var url_stations = '/api/stations' + "/" + locationID
    var url_map = '/api/citymap' + "/" + locationID
}
else {
    var url_stations = '/api/stations'
    var url_map = '/api/citymap'
}


d3.json(url_stations).then((data) => {
    
    // Initialize an array to hold bike markers
    var bikeMarkers = [];

    // For each station, create a marker and bind a popup with the station's name
    for(var i =0; i<data.length; i++){

        station_name=data[i].station_name
        lat=data[i].latitude
        long=data[i].longitude

        var bikeMarker = L.marker([lat, long])
        .bindPopup("<h3>" + station_name+ "<h3>");

        // Add the marker to the bikeMarkers array
        bikeMarkers.push(bikeMarker);
    }
    createMap(L.layerGroup(bikeMarkers));
});

  function createMap(bikeStations) {

    // Create the tile layer that will be the background of our map
    var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "light-v10",
      accessToken: API_KEY
    });
  
    // Create a baseMaps object to hold the lightmap layer
    var baseMaps = {
      "Light Map": lightmap
    };
  
    // Create an overlayMaps object to hold the bikeStations layer
    var overlayMaps = {
      "Bike Stations": bikeStations
    };
  
    // Create the map object with options
    var map = L.map("map-id", {
      center: center,
      zoom: zoomx,
      layers: [lightmap, bikeStations]
    });
  
    // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(map);
  }
// Get value for current city
var current_url = location.href;
var locationID = current_url.split('=')[1];

if (typeof locationID !== 'undefined') {
    var url_stations = '/api/stations' + "/" + locationID
    var url_map = '/api/citymap' + "/" + locationID
    console.log(url_stations);
    console.log(url_map);

}
else {
    var url_stations = '/api/stations'
    var url_map = '/api/citymap'
}

console.log(locationID)

//function to populate dropdown with the start station names
function init() {
  var dropdown = d3.select("#selDataset");
  d3.json(url_stations).then((data) => {
    for(var i =0; i<data.length; i++){
      name = data[i].station_name;
      ID = data[i].station_id;
      dropdown.append("option").text(name).property("value", ID);
  }
  var initID = dropdown.property("value");
  console.log(initID);
  CreateMarkers(initID);
})
};


// // function to display data with the selected dropdown menu item
function optionChanged(ID) {
  console.log(ID);
  CreateMarkers(ID);
}

// Function to create markers on a map
function CreateMarkers(ID){
  var a = url_map + "/" + ID;
  console.log(a);

  // Initialize an array to hold bike markers
  var bikeMarkers = [];

  d3.json(a).then((data) => {
    console.log(data);
  
    // For each station, create a marker and bind a popup with the station's name
    for(var i =0; i<data.length; i++){
  
        station_name=data[i].station_name
        people_count = data[i].trips_count
        lat=data[i].latitude
        long=data[i].longitude
  
        var bikeMarker = L.marker([lat, long])
        .bindPopup("<h6> End station: " + station_name + "<h6><hr><h6>Trips in a year: " + people_count + "</h6>");
  
        // Add the marker to the bikeMarkers array
        bikeMarkers.push(bikeMarker);
    }
    createMap(L.layerGroup(bikeMarkers));
  });

}

// Function to create map
function createMap(bikeStations) {

  // Define streetmap and darkmap layers
var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: "pk.eyJ1IjoibWFuaXNoYWxhbCIsImEiOiJja2tlc3Y5eGcwMzV0MnZxZThvb3g3d3MwIn0.DPmfdzNu4SykIHWqzFoYjA"
});

var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "dark-v10",
  accessToken: "pk.eyJ1IjoibWFuaXNoYWxhbCIsImEiOiJja2tlc3Y5eGcwMzV0MnZxZThvb3g3d3MwIn0.DPmfdzNu4SykIHWqzFoYjA"
});

// Define a baseMaps object to hold our base layers
var baseMaps = {
  "Street Map": streetmap,
  "Dark Map": darkmap
};

// Create overlay object to hold our overlay layer
var overlayMaps = {
  "Bike Stations": bikeStations
};

var center_toronto = [43.645609, -79.380386];
var center_boston = [42.361145, -71.057083];
var center_vancouver = [49.24966 -123.11934];
var center_newyork = [40.730610, -73.935242];
var center_center = [54.5260, -99.9018];


if (locationID == 1) {
 var center1 = center_toronto;
 var zoomx = 13;
} else if (locationID == 2) {
 var center1 = center_vancouver;
 var zoomx = 13;
} else if (locationID == 3) {
 var center1 = center_boston;
 var zoomx = 13;
} else if (locationID == 4) {
 var center1 = center_newyork;
 var zoomx = 13;
}
else {
 var center1 = center_center;
 var zoomx = 4;
}

// Before initializing map check for is the map is already initiated or not
var container = L.DomUtil.get('map-id');
if(container != null){
container._leaflet_id = null;
}

// Create our map, giving it the streetmap and bikestation layers to display on load
var myMap = L.map("map-id", {
  center: center1,
  zoom: zoomx,
  layers: [streetmap, bikeStations]
});

// Create a layer control
// Pass in our baseMaps and overlayMaps
// Add the layer control to the map
L.control.layers(baseMaps, overlayMaps, {
  collapsed: false
}).addTo(myMap);
}

init();

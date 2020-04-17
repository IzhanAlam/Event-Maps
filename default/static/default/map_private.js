
//get geojson data from link
function get_data_from_url(url){
    var http_req = new XMLHttpRequest();
    http_req.open("GET",url,false);
    http_req.send(null);
    return http_req.responseText;          
}

mapboxgl.accessToken = 'pk.eyJ1IjoiaXpoYW5hbGFtIiwiYSI6ImNrN2s2ZDFiaTAzbzgzZG11MG1xMHdlZzEifQ.uBG-TBw1B2h81lSwJcLPvg';
var map = new mapboxgl.Map({
  container: 'map', 
  style: 'mapbox://styles/izhanalam/ck846sjfv199t1io8gd7v2h9u', 
  center: [-114.0719,51.0447],
  zoom: 10
});

var marker = new mapboxgl.Marker({
    draggable: true
})
.setLngLat([-114.0719,51.0447])
.addTo(map);

var lati;
var longi;

function onDragEnd() {
    var lngLat = marker.getLngLat();
    coordinates.style.display = 'block';
    coordinates.innerHTML =
    'Longitude: ' + lngLat.lng + '<br />Latitude: ' + lngLat.lat;
    document.getElementById("lat").value=lngLat.lat;
    document.getElementById("long").value=lngLat.lng;
    lati = lngLat.lat;
    longi = lngLat.lng;
}
     
marker.on('dragend', onDragEnd);
 

//Geolocation
var position = [];
var geolocate = new mapboxgl.GeolocateControl();

map.addControl(geolocate);

geolocate.on('geolocate', function(e) {
      lon = e.coords.longitude;
      lat = e.coords.latitude
      //document.getElementById("lat").value=lat;
      //document.getElementById("long").value=lon;
      position = [lat, lon];
      console.log(position);
});

var template = document.getElementById('my-element');
var val = (template.innerHTML);

var geojson = 'http://127.0.0.1:8000/geojsondumpsprivate.geojson/' + (val);
console.log(geojson)
var geojson_obj = get_data_from_url(geojson);
var data = JSON.parse((geojson_obj).replace(/&quot;/g,'"'));




//get the icon
icon = document.getElementById("icon")


map.on('load', function() {
    map.addLayer({
      id: 'private',
      type: 'symbol',
      source: {
        type: 'geojson',
        data: data
      },
      layout: {
        'icon-image':  ['get', 'icon'],
        'icon-allow-overlap': true
      },
      paint: { }
    });

  });


var popup = new mapboxgl.Popup();

map.on('mousemove', function(e) {
  var features = map.queryRenderedFeatures(e.point, { layers: ['private'] });
  if (!features.length) {
    popup.remove();
    return;
  }
  var feature = features[0];

  popup.setLngLat(feature.geometry.coordinates)
    //.setHTML(feature.properties.description)
    .setHTML('<h5>'+ feature.properties.description + '</h5>'+ '<br>' + feature.properties.comment)

    .addTo(map);

  map.getCanvas().style.cursor = features.length ? 'pointer' : '';
});


var canvas = map.getCanvasContainer();



var start = [longi, lati];

// create a function to make a directions request
function getRoute(end) {
    // make a directions request using cycling profile
    // an arbitrary start will always be the same
    // only the end or destination will change
    var start = [longi,lati];
    var url = 'https://api.mapbox.com/directions/v5/mapbox/driving/' + start[0] + ',' + start[1] + ';' + end[0] + ',' + end[1] + '?steps=true&geometries=geojson&access_token=' + mapboxgl.accessToken;
    
    // make an XHR request https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
    var req = new XMLHttpRequest();
    req.open('GET', url, true);
    req.onload = function() {
      var json = JSON.parse(req.response);
      var data = json.routes[0];
      var route = data.geometry.coordinates;
      var geojson = {
        type: 'Feature',
        properties: {},
        geometry: {
          type: 'LineString',
          coordinates: route
        }
      };
      // if the route already exists on the map, reset it using setData
      if (map.getSource('route')) {
        map.getSource('route').setData(geojson);
      } else { // otherwise, make a new request
        map.addLayer({
          id: 'route',
          type: 'line',
          source: {
            type: 'geojson',
            data: {
              type: 'Feature',
              properties: {},
              geometry: {
                type: 'LineString',
                coordinates: geojson
              }
            }
          },
          layout: {
            'line-join': 'round',
            'line-cap': 'round'
          },
          paint: {
            'line-color': '#3887be',
            'line-width': 2,
            'line-opacity': 0.75
          }
        });
      }
      // add turn instructions here at the end
      var instructions = document.getElementById('instructions');
      var steps = data.legs[0].steps;
      var tripInstructions = [];
      for (var i = 0; i < steps.length; i++) {
        tripInstructions.push('<br><li>' + steps[i].maneuver.instruction) + '</li>';
        instructions.innerHTML = '<br><span class="duration">Trip duration: ' + Math.floor(data.duration / 60) + ' min 🚗 </span>' + tripInstructions;
    }
    };
    req.send();
  }
  
  map.on('load', function() {
    // make an initial directions request that
    // starts and ends at the same location
    getRoute(start);
  
    // Add starting point to the map
    map.addLayer({
      id: 'point',
      type: 'circle',
      source: {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features: [{
            type: 'Feature',
            properties: {},
            geometry: {
              type: 'Point',
              coordinates: start
            }
          }
          ]
        }
      },
      paint: {
        'circle-radius': 10,
        'circle-opacity':0.5,
        'circle-color': '#3887be'
      }
    });

    map.on('click', function(e) {
        var coordsObj = e.lngLat;
        canvas.style.cursor = '';
        var coords = Object.keys(coordsObj).map(function(key) {
          return coordsObj[key];
        });
        var end = {
          type: 'FeatureCollection',
          features: [{
            type: 'Feature',
            properties: {},
            geometry: {
              type: 'Point',
              coordinates: coords
            }
          }
          ]
        };
        if (map.getLayer('end')) {
          map.getSource('end').setData(end);
        } else {
          map.addLayer({
            id: 'end',
            type: 'circle',
            source: {
              type: 'geojson',
              data: {
                type: 'FeatureCollection',
                features: [{
                  type: 'Feature',
                  properties: {},
                  geometry: {
                    type: 'Point',
                    coordinates: coords
                  }
                }]
              }
            },
            paint: {
              'circle-radius': 3,
             
              'circle-color': '#f30'
            }
          });
        }
        getRoute(coords);
      });
  });
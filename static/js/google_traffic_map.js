var map;
var trafficLayer;
var startMarker = null;
var endMarker = null;
var geocoder;

function initMap() {
  // Initialize the map with options
  var mapOptions = {
    // center: { lat: 51.50596083481134, lng: -0.10428420421818965 }, // London-UK
    center: { lat: 15.34060867334686, lng: 44.197572107055755 },
    zoom: 12,
    styles: [
      {
        featureType: "all",
        elementType: "all",
        stylers: [
          { invert_lightness: true },
          { saturation: -100 },
          { lightness: 0 },
          { visibility: "on" },
        ],
      },
    ],
  };

  // Create the map instance
  map = new google.maps.Map(document.getElementById("map"), mapOptions);

  // Initialize the geocoder
  geocoder = new google.maps.Geocoder();

  // Add the traffic layer to the map
  trafficLayer = new google.maps.TrafficLayer();
  trafficLayer.setMap(map);

  // Load existing marker positions if available
  var startLatLng = getLatLngFromField("id_traffic_start_point");
  var endLatLng = getLatLngFromField("id_traffic_end_point");

  function getLatLngFromField(fieldId) {
    var fieldValue = document.getElementById(fieldId).value;
    if (fieldValue) {
      var latLngArray = fieldValue.split(",");
      return new google.maps.LatLng(
        parseFloat(latLngArray[0]),
        parseFloat(latLngArray[1])
      );
    }
    return null;
  }

  if (startLatLng) {
    startMarker = new google.maps.Marker({
      position: startLatLng,
      map: map,
      label: "S",
      draggable: true,
    });
    map.setCenter(startLatLng);
    startMarker.addListener("dragend", function (e) {
      updateAddressField(e.latLng, "start");
    });
  }

  if (endLatLng) {
    endMarker = new google.maps.Marker({
      position: endLatLng,
      map: map,
      label: "E",
      draggable: true,
    });
    if (!startLatLng) {
      map.setCenter(endLatLng);
    }
    endMarker.addListener("dragend", function (e) {
      updateAddressField(e.latLng, "end");
    });
  }

  // Add a click event listener to place start and end markers
  map.addListener("click", function (event) {
    if (!startMarker) {
      // Create the start marker if it doesn't exist
      startMarker = new google.maps.Marker({
        position: event.latLng,
        map: map,
        label: "S", // Label for Start
        draggable: true,
      });
      updateAddressField(event.latLng, "start");
      startMarker.addListener("dragend", function (e) {
        updateAddressField(e.latLng, "start");
      });
    } else if (!endMarker) {
      // Create the end marker if it doesn't exist
      endMarker = new google.maps.Marker({
        position: event.latLng,
        map: map,
        label: "E", // Label for End
        draggable: true,
      });
      updateAddressField(event.latLng, "end");
      endMarker.addListener("dragend", function (e) {
        updateAddressField(e.latLng, "end");
      });
    }
  });

  directionsService = new google.maps.DirectionsService();
  directionsDisplay = new google.maps.DirectionsRenderer();
  directionsDisplay.setMap(map);
  directionsDisplay.setOptions({
    polylineOptions: {
      strokeColor: 'red'
    }
  });

  var searchButton = document.getElementById("search-button");
  if (searchButton) {
    searchButton.addEventListener("click", function () {
      var searchInput = document.getElementById("search-input").value.trim();
      if (searchInput) {
        performSearch(searchInput);
      }
    });
  }

  var directionsForm = document.getElementById("directions-form");
  if (directionsForm) {
    directionsForm.addEventListener("submit", getDirections);
  }

  var toggleButton = document.getElementById("toggle-button");
  if (toggleButton) {
    toggleButton.addEventListener("click", toggleRoute);
  }
}

function updateAddressField(latLng, type) {
  geocoder.geocode({ location: latLng }, function (results, status) {
    if (status === google.maps.GeocoderStatus.OK && results.length > 0) {
      var address = results[0].formatted_address;
      if (type === "start") {
        document.getElementById("id_address").value = address;
        document.getElementById("id_traffic_start_point").value =
          latLng.lat() + "," + latLng.lng();
      } else if (type === "end") {
        document.getElementById("id_end_address").value = address;
        document.getElementById("id_traffic_end_point").value =
          latLng.lat() + "," + latLng.lng();
      }
    } else {
      console.log("Geocoder failed due to: " + status);
    }
  });
}

function performSearch(query) {
  var geocoder = new google.maps.Geocoder();
  geocoder.geocode({ address: query }, function (results, status) {
    if (status === google.maps.GeocoderStatus.OK && results.length > 0) {
      var location = results[0].geometry.location;
      map.setCenter(location);
      new google.maps.Marker({
        map: map,
        position: location,
      });
    } else {
      console.log("No results found for the search query.");
    }
  });
}

function getDirections(event) {
  event.preventDefault();
  var originInput = document.getElementById("origin-input").value;
  var destinationInput = document.getElementById("destination-input").value;
  var request = {
    origin: originInput,
    destination: destinationInput,
    travelMode: google.maps.TravelMode.DRIVING,
  };
  directionsService.route(request, function (result, status) {
    if (status === google.maps.DirectionsStatus.OK) {
      currentRoute = result;
      directionsDisplay.setDirections(result);
      var directionsResultDiv = document.getElementById("directions-result");
      directionsResultDiv.innerHTML = "";
      var directionsResultText = document.createElement("div");
      directionsResultText.innerHTML = "<strong>Directions:</strong>";
      directionsResultDiv.appendChild(directionsResultText);
      var steps = result.routes[0].legs[0].steps;
      for (var i = 0; i < steps.length; i++) {
        var stepText = document.createElement("div");
        stepText.innerHTML =
          "<div style='font-size: 0.9em'>" + steps[i].instructions + "</div>";
        directionsResultDiv.appendChild(stepText);
      }
      directionsDisplay.setMap(map);
    } else {
      console.log("Error occurred while retrieving directions:", status);
    }
  });
}

function toggleRoute() {
  if (directionsDisplay) {
    if (directionsDisplay.getMap()) {
      directionsDisplay.setMap(null);
    } else {
      directionsDisplay.setMap(map);
    }
  }
}

window.onload = initMap;

// var map;
// var directionsService;
// var directionsDisplay;
// var currentRoute;
// var trafficLayer;

// function initMap() {
//     var mapOptions = {
//         // center: { lat: 15.34060867334686, lng: 44.197572107055755 }, sana'a
//         center: { lat: 51.50596083481134, lng: -0.10428420421818965 },  // london-UK
//         // center: {  lat: 53.34582214814564, lng: -6.249488115485492 },  // Dublin-Ireland
//         zoom: 12,
//         styles: [
//             {
//                 featureType: "all",
//                 elementType: "all",
//                 stylers: [
//                     { invert_lightness: true },
//                     { saturation: -100 },
//                     { lightness: 0 },
//                     { visibility: "on" },
//                 ],
//             },
//         ],
//     };
//     map = new google.maps.Map(document.getElementById("map"), mapOptions);

//     var legendContainer = document.getElementById("legend");
//     if (legendContainer) {
//         map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(legendContainer);
//     }

//     trafficLayer = new google.maps.TrafficLayer();
//     trafficLayer.setMap(map);

//     directionsService = new google.maps.DirectionsService();
//     directionsDisplay = new google.maps.DirectionsRenderer();
//     directionsDisplay.setMap(map);

//     var searchButton = document.getElementById("search-button");
//     if (searchButton) {
//         searchButton.addEventListener("click", function() {
//             var searchInput = document.getElementById("search-input").value.trim();
//             if (searchInput) {
//                 performSearch(searchInput);
//             }
//         });
//     }

//     var directionsForm = document.getElementById("directions-form");
//     if (directionsForm) {
//         directionsForm.addEventListener("submit", getDirections);
//     }

//     var toggleButton = document.getElementById("toggle-button");
//     if (toggleButton) {
//         toggleButton.addEventListener("click", toggleRoute);
//     }
// }

// function performSearch(query) {
//     var geocoder = new google.maps.Geocoder();
//     geocoder.geocode({ address: query }, function(results, status) {
//         if (status === google.maps.GeocoderStatus.OK && results.length > 0) {
//             var location = results[0].geometry.location;
//             map.setCenter(location);
//             new google.maps.Marker({
//                 map: map,
//                 position: location,
//             });
//         } else {
//             console.log("No results found for the search query.");
//         }
//     });
// }

// function getDirections(event) {
//     event.preventDefault();
//     var originInput = document.getElementById("origin-input").value;
//     var destinationInput = document.getElementById("destination-input").value;
//     var request = {
//         origin: originInput,
//         destination: destinationInput,
//         travelMode: google.maps.TravelMode.DRIVING,
//     };
//     directionsService.route(request, function(result, status) {
//         if (status === google.maps.DirectionsStatus.OK) {
//             currentRoute = result;
//             directionsDisplay.setDirections(result);
//             var directionsResultDiv = document.getElementById("directions-result");
//             directionsResultDiv.innerHTML = "";
//             var directionsResultText = document.createElement("div");
//             directionsResultText.innerHTML = "<strong>Directions:</strong>";
//             directionsResultDiv.appendChild(directionsResultText);
//             var steps = result.routes[0].legs[0].steps;
//             for (var i = 0; i < steps.length; i++) {
//                 var stepText = document.createElement("div");
//                 stepText.innerHTML =
//                     "<div style='font-size: 0.9em'>" + steps[i].instructions + "</div>";
//                 directionsResultDiv.appendChild(stepText);
//             }
//             directionsDisplay.setMap(map);
//         } else {
//             console.log("Error occurred while retrieving directions:", status);
//         }
//     });
// }

// function toggleRoute() {
//     if (directionsDisplay) {
//         if (directionsDisplay.getMap()) {
//             directionsDisplay.setMap(null);
//         } else {
//             directionsDisplay.setMap(map);
//         }
//     }
// }

// window.onload = initMap;

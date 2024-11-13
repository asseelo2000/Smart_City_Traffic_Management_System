var map;
var directionsService;
var directionsDisplay;
var currentRoute;
var trafficLayer;
//var routeVisible = false;

function initMap() {
  var mapOptions = {
    center: { lat: 30.267153, lng: -97.743057 },
    zoom: 12,
    styles: [
      // Custom map styles here
      // Example:
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
  map = new google.maps.Map(document.getElementById("map"), mapOptions);

  var legendContainer = document.getElementById("legend");
  map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(legendContainer);

  trafficLayer = new google.maps.TrafficLayer();
  trafficLayer.setMap(map);

  directionsService = new google.maps.DirectionsService();
  directionsDisplay = new google.maps.DirectionsRenderer();
  directionsDisplay.setMap(map);

  var searchForm = document.getElementById("search-form");
  searchForm.addEventListener("submit", performSearch);

  var directionsForm = document.getElementById("directions-form");
  directionsForm.addEventListener("submit", getDirections);

  var toggleButton = document.getElementById("toggle-button");
  toggleButton.addEventListener("click", toggleRoute);

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
        // Show the route by default
        directionsDisplay.setMap(map);
        routeVisible = true;
      } else {
        console.log("Error occurred while retrieving directions:", status);
      }
    });
  }

  function toggleRoute() {
    if (directionsDisplay) {
      if (directionsDisplay.getMap()) {
        directionsDisplay.setMap(null); // Hide the route on the map
      } else {
        directionsDisplay.setMap(map); // Show the route on the map
      }
    }
  }
}

function performSearch(event) {
  event.preventDefault();
  var searchInput = document.getElementById("search-input").value;
  var geocoder = new google.maps.Geocoder();
  geocoder.geocode({ address: searchInput }, function (results, status) {
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

// Initialize the map on page load
window.onload = initMap;

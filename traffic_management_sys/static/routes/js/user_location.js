document.addEventListener('DOMContentLoaded', function() {
    // Get the city, start_address, and start_location fields
    const cityField = document.getElementById('id_city');
    const startAddressField = document.getElementById('id_start_address');
    const startLocationField = document.getElementById('id_start_location');

    // Get the end_address and end_location fields
    const endAddressField = document.getElementById('id_end_address');
    const endLocationField = document.getElementById('id_end_location');

    // Initialize the Google Maps Geocoder
    const geocoder = new google.maps.Geocoder();

    // Function to update the map for a given location field
    function updateMap(locationField) {
        const mapContainer = locationField.closest('map-widget'); // Locate the map container
        if (mapContainer) {
            const iframe = mapContainer.querySelector('iframe'); // Find the map iframe
            if (iframe) {
                // Refresh the iframe by updating its src attribute
                iframe.src = iframe.src;
            }
        }
    }

    // Function to update start_location with geocoded coordinates and refresh the map
    function updateStartLocation() {
        if (cityField && startAddressField && startLocationField) {
            const fullStartAddress = `${startAddressField.value}, ${cityField.value}`;
            geocoder.geocode({ address: fullStartAddress }, function(results, status) {
                if (status === 'OK' && results[0]) {
                    const location = results[0].geometry.location;
                    startLocationField.value = `${location.lat()}, ${location.lng()}`;
                    updateMap(startLocationField); // Refresh the map in real time
                } else {
                    console.error('Geocoding error: ' + status);
                }
            });
        }
    }

    // Function to update end_location with geocoded coordinates and refresh the map
    function updateEndLocation() {
        if (cityField && endAddressField && endLocationField) {
            const fullEndAddress = `${endAddressField.value}, ${cityField.value}`;
            geocoder.geocode({ address: fullEndAddress }, function(results, status) {
                if (status === 'OK' && results[0]) {
                    const location = results[0].geometry.location;
                    endLocationField.value = `${location.lat()}, ${location.lng()}`;
                    updateMap(endLocationField); // Refresh the map in real time
                } else {
                    console.error('Geocoding error: ' + status);
                }
            });
        }
    }

    // Add event listeners to update the fields when input changes
    if (cityField && startAddressField) {
        cityField.addEventListener('input', updateStartLocation);
        startAddressField.addEventListener('input', updateStartLocation);
    }

    if (cityField && endAddressField) {
        cityField.addEventListener('input', updateEndLocation);
        endAddressField.addEventListener('input', updateEndLocation);
    }
});

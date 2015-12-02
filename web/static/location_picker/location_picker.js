$(document).unload(function(){
    google.maps.Unload();
});

$(document).ready(function(){
    $("input.location_picker").each(function (i) {
        var me = $(this),
            wrap = $('<div>').insertBefore(me).addClass('location-picker-wrap'),
            mapDiv = $('<div>').appendTo(wrap).addClass('location-picker-map');
        
        me.prependTo(wrap);
        
        var lat = -43.531065;
        var lng = 172.636671;
        if (me.val().split(/,\s*/).length == 2) {
            values = this.value.split(',');
            lat = values[0];
            lng = values[1];
        }
        var center = new google.maps.LatLng(lat, lng);

        var input = document.getElementById('id_location');
        var autocomplete = new google.maps.places.Autocomplete(input);

        autocomplete.addListener('place_changed', function() {
            var place = autocomplete.getPlace();
            if (!place.geometry) {
              window.alert("Autocomplete's returned place contains no geometry");
              return;
            }

            // If the place has a geometry, then present it on a map.
            if (place.geometry.viewport) {
              map.fitBounds(place.geometry.viewport);
            } else {
              map.setCenter(place.geometry.location);
              map.setZoom(17);  // Why 17? Because it looks good.
            }
            // marker.setIcon(/** @type {google.maps.Icon} */({
            //   url: place.icon,
            //   size: new google.maps.Size(71, 71),
            //   origin: new google.maps.Point(0, 0),
            //   anchor: new google.maps.Point(17, 34),
            //   scaledSize: new google.maps.Size(35, 35)
            // }));
            marker.setPosition(place.geometry.location);
            marker.setVisible(true);
            me.val(place.geometry.location.lat() + ", " + place.geometry.location.lng())
        });

        var map = new google.maps.Map(mapDiv[0], {
            zoom: 15,
            center: center,
            search: true,
            // scaleControl: false,
            // navigationControl: false,
            // navigationControlOptions: {
            //     position: google.maps.ControlPosition.RIGHT
            // },
            disableDefaultUI: false,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var marker = new google.maps.Marker({
            position: center,
            map: map
        });

        google.maps.event.addListener(map, 'click', function (e) {
            me.val(e.latLng.lat() + ',' + e.latLng.lng());
            marker.setPosition(e.latLng);
        });
        function update() {
            var bits = $(this).val().split(/,\s*/),
                latLng = new google.maps.LatLng(parseFloat(bits[0]), parseFloat(bits[1]));
            marker.setPosition(latLng);
            map.setCenter(latLng);
        }
        me.change(update);
        me.keyup(update);
    });
});



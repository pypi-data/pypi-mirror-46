/*
 * Leaflet plugin to create map icons using Maki Icons from MapBox.
 *
 * References:
 *   Maki Icons: https://www.mapbox.com/maki/
 *   Mapbox Marker API: https://www.mapbox.com/api-documentation/#retrieve-a-standalone-marker
 *   Possible icon names: https://raw.githubusercontent.com/mapbox/maki/master/layouts/all.json
 *
 * Usage:
 *   L.MakiMarkers.accessToken = '<YOUR_ACCESS_TOKEN>';
 *   var icon = L.MakiMarkers.icon({icon: 'rocket', color: '#b0b', size: 'm'});
 *
 * License:
 *   MIT: http://jseppi.mit-license.org/
 */

L.MakiMarkers = {
    apiUrl: '/',
    defaultColor: '#0a0',
    defaultIcon: 'circle-stroked',
    defaultSize: 's',
    smallOptions: {
        iconSize: [23, 35],
        popupAnchor: [0, -20]
    },
    largeOptions: {
        iconSize: [27, 41],
        popupAnchor: [0, -35]
    }
};

L.MakiMarkers.Icon = L.Icon.extend({
    options: {
        // Maki icon: any valid name, see https://raw.githubusercontent.com/mapbox/maki/master/layouts/all.json
        icon: L.MakiMarkers.defaultIcon,
        // Marker color: short or long form hex color code
        color: L.MakiMarkers.defaultColor,
        // Marker size: 's' (small), or 'l' (large)
        size: L.MakiMarkers.defaultSize,
        shadowAnchor: null,
        shadowSize: null,
        shadowUrl: null,
        className: 'maki-marker'
    },

    initialize: function(options) {
        options = L.setOptions(this, options);

        var sizeOptions = {
            's': L.MakiMarkers.smallOptions,
            'l': L.MakiMarkers.largeOptions
        };
        if (!(options.size in sizeOptions)) {
            options.size = 's';
        }
        L.extend(options, sizeOptions[options.size]);

        var pin = 'pin-' + options.size;

        if (options.icon !== null) {
            pin += '-' + options.icon;
        }

        if (options.color !== null) {
            if (options.color.charAt(0) === '#') {
                options.color = options.color.substr(1);
            }

            pin += '+' + options.color;
        }

        options.iconUrl = '/maki' + L.MakiMarkers.apiUrl + pin + '.png';
    }
});

function maki(options) {
    return new L.MakiMarkers.Icon(options);
}
L.MakiMarkers.icon = maki;

export {maki};

/*
 * Small round marker containing a number.
 */

import L from 'leaflet';
import './leaflet-number-marker.css';

var NumberIcon = L.NumberIcon = L.DivIcon.extend({
    options: {
        html: '',
        shadowUrl: null,
        iconSize: new L.Point(20, 20),

        className: 'leaflet-number-marker'
    }
});

var numberIcon = L.numberIcon = function (number) {
    var options = (typeof(number) == 'object') ? number : {html: number};
    return new L.NumberIcon(options);
};

var numberMarker = L.numberMarker = function (latlng, number) {
    return L.marker(latlng, {
        icon: L.numberIcon(number)
    });
};

export {NumberIcon, numberIcon, numberMarker};

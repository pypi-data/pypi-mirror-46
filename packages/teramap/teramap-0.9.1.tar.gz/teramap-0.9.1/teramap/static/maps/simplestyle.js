// https://github.com/mapbox/mapbox.js/blob/mb-pages/src/simplestyle.js
// BSD
'use strict';

// an implementation of the simplestyle spec for polygon and linestring features
// https://github.com/mapbox/simplestyle-spec
var defaults = {
    stroke: '#555555',
    'stroke-width': 2,
    'stroke-opacity': 1,
    fill: '#555555',
    'fill-opacity': 0.5,

    // non-standard styles
    'stroke-style': null
};

var mapping = [
    ['stroke', 'color'],
    ['stroke-width', 'weight'],
    ['stroke-opacity', 'opacity'],
    ['fill', 'fillColor'],
    ['fill-opacity', 'fillOpacity'],

    // non-standard styles
    ['stroke-style', 'dashArray'],
];

function fallback(a, b) {
    var c = {};
    for (var k in b) {
        c[k] = (a[k] === undefined) ? b[k] : a[k];
    }
    return c;
}

function remap(a) {
    var d = {};
    for (var i = 0; i < mapping.length; i++) {
        d[mapping[i][1]] = a[mapping[i][0]];
    }
    return d;
}

function style(feature) {
    return remap(fallback(feature.properties || {}, defaults));
}

export {style, defaults};

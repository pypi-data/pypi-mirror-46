import L from 'leaflet';

// we assume the resulting teramap.js is consumed using the bundle
// with leaflet loaded externally.
// can be replaced with externals options if this is merged:
// https://github.com/webpack-contrib/css-loader/pull/496
// import 'leaflet/dist/leaflet.css';

// make sure Leaflet's images work properly:
// delete L.Icon.Default.prototype._getIconUrl;
// L.Icon.Default.mergeOptions({
//     iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
//     iconUrl: require('leaflet/dist/images/marker-icon.png'),
//     shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
// });


import 'leaflet-fullscreen';
import 'leaflet-fullscreen/dist/leaflet.fullscreen.css';

import 'leaflet-control-geocoder';
import 'leaflet-control-geocoder/Control.Geocoder.css';

import preventAccidentalScroll from '../lib/leaflet-scroll-intent.js';

import MiniMap from 'leaflet-minimap';
import 'leaflet-minimap/src/Control.MiniMap.css';

// monkeypatch WKT point utils into Leaflet
if (!L.LatLng.toWKT) {
    L.LatLng.prototype.toWKT = function () {
        return L.Util.template('POINT({lng} {lat})', this);
    };
}
if (!L.Util.parseWKT) {
    L.Util.parseWKT = function (value) {
        if (value.indexOf('POINT') === -1 || value.indexOf('(') === -1) {
            return;
        }

        var start = value.indexOf('(') + 1;
        var coords = value.substr(start, value.indexOf(')') - start).split(' ');

        return L.latLng([parseFloat(coords[1]), parseFloat(coords[0])]);
    };
}

function leaflet_map(map_id, options) {
    options = L.extend({
        center: [51, 4],
        zoom: 6,
        callback: L.Util.falseFn,
        // name -> L.TileLayer mapping of base layers. to add to the layers control.
        baselayers: {
            'map': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                'minZoom': 1,
                'maxZoom': 19,
                'attribution': '&copy; OpenStreetMap',
            })
        },
        // name -> L.TileLayer mapping of overlays to add to the layers control.
        overlays: {},

        // controls/plugins to activate or not:
        preventAccidentalScroll: true,
        scaleControl: false,
        fullscreenControl: true,
        searchControl: false,
        minimap: false,
        // default options for the Layers Control. Set to false to disable layers control.
        layersControlOptions: {
            collapsed: false
        }
    }, options || {});

    // allow passing a single tile layer.
    if (options.baselayers instanceof L.TileLayer) {
        options.baselayers = {
            'default': options.baselayers
        };
    }
    map_id = L.DomUtil.get(map_id);
    L.DomUtil.addClass(map_id, 'teramap');

    var map = L.map(map_id).setView(options.center, options.zoom);
    // attach map container to data attribute of DOM element
    map._container.data = map;

    // By default, we add the first layer in the dict, but if another layer was previously
    // selected and stored in localStorage.
    var initialLayerName = Object.keys(options.baselayers)[0];
    if (localStorage) {
        var BASELAYER_KEY = 'teramap-remember-basemap';
        var layerName = localStorage.getItem(BASELAYER_KEY);
        if (layerName && layerName in options.baselayers) {
            initialLayerName = layerName;
        }
        map.on('baselayerchange', function (e) {
            localStorage.setItem(BASELAYER_KEY, e.name);
        });
    }
    map.addLayer(options.baselayers[initialLayerName]);

    if (options.layersControlOptions && (Object.keys(options.baselayers).length > 1 || Object.keys(options.overlays).length > 0)) {
        map.layersControl = L.control.layers(options.baselayers, options.overlays, options.layersControlOptions).addTo(map);
    }

    if (options.fullscreenControl) {
        map.fullscreenControl = L.control.fullscreen(
            L.extend({postion: 'topleft'}, options.fullscreenControl)
        ).addTo(map);
    }
    if (options.scaleControl) {
        map.scale = L.control.scale(L.extend({imperial: false}, options.scaleControl)).addTo(map);
    }
    if (options.searchControl) {
        new L.Control.Geocoder(options.searchControl).addTo(map);
    }
    if (options.preventAccidentalScroll) {
        preventAccidentalScroll(map);
    }
    if (options.minimap) {
        var controlOptions = L.extend({
            minimapLayer: L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png')
        }, options.minimap);
        new MiniMap(controlOptions['minimapLayer'], controlOptions).addTo(map);
    }

    if (typeof options.callback == 'function') {
        options.callback(map);
    }

    return map;
}

export default leaflet_map;

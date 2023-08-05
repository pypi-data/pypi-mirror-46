import corslite from 'corslite';

import {numberIcon} from '../lib/leaflet-number-marker.js';
import {maki} from './makimarkers.js';
import {style} from './simplestyle.js';

// loosely based on https://github.com/mapbox/mapbox.js/blob/mb-pages/src/feature_layer.js

function createPopup (properties) {
    if ('no-popup' in properties) {
        return;
    }
    // explicit popup_content takes precedence over other values.
    if ('popup-content' in properties) {
        return properties['popup-content'];
    }

    if ('description' in properties) {
        return properties['description'];
    }
}

function request (url, callback) {
    function onload(err, resp) {
        if (!err && resp) {
            resp = JSON.parse(resp.responseText);
        }
        callback(err, resp);
    }

    return corslite(url, onload);
}

var FeatureLayer = L.FeatureGroup.extend({
    options: {
        filter: function() { return true; },
        style: style,
        popupOptions: { closeButton: false },
        pointToLayer: function (feature, latlng) {
            var properties = feature.properties;
            var pointStyle;
            if ('circle-marker' in properties) {
                pointStyle = style(feature);
                pointStyle['radius'] = properties['circle-marker'];

                return L.circleMarker(latlng, pointStyle);
            }
            var marker = L.marker(latlng);
            if ('number-marker' in properties) {
                // TODO: console.error('number-marker: <number> is deprecated, use marker-symbol: <number>');
                // properties['marker-symbol'] = properties['number-marker'];
                marker.setIcon(numberIcon(properties['number-marker']));
                return marker;
            }
            // allow creating L.Circle() instances
            if ('radius' in properties) {
                pointStyle = style(feature);
                pointStyle['radius'] = properties['radius'];
                return L.circle(latlng, pointStyle);
            }

            if (('marker-size' in properties || 'marker-symbol' in properties || 'marker-color' in properties) && marker.setIcon) {
                marker.setIcon(maki({
                    'size': (properties['marker-size'] || 'large').charAt(0),
                    'icon': ('marker-symbol' in properties && properties['marker-symbol'] !== '') ? properties['marker-symbol'] : '',
                    'color': (properties['marker-color'] || '7e7e7e').replace('#', '')
                }));
            }
            return marker;
        }
    },
    initialize: function(_, options) {
        L.setOptions(this, options);
        this._layers = {};

        if (typeof _ === 'string') {
            this.loadURL(_);
        } else if (_ && typeof _ === 'object') { // GeoJSON
            this.setGeoJSON(_);
        }
    },

    setGeoJSON: function(_) {
        this._geojson = _;
        this.clearLayers();
        this._initialize(_);
        return this;
    },

    getGeoJSON: function() {
        return this._geojson;
    },

    loadURL: function(url) {
        if (this._request && 'abort' in this._request) this._request.abort();
        this._request = request(url, L.bind(function(err, json) {
            this._request = null;
            if (err && err.type !== 'abort') {
                // eslint-disable-next-line no-console
                console.error('Could not load features at ' + url);
                this.fire('error', {error: err});
            } else if (json) {
                this.setGeoJSON(json);
                this.fire('ready');
            }
        }, this));
        return this;
    },

    setFilter: function(_) {
        this.options.filter = _;
        if (this._geojson) {
            this.clearLayers();
            this._initialize(this._geojson);
        }
        return this;
    },

    getFilter: function() {
        return this.options.filter;
    },

    _initialize: function(json) {
        var features = L.Util.isArray(json) ? json : json.features,
            i, len;

        if (features) {
            for (i = 0, len = features.length; i < len; i++) {
                // Only add this if geometry or geometries are set and not null
                if (features[i].geometries || features[i].geometry || features[i].features) {
                    this._initialize(features[i]);
                }
            }
        } else if (this.options.filter(json)) {
            var layer = L.GeoJSON.geometryToLayer(json, {
                pointToLayer: this.options.pointToLayer
            });

            var style = this.options.style;
            if (style && 'setStyle' in layer) {
                if (typeof style === 'function') {
                    style = style(json);
                }
                layer.setStyle(style);
            }

            layer.feature = json;

            var popupHtml = createPopup(json.properties);
            if (popupHtml) {
                layer.bindPopup(popupHtml, this.options.popupOptions);
            }
            if ('title' in json.properties && json.properties.title) {
                layer.bindTooltip(json.properties.title);
            }

            this.addLayer(layer);
        }
    }
});

function featureLayer (_, options) {
    return new FeatureLayer(_, options);
}

export {FeatureLayer, featureLayer};

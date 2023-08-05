import L from 'leaflet';
import leaflet_map from './leaflet-map.js';
import {FeatureLayer, featureLayer} from './featurelayer.js';

require('leaflet-legend');
require('leaflet-legend/leaflet-legend.css');

function layer_bounds(layer) {
    if (layer.getBounds) {
        return layer.getBounds();
    } else {
        return L.latLngBounds(layer.getLatLng(), layer.getLatLng());
    }
}

function map_with_geojson(map_id, options) {
    var map = leaflet_map(map_id, options);

    if (options && options.geojson) {
        var layer = featureLayer(options.geojson).addTo(map);
        map.geojson_layer = layer;

        var properties = options.geojson.properties;
        if (properties && properties.legend) {
            L.control.legend({
                position: 'bottomright',
                buttonHtml: properties['legend-title'] || 'legend',
                items: properties.legend
            }).addTo(map);
        }
        map.zoomExtent = function () {
            var bounds = layer.getBounds();
            if (bounds.isValid()) {
                map.fitBounds(bounds, {maxZoom: 16});
            }
        };
        map.zoomExtent();

        map.focusOnFeature = function (key, value) {
            // focus on the feature or the features which have key=value in their properties.
            var bounds;
            layer.eachLayer(function (layer) {
                var properties = layer.feature.properties;
                if (key in properties && properties[key] == value) {
                    if (bounds) {
                        bounds.extend(layer_bounds(layer));
                    } else {
                        bounds = layer_bounds(layer);
                    }
                }
            });
            map.fitBounds(bounds, {maxZoom: 16});
        };

    }

    map.reload = function () {
        map.invalidateSize();

        if (map.geojson_layer) {
            map.zoomExtent();
        }
    };

    map.reload();
    return map;
}

export {FeatureLayer, featureLayer, map_with_geojson};

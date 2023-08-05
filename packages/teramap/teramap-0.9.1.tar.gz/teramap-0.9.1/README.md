# Teramap

Shared mapping functionality for Zostera projects.

The basic idea is to define as much properties of the geometries in the [GeoJSON] string. The JavaScript code used to render the json on a [Leaflet] map can then be fairly standard throughout the projects and applications.

**Installation**

As Teramap lives in a private bitbucket repository, but is published on pypi:
```
pip install teramap==0.4.11
```

Make sure to always pin to a specific version (by appending a tag name (i.e. `teramap==0.4.11`), as this is not yet crystallized and development will introduce breaking changes.

Add `teramap` to `INSTALLED_APPS` in `settings.py`

**API**

- python object `teramap.GeoJSON`
- python mixin `teramap.TransformToPoint`
- python view `teramap.GeoJSONView`
- python function `teramap.formatters.format_point(p, srs)`
- JavaScript `teramap(id, options)`
- JavaScript `teramap.fieldwork.Pinpoint(data)`
- JavaScript `teramap.fieldwork.PinpointRenderer(pinpoint)`

## python object `teramap.GeoJSON`

Wrapper for objects with geometries providing conversion to a [GeoJSON] string.

Geometries will will be [simplified](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/geos/#django.contrib.gis.geos.GEOSGeometry.simplify) to the value specified in `GEOJSON_DEFAULT_SIMPLIFY`, which defaults to `25 / 115000`.

Instances of `teramap.GeoJSON` can be added together to merge them.
This allows one to pass one `geojson` context variable to the template.
The type of features doesn't matter.
```python
geojson = LocationGeoJSON(Location.objects.all())
geojson += RegionGeoJSON(Region.objects.all())
```

### attribute `collection_properties`

Allows the definition of additional features such as legends, via:
```python
collection_properties = {'legend':
  [{'color': 'red', 'label': 'active'}, {...}]
}
```

### attribute `properties`
Defines the contents of each feature in the generated GeoJSON, as key-value pairs.
Values can be:

- **bool**: Will include the value `key: value` in the properties.
- **callable**: Will include the value `key: value(item)` in the properties. The `item` argument will be the model for the current feature.
- **str**: Accessor, dotted path, allows following foreign key relations.
   Example: `user.first_name` will look for the attribute `user` on the model and return the value of it's `first_name` attribute.
    Default value: `{'id': 'pk'}` will include the primary key.

If there is a need to call a function to define a property, one can redefine properties as follows:
```python
    @property
    def properties(self):
        return {
            'id': 'id',
            'project_id': 'project_id',
            'location_id': 'location_id',
            'url': lambda obj: attr_or_key(obj, 'get_absolute_url') or None,
            'name': 'location.name',
            'fill': self.get_color,
            'stroke': self.get_color,
            'popup-content': self.get_popup_content
        }
```

Calling the function as:
```python
    def get_popup_content(self, obj):
        """
        Generates HTML to be attached to this feature as a popup.
        """
        html = 'some html content'
        return html
```

If inheriting a self defined GeoJSON class, and there is a need to add or change properties,
do so as follows:
```python
    @property
    def properties(self):
        props = super(ProjectLocationsGeoJSON, self).properties
        props.update({
            'user': lambda obj: attr_or_key(obj, 'user_id') or 0,
            'fill-opacity': lambda obj: 0.25,
            'marker-color': self.get_color,
            'is_active': lambda obj: attr_or_key(obj, 'is_active') or False,
        })
        return props
```
One can redefine called functions by over-riding them in the daughter class.

## maki-markers
teramap supports maki-markers and requires the following:
* `cairo` needs to be installed system wide (Note this requires
UTF-8 locale to be recognized)
* make sure teramap comes with `python-makiwich==0.0.07`
* to `app/urls.py` add `from maki.contrib.django import maki_icon` and
`path("maki/<str:name>", maki_icon, name="maki_icon"))`
* in geojson properties use `marker-symbol: lambda obj: attr_or_key(obs, 'marker')`,
`marker-size` and `marker-color`

### attribute `geom_field`

Name of the geometry field, defaults to `geom`.

### attribute `precision`

Number of digits to round the coordinates too.

### attribute `simplify`

Tolerance for geometry simplification, defaults to GEOJSON_DEFAULT_SIMPLIFY

### attribute `url_name`

When a url to the object is required in properties, you can use the `url` method to generate it.
```python
class GeoJSON(teramap.GeoJSON):
    properties = {'url': self.url}
    url_name = 'location_detail'
```
will result in a call to `django.urls.reverse(url_name, kwargs={'pk': obj.pk})`.


### method `to_geojson_str(indent=None)`

Returns a string representation of the [GeoJSON] object. Optional `indent` argument allows formatting the output to be more readable (passed on to [json.dump()](https://docs.python.org/2/library/json.html#json.dump)).

### Example

This example will add both the model fields `id` and `name` to the `properties` map of the generated geojson.
```python
class GeoJSON(teramap.GeoJSON):
    properties = {
        'id': 'id',
        'title': 'name'
    }

geojson = GeoJSON(Location.objects.all())

>>> # returns a mark_safe()ed string containing the GeoJSON
>>> str(geojson)
'{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [4.0, 52.0]}, "type": "Feature", "properties": {"id": 1, "name": "Point"}}, {"geometry": {"type": "Point", "coordinates": [4.0, 54.0]}, "type": "Feature", "properties": {"id": 2, "name": "Point 2"}}]}'

>>> geojson.to_geojson_str(2)
'{
  "type": "FeatureCollection",
  "features": [{
      "geometry": {
        "type": "Point",
        "coordinates": [4.0, 52.0]
      },
      "type": "Feature",
      "properties": {
        "id": 1,
        "title": "Point 1"
      }
    },
    {
      "geometry": {
        "type": "Point",
        "coordinates": [4.0, 54.0]
      },
      "type": "Feature",
      "properties": {
        "id": 2,
        "title": "Point 2"
      }
    }
  ]
}'
```

## python mixin `teramap.TransformToPoint`

When dealing with large amounts polygons, it often doesn't make sense to display them all as polygons.

```python
class GeoJSON(TransformToPoint, teramap.GeoJSON):
    pass
```

Adding the `TransformToPoint` mixin will collapse all non-point geometries to their centroids.


## python view `teramap.GeoJSONView`

View that enables `django.views.generic.ListView` to emit [GeoJSON].

```python
class View(teramap.GeoJSONView, ListView):
    GeoJSONClass = GeoJSON
    model = Location
```

## JavaScript prerequisites

Before you can use teramap, you have to make sure you include both `teramap.js` and `teramap.css` assets into your template. It is also assumed that leaflet is loaded, make sure that's done before loading teramap:

```HTML
{% load teramap %}
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.1/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.3.1/dist/leaflet.js"></script>

<script src="{% static "teramap/maps.js" %}?version={% teramap_version %}"></script>
<link rel="stylesheet" href="{% static "teramap/maps.css" %}?version={% teramap_version %}"/>

```

## JavaScript `teramap(id, options, geojson)`

Create's a Leaflet map in element with `id` `#<id>` using `options` explained later. If `geojson` is an object, it is assumed to be geojson and added using [L.geoJSON](http://leafletjs.com/reference-1.2.0.html#geojson).

### options for `teramap()`

- `fullscreenControl`: if `true`, a [Leaflet.fullscreen](https://github.com/Leaflet/Leaflet.fullscreen) control is added to the map.
- `preventAccidentalScroll`: if `true`, interacting with the map requires explicit intent first i.e. clicking the map container.
- `callback`: if type is function, it's called after creating the map with the map as argument.
- `baseLayers`: base layer to use for the map, (instance of [L.TileLayer](http://leafletjs.com/reference-1.3.1.html#tilelayer), defaults to openstreetmap, or a mapping of layer names and `L.TileLayer` instances.
- `overlays`: mapping of overlay layer names. If at least one is in the object, a [L.Control.Layers](http://leafletjs.com/reference-1.2.0.html#control-layers) is added with this item as second argument.
- `layersControlOptions`: dictionary of layerControle options, e.g. { collapsed: true }
- `center`: initial map center, defaults to `[51, 4]`
- `zoom`: initial map zoom, defaults to `6`.
- `minimap`: if `true`, shows minimap overview.
- `geojson`: JSON object containing [GeoJSON] object or string containing an url to a GeoJSON endpoint.

Chances are this list is incomplete and/or outdated. Have a look at [the implementation](https://bitbucket.org/zostera/teramap/src/master/teramap/static/maps/leaflet-map.js) to make sure the correct options are used.

## GeoJSON styling in JavaScript

[simplestyle 1.1.0](https://github.com/mapbox/simplestyle-spec/tree/master/1.1.0) is supported, sans the `marker-size` and `marker-icon`.

`marker-color` has a limited set of (named) colors for now: `black, green, grey, orange, red, violet, yellow`.

## JavaScript `teramap.fieldwork.Pinpoint(data)`

## JavaScript `teramap.fieldwork.PinpointRenderer(pinpoint)`

## Other template features

Other functions like `focusOnFeature(key, value)` can be accessed within a template beyond the scope
of the map by simply redefining the function as:
```JavaScript
  window.focusOnFeature = function (key, value) {
    map.focusOnFeature(key, value);
  };
```

Functions include:
- `map.focusOnFeature(key, value)`: searches the feature properties for a feature with a property `key=value`, and zooms to the extend of that feature.
- `map.zoomExtent()`: zooms out to the extent of all features.
- `map.reload()`: call after the size of the map container changed (window resize or modal show), to make sure the map is sized correctly and zoom to the feature extents.


## Development

`webpack` is used to build the bundles in `teramap/static/teramap/`.

You can install it an its dependencies using `npm install`.
- Running `npm run bundle` will recreate the bundles.
- Running `npm run watch` will watch the source JavaScript files for changes and rebuild the bundles if required.


[GeoJSON]: http://geojson.org/
[Leaflet]: http://leafletjs.com/

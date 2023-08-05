/* eslint-env mocha */


describe('teramap maps', function () {

    function create_container () {
        return L.DomUtil.create('div', 'teramap-container', document.querySelector('body'));
    }

    describe('toWKT', function () {
        it('should convert latlng to WKT', function () {
            L.latLng([54, 2]).toWKT().should.equal('POINT(2 54)');
            L.latLng([-1.05, 2.05]).toWKT().should.equal('POINT(2.05 -1.05)');
        });
    });
    describe('parseWKT', function () {
        it('should convert WKT to latlng', function () {
            var wkt = 'POINT(2 54)';
            L.Util.parseWKT(wkt).toWKT().should.equal(wkt);
        });
    });

    describe('leaflet-geojson-map', function () {
        var map;

        describe('adding more than one base layer should add a layers control', function () {
            var baselayers = {
                'Streets': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                }),
                'Topo': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
                    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
                })
            };
            before(function () {
                if (map) {
                    map.remove();
                }
                map = teramap.map_with_geojson(create_container(), {
                    baselayers: baselayers
                });
            });

            it('should have added the first layer to the map, but not the second', function () {
                map.hasLayer(baselayers['Streets']).should.be.ok;
                map.hasLayer(baselayers['Topo']).should.not.be.ok;
            });

            it('should have a layers control', function (){
                map.layersControl.should.be.an.instanceof(L.Control.Layers);
            });
            it('should not have a search control', function () {
                document.querySelectorAll('.leaflet-control-geocoder').length.should.equal(0);
            });
        });

        describe('adds searchControl if required', function () {
            before(function () {
                if (map) {
                    map.remove();
                }
                map = teramap.map_with_geojson(create_container(), {searchControl: true});
            });
            it('should have a search control', function () {
                document.querySelectorAll('.leaflet-control-geocoder').length.should.equal(1);
            });
        });
    });
});

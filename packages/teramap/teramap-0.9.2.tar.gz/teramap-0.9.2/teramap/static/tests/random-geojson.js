/* eslint-env node */
/*eslint-disable no-console */

var fs = require('fs');
var random = require('geojson-random');

var bbox = [0, 50, 6, 55];
var outfile = 'fixtures/random.geojson';
var count = 1000;


var gj = random.point(count, bbox);

gj.features.map(function (feature) {
    feature.properties = {'circle_marker': 2};
});

fs.writeFile(__dirname + '/' + outfile, JSON.stringify(gj));
console.log(`Wrote ${count} random points to ${outfile}`);

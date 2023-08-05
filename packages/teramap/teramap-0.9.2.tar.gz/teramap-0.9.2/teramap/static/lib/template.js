// https://github.com/Leaflet/Leaflet/blob/master/src/core/Util.js

var templateRe = /\{ *([\w_-]+) *\}/g;

export default function template(str, data) {
    return str.replace(templateRe, function (str, key) {
        var value = data[key];

        if (value === undefined) {
            throw new Error('No value provided for variable ' + str);
        } else if (typeof value === 'function') {
            value = value(data);
        }
        return value;
    });
}

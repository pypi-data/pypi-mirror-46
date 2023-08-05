import template from '../lib/template.js';
import {render_species_name} from './utils.js';


class PinpointTable {
    constructor (form_data, options, selector) {
        this.form_data = form_data;
        this.options = options;
        this.selector = selector;
    }

    render (data) {
        var options = this.options;

        var edit_fmt = '<div class="leaflet-number-marker">{name}</div>&nbsp;&nbsp;' +
            '<span data-pin-name="{name}" class="btn-group btn-group-xs">' +
                '<span data-target="edit" class="btn btn-default"><i class="fa fa-edit"></i></span>' +
                (options.mapclick_create ? '<span data-target="move-marker" class="btn btn-default"><i class="fa fa-map-marker"></i></span>' : '') +
                '<span data-target="delete" class="btn btn-danger"><i class="fa fa-remove"></i></span>' +
            '</span>';

        var html = '<thead><tr>';
        data[0].forEach(function (header) {
            html += '<th>' + header + '</th>';
        });
        html += '</tr>';

        var prev_name;
        data.slice(1).forEach(function (row) {
            var name = row[0];
            if (prev_name === undefined || prev_name != name) {
                html += '<tr class="first"><td>' + template(edit_fmt, {
                    name: name
                });
            } else {
                html += '<tr><td>';
            }
            html += '</td>';
            html += '<td>' + render_species_name(row[1]) + '</td>';

            row.slice(2).forEach(function (column) {
                column = (column === undefined) ? '' : column;
                html += '<td>' + column + '</td>';
            });
            prev_name = name;
        });
        html += '</tbody>';

        this.selector.html(html);
    }
}

export default PinpointTable;

import extend from '../lib/extend.js';
import SpeciesSelect from './species-select.js';
import {render_species_name} from './utils.js';

function form_group(contents) {
    return '<div class="form-group">' + contents + '</div>';
}

// renders an input (type=text by default)
function render_input(attributes) {
    attributes = extend({type: 'text'}, attributes);

    var attrs = [];
    for (var name in attributes) {
        attrs.push(name + '="' + attributes[name] + '"');
    }

    return '<input ' + attrs.join(' ') + '/>';
}

function PinpointModal (form_data, options) {
    var _ = form_data._;
    var protocol = form_data.protocol;

    // Render an input row for a species.
    function render_input_row(pin_name, species, group) {
        var row = '<tr><td>' + render_species_name(species, 'form-control-static text-right') + '</td>';

        protocol.eachSubject(function (name, subject_pk) {
            var value = form_data.observedCount(pin_name, species.pk, subject_pk);
            if (value === undefined) {
                value = '';
            }

            var input = render_input({
                'class': 'form-control app-transect-subject-input number-input center-block',
                'data-species': species.pk,
                'data-subject': subject_pk,
                'value': value
            });
            row += '<td>' + input + '</td>';
        }, group.pk);
        row += '</tr>';
        return row;
    }

    function render_secondary_selector(group) {
        var subject_count = 0;
        protocol.eachSubject(function () { subject_count++; }, group.pk);

        var html = '<tr>' +
            '<td><select class="form-control species-selector" data-group="' + group.pk + '"></select></td>' +
            '<td colspan="' + subject_count + '">' +
            '</td>' +
            '</tr>';

        return html;
    }

    this.modal = function(selector, pin_name) {
        var pin = form_data.getPin(pin_name);

        selector.data('name', pin_name);
        selector.find('.pinpoint-name').html('<div class="leaflet-number-marker">' + pin_name + '</div>');
        selector.find('form').html('<div class="modal-body"></div>');

        var header = selector.find('.modal-header');
        header.find('label').remove();
        if (options.enable_fix_location_checkbox) {
            header.prepend(
                '<label class="pull-right"><input type="checkbox" /> ' +
                _('fix location', true) +
                '</label>'
            );
            var checked = ('fix_location' in pin && pin.fix_location === true);
            header.find('input[type=checkbox]').prop('checked', checked);
        }

        var body = selector.find('.modal-body');
        var html = '';
        if (protocol.hasSampleAttrs()) {
            html += '<h4>' + _('attributes', true) + '</h4>';
            protocol.eachSampleAttr(function (attr, pk) {
                var input = '<label class="control-label col-sm-4">' + attr.name + '</label>';
                input += '<div class="col-sm-6">';

                var current_value = pin.attributes[pk] || '';
                var valid_input_types = ['number', 'color', 'date', 'month', 'password', 'range', 'time', 'text'];

                if (attr.choices && attr.choices.length > 0) {
                    input += '<select data-sample-attr="' + pk + '" class="form-control">';
                    attr.choices.forEach(function (choice) {
                        var selected = (choice[0] == current_value) ? 'selected="selected"' : '';
                        input += '<option value="' + choice[0] + '" ' + selected + '>' + choice[1] + '</option>';
                    });
                    input += '</select>';
                } else {
                    input += render_input({
                        type: (valid_input_types.indexOf(attr.type) !== -1) ? attr.type : 'text',
                        class: 'form-control',
                        'data-sample-attr': pk,
                        value: current_value
                    });
                }
                input += '</div>';
                html += form_group(input);
            });
            body.append(html);
        }

        var dropdownParent = $(options.modal_selector).find('.modal-content');
        var species_select = new SpeciesSelect(protocol, dropdownParent, _('type the first 4 letters of the species name and select a species', true));

        if (protocol.pinpoint_observation) {
            // let the user choose species, subjects and supply a count.
            body.append(form_group(
                '<select class="form-control species-selector"></select>' +
                '<select class="form-control subject-selector"><option disabled="disabled">' +
                    _('select species first', true) +
                '</option></select> ' +
                render_input({
                    class: 'form-control number-input',
                    'min': 0,
                    name: 'count',
                    placeholder: 'count'
                })
            ));

            // what species should be selected?
            var observation = form_data.getObservation(pin_name);
            var species = undefined;
            if (observation && observation.species || (!protocol.species_url && Object.keys(protocol.species).length == 1)) {
                var pk = (observation && observation.species) ? observation.species : Object.keys(protocol.species)[0];
                species = protocol.species[pk];
            }

            species_select.render(body.find('.species-selector'), species)
                .on('change', function () {
                    var item = $(this).select2('data')[0];
                    if (!item || !item.original) {
                        return;
                    }
                    update_subject_selector(item.original);
                });
            var subject_selector = body.find('.subject-selector');

            var update_subject_selector = function (species) {
                protocol.activateSpecies(species.pk, species);

                var current_value = +subject_selector.val();
                var current_value_valid = false;
                var subjects = [];
                protocol.eachSubject(function (name, pk) {
                    subjects.push({id: pk, text: name});
                    if (pk == current_value) {
                        current_value_valid = true;
                    }
                }, species.group);

                subject_selector.empty().select2({
                    dropdownParent: $(options.modal_selector).find('.modal-content'),
                    data: subjects
                });
                // reset previous selection if it's still valid for this species.
                if (current_value && current_value_valid) {
                    subject_selector.val(current_value).trigger('change');
                }
            };

            // if we have initial species, update the subject selector
            if (species) {
                update_subject_selector(species);
            }

            // set the rest of the initial values
            if (observation && observation.subject && observation.count) {
                if (observation.subject) {
                    subject_selector.val(observation.subject).trigger('change');
                    body.find('[name="count"]').val(observation.count);
                }
            }
        } else { // pinpoint sample
            html = '<table class="table app-transect-table">';
            protocol.eachGroup(function(group) {
                html += '<tr><th>' + group.name + '</th>';
                protocol.eachSubject(function (name) {
                    html += '<td>' + name + '</td>';
                }, group.pk);
                html += '</tr>';

                protocol.eachActiveSpecies(function (species) {
                    html += render_input_row(pin_name, species, group);
                }, group.pk);

                html += render_secondary_selector(group);
            });

            html += '</table>';
            body.append(html);

            protocol.eachGroup(function (group) {
                species_select.set_group(group).render(
                    $('.species-selector[data-group="' + group.pk + '"]')
                );
            });
        }
        selector.find('form')
            .toggleClass('form-inline', protocol.pinpoint_observation)
            .toggleClass('form-horizontal', !protocol.pinpoint_observation);
    };
}

export default PinpointModal;

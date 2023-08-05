import extend from '../lib/extend.js';
import Pinpoint from './pinpoint.js';
import PinpointTable from './pinpoint-table.js';
import PinpointModal from './pinpoint-modal.js';

class PinpointController {
    constructor (map, pinpoint_data, options) {
        this.map = map;

        this.options = options = extend({
            output_selector: '[name=samples]',
            modal_selector: '#pinpoint_form',
            table_selector: '#observations',

            // if mapclick_create is disabled, new samples can only be created Using
            // the create_button.
            mapclick_create: true,
            // If this contains a selector, a click event will be attached
            // which creates a new pin without a latlng/marker.
            create_button_selector: '',

            // adds a checkbox to the modal to mark this pinpoint location
            // fixed to make it available in the next pinpoint sessions.
            // If the checkbox is checked,
            enable_fix_location_checkbox: false,
            // The default value for the state of the fix_location checkbox
            default_fix_location_state: true,

            // warn when trying to navigate away when the editor has unsaved changes
            warn_for_unsaved_changes: true
        }, options);

        this.modal = $(options.modal_selector);
        this.table = $(options.table_selector);

        try {
            var form_data = this.form_data = new Pinpoint(pinpoint_data);
        } catch (e) {
            this.table.html('<h1>Error in protocol: <em>' + e + '</em></h1>');
            return;
        }

        this.renderer = new PinpointModal(this.form_data, options);
        this._ = this.form_data._;

        this.markers = {};
        this.editing_state = false;

        this.tableRenderer = new PinpointTable(form_data, options, this.table);

        var controller = this;
        if (options.mapclick_create) {
            map.on('click', function (e) {
                if (!controller.editing_state) {
                    // add marker and open modal
                    var pin = form_data.createPin(e.latlng);
                    if (options.enable_fix_location_checkbox) {
                        pin.fix_location = options.default_fix_location_state;
                    }

                    controller.addMapMarker(form_data.createMarker(pin));
                    controller.showEditor(pin.name);
                }
            });
        }
        if (options.create_button_selector) {
            $(options.create_button_selector).on('click', function () {
                var pin = form_data.createPin();
                controller.showEditor(pin.name);
            });
        }

        // add initial map markers.
        var bounds = L.latLngBounds();
        if (map.geojson_layer) {
            bounds.extend(map.geojson_layer.getBounds());
        }
        form_data.eachPin(function (pin) {
            if (pin.latlng) {
                var marker = controller.addMapMarker(form_data.createMarker(pin));
                bounds.extend(marker.getLatLng());
            }
        }, this);
        if (bounds.isValid()) {
            map.fitBounds(bounds.pad(0.2));
        }

        this.update();
        this.initModal();

        this.table.on('click', '[data-target]', function () {
            var pin_name = '' + $(this).parent().data('pin-name');

            switch ($(this).data('target')) {
            case 'move-marker':
                var marker = controller.markers[pin_name];
                alert(form_data._('click on map to choose new location'));
                controller.editing_state = true;

                map.once('click', function (e) {
                    L.DomEvent.preventDefault(e);

                    form_data.setLatLng(pin_name, e.latlng);
                    marker.setLatLng(e.latlng);
                    controller.update();
                    controller.editing_state = false;
                    controller.dirty = true;
                });

                break;
            case 'delete':
                controller.dirty = true;
                controller.removePin(pin_name);
                break;
            default:
                controller.showEditor(pin_name);
            }
        });

        controller.dirty = false;
        if (options.warn_for_unsaved_changes) {
            window.onbeforeunload = function () {
                if (controller.dirty) {
                    return true;
                }
            };
            // make sure the form submit button still works.
            $(options.output_selector).parents('form').find('input[type="submit"]').on('click', function () {
                window.onbeforeunload = null;
            });
        }
    }

    initModal () {
        var modal = this.modal;
        var form_data = this.form_data;
        var _ = form_data._;
        var renderer = this.renderer;
        var controller = this;
        var pinpoint_observation = form_data.protocol.pinpoint_observation;

        modal.on('shown.bs.modal', function () {
            $(this).find('input').first().focus();
        });
        modal.on('hidden.bs.modal', function () {
            controller.update();
        });

        if (!pinpoint_observation) {
            // listen for change on species-selector, (of which the modal might have multiple instances).
            modal.on('select2:close', '.species-selector', function () {
                var pin_name = modal.data('name');
                var species_pk = +$(this).val();

                // initial render quick exit.
                if (species_pk == '') {
                    return;
                }
                var item = $(this).select2('data')[0];

                modal.find('.select2-hidden-accessible').select2('destroy');
                controller.saveEditorData(true);

                form_data.protocol.activateSpecies(species_pk, item.original);

                // re-render modal.
                renderer.modal(modal, pin_name);
                // focus on firt input in newly added row:
                modal.find('input[data-species="' + species_pk + '"]').first().focus();
            });
        }

        var modal_save = function () {
            if (pinpoint_observation) {
                var is_set = function (selector) {
                    var val = $(modal).find(selector).val();
                    return val != '' && val != undefined && val != null;
                };
                if (!is_set('.species-selector')) {
                    alert(_('you must select a species', true));
                    return;
                }
                if (!is_set('.subject-selector')) {
                    alert(_('you must select a subject', true));
                    return;
                }
            }

            controller.saveEditorData();
            modal.modal('hide');
        };

        // save button in modal
        modal.on('click', '[data-save]', modal_save);

        // submit form in modal on enter.
        modal.on('keypress', function (e) {
            if (e.which == 13) { // enter
                modal_save();
                // prevent the form in the modal from submitting
                e.preventDefault();
            }
        });

        // cancel button in modal
        modal.on('click', '[data-dismiss]', function () {
            var pin = form_data.getPin($(modal).data('name'));

            if ('delete_on_cancel' in pin) {
                // remove pin without asking for permission
                controller.removePin(pin.name, true);
            }
            controller.update();
            modal.modal('hide');
        });
    }

    showEditor(pin_name) {
        this.form_data.protocol.sortActiveSpecies();
        this.renderer.modal(this.modal, pin_name);
        this.modal.modal({backdrop: 'static', keyboard: false});
    }

    addMapMarker (marker) {
        var controller = this;

        marker.addTo(this.map);
        marker.on('click', function markerclick(e) {
            controller.showEditor(e.target.feature.properties.name);

            // do not propagate click to map.
            L.DomEvent.stopPropagation(e);
        });

        this.markers[marker.feature.properties.name] = marker;
        return marker;
    }

    removePin (pin_name, no_ask_permission) {
        var _ = this.form_data._;
        if (!no_ask_permission && !confirm(_('are you sure you want to delete this observation?', true))) {
            return false;
        }

        if (this.markers[pin_name]) {
            this.markers[pin_name].removeFrom(this.map);
        }

        this.form_data.removePin(pin_name);
        this.update();
        return true;
    }

    saveEditorData (preserve_delete_on_cancel) {
        preserve_delete_on_cancel = preserve_delete_on_cancel === true;
        var count_input_selector = 'input.number-input';

        var pin_name = this.modal.data('name');
        var form_data = this.form_data;
        var pin = form_data.getPin(pin_name);
        var modal = this.modal;

        if (form_data.protocol.pinpoint_observation) {
            form_data.updateCount(
                pin_name,
                +$('.species-selector').val(),
                +$('.subject-selector').val(),
                modal.find(count_input_selector).val()
            );
        } else {
            // set not_counted to false on save, if it exists
            if (pin.not_counted) {
                pin.not_counted = false;
            }

            // sample attributes
            modal.find('[data-sample-attr]').each(function () {
                var input = $(this);
                form_data.updateAttribute(pin_name, +input.data('sample-attr'), input.val());
            });

            // observed counts
            modal.find(count_input_selector).each(function () {
                var input = $(this);
                form_data.updateCount(
                    pin_name,
                    +input.data('species'),
                    +input.data('subject'),
                    input.val()
                );
            });
        }

        if (this.options.enable_fix_location_checkbox) {
            pin.fix_location = (modal.find('input[type=checkbox]').prop('checked'));
        }
        if (!preserve_delete_on_cancel) {
            delete pin['delete_on_cancel'];

            // set dirty state, we saved something that should not be lost without confirmation
            this.dirty = true;
        }
    }

    update () {
        $(this.options.output_selector).val(this.form_data.serialize());

        this.form_data.protocol.sortActiveSpecies();
        this.tableRenderer.render(this.form_data.tableData());
    }

}
export default PinpointController;

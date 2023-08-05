import {is_primary} from './protocol.js';

function transform_factory (protocol) {
    return function (item) {
        return {
            original: item,
            id: item.id === undefined ? item.pk : item.id,
            text: item.name || '<em>' + item.scientific_name + '</em>',
            is_primary: is_primary(item),
            group: item.group || protocol.getGroupForSpecies(item)
        };
    };
}

class SpeciesSelect {

    constructor (protocol, dropdownParent, placeholder) {
        this.protocol = protocol;
        this.group = undefined;
        this.dropdownParent = dropdownParent;

        this.placeholder = placeholder;
    }

    data () {
        var protocol = this.protocol;
        var data = [];
        function add(item) {
            data.push(item);
        }

        // in case of pinpoint_observation, also include active species.
        if (protocol.pinpoint_observation) {
            protocol.eachActiveSpecies(add, this.group);
        }
        protocol.eachSelectableSpecies(add, this.group);

        data = data.map(transform_factory(protocol));
        data.unshift({
            id: '',
            text: this.placeholder
        });
        return data;
    }

    set_group (group) {
        this.group = group.pk;
        return this;
    }

    render (element, selected_species) {
        var options = {
            dropdownParent: this.dropdownParent,
            escapeMarkup: function (a) { return a; },
            templateResult: function (data) {
                if ('is_primary' in data && is_primary(data)) {
                    return '<span class="app-transect-species-primary">' + data.text + '</span>';
                }
                return data.text;
            }
        };

        if (this.protocol.species_url) {
            var transformer = transform_factory(this.protocol);
            var group_pk = this.group;
            options.placeholder = this.placeholder;
            options.ajax = {
                url: this.protocol.species_url,
                dataType: 'json',
                data: function (params) {
                    var query = {
                        json: true,
                        group: group_pk,
                        search: params.term,
                        page: params.page || 1
                    };
                    return query;
                },
                processResults: function (data) {
                    data.results = data.results.map(transformer);
                    return data;
                }
            };
            element.select2(options);

            if (selected_species) {
                var item = transformer(selected_species);
                var option = new Option(item.text, item.id, true, true);
                element.append(option);
                element.trigger({
                    type: 'select2:change',
                    params: {data: item}
                });
            }
        } else {
            options.data = this.data();
            if (options.data.length == 1) {
                element.hide();
                return false;
            }
            element.select2(options);
            if (selected_species) {
                element.val(selected_species.pk).trigger('change');
            }
        }

        return element;
    }
}


export default SpeciesSelect;

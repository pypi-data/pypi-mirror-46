import {is_primary} from './protocol.js';
import template from '../lib/template.js';

function render_species_name (species, extra_classes) {
    var classNames = extra_classes || '';
    if (is_primary(species)) {
        classNames += ' app-transect-species-primary';
    }

    return template('<span class="{class}" title="{scientific_name}">{name}</span>', {
        class: classNames,
        scientific_name: species.scientific_name || '',
        name: species.name || '<em>' + species.scientific_name + '</em>'
    });
}

export {render_species_name};

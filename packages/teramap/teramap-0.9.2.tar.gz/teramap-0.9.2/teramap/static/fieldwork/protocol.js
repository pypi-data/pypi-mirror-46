function is_primary(species) {
    return 'is_primary' in species ? species.is_primary : false;
}

function sort_species (species) {
    // sort species objects first on primary / secondary distinction, then alphabetically on name
    // input: array of species objects
    species.sort(function (a, b) {
        if (is_primary(a) && ! is_primary(b)) {
            return -1;
        }
        if (is_primary(b) && !is_primary(a)) {
            return 1;
        }
        return (a.name < b.name) ? -1 : 1;
    });
}

function _active_species (protocol) {
    var active = [];
    var species = protocol.species;
    for (var i in species) {
        if (is_primary(species[i]) || species[i].is_active) {
            active.push(species[i]);
        }
    }
    sort_species(active);

    return active.map(function (species) {
        return species.pk;
    });
}


class Protocol {
    /* Class to manage the a protocol.
     * Refer to ./README.md for documentation
     */
    constructor (protocol) {
        var required_keys = ['subjects', 'groups'];

        required_keys.forEach(function (type) {
            if (Object.keys(protocol[type]).length === 0) {
                throw new Error('No ' + type + ' provided');
            }
        });
        if (Object.keys(protocol.species).length === 0 && !protocol.species_url) {
            throw new Error('Either species or species_url (or both) should be defined');
        }

        // copy the keys from the protocol argument.
        var keys = required_keys.concat(['species', 'pinpoint_target', 'species_url']);
        var self = this;
        keys.forEach(function (key) {
            if (protocol[key]) {
                self[key] = protocol[key];
            }
        });

        this.pinpoint_observation = protocol.pinpoint_target == 'observation';
        this.sample_attrs = protocol.sample_attrs || {};
        this.active_species = _active_species(protocol);

        // copy species id's to a list of species for the group.
        this.eachGroup(function(group) {
            group.species = [];
        });
        if (this.species) {
            for (var species_pk in this.species) {
                var species = this.species[species_pk];
                this.groups[species.group].species.push(+species_pk);
            }
        }
    }

    activateSpecies (species_pk, species) {
        // if the species is not yet in our collection (ajax request),
        // add it to the structure.
        if (!this.species[species_pk]) {
            this.species[species_pk] = species;
            this.groups[species.group].species.push(species_pk);
        }
        this.species[species_pk].is_active = true;
        if (this.active_species.indexOf(species_pk) === -1) {
            this.active_species.push(species_pk);
        }
    }

    eachSubject (fn, group_pk) {
        var subjects;
        if (group_pk !== undefined) {
            subjects = this.groups[group_pk].subjects;
        } else {
            subjects = Object.keys(this.subjects);
        }
        subjects.forEach(function (pk) {
            fn(this.subjects[pk], pk);
        }, this);
    }

    // iterate over subjects by unique name.
    eachSubjectName (fn) {
        var subjects = {};
        this.eachSubject(function (subject, pk) {
            if (!(subject in subjects)) {
                subjects[subject] = [];
            }
            subjects[subject].push(+pk);
        });

        for (var name in subjects) {
            fn(name, subjects[name]);
        }
    }

    _eachSpecies (callback, filter, context) {
        // low level eachSpecies, which takes custom filter method.
        for (var i in this.species) {
            if (filter && !filter(this.species[i])) {
                continue;
            }
            callback.call(context, this.species[i], this.species[i].pk);
        }
    }

    sortActiveSpecies () {
        this.active_species = _active_species(this);
    }

    eachActiveSpecies (callback, group_pk) {
        var active_species = this.active_species;  // species pk values

        // filter active species for a certain group if a group_pk is supplied
        if (group_pk !== undefined) {
            var group_species = this.groups[group_pk].species;
            active_species = active_species.filter(function (pk) {
                return group_species.indexOf(pk) !== -1;
            });
        }

        // transform the list of pk's into a list of species objects
        active_species = active_species.map(function (species_pk) {
            return this.species[species_pk];
        }, this);

        active_species.forEach(function (species) {
            callback(species, species.pk);
        }, this);
    }

    // all species, except those active
    eachSelectableSpecies (callback, group_pk) {
        var group_species = false;
        if (group_pk !== undefined) {
            group_species = this.groups[group_pk].species;
        }

        this._eachSpecies(callback, function (species) {
            if (group_species && group_species.indexOf(species.pk) === -1) {
                return false;
            }
            return !(is_primary(species) || species.is_active);
        });
    }

    eachGroup (fn) {
        for (var pk in this.groups) {
            fn(this.groups[pk], pk);
        }
    }

    getGroupForSpecies (species) {
        // returns the group species belongs to.
        for (var pk in this.groups) {
            var group = this.groups[pk];
            if (group.species.indexOf(species.pk) !== -1) {
                return group;
            }
        }
    }

    selectSubjectForSpecies (subject_pks, species) {
        // from a list of subject pks, get the one relevant for this species.
        var ret;
        var group = this.getGroupForSpecies(species);
        group.subjects.forEach(function (subject) {
            if (subject_pks.indexOf(subject) !== -1) {
                ret = subject;
            }
        });
        return ret;
    }

    hasSampleAttrs () {
        return (
            !this.pinpoint_observation &&
            Object.keys(this.sample_attrs).length > 0
        );
    }

    eachSampleAttr (fn) {
        for (var pk in this.sample_attrs) {
            fn(this.sample_attrs[pk], pk);
        }
    }
}

export {is_primary, Protocol};
export default Protocol;

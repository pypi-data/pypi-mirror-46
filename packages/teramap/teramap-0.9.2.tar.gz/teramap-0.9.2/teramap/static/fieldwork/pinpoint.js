import {numberMarker} from '../lib/leaflet-number-marker.js';

import {is_primary, Protocol} from './protocol.js';


function Pinpoint(pinpoint_data) {
    /* Class to manage the data for pinpoint form.
     * Refer to ./README.md for documentation
     */
    var protocol = this.protocol = new Protocol(pinpoint_data.protocol);
    var pinpoint_observation = protocol.pinpoint_observation;

    this.samples = pinpoint_data.initial_data || [];

    // add dummy sample when we use pinpoint_observation
    if (pinpoint_observation && this.samples.length === 0) {
        this.samples.push({observations: []});
    }

    // mark species active if one of the pins has an observation containing it.
    try {
        this.samples.forEach(function (sample) {
            sample.observations.forEach(function (observation) {
                if (observation.species) {
                    protocol.activateSpecies(observation.species);
                }
            });
        });
    } catch (e) {
        throw new Error(
            'Could not activate species for initial data. Make sure all ' +
            'species refered to in initial_data are present in protocol.species.'
        );
    }

    this.updateAttribute = function (pin_name, attr_pk, value) {
        var sample = this.getSample(pin_name);
        sample.attributes[attr_pk] = value;
    };

    this.getSample = function (pin_name) {
        if (pinpoint_observation) {
            // for pinpoint_sample, all observations are part of the dummy sample.
            return this.samples[0];
        } else {
            var ret;
            this.samples.forEach(function (sample) {
                if (sample.name == pin_name) {
                    ret = sample;
                }
            });
            return ret;
        }
    };

    this.getObservation = function (pin_name, species_pk, subject_pk) {
        var observation;

        var sample = this.getSample(pin_name);
        sample.observations.forEach(function (obs) {
            if (pinpoint_observation) {
                if (obs.name === pin_name) {
                    observation = obs;
                }
            } else {
                var equals = obs.species == species_pk && obs.subject == subject_pk;
                if (sample.name == pin_name && equals) {
                    observation = obs;
                }
            }
        });

        return observation;
    };

    this.removeObservation = function (pin_name, species_pk, subject_pk) {
        var sample = this.getSample(pin_name);
        var observation = this.getObservation(pin_name, species_pk, subject_pk);

        var index = sample.observations.indexOf(observation);
        if (pinpoint_observation) {
            observation.count = undefined;
        } else {
            sample.observations.splice(index, 1);
        }
    };

    this.updateCount = function (pin_name, species_pk, subject_pk, count) {
        // coerce to number if not undefined.
        if (count !== undefined && count !== '') {
            count = Math.abs(+count);
        }
        var species = protocol.species[species_pk];

        var sample = this.getSample(pin_name);
        var observation = this.getObservation(pin_name, species_pk, subject_pk);

        if (observation) {
            L.extend(observation, {
                species: species_pk,
                subject: subject_pk,
                count: count
            });
        }
        // do not save 0-counts for non-primary species and no undefined counts at all
        if ((!is_primary(species) && count === undefined) || count === '') {
            if (observation) {
                this.removeObservation(pin_name, species_pk, subject_pk);
            }
            return;
        }

        if (!observation && !pinpoint_observation) {
            sample.observations.push({
                species: species_pk,
                subject: subject_pk,
                count: count
            });
        }
    };

    this.observedCount = function (pin_name, species_pk, subject_pk) {
        var observation = this.getObservation(pin_name, species_pk, subject_pk);

        return observation ? observation.count : undefined;
    };

    // return the maxiumum pin name currently used + 1
    this.next_pin_name = function () {
        var pin_name = 0;
        this.samples.forEach(function (sample) {
            if (pinpoint_observation) {
                sample.observations.forEach(function (obs) {
                    pin_name = Math.max(pin_name, +obs.name);
                });
            } else {
                pin_name = Math.max(pin_name, +sample.name);
            }
        });

        return '' + (pin_name + 1);
    };

    function convertLatLng(latlng) {
        latlng = L.latLng(latlng);
        return [latlng.lat, latlng.lng];
    }

    // Create a new empty pin at latlng, initializing the list of observations.
    this.createPin = function (latlng) {
        var pin = {
            name: this.next_pin_name(),
            // identify this new pin to delete is when edit cancelled.
            delete_on_cancel: true
        };

        if (pinpoint_observation) {
            var sample = this.getSample();
            sample.observations.push(pin);
        } else {
            L.extend(pin, {
                observations: [],
                attributes: {}
            });
            this.samples.push(pin);
        }

        if (latlng) {
            pin.latlng = convertLatLng(latlng);
        }
        return pin;
    };

    this.createMarker = function (pin) {
        var marker = numberMarker(pin.latlng, pin.name);
        marker.feature = {properties: pin};
        return marker;
    };

    this.setLatLng = function (pin_name, latlng) {
        this.getPin(pin_name).latlng = convertLatLng(latlng);
    };

    this.getPin = function (pin_name) {
        if (pinpoint_observation) {
            return this.getObservation(pin_name);
        } else {
            return this.getSample(pin_name);
        }
    };

    this.eachPin = function (fn) {
        var list = pinpoint_observation ? this.samples[0].observations : this.samples;

        for (var i in list) {
            fn(list[i], i);
        }
    };

    this.hasObservations = function (pin_name) {
        var pin = this.getPin(pin_name);
        if (pin === undefined) {
            return false;
        }
        if (pinpoint_observation) {
            return 'species' in pin;
        } else {
            return pin.observations.length > 0;
        }
    };

    this.removePin = function (pin_name) {
        var list;
        if (pinpoint_observation) {
            var sample = this.getSample();
            list = sample.observations;
        } else {
            list = this.samples;
        }
        for (var i in list) {
            if (list[i].name == pin_name) {
                list.splice(i, 1);
            }
        }
    };

    // Gather the data for the table below the map.
    this.tableData = function () {
        var ret = [];
        var header = [_('location'), _('species')];
        if (pinpoint_observation) {
            header.push(_('subject'), _('count'));
        } else {
            protocol.eachSubjectName(function (name) {
                header.push(name);
            });
        }
        ret.push(header);
        var self = this;
        this.samples.forEach(function (sample) {
            if (pinpoint_observation) {
                sample.observations.forEach(function (obs) {
                    var species = protocol.species[obs.species];
                    var subject = protocol.subjects[obs.subject];
                    ret.push([obs.name, species, subject, obs.count]);
                });
            } else {
                if (sample.observations.length < 1) {
                    var row = [sample.name, {name: _('no observations')}];
                    // add enough empty columns for the subjects.
                    protocol.eachSubjectName(function () {
                        row.push('');
                    });
                    ret.push(row);
                    return;
                }
                protocol.eachActiveSpecies(function (species) {
                    var counts = [];
                    protocol.eachSubjectName(function (name, subject_pks) {
                        var subject_pk = protocol.selectSubjectForSpecies(subject_pks, species);
                        counts.push(self.observedCount(sample.name, species.pk, subject_pk));
                    });

                    if (is_primary(species) || counts.some(function(c) { return c !== undefined; })) {
                        ret.push([sample.name, species].concat(counts));
                    }
                });
            }
        });

        return ret;
    };

    this.serialize = function () {
        return JSON.stringify(this.samples, null, 2);
    };

    this._ = function (key, ucfirst) {
        var value = key;
        if ('messages' in pinpoint_data) {
            value = pinpoint_data.messages[key] || key;
        }

        if (ucfirst) {
            return value.charAt(0).toUpperCase() + value.substring(1);
        } else {
            return value;
        }
    };
    var _ = this._;
}

export default Pinpoint;

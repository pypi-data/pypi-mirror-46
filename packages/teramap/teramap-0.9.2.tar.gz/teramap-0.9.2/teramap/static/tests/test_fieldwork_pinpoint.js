/* eslint-env mocha */

var i18n_messages = {
    'attributes': 'attributes',
    'add': 'add',
    'location': 'location',
    'species': 'species'
};
var species = {
    '192': {pk: 192, is_primary: true, name: 'Huiskrekel', group: 1},
    '209': {pk: 209, is_primary: true, name: 'Beekoeverlibel', group: 1},
    '205': {pk: 205, is_primary: false, name: 'Bandheidelibel', group: 1},
    '206': {pk: 206, is_primary: false, name: 'Bloedrode heidelibel', group: 1}
};
var subjects = {
    '24': 'adult man',
    '25': 'adult vrouw'
};
var sample_attrs = {
    '32': {name: 'criteria occupation', choices: []},
    '9': {name: 'shading', choices: [['unknown', 'unknown'], ['no shade', 'no shade'], ['<30%', '<30%'], ['30-60%', '30-60%'], ['>60%', '>60%']]},
    '3': {name: 'wind-force (bft)', choices: []},
    '37': {name: 'accessibility', choices: []}
};
var groups = {
    1: {
        pk: 1,
        name: 'Insecten',
        subjects: [24, 25]
    }
};

var protocol_sample = function () {
    // make sure to clone
    return L.extend({}, {
        name: 'Instippen (sample)',
        pinpoint_target: 'sample',
        species: species,
        subjects: subjects,
        sample_attrs: sample_attrs,
        groups: groups
    });
};
var protocol_observation = {
    name: 'Instippen (observation)',
    pinpoint_target: 'observation',
    species: species,
    subjects: subjects,
    sample_attrs: {},
    groups: groups
};


describe('Fieldwork.is_primary', function () {
    chai.should();

    describe('is_primary', function () {
        var is_primary = teramap.fieldwork.is_primary;

        it('returns false if is_primary is not defined', function () {
            is_primary({pk: 192, name: 'Beekoeverlibel'}).should.be.false;
        });
        it('returns true if is_primary is set to true', function () {
            is_primary({pk: 192, is_primary: true, name: 'Beekoeverlibel'}).should.be.true;
        });
        it('returns false if is_primary is set to false', function () {
            is_primary({pk: 192, is_primary: false, name: 'Beekoeverlibel'}).should.be.false;
        });
    });
});

describe('Protocol', function () {
    chai.should();

    describe('load species without is_primary set', function () {
        var protocol_json = {
            name: 'Instippen (observation)',
            pinpoint_target: 'observation',
            species: {
                '192': {pk: 192, name: 'Beekoeverlibel', group: 1},
                '209': {pk: 209, name: 'Huiskrekel', group: 1},
                '205': {pk: 205, name: 'Bandheidelibel', group: 1},
                '206': {pk: 206, name: 'Bloedrode heidelibel', group: 1}
            },
            subjects: subjects,
            groups: {
                1: {name: 'Birds', subjects: [24, 25]},
            },
            sample_attrs: {},
        };
        var protocol = new teramap.fieldwork.Protocol(protocol_json);

        it('has the correct pinpoint_observation property', function () {
            protocol.pinpoint_observation.should.be.true;
        });

        it('returns correct species', function () {
            var actual_species = {};
            protocol._eachSpecies(function (s) {
                actual_species[s.pk] = s;
            });

            actual_species.should.deep.equal(protocol_json.species);
        });
        it('returns correct subjects', function () {
            var actual_subjects = {};
            protocol.eachSubject(function (s, pk) {
                actual_subjects[pk] = s;
            });

            actual_subjects.should.deep.equal(subjects);
        });
    });

    describe('pinpoint sample', function () {
        it('has the correct pinpoint_observation property', function () {
            var protocol = new teramap.fieldwork.Protocol(protocol_sample());

            protocol.pinpoint_observation.should.be.false;
        });
    });

    describe('groups', function () {
        var protocol_json = {
            name: 'Instippen (observation)',
            pinpoint_target: 'observation',
            species: {
                '192': {pk: 192, name: 'Beekoeverlibel', group: 2},
                '209': {pk: 209, name: 'Huiskrekel', group: 2},
                '206': {pk: 206, name: 'Zwaluwstaartmeeuw', group: 1},
                '207': {pk: 207, name: 'Ivoormeeuw', group: 1}
            },
            subjects: {
                '24': 'adult man',
                '25': 'adult vrouw',
                '26': 'Eieren',
                '27': 'Kuikens'
            },
            groups: {
                1: {
                    name: 'Birds',
                    species: [206, 207],
                    subjects: [24, 25, 26, 27]
                },
                2: {
                    name: 'Insects',
                    species: [192, 209],
                    subjects: [24, 25]
                }
            }
        };
        var protocol = new teramap.fieldwork.Protocol(protocol_json);

        it('Should return correct subjects for the specified species_group', function () {
            var subjects = [];
            protocol.eachSubject(function (subject, pk) {
                subjects.push(pk);
            }, 1);

            subjects.should.deep.equal([24, 25, 26, 27]);

            subjects = [];
            protocol.eachSubject(function (subject, pk) {
                subjects.push(pk);
            }, 2);
            subjects.should.deep.equal([24, 25]);
        });

        it('Should return correct species for the specified species_group', function () {
            protocol.activateSpecies(206);
            protocol.activateSpecies(207);
            protocol.sortActiveSpecies();

            var species = [];
            protocol.eachActiveSpecies(function (sp, pk) {
                species.push(pk);
            }, 1);

            species.should.deep.equal([207, 206]);  // alphabetically sorted
        });
    });
});

describe('Pinpoint', function () {
    chai.should();

    function compareTable(actual, expected) {
        actual.forEach(function (row, i) {
            row[0].should.deep.equal(expected[i][0]);
            if (i == 0) {
                row[1].should.deep.equal(expected[i][1]);
            } else {
                row[1].name.should.deep.equal(expected[i][1].name);
            }
            if (row[2] === undefined) {
                (expected[i][2] === undefined).should.be.true;
            }
            if (row[3] === undefined) {
                (expected[i][3] === undefined).should.be.true;
            }
        });
    }

    describe('pinpoint observation', function () {
        describe('without initial data', function () {
            var form_data = new teramap.fieldwork.Pinpoint({
                protocol: protocol_observation,
                initial_data: [],
                messages: i18n_messages
            });

            it('adds the dummy sample', function () {
                var data = new teramap.fieldwork.Pinpoint({
                    protocol: protocol_observation,
                    initial_data: [],
                    messages: i18n_messages
                });

                data.samples[0].should.have.key('observations');
            });

            it('correctly record and update observations', function () {
                var pin = form_data.createPin([51, 2]);

                var species_pk = Object.keys(species)[0];
                var subject_pk = Object.keys(subjects)[0];

                form_data.updateCount(pin.name, species_pk, subject_pk, 3);
                form_data.observedCount(pin.name, species_pk, subject_pk).should.equal(3);

                form_data.updateCount(pin.name, species_pk, subject_pk, 10);
                form_data.observedCount(pin.name, species_pk, subject_pk).should.equal(10);

                form_data.updateCount(pin.name, species_pk, subject_pk, 3);
                form_data.observedCount(pin.name, species_pk, subject_pk).should.equal(3);
            });

            it('returns the right table structure.', function () {
                var data = form_data.tableData();
                var expected = [
                    ['location', 'species', 'subject', 'count'],
                    ['1', species[192], 'adult man', 3]
                ];
                data.should.deep.equal(expected);
            });

            it('should remove an observation if a pin is removed', function () {
                var pin = form_data.createPin([51, 2]);

                form_data.getPin(pin.name).name.should.equal(pin.name);

                // remove the pin
                form_data.removePin(pin.name);

                (form_data.getPin(pin.name) === undefined).should.be.true;

                form_data.samples[0].observations.length.should.equal(1);
            });

            it('should allow moving the location of a pin', function () {
                var pin = form_data.createPin([51, 2]);

                form_data.getPin(pin.name).latlng.should.deep.equal([51, 2]);

                form_data.setLatLng(pin.name, [33, 1]);
                form_data.getPin(pin.name).latlng.should.deep.equal([33, 1]);
            });

            it('should correctly iterate each species', function () {
                var obj = {};
                form_data.protocol._eachSpecies(function (species) {
                    obj[species.pk] = species;
                });
                var expected = L.extend({}, species);
                expected[205].is_active = true;

                obj.should.deep.equal(expected);
            });
        });

        describe('Using initial data', function () {
            it('correctly marks secondary species active if they are in in initial_data', function () {
                var initial_data = [{
                    pk: 111,
                    observations: [
                        {'pk': 34, species: 205, subject: 24, count: 23},
                        {'pk': 35, species: 205, subject: 25, count: 2},
                    ]
                }];
                var data = new teramap.fieldwork.Pinpoint({
                    protocol: protocol_observation,
                    initial_data: initial_data,
                    messages: i18n_messages
                });

                data.protocol.species[205].is_active.should.be.true;
            });
        });
    });

    describe('pinpoint sample', function () {
        it('has the correct pinpoint_observation property', function () {
            var form_data = new teramap.fieldwork.Pinpoint({
                protocol: protocol_sample(),
                initial_data: [],
                messages: i18n_messages
            });
            form_data.protocol.pinpoint_observation.should.be.false;
        });

        it('correctly records observations', function () {
            var form_data = new teramap.fieldwork.Pinpoint({
                protocol: protocol_sample(),
                initial_data: [],
                messages: i18n_messages
            });
            var pin = form_data.createPin([51, 2]);
            var species_pk = Object.keys(species)[0];

            form_data.protocol.eachSubject(function (name, subject_pk) {
                form_data.updateCount(pin.name, species_pk, subject_pk, 3);
                form_data.observedCount(pin.name, species_pk, subject_pk).should.equal(3);
            });

            compareTable(form_data.tableData(), [
                ['location', 'species', 'adult man', 'adult vrouw'],
                ['1', species[209], undefined, undefined],  // alphabetically sorted
                ['1', species[192], 3, 3],
                ['1', species[205], undefined, undefined]
            ]);

            form_data.protocol.eachSubject(function (name, subject_pk) {
                form_data.updateCount(pin.name, 209, subject_pk, 6);
            });

            compareTable(form_data.tableData(), [
                ['location', 'species', 'adult man', 'adult vrouw'],
                ['1', species[209], 6, 6],  // alphabetically sorted
                ['1', species[192], 3, 3],
                ['1', species[205], undefined, undefined]
            ]);
        });

        it('should add a sample when a pin is added', function () {
            var form_data = new teramap.fieldwork.Pinpoint({
                protocol: protocol_sample(),
                initial_data: [],
                messages: {}
            });
            form_data.createPin([41, 4]);
            form_data.createPin([33, 3]);

            form_data.samples.length.should.equal(2);
        });
        // for obs - projecten, it is not desirable that things get thrown away.
        // it('should not report 0-observations for secondary species', function () {
        //     var form_data = new teramap.fieldwork.Pinpoint({
        //         protocol: protocol_sample(),
        //         initial_data: [],
        //         messages: {}
        //     });
        //
        //     var pin = form_data.createPin([22, 33]);
        //     var sample = form_data.getSample(pin.name);
        //
        //     var primary_pk = 192;
        //     var secondary_pk = 205;
        //     var secondary_pk2 = 206;
        //
        //     // first 'form row', primary species, explicit non-zero count
        //     form_data.updateCount(pin.name, primary_pk, 25, 3);
        //     // this should not result in a 0-observation but will be
        //     // created as a 0-observation server-side.
        //     form_data.updateCount(pin.name, primary_pk, 24, '');
        //
        //     // second 'form row', secondary species
        //     form_data.updateCount(pin.name, secondary_pk, 25, 3);
        //     // this should not result in an observation
        //     form_data.updateCount(pin.name, secondary_pk, 24, '');
        //
        //     // third 'form row', another secondary species, should both not result
        //     // in an observation.
        //     form_data.updateCount(pin.name, secondary_pk2, 25, '');
        //     form_data.updateCount(pin.name, secondary_pk2, 25, '');
        //
        //     sample.observations.length.should.equal(2);
        //
        //     // explicit 0-observation for primary species should result in a 0-observation
        //     form_data.updateCount(pin.name, primary_pk, 24, 0);
        //     sample.observations.length.should.equal(3);
        //
        //     // explicit 0-observations for secondary species should result in a 0-observation
        //     form_data.updateCount(pin.name, secondary_pk2, 24, 0);
        //     sample.observations.length.should.equal(4);
        //
        //     // tableData defaults to show_zero_observations=true
        //     compareTable(form_data.tableData(), form_data.tableData(true));
        //
        //     // when show_zero_observations=false, zero-rows should not be displayed.
        //     compareTable(form_data.tableData(false), [
        //         ['location', 'species', 'adult man', 'adult vrouw'],
        //         ['1', species[192], 0, 3],
        //         // this is currently expected, but not be showed (because secondary species).
        //         ['1', species[209], undefined, undefined],
        //         ['1', species[205], undefined, 3]
        //     ]);
        // });
    });
});

describe('PinpointRenderer', function () {
    chai.should();

    describe('renders a modal', function () {
        var form_data = new teramap.fieldwork.Pinpoint({
            protocol: protocol_observation,
            initial_data: [],
            messages: i18n_messages
        });
        var pin = form_data.createPin([52, 4]);
        var renderer = new teramap.fieldwork.PinpointModal(form_data, {
            'modal_selector': '#pinpoint_form'
        });
        var selector = $('#pinpoint_form');
        var visible = false;

        it('shows a modal', function () {
            renderer.modal(selector, pin.name);
            selector.on('show.bs.modal', function () {
                visible = true;
            });
            selector.on('hide.bs.modal', function () {
                visible = false;
            });
            selector.modal({backdrop: 'static'});
            visible.should.be.true;

            selector.modal('hide');
            visible.should.be.false;
        });
    });
});

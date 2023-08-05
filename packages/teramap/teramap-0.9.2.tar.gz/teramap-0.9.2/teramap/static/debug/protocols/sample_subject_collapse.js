/* eslint-disable no-unused-vars, quotes */

var data = {
    protocol: {
        name: 'Instippen (sample)',
        pinpoint_target: 'sample',
        species: {
            '192': {pk: 192, name: 'Beekoeverlibel', group: 2},
            '209': {pk: 209, name: 'Huiskrekel', group: 2},
            '206': {pk: 206, name: 'Zwaluwstaartmeeuw', group: 1},
            '207': {pk: 207, name: 'Ivoormeeuw', group: 1}
        },
        subjects: {
            '24': 'Aantal exemplaren',
            '25': 'Aantal exemplaren',
        },
        groups: {
            1: {pk: 1, name: 'Birds', subjects: [24]},
            2: {pk: 2, name: 'Insects', subjects: [25]}
        }
    },
    initial_data: [{
        "name": "1",
        "observations": [
            {"species": 206, "subject": 24, "count": 3}
        ],
        "attributes": {},
        "latlng": [51, -0.10],
        "fix_location": false
    },
    {
        "name": "2",
        "observations": [
            {"species": 209, "subject": 25, "count": 3}
        ],
        "attributes": {},
        "latlng": [50.98, -0.1],
        "fix_location": false
    }]
};

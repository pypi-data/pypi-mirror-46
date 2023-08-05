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
            '24': 'adult man',
            '25': 'adult vrouw',
            '26': 'Eieren',
            '27': 'Kuikens'
        },
        groups: {
            1: {
                pk: 1,
                name: 'Birds',
                subjects: [24, 25, 26, 27]
            },
            2: {
                pk: 2,
                name: 'Insects',
                subjects: [24, 25]
            }
        }
    },
    initial_data: [{
        "name": "1",
        "pk": 1,
        "observations": [
            {"species": 207, "subject": 24, "count": 3},
            {"species": 206, "subject": 24, "count": 9},
        ],
        "attributes": {},
        "latlng": [50.99, -0.10],
        "fix_location": true
    },
    {
        "name": "2",
        "pk": 2,
        "observations": [
            {"species": 206, "subject": 24, "count": 3},
            {"species": 207, "subject": 24, "count": 0}
        ],
        "attributes": {},
        "latlng": [50.98, -0.071]
    },
    {
        "name": "3",
        "pk": 3,
        "observations": [
            {"species": 206, "subject": 24, "count": 3}
        ],
        "attributes": {},
        "latlng": [50.98, -0.061]
    },
    {
        "name": "4",
        "pk": 4,
        "observations": [],
        "attributes": {},
        "latlng": [50.98, -0.077],
        "not_counted": true
    }]
};

/* eslint-disable no-unused-vars, quotes */

var data = {
    protocol: {
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
    initial_data: [
        {"observations": [
            {
                "name": "1",
                pk: 2,
                "latlng": [50.98, -0.089],
                "species": 192,
                "subject": 24,
                "count": 23
            }
        ]}
    ]
};

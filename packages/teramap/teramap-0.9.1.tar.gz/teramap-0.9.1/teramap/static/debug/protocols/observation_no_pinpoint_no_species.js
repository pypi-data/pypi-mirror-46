/* eslint-disable no-unused-vars, quotes */

// no species or species_url, should result in an error.

var options = {
    mapclick_create: false,
    create_button_selector: '#addSample'
};

var data = {
    "protocol": {
        "name": "Schepnetonderzoek amfibie\u00ebn",
        "sample_attrs": {},
        "subjects": {
            "1": "Adult man",
            "2": "Adult vrouw",
            "17": "Larve",
            "18": "Onvolwassen",
            "19": "Adult onbekend",
            "25": "Eieren/Legsels",
            "29": "Aantal volwassen exemplaren",
            "30": "Aantal juveniele exemplaren"
        },
        "pinpoint_target": "observation",
        "groups": {
            "9": {"pk": 9, "subjects": [29, 30], "name": "Vissen"},
            "3": {"pk": 3, "subjects": [25, 17, 18, 19, 1, 2], "name": "Reptielen en amfibie\u00ebn"}},
        "species": {}
    },
    "initial_data": []
};

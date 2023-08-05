/* eslint-disable no-unused-vars, quotes */

var options = {
    // hidden field to put the serialized data in.
    output_selector: '[name=samples]'
};

var data = {
    "protocol": {
        "name": "Telling uitvliegers",
        "pinpoint_target": "observation",
        "species": {
            // this one is in initial_data, so must be defined here too.
            "2049": {"scientific_name": "Gobio gobio", "pk": 2049, "name": "Gudgeon", "group": 9},
        },
        "groups": {
            "9": {"pk": 9, "name": "Fish", "subjects": [28, 27]},
            "3": {"pk": 3, "name": "Reptiles and Amphibians", "subjects": [12, 13, 14, 15, 16]}
        },
        "subjects": {
            "12": "Larve onbekend",
            "13": "Onvolwassen onbekend",
            "14": "Adult onbekend",
            "15": "Adult man",
            "16": "Adult vrouw",
            "27": "Aantal volwassen exemplaren",
            "28": "Aantal juveniele exemplaren"
        },
        "sample_attrs": {},
        "species_url": '/debug/protocols/extra_species.json',
    },
    "initial_data": [
        {
            "observations": [
                {
                    "name": "1",
                    "latlng": [
                        50.993770727516214,
                        -0.05424499511718751
                    ],
                    "species": 2049,
                    "subject": 28,
                    "count": 3
                }
            ]
        }
    ]
};

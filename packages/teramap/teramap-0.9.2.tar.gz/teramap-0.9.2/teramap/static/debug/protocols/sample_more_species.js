/* eslint-disable no-unused-vars, quotes */

// More species are defined at an url in 'species_url'
var data = {
    "protocol": {
        "name": "Fuikonderzoek amfibie\u00ebn",
        "sample_attrs": {
            "45": {"name": "datum", "type": "date"},
            "43": {"name": "tijd", "type": "time"},
            "34": {
                "name": "Fuiktype",
                "type": "choices",
                "choices": [
                    [null, "--"],
                    ["Vermandel fuik", "Vermandel fuik"],
                    ["Flesfuik", "Flesfuik"],
                    ["Vouwfuik", "Vouwfuik"],
                    ["Drijvende fuik", "Drijvende fuik"],
                    ["Schietfuik", "Schietfuik"],
                    ["ander type fuik", "ander type fuik"]
                ]
            }
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
        "pinpoint_target": "sample",
        "groups": {
            "9": {"pk": 9, "name": "Fish", "subjects": [28, 27], },
            "3": {"pk": 3, "name": "Reptiles and Amphibians", "subjects": [12, 13, 14, 15, 16]}
        },
        "species_url": '/debug/protocols/extra_species.json',
        "species": {
            "2184": {"scientific_name": "Rutilus rutilus", "pk": 2184, "name": "", "group": 9}
        }
    },
    "initial_data": [{
        "name": "1",
        "observations": [{"species": 2184, "subject": 28, "count": 323}],
        "attributes": {"34": "Flesfuik", "43": "15:24", "45": "2014-03-23"},
        "latlng": [51.003169, -0.158972]
    }]
};

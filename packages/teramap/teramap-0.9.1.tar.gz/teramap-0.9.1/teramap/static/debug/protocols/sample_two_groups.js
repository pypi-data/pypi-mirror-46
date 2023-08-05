/* eslint-disable no-unused-vars, quotes */

// cannot add fish (or any from the second group in the modal).
// https://trello.com/c/KRMSEbhU/388-select-species
var data = {
    "protocol": {
        "name": "Fuikonderzoek amfibie\u00ebn",
        "sample_attrs": {
            "34": {"name": "Fuiktype", "choices": [[null, "--"], ["Vermandel fuik", "Vermandel fuik"], ["Flesfuik", "Flesfuik"], ["Vouwfuik", "Vouwfuik"], ["Drijvende fuik", "Drijvende fuik"], ["Schietfuik", "Schietfuik"], ["ander type fuik", "ander type fuik"]]}
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
            "9": {"pk": 9, "subjects": [28, 27], "name": "Fish"},
            "3": {"pk": 3, "subjects": [12, 13, 14, 15, 16], "name": "Reptiles and Amphibians"}
        },
        "species": {
            // fish
            "2163": {"scientific_name": "Perca fluviatilis", "pk": 2163, "name": "European perch", "group": 9},
            "2176": {"scientific_name": "Scardinius erythrophthalmus", "pk": 2176, "name": "Rudd", "group": 9},
            "2049": {"scientific_name": "Gobio gobio", "pk": 2049, "name": "Gudgeon", "group": 9},
            "2184": {"scientific_name": "Rutilus rutilus", "pk": 2184, "name": "", "group": 9},
            "2185": {"scientific_name": "Rhodeus amarus", "pk": 2185, "name": "Bitterling", "group": 9},
            "2195": {"scientific_name": "Pungitius pungitius", "pk": 2195, "name": "", "group": 9},
            "2196": {"scientific_name": "Pseudorasbora parva", "pk": 2196, "name": "", "group": 9},
            "2117": {"scientific_name": "Carassius gibelio", "pk": 2117, "name": "Prussian carp", "group": 9},
            "2082": {"scientific_name": "Barbatula barbatula", "pk": 2082, "name": "Stone loach", "group": 9},
            "2130": {"scientific_name": "Gasterosteus aculeatus", "pk": 2130, "name": "Three-spined stickleback", "group": 9},

            // Reptiles and Amphibians
            "80687": {"scientific_name": "Bufo calamita", "pk": 80687, "name": "", "group": 3},
            "438": {"scientific_name": "Ichthyosaura alpestris", "pk": 438, "name": "Alpine Newt", "group": 3},
            "440": {"scientific_name": "Rana temporaria", "pk": 440, "name": "Common Frog", "group": 3},
            "442": {"scientific_name": "Bufo bufo", "pk": 442, "name": "Common Toad", "group": 3},
            "444": {"scientific_name": "Pelophylax spec.", "pk": 444, "name": "Green Frog spec.", "group": 3},
            "446": {"scientific_name": "Rana arvalis", "pk": 446, "name": "Moor Frog", "group": 3},
            "447": {"scientific_name": "Triturus cristatus", "pk": 447, "name": "Northern Crested Newt", "group": 3},
            "448": {"scientific_name": "Lissotriton vulgaris", "pk": 448, "name": "Smooth Newt", "group": 3},
            "449": {"scientific_name": "Pelobates fuscus", "pk": 449, "name": "Common Eurasian Spadefoot", "group": 3},
            "451": {"scientific_name": "Pelophylax ridibundus", "pk": 451, "name": "Eurasian Marsh Frog", "group": 3},
            "453": {"scientific_name": "Pelophylax lessonae", "pk": 453, "name": "Pool Frog", "group": 3},
            "2118": {"scientific_name": "Carassius auratus", "pk": 2118, "name": "", "group": 3},
            "456": {"scientific_name": "Lissotriton helveticus", "pk": 456, "name": "Palmate Newt", "group": 3},
            "457": {"scientific_name": "Alytes obstetricans", "pk": 457, "name": "Midwife Toad", "group": 3},
            "458": {"scientific_name": "Salamandra salamandra", "pk": 458, "name": "Fire Salamander", "group": 3},
            "2270": {"scientific_name": "Pelophylax kl. esculentus", "pk": 2270, "name": "Edible Frog", "group": 3},

        }
    },
    "initial_data": []
};

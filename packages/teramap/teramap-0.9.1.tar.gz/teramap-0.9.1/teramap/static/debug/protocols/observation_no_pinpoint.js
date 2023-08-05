/* eslint-disable no-unused-vars, quotes */

var options = {
    mapclick_create: false,
    create_button_selector: '#addSample'
};

var data = {
    "protocol": {
        "name": "Sporenonderzoek faunapassages",
        "sample_attrs": {"14": {"name": "Staalnummer", "choices": null}},
        "subjects": {
            "24": "Aantal verschillende dieren",
            "26": "Aantal verschillende dieren",
            "23": "Aantal verschillende dieren"
        },
        "pinpoint_target": "observation",
        "groups": {
            "1": {"pk": 1, "subjects": [24], "name": "Birds"},
            "2": {"pk": 2, "subjects": [23], "name": "Mammals"},
            "3": {"pk": 3, "subjects": [26], "name": "Reptiles and Amphibians"}
        },
        "species": {
            // Birds
            "150": {"scientific_name": "Turdus merula", "pk": 150, "name": "Common Blackbird", "group": 1},
            "168": {"scientific_name": "Erithacus rubecula", "pk": 168, "name": "European Robin", "group": 1},
            "195": {"scientific_name": "Gallinula chloropus", "pk": 195, "name": "Common Moorhen", "group": 1},
            "198": {"scientific_name": "Anas platyrhynchos", "pk": 198, "name": "Mallard", "group": 1},
            "199": {"scientific_name": "Troglodytes troglodytes", "pk": 199, "name": "Eurasian Wren", "group": 1},
            "348": {"scientific_name": "Rallus aquaticus", "pk": 348, "name": "Water Rail", "group": 1},
            "18926": {"scientific_name": "Aves indet.", "pk": 18926, "name": "Unidentified bird", "group": 1},

            // Mammals
            "376": {"scientific_name": "Martes martes", "pk": 376, "name": "Pine Marten", "group": 2},
            "377": {"scientific_name": "Apodemus sylvaticus", "pk": 377, "name": "Wood Mouse", "group": 2},
            "381": {"scientific_name": "Mustela putorius", "pk": 381, "name": "Western Polecat", "group": 2},
            "596862": {"scientific_name": "Martes foina/martes", "pk": 596862, "name": "Stone or Pine Marten", "group": 2},
            "20123": {"scientific_name": "Soricidae spec.", "pk": 20123, "name": "Soricidae spec.", "group": 2},
            "70044": {"scientific_name": "Mustelidae spec.", "pk": 70044, "name": "Mustelid unknown", "group": 2},
            "417": {"scientific_name": "Lutra lutra", "pk": 417, "name": "Eurasian Otter", "group": 2},
            "421": {"scientific_name": "Martes foina", "pk": 421, "name": "Beech Marten", "group": 2},
            "200878": {"scientific_name": "Myodes glareolus", "pk": 200878, "name": "Bank Vole", "group": 2},
            "431": {"scientific_name": "Mustela nivalis", "pk": 431, "name": "Least Weasel", "group": 2},
            "1509": {"scientific_name": "Rattus norvegicus", "pk": 1509, "name": "Common Rat", "group": 2},
            "20332": {"scientific_name": "Felis catus", "pk": 20332, "name": "Domesticated Cat", "group": 2},

            // Reptiles and Amphibians
            "438": {"scientific_name": "Ichthyosaura alpestris", "pk": 438, "name": "Alpine Newt", "group": 3},
            "440": {"scientific_name": "Rana temporaria", "pk": 440, "name": "Common Frog", "group": 3},
            "442": {"scientific_name": "Bufo bufo", "pk": 442, "name": "Common Toad", "group": 3},
            "444": {"scientific_name": "Pelophylax spec.", "pk": 444, "name": "Green Frog spec.", "group": 3},
        }
    },
    "initial_data": []
};

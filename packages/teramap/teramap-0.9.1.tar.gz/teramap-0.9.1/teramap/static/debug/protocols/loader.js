/* eslint-disable no-unused-vars, no-console */


var known_protocols = [
    'sample',
    'observation',
    'observation_no_pinpoint',
    'observation_no_pinpoint_no_species',
    'observation_remote_species',
    'observation_single_species',
    'observation_single_species_single_subject',
    'sample_two_groups',
    'sample_subject_collapse',
    'sample_no_pinpoint',
    'sample_more_species',
    'sample_more_species_only_remote',
];

function load_protocol(callback) {
    var protocol = location.hash.substr(1);
    if (known_protocols.indexOf(protocol) === -1) {
        console.error('Specified protocol (' + protocol + ') is not in known_protocols');
        protocol = known_protocols[0];
    }
    var filename = 'protocols/' + protocol + '.js';
    console.log('Using protocol', filename);

    var script = document.createElement('script');
    script.src = filename;

    script.onload = callback;
    document.head.appendChild(script);
}

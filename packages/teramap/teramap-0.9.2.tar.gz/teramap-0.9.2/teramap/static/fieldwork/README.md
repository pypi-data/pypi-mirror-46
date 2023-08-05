# Pinpoint input form data magager `Pinpoint`

Input argument `pinpoint_data`, object:

```
{
    protocol: Protocol,
    initial_data: Initial_data,
    [messages: I18n_messages]
}
```

## `protocol` object
```
{
     pinpoint_target: 'observation' or 'sample'
     species: {
        2: {name: "Stag Beetle", is_primary: true, group: 2},
        4: {name: ..., group: 2}
    },
     subjects: {4: "adult male", 7: "adult female"}},
     sample_attrs: {
         4: {name: 'Wind (Bft)'},
         5: {name: 'schaduw', choices: [['geen', 'geen'], ['30%', '30%'], ['60%', '60%'], ['100%', '100%']]
     }
}
```
By default, the form allows any combination between species and subjects.
This often doesn't make sense, for example, number of eggs for a mouse.

To prevent this, the `protocol` object can take a `groups` key to specify subjects
for a certain named group. For each species, one group needs to be specified as seen above.

```
{
    1: {
        pk: 1,
        name: 'Birds',
        subjects: [1, 2, 3]
    },
    2: {
        pk: 2,
        name: 'Mammals',
        subjects: [3, 5, 7]
    }
}
```
This will result in subjects 1, 2, 3 selectable for birds and 3, 5, 7 selectable for mammals.

## `sample_attrs` object

The bare minimum for a sample attribute is to provide a name.
This will result in a standard `<input type="text">` being available with each sample.
If you need different input types, supply a `type` key, valid values are:

```JavaScript
['number', 'color', 'date', 'month', 'password', 'range', 'time', 'text']
```

If a key `choices` containing an array of value/label-pairs is defined, a `<select>` is rendered using those choices, the value for `type` will be ignored.

## `initial_data` object

List of pins containing:
   - a name, pk (if updating)
   - observations, containing a list of observations.

For example:
```
[
    // in case of pinpoint sample:
    {
        pk: 42,
        name: 1,
        latlng: [54, 2],
        attributes: {11: 'value', 12: '6'},
        observations: [
            {species: 2, subject: 2, count: 3, [pk: 4]},
            {species: 2, subject: 3, count: 1, [pk: 4]},
            ...
        ]
     },

     // in case of pinpoint observation, the sample is just a dummy
     // (containing only it's pk while editing)
     {
         pk: 43,
         observations: [
            {species: 2, subject: 2, count: 3, [pk: 4], latlng: [52, 2], name: 1},
            {species: 2, subject: 2, count: 3, [pk: 4], latlng: [52, 3], name: 2},

         ]
     }
]
```

This is also the serialisation format used save the data.

## messages

Translations to be used when rendering, mapping from english to the current language. Can be omitted.

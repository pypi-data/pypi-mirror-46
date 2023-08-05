/*
 * Prevent accidental scrolling on a map if the user only tries to
 * scroll the page.
 * amended from: https://gist.github.com/acdha/9143318
 */
import L from 'leaflet';

var gettext = window.gettext || function (s) { return s; };

var ScrollIntentMessage = L.Control.extend({
    options: {
        position: 'bottomleft'
    },
    onAdd: function () {
        var container = L.DomUtil.create('div', 'scroll-intent-message leaflet-control');

        container.innerHTML = gettext('click map for interaction');

        container.style.fontSize = '20px';
        container.style.backgroundColor = 'white';
        container.style.border = '2px solid gray';
        container.style.borderRadius = '4px';
        container.style.padding = '4px 10px';

        // initially hidden
        container.style.display = 'none';
        return container;
    },
    hide: function () {
        this._container.style.display = 'none';
    },
    show: function () {
        var size = this._map.getSize();
        this._container.style.left = ((size.x - 280) / 2) + 'px';
        this._container.style.bottom = '20px';
        this._container.style.display = 'block';
    }
});

function disableMapInteraction () {
    this.scrollWheelZoom.disable();
    this.touchZoom.disable();
}
function enableMapInteraction (e) {
    L.DomEvent.preventDefault(e);
    this.scrollWheelZoom.enable();
    this.touchZoom.enable();

    this._scrollIntentMessage.hide();
}

function preventAccidentalScroll(map) {
    var control = new ScrollIntentMessage().addTo(map);
    disableMapInteraction.call(map);

    map.on('mouseover', function () {
        if (!map.scrollWheelZoom.enabled()) {
            control.show();
        }
    }, map);
    map.on('mouseout', function () {
        setTimeout(function () {
            control.hide();
        }, 1000);
    });

    map.on('click touch focus dragstart', enableMapInteraction, map);
    map.on('blur', disableMapInteraction, map);

    map._scrollIntentMessage = control;
}
L.Map.include({
    preventAccidentalScroll: function () {
        preventAccidentalScroll(this);
    }
});
export default preventAccidentalScroll;

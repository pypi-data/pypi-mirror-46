
import Pinpoint from './fieldwork/pinpoint.js';
import PinpointController from './fieldwork/pinpoint-controller.js';
import PinpointTable from './fieldwork/pinpoint-table.js';
import PinpointModal from './fieldwork/pinpoint-modal.js';
import {is_primary, Protocol} from './fieldwork/protocol.js';

import './fieldwork/fieldwork.css';

var fieldwork = {
    Protocol,
    PinpointController,
    Pinpoint,
    PinpointModal,
    PinpointTable,
    is_primary
};

export {
    fieldwork
};

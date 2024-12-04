const mongoose = require('mongoose');

const lorawanSchema = new mongoose.Schema({
    deduplicationId: String,
    time: String,
    deviceInfo: Object,
    devAddr: String,
    adr: Boolean,
    dr: Number,
    fCnt: Number,
    fPort: Number,
    confirmed: Boolean,
    data: String,
    rxInfo: Array,
    txInfo: Object,
});

module.exports = mongoose.model('LorawanData', lorawanSchema);

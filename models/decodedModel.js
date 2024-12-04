const mongoose = require('mongoose');

const moment = require('moment-timezone');

const infoSchema = new mongoose.Schema({
    decodedData: {
        type: Object, // Flexible field to store dynamic data
        required: true,
    },
    portNumber: {
        type: Number, // Field to store the port number
        required: true,
    },
    deviceName: {
        type: String, // Field to store the port number
        required: true,
    },
}, { timestamps: true });

infoSchema.methods.toEST = function () {
    const createdAtEST = moment(this.createdAt).tz('America/Indiana/Indianapolis').format('YYYY-MM-DD HH:mm:ss');
    const updatedAtEST = moment(this.updatedAt).tz('America/Indiana/Indianapolis').format('YYYY-MM-DD HH:mm:ss');
    return {
        ...this.toObject(),
        createdAt: createdAtEST,
        updatedAt: updatedAtEST,
    };
};

module.exports = mongoose.model('Info', infoSchema);

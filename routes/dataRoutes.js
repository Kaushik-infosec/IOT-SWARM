const express = require('express');
const { saveLorawanData } = require('../controllers/dataController');

const router = express.Router();

// POST route for saving Lorawan data
router.post('/', saveLorawanData);

module.exports = router;

require('dotenv').config(); // Load environment variables
const express = require('express');
const bodyParser = require('body-parser');
const connectDB = require('./config/db');
const dataRoutes = require('./routes/dataRoutes');
const dataRead = require('./routes/readData');
const cors = require("cors"); 
const app = express();
app.use(cors());
// Middleware for parsing JSON
app.use(bodyParser.json());

// Connect to MongoDB
connectDB();

// Routes
app.use('/api/lorawan', dataRoutes);
app.use('/api/lorawan', dataRead);
// Start the server
const PORT = process.env.PORT || 9000;
const HOST = '0.0.0.0';

app.listen(PORT, HOST, () => {
    console.log(`Server is running on http://${HOST}:${PORT}`);
});


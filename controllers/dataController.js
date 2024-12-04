const LorawanData = require('../models/dataModel');
const Info = require('../models/decodedModel');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

const runDecodeAndSaveToDB = async (inputBytes, timeInterval, portNumber,deviceName) => {
    try {
        // Command to run decode.py
        const command = `python3 decode.py --out output.csv --input_bytes "${inputBytes}" --time_interval ${timeInterval} --port_number ${portNumber}`;
        
        // Execute the decode.py script
        await new Promise((resolve, reject) => {
            exec(command, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error executing command: ${stderr}`);
                    return reject(error);
                }
                console.log(`Command executed successfully: ${stdout}`);
                resolve();
            });
        });

        console.log("Decoding complete. File output.csv created.");

        // Read and parse the output file
        const filePath = path.join(__dirname,"../" ,'output.csv');
        const fileContent = fs.readFileSync(filePath, 'utf8');
        const rows = fileContent.split('\n').filter(row => row.trim() !== '');

        // Parse the CSV into a JSON structure
        const data = {};
        rows.forEach(row => {
            const [field, hex, value, interpreted] = row.split(',').map(item => item.trim());
            if (field) {
                data[field] = {
                    Hex: hex,
                    Value: value,
                    Interpreted: interpreted,
                };
            }
        });

        console.log("Parsed data:", data);

        // Save to MongoDB
        const infoRecord = new Info({
            decodedData: data,
            portNumber,
            deviceName
        });
        await infoRecord.save();

        console.log("Data saved to the database.");
    } catch (error) {
        console.error("Error during decoding or saving to database:", error);
        throw error;
    }
};

// Save data to MongoDB
const saveLorawanData = async (req, res) => {
    try {
        const lorawanData = new LorawanData(req.body); // Parse and save the incoming JSON data
        await lorawanData.save(); // Save to MongoDB
        const { data, fPort } = req.body;
        const deviceName = req.body.deviceInfo.deviceName;
        const dataBuffer = Buffer.from(data, 'base64');
        const dataHex = dataBuffer.toString('hex');
        console.log(dataHex);
        console.log(fPort);
        runDecodeAndSaveToDB(dataHex, 15, fPort, deviceName);
        //send to pyton 
        res.status(201).send({ message: 'Data saved successfully!' });
    } catch (error) {
        console.error(error);
        res.status(500).send({ message: 'Failed to save data', error });
    }
};

module.exports = {
    saveLorawanData,
};

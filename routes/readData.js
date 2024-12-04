const Info = require("../models/decodedModel");
const express = require("express");

const router = express.Router();

// Route to fetch all infos
router.get("/read", async (req, res) => {
    try {
        const infos = await Info.find(); // Fetch all records
        res.status(200).json({ success: true, data: infos });
    } catch (error) {
        console.error("Error fetching infos:", error);
        res.status(500).json({ success: false, error: "Server error" });
    }
});

module.exports = router;
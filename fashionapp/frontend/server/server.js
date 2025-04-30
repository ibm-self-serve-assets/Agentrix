const express = require("express");
const fs = require("fs");
const path = require("path");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());

const filePath = path.join(__dirname, "public", "userdata_complete.json");

// API to update JSON file
app.post("/update-json", (req, res) => {
  fs.writeFile(filePath, JSON.stringify(req.body, null, 2), (err) => {
    if (err) {
      return res.status(500).json({ message: "Failed to update JSON" });
    }
    res.json({ message: "JSON updated successfully" });
  });
});

app.listen(5000, () => console.log("Server running on port 5000"));

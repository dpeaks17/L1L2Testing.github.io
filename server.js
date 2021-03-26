const express = require("express");
const path = require("path");
const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.static(path.join(__dirname)));

app.get("/test-manifest.json", (req, res) =>

	res.sendFile(path.resolve(__dirname, "test-manifest.json"))
);

app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
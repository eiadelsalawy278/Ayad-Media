const express = require("express");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());

// Endpoint لاختبار الاتصال
app.get("/", (req, res) => {
    res.send("Ayad Media Backend is running!");
});

// بدء تشغيل الخادم
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

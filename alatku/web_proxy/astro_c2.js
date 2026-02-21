const express = require('express');
const app = express();
const port = 8888;

app.use(express.json());

let nextCommand = "telemetry";
let results = {};

app.get('/get_cmd', (req, res) => {
    res.send(nextCommand);
    nextCommand = "idle";
});

app.post('/post_res', (req, res) => {
    results = req.body;
    const logEntry = `[${new Date().toISOString()}] Received: ${JSON.stringify(results)}\n`;
    require('fs').appendFileSync('astro_link.log', logEntry);
    console.log("[+] Received Data from Arch Linux:", results);
    res.send("OK");
});

app.get('/get_res', (req, res) => {
    res.json(results);
});

app.listen(port, () => {
    console.log(`ASTRO-C2 listening at http://localhost:${port}`);
});

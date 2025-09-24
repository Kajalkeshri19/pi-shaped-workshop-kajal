const express = require('express');
const app = express();
const port = process.env.PORT || 5000;

const API_KEY = process.env.API_KEY;

app.get('/', (req, res) => {
  res.send(`Hello DevSecOps! (demo key length: ${API_KEY.length})`);
});

app.listen(port, () => {
  console.log(`App running on http://localhost:${port}`);
});

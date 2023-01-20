const express = require("express");
const { pushData } = require("./services/mySqlConnectorService");
const app = express();

app.use(express.json({ limit: "50mb" }));

app.post("/api/v1/auchan/products", (req, res) => {
  pushData(req.body, "AUC");
  return res.send("Received a GET HTTP method");
});

app.post("/api/v1/pingodoce/products", (req, res) => {
  pushData(req.body, "PDC");
  return res.send("Received a GET HTTP method");
});

app.listen(8080, () => console.log(`Example app listening on port 8080!`));

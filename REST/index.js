const express = require("express");
var db = require('./services/mySqlConnectorService')

const app = express();

app.use(express.json({ limit: "50mb" }));

app.post("/api/v1/auchan/products", (req, res) => {
  db.pushData(req.body, "AUC");
  return res.send("Received a POST HTTP method");
});

app.post("/api/v1/pingodoce/products", (req, res) => {
  db.pushData(req.body, "PDC");
  return res.send("Received a POST HTTP method");
});

app.get("/api/products", (req, res) => {
  if(req.query.super != null){
    db.getAllProductsBySuper(req.query.super)
    .then(data => res.jsonp(data))
    .else(e => res.status(501).jsonp(e))  
  }else if(req.query.ean != null){
    db.getAllProductsByEAN(req.query.ean)
    .then(data => res.jsonp(data))
    .else(e => res.status(502).jsonp(e))  
  }else{
    db.getAllProducts()
      .then(data => res.jsonp(data))
      .else(e => res.status(503).jsonp(e))
  }
})

app.get("/api/products", (req, res) => {
  db.getProductsCheaper()
    .then(data => res.jsonp(data))
    .else(e => res.status(504).jsonp(e))
})

app.get("/api/shopList/:id", (req, res) => {
  db.getShopList(req.params.id)
    .then(data => res.jsonp(data))
    .else(e => res.status(505).jsonp(e))
})

app.listen(8080, () => console.log(`API listening on port 8080!`));

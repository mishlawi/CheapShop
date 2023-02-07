const express = require("express");
const router = express.Router();
const { checkAuthenticated, _ } = require("../auth_checks");
var axios = require("axios");

router.get("/", checkAuthenticated, async (req, res) => {
  page = 1;
  offset = 0;
  if (req.query.offset != null && req.query.offset != 0) {
    page = req.query.offset / 30 + 1;
    offset = req.query.offset;
  }
  return await axios(
    "http://localhost:8080/api/productsCheaper?offset=" + offset
  )
    .then((resp) => {
      console.log(resp.data, "\n\ndata", offset);
      res.render("products", {
        products: resp.data[0],
        page: page,
        perPage: 30,
        total: resp.data[1]["COUNT('total')"],
      });
    })
    .catch((e) => console.log(e));
});

router.get("/:ean", checkAuthenticated, async (req, res) => {
  return await axios("http://localhost:8080/api/products?ean=" + req.params.ean)
    .then((resp) => {
      res.render("product", { produto: resp.data });
    })
    .catch((e) => console.log(e));
});

module.exports = router;

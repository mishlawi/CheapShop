const express = require("express");
const router = express.Router();
const { checkAuthenticated, _ } = require("../auth_checks");
var axios = require("axios");

// COMO VERIFICAR A LISTA DE COMPRAS QUE QUERO??
router.get("/", checkAuthenticated, async (req, res) => {
  return await axios("http://localhost:8080/api/shopList/" + req.user.EmailUser)
    .then((resp) => res.render("shoplist", { listaCompras: resp.data }))
    .catch((e) => console.log(e));
});

router.post("/", checkAuthenticated, async (req, res) => {});

module.exports = router;

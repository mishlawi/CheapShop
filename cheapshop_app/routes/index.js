var express = require("express");
var router = express.Router();
const { checkAuthenticated, _ } = require("../auth_checks");

/* GET home page. */
router.get("/", checkAuthenticated, async (req, res, next) => {
  res.render("index", { name: await req.user.Nome });
});

// TODO - ADICIONAR PRODUTO À LISTA DE COMPRAS
// TODO - LISTA DE COMPRAS DO PRODUTO MAIS BARATO
// TODO - LISTA DE COMPRAS DO MESMO SUPERMERCADO

module.exports = router;

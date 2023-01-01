var express = require("express");
var router = express.Router();
var { checkAuthenticated, _ } = require("../auth_checks");

/* GET home page. */
router.get("/", checkAuthenticated, async (req, res, next) => {
  res.render("index", { name: await req.user.name });
});

module.exports = router;

var express = require("express");
var router = express.Router();
var { checkAuthenticated, _ } = require("../auth_checks");

/* LOGOUT. */
router.delete("/", checkAuthenticated, (req, res, next) => {
  req.logOut(function (err) {
    if (err) {
      return next(err);
    }
    res.redirect("/login");
  });
});

module.exports = router;

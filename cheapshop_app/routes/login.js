const express = require("express");
const router = express.Router();
const passport = require("passport");
const { _, checkNotAuthenticated } = require("../auth_checks");

/* GET login page. */
router.get("/login", checkNotAuthenticated, (req, res, next) => {
  res.render("login");
});

/* POST login */
router.post(
  "/login",
  checkNotAuthenticated,
  passport.authenticate("local", {
    successRedirect: "/",
    failureRedirect: "/login",
    failureFlash: true,
  })
);

module.exports = router;

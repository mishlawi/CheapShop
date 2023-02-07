const express = require("express");
const router = express.Router();
const passport = require("passport");
const { _, checkNotAuthenticated } = require("../auth_checks");

/* GET login page. */
router.get("/", checkNotAuthenticated, (req, res, next) => {
  res.render("login");
});

/* POST login */
router.post(
  "/",
  checkNotAuthenticated,
  passport.authenticate("local", {
    successRedirect: "/produtos",
    failureRedirect: "/login",
    failureFlash: true,
  })
);

module.exports = router;

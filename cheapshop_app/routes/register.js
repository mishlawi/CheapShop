const express = require("express");
const router = express.Router();
const bcrypt = require("bcrypt");
const { _, checkNotAuthenticated } = require("../auth_checks");
const User = require("../db_conn");

/* GET register page. */
router.get("/", checkNotAuthenticated, (req, res, next) => {
  res.render("register", { message: req.flash("error_message") });
});

/* POST new user. */
router.post("/", checkNotAuthenticated, async (req, res, next) => {
  try {
    const hashPassword = await bcrypt.hash(req.body.password, 10);
    if (!(await User.get_user_by_email(req.body.email))) {
      User.register_user(
        req.body.email,
        req.body.name,
        hashPassword,
        req.body.address
      );
      res.redirect("/login");
    } else {
      req.flash("error_message", "Email already registered, please login.");
      res.render("register", { message: req.flash("error_message") });
    }
  } catch (e) {
    console.log(e);
    res.redirect("/register");
  }
});

module.exports = router;

const express = require("express");
const router = express.Router();
const bcrypt = require("bcrypt");
const { _, checkNotAuthenticated } = require("../auth_checks");
const User = require("../db_conn");

/* GET register page. */
router.get("/register", checkNotAuthenticated, (req, res, next) => {
  res.render("register");
});

/* POST new user. */
router.post("/register", checkNotAuthenticated, async (req, res, next) => {
  try {
    const hashPassword = await bcrypt.hash(req.body.password, 10);

    User.register_user(req.body.email, req.body.name, hashPassword, "");
    // const user = new User({
    //   _id: req.body.email,
    //   name: req.body.name,
    //   email: req.body.email,
    //   password: hashPassword,
    // });
    // user.save().then(
    //   () => console.log("One entry added"),
    //   (err) => console.log(err)
    // );
    res.redirect("/login");
  } catch {
    res.redirect("/register");
  }
});

module.exports = router;

var express = require("express");
var router = express.Router();
const { checkAuthenticated, checkNotAuthenticated } = require("../auth_checks");
const bcrypt = require("bcrypt");
const User = require("../db_conn");
const passport = require("passport");
var axios = require("axios");

/* GET home page. */
router.get("/", checkAuthenticated, async (req, res, next) => {
  res.render("index", { name: await req.user.Nome });
});

/* GET login page. */
router.get("/login", checkNotAuthenticated, (req, res, next) => {
  res.render("login");
});

/* POST login */
router.post(
  "/login",
  checkNotAuthenticated,
  passport.authenticate("local", {
    successRedirect: "/produtos",
    failureRedirect: "/login",
    failureFlash: true,
  })
);

/* LOGOUT. */
router.delete("/logout", checkAuthenticated, (req, res, next) => {
  req.logOut(function (err) {
    if (err) {
      return next(err);
    }
    res.redirect("/login");
  });
});

/* GET register page. */
router.get("/register", checkNotAuthenticated, (req, res, next) => {
  res.render("register", { message: req.flash("error_message") });
});

/* POST new user. */
router.post("/register", checkNotAuthenticated, async (req, res, next) => {
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
  } catch (e) {
    console.log(e);
    res.redirect("/register");
  }
});

router.get("/produtos", checkAuthenticated, async (req, res) => {
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

router.get("/produto/:ean", checkAuthenticated, async (req, res) => {
  return await axios("http://localhost:8080/api/products?ean=" + req.params.ean)
    .then((resp) => {
      res.render("product", { produto: resp.data });
    })
    .catch((e) => console.log(e));
});

// COMO VERIFICAR A LISTA DE COMPRAS QUE QUERO??
router.get("/listaCompras", checkAuthenticated, async (req, res) => {
  return await axios("http://localhost:8080/api/shopList/" + req.user.EmailUser)
    .then((resp) => res.render("shoplist", { listaCompras: resp.data }))
    .catch((e) => console.log(e));
});

router.post("/listaCompras", checkAuthenticated, async (req, res) => {});

// TODO - ADICIONAR PRODUTO À LISTA DE COMPRAS
// TODO - LISTA DE COMPRAS DO PRODUTO MAIS BARATO
// TODO - LISTA DE COMPRAS DO MESMO SUPERMERCADO

module.exports = router;

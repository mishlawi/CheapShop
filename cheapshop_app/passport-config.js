const LocalStrategy = require("passport-local").Strategy;
const bcrypt = require("bcrypt");

var User = require("./db_conn");

function initialize(passport) {
  const authenticateUser = async (email, password, done) => {
    var user = await User.get_user_by_email(email);
    console.log(user);
    if (user == null) {
      return done(null, false, { message: "No user with that email" });
    }

    try {
      if (await bcrypt.compare(password, user.password)) {
        return done(null, user);
      } else {
        return done(null, false, { message: "Password incorrect" });
      }
    } catch (e) {
      return done(e);
    }
  };
  passport.use(new LocalStrategy({ usernameField: "email" }, authenticateUser));

  passport.serializeUser((user, done) => done(null, user.iduser));
  passport.deserializeUser(async (id, done) =>
    done(null, await User.get_user_by_id(id))
  );
}

module.exports = initialize;

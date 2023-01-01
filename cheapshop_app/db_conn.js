const mongoose = require("mongoose");
const mysql = require("mysql2");

const con = mysql.createConnection({
  host: process.env.MYSQL_HOST,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASSWORD,
  database: process.env.MYSQL_DATABASE,
});
con.connect();

const register_user = (email, name, password, address) => {
  var prepared_statement =
    "INSERT INTO user (EmailUser, Nome, Pass, Morada) VALUES (?,?,?,?)";

  con.execute(
    prepared_statement,
    [email, name, password, address],
    function (err, result) {
      if (err) throw err;
      console.log("1 record inserted");
    }
  );
};

const get_user_by_email = async (email) => {
  return new Promise(data => {
    var prepared_statement = "SELECT * FROM user WHERE EmailUser = ?";

    con.execute(prepared_statement, [email], function (err, result) {
      if (err) throw err;
      data(result[0])
    });
  })
};

const get_user_by_id = async (email) => {
  return new Promise(data => {
    var prepared_statement = "SELECT * FROM user WHERE EmailUser = ?";

    con.execute(prepared_statement, [email], function (err, result) {
      if (err) throw err;
      data(result[0]);
    });
  });
};

mongoose.set("strictQuery", false);

mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const userSchema = new mongoose.Schema({
  _id: String,
  name: String,
  email: String,
  password: String,
});

const User = mongoose.model("User", userSchema);

const getUserByEmail = async (email) =>
  await User.findOne({
    email: email,
  });

const getUserById = async (id) =>
  await User.findOne({
    _id: id,
  });

module.exports = User;
module.exports.getUserByEmail = getUserByEmail;
module.exports.getUserById = getUserById;
module.exports.register_user = register_user;
module.exports.get_user_by_email = get_user_by_email;
module.exports.get_user_by_id = get_user_by_id;

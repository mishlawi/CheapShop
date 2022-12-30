const mongoose = require("mongoose");

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

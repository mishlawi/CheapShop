// // Importing mysql and fs packages
// // Requiring modules
const mysql = require("mysql2");
require("dotenv").config();

// Establish connection to the database
let con = mysql.createConnection({
  host: process.env.HOST,
  port: process.env.PORT,
  user: process.env.USERNAME,
  password: process.env.PASSWORD,
  database: process.env.DBNAME,
});

function pushData(jsonData, Superficie) {
  console.log("Starting data push..");
  for (i = 0; i < jsonData.length; i++) {
    // Extract data from each object in the array
    var Nome = jsonData[i]["Nome"],
      Marca = jsonData[i]["Marca"],
      Quantidade = jsonData[i]["Quantidade"],
      PrecoPrim = jsonData[i]["Preço Primário"],
      PrecoUni = jsonData[i]["Preço Por Unidade"],
      Promo = jsonData[i]["Promo"],
      EAN = jsonData[i]["EAN"];

    var insertStatement = `INSERT INTO cheapshop.item (Nome, EAN, Marca, Quantidade, PrecoPrim, PrecoUni, Promo, superficie_IDsup) 
                values(?, ?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE Nome = ?, Marca = ?, Quantidade = ?, PrecoPrim = ?, PrecoUni = ?, Promo = ?;`;
    var items = [
      Nome,
      EAN,
      Marca,
      Quantidade,
      PrecoPrim,
      PrecoUni,
      Promo,
      Superficie,
      Nome,
      Marca,
      Quantidade,
      PrecoPrim,
      PrecoUni,
      Promo,
    ];

    // Insert data into database
    con.query(insertStatement, items, (err, results, fields) => {
      if (err) {
        console.log("Unable to insert item at row ", i + 1);
        return console.log(err);
      }
    });
  }
  console.log("Data push complete!");
}

module.exports = { pushData };

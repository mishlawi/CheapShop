// Importing mysql and fs packages
// Requiring modules
const mysql = require("mysql2");
const fs = require('fs');

// Database credentials
const hostname = "localhost",
    username = "root",
    password = "password",
    databsename = "cheapshop"
  
// Establish connection to the database
let con = mysql.createConnection({
    host: hostname,
    user: username,
    password: password,
    database: databsename,
});

// Read JSON file
const jsonFile = fs.readFileSync('./data.json');

// Parse JSON data
const jsonData = JSON.parse(jsonFile);

var sql = "INSERT INTO cheapshop.superficie (Nome, IDsup, Website) values('Froiz', 1, 'https://www.froiz.pt');"
    con.query(sql, function (err, result) {
      if (err) throw err;
      console.log("Inserted to SUPERFICIE");
    });

// Loop through the JSON data
for (let i = 0; i < jsonData.length; i++) {
  // Extract data from each object in the array
  var Nome = jsonData[i]["Nome"],
      Marca = jsonData[i]["Marca"],
      Quantidade = jsonData[i]["Quantidade"],
      PrecoPrim = jsonData[i]["Preço Primário"],
      PrecoUni = jsonData[i]["Preço Por Unidade"],
      Promo = jsonData[i]["Promo"],
      //EAN = jsonData[i]["EAN"],
      IDitem = i,
      EAN = i,
      Superficie = 1

  var insertStatement = 
  `INSERT INTO cheapshop.item (Nome, IDitem, EAN, Marca, Quantidade, PrecoPrim, PrecoUni, Promo, superficie_IDsup) 
  values(?, ?, ?, ?, ?, ?, ?, ?, ?)`;
  var items = [Nome, IDitem, EAN, Marca, Quantidade, PrecoPrim, PrecoUni, Promo, Superficie];

  // Insert data into database
  con.query(insertStatement, items, 
      (err, res) => {
          console.log(err || res);
      }
  );
}
console.log("All items stored into database successfully");
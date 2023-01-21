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
let jsonFile = [fs.readFileSync('Data\\ProdutosAuchan.json'), fs.readFileSync('Data\\ProdutosPingoDoce.json')];
//const jsonFile0 = fs.readFileSync('C:\\Users\\hugom\\Desktop\\MIEI\\5ANO\\CheapShop\\DataBase\\Data\\ProdutosAuchan.json');
//const jsonFile1 = fs.readFileSync('C:\\Users\\hugom\\Desktop\\MIEI\\5ANO\\ProdutosAuchan.json');
let k = 0;
let i;
for (let j = 0; j<jsonFile.length;j++){
// Parse JSON data

const Super = ['AUC','PDC','FRO','INM','CON','ECI','ELE'];
let SUP = Super[j];
const jsonData = JSON.parse(jsonFile[j]);
// Loop through the JSON data
for (i = 0; i < jsonData.length; i++) {
  // Extract data from each object in the array
  var Nome = jsonData[i]["Nome"],
      Marca = jsonData[i]["Marca"],
      Quantidade = jsonData[i]["Quantidade"],
      PrecoPrim = jsonData[i]["Preço Primário"],
      PrecoUni = jsonData[i]["Preço Por Unidade"],
      Promo = jsonData[i]["Promo"],
      EAN = jsonData[i]["EAN"]
      //IDitem = k + i

  let Superficie = SUP
  var insertStatement = 
  `INSERT INTO cheapshop.item (Nome, EAN, Marca, Quantidade, PrecoPrim, PrecoUni, Promo, superficie_IDsup) 
  values(?, ?, ?, ?, ?, ?, ?, ?)`;
  var items = [Nome, EAN, Marca, Quantidade, PrecoPrim, PrecoUni, Promo, Superficie];

  // Insert data into database
  con.query(insertStatement, items, 
      (err, results, fields) => {
        if (err) {
            console.log("Unable to insert item at row ", i + 1);
                return console.log(err);
        }
      }
  );
}
k += i;
console.log("All items from", SUP, "stored into database successfully");
}
console.log("All items stored into database successfully");

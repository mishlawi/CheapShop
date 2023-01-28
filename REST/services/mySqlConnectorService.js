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

module.exports.pushData = (jsonData, Superficie) => {
  console.log("Starting data push..");
  for (i = 0; i < jsonData.length; i++) {
    // Extract data from each object in the array
    var Nome = jsonData[i]["Nome"],
      Marca = jsonData[i]["Marca"],
      Quantidade = jsonData[i]["Quantidade"],
      PrecoPrim = jsonData[i]["Preco Primario"],
      PrecoUni = jsonData[i]["Preco Por Unidade"],
      Promo = jsonData[i]["Promo"],
      EAN = jsonData[i]["EAN"],
      LinkImagem = jsonData[i]["Link Imagem"],
      LinkProduto = jsonData[i]["Link Produto"];

    var insertStatement = `INSERT INTO cheapshop.item (Nome, EAN, Marca, Quantidade, PrecoPrim, PrecoUni, Promo, LinkImagem, LinkProduto, superficie_IDsup) 
                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE Nome = ?, Marca = ?, Quantidade = ?, PrecoPrim = ?, PrecoUni = ?, Promo = ?, LinkImagem = ?, LinkProduto = ?;`;
    var items = [
      Nome,
      EAN,
      Marca,
      Quantidade,
      PrecoPrim,
      PrecoUni,
      Promo,
      LinkImagem,
      LinkProduto,
      Superficie,
      Nome,
      Marca,
      Quantidade,
      PrecoPrim,
      PrecoUni,
      Promo,
      LinkImagem,
      LinkProduto,
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

module.exports.getAllProducts = () => {
  query = "SELECT * FROM cheapshop.item"
  con.query(query, (err, results, fields) => {
    if (err) return console.log(err);
    return results;
  });
}

module.exports.getProductsCheaper = () => {
  query = "SELECT DISTINCT item.EAN, MIN(item.PrecoUni) FROM item GROUP BY item.EAN"
  con.query(query, (err, results, fields) => {
    if (err) return console.log(err);
    return results;
  });
}

module.exports.getAllProductsBySuper = (id) => {
  query = `SELECT * FROM cheapshop.item WHERE superficie_IDsup = ${id}`
  con.query(query, (err, results, fields) => {
    if (err) return console.log(err);
    return results;
  });
}

module.exports.getAllProductsByEAN = (ean) => {
  query = `SELECT * FROM cheapshop.item WHERE ean = ${ean}`
  con.query(query, (err, results, fields) => {
    if (err) return console.log(err);
    return results;
  });
}


module.exports.getShopList = (userId) => {
  query = `SELECT * FROM cheapshop.lista WHERE user_EmailUser == ${userID}`
  con.query(query, (err, results, fields) => {
    if (err) return console.log(err);
    return results;
  });
}
/*
module.exports.addProdToShopCart = (qtd, userId, ean, sup) => {
  console.log("Starting data push..");

    var insertStatement = `INSERT INTO cheapshop.lista (Quantidade, EAN, Marca, Quantidade, PrecoPrim, PrecoUni, Promo, LinkImagem, LinkProduto, superficie_IDsup) 
                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE Nome = ?, Marca = ?, Quantidade = ?, PrecoPrim = ?, PrecoUni = ?, Promo = ?, LinkImagem = ?, LinkProduto = ?;`;
    var items = [
      Nome,
      EAN,
      Marca,
      Quantidade,
      PrecoPrim,
      PrecoUni,
      Promo,
      LinkImagem,
      LinkProduto,
      Superficie,
      Nome,
      Marca,
      Quantidade,
      PrecoPrim,
      PrecoUni,
      Promo,
      LinkImagem,
      LinkProduto,
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
}*/
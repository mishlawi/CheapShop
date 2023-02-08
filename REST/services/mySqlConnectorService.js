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
};

module.exports.getAllProducts = (offset) => {
  query = "SELECT * FROM cheapshop.item LIMIT 30 OFFSET ?";
  items = [offset];
  return new Promise((data) => {
    con.query(query, items, (err, results, fields) => {
      if (err) return console.log(err);
      data(results);
    });
  });
};

module.exports.getTotalNumberOfProducts = () => {
  query = "SELECT COUNT('total') FROM cheapshop.item";

  return new Promise((data) => {
    con.query(query, (err, results, fields) => {
      if (err) return console.log(err);
      data(results[0]);
    });
  });
};

module.exports.getProductsCheaper = (offset) => {
  query =
    "SELECT prod.* FROM cheapshop.item AS prod JOIN (SELECT DISTINCT EAN, MIN(PrecoUni) AS PrecoUni FROM item GROUP BY EAN LIMIT 30 OFFSET ?) AS min ON prod.ean = min.ean AND prod.PrecoUni = min.PrecoUni";
  items = [parseInt(offset)];
  return new Promise((data) => {
    con.query(query, items, (err, results, fields) => {
      if (err) return console.log(err);
      data(results);
    });
  });
};

module.exports.getAllProductsBySuper = (id) => {
  query = `SELECT * FROM cheapshop.item WHERE superficie_IDsup = ?`;
  items = [id];
  return new Promise((data) => {
    con.query(query, items, (err, results, fields) => {
      if (err) return console.log(err);
      data(results);
    });
  });
};

module.exports.getAllProductsByEAN = (ean) => {
  query = `SELECT * FROM cheapshop.item WHERE ean = ?`;
  items = [ean];
  return new Promise((data) => {
    con.query(query, items, (err, results, fields) => {
      if (err) return console.log(err);
      data(results);
    });
  });
};

module.exports.getShopList = (userId) => {
  query = `SELECT * FROM cheapshop.lista WHERE user_EmailUser = ?`;
  items = [userId];
  return new Promise((data) => {
    con.query(query, items, (err, results, fields) => {
      if (err) return console.log(err);
      data(results);
    });
  });
};


module.exports.addProdToShopCart = (Quantidade, user_EmailUser, item_EAN, item_superficie_IDsup) => {
  console.log("Adding product to cart..");

    var insertStatement = `INSERT INTO cheapshop.lista (Quantidade, user_EmailUser, item_EAN, item_superficie_IDsup) 
                values(?, ?, ?, ?) ON DUPLICATE KEY UPDATE Quantidade = ?, user_EmailUser = ?, item_EAN = ?, item_superficie_IDsup = ?;`;
    
    var items = [
      Quantidade,
      user_EmailUser,
      item_EAN,
      item_superficie_IDsup,
    ];

    // Insert data into database
    con.query(insertStatement, items, (err, results, fields) => {
      if (err) {
        console.log("Unable to insert product to cart");
        return console.log(err);
      }
    });
}
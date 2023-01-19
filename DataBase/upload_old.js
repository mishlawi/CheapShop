// Importing mysql and csvtojson packages
// Requiring module
const csvtojson = require('csvtojson');
const mysql = require("mysql2");
  
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
  
/* con.connect((err) => {
    if (err) return console.error(
            'error: ' + err.message);
  
    con.query("DROP TABLE sample", 
        (err, drop) => {
  
        // Query to create table "sample"   ------------------------ COLOCAR AQUI PARAMETOS DE CADA TABLE
        var createStatament = 
        "CREATE TABLE sample(Name char(50), " +
        "Email char(50), Age int, city char(30))"
  
        // Creating table "sample"   ------------------------------- CRIAR CADA TABLE (UNECESSARY?)
        con.query(createStatament, (err, drop) => {
            if (err)
                console.log("ERROR: ", err);
        });
    });
}); */
  
// CSV file names
const Froiz = 'C:\\Users\\hugom\\Desktop\\MIEI\\5ANO\\ProdutosFroiz.csv';
var sql = "INSERT INTO cheapshop.superficie (Nome, IDsup, Website) values('Froiz', 1, 'https://www.froiz.pt');"
    con.query(sql, function (err, result) {
      if (err) throw err;
      console.log("Inserted to SUPERFICIE");
    });

// const Inter = '.\Users\hugom\Desktop\MIEI\5ANO\ProdutosFroiz.csv';
// const Conti = '.\Users\hugom\Desktop\MIEI\5ANO\ProdutosFroiz.csv';
// const Pingo = '.\Users\hugom\Desktop\MIEI\5ANO\ProdutosFroiz.csv';
// const Aucha = '.\Users\hugom\Desktop\MIEI\5ANO\ProdutosFroiz.csv';
// const Aucha = '.\Users\hugom\Desktop\MIEI\5ANO\ProdutosFroiz.csv';

csvtojson().fromFile(Froiz).then(source => {
  
    // Fetching the data from each row       -------------------------  PEGAR EM CADA PARAMETRO DO CSV
    // and inserting to the table "sample"             ---------------  AQUI COLOCA NA TABLE SAMPLE
    //                                                    ------------  DIVIDIR POR TABLES OS PARAMETROS A PREENCHER
    for (var i = 0; i < source.length; i++) {     
        var Nome = source[i]["Nome"],
            Marca = source[i]["Marca"],
            Quantidade = source[i]["Quantidade"],
            PrecoPrim = source[i]["Preço Primário"],
            PrecoUni = source[i]["Preço Por Unidade"],
            Promo = source[i]["Promo"],
            //EAN = source[i]["EAN"],
            IDitem = i,
            EAN = i,
            Superficie = 1

        var insertStatement = 
        `INSERT INTO cheapshop.item (Nome, IDitem, EAN, Marca, Quantidade, PrecoPrim, PrecoUni, Promo, superficie_IDsup) 
        values(?, ?, ?, ?, ?, ?, ?, ?, ?)`;
        var items = [Nome, IDitem, EAN, Marca, Quantidade, PrecoPrim, PrecoUni, Promo, Superficie];
  
        // Inserting data of current row
        // into database
        con.query(insertStatement, items, 
            (err, results, fields) => {
            if (err) {
                console.log(
    "Unable to insert item at row ", i + 1);
                return console.log(err);
            }
        });
    }
    console.log(
"All items stored into database successfully");
});
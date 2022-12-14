// Importing mysql and csvtojson packages
// Requiring module
const csvtojson = require('csvtojson');
const mysql = require("mysql2");
  
// Database credentials
const hostname = "localhost",
    username = "root",
    password = "root",
    databsename = "mydb"
  
  
// Establish connection to the database
let con = mysql.createConnection({
    host: hostname,
    user: username,
    password: password,
    database: databsename,
});
  
con.connect((err) => {
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
});
  
// CSV file name
const fileName = "sample.csv";
  
csvtojson().fromFile(fileName).then(source => {
  
    // Fetching the data from each row       -------------------------  PEGAR EM CADA PARAMETRO DO CSV
    // and inserting to the table "sample"             ---------------  AQUI COLOCA NA TABLE SAMPLE
    //                                                    ------------  DIVIDIR POR TABLES OS PARAMETROS A PREENCHER
    for (var i = 0; i < source.length; i++) {     
        var Name = source[i]["Name"],
            Email = source[i]["Email"],
            Age = source[i]["Age"],
            City = source[i]["City"]
  
        var insertStatement = 
        `INSERT INTO sample values(?, ?, ?, ?)`;
        var items = [Name, Email, Age, City];
  
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
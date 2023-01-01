# CheapShop WebApp – Session Management

To run the app you must have mysql installed and running and the database schema created on the server, to make the connection from the app to mysql you need to create a file named `.env` (on the root directory) and add the following key=value pairs:

```
MYSQL_HOST=<host>
MYSQL_USER=<user>
MYSQL_PASSWORD=<password>
MYSQL_DATABASE=<database_name>
```

Run following commands to start the app:

```
npm i
```

For develop mode that updates everytime there's a change in the code:

```
npm run dev
```

For production mode:

```
npm start
```

Then on your browser go to `localhost:3000` and enjoy!

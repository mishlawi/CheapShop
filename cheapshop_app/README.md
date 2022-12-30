# CheapShop WebApp – Session Management

To run the app you must have mongo installed and running, and to make the connection from the app to mongo you need to create a file named `.env` (on the root directory) and add the following key=value pair: `MONGODB_URI=<your mongodb connection URI>` to the file.

The URI must be something like `mongodb://<ip>:<port>/<collection name>`

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

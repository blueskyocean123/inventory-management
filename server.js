const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.status(200).json("Hello world!");
});

module.exports = app.listen(process.env.PORT || 8000, () =>
  console.log("Server is working")
);

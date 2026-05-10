const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const rateLimit = require("express-rate-limit");

const routes = require("./routes");
const { notFoundMiddleware } = require("./middleware/not-found.middleware");
const { errorMiddleware } = require("./middleware/error.middleware");

const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());

app.use(
  rateLimit({
    windowMs: 15 * 60 * 1000,
    limit: 100,
    message: {
      success: false,
      message: "Too many requests. Please try again later.",
    },
  })
);

app.use("/api", routes);

app.get("/", (req, res) => {
  res.json({
    success: true,
    service: "F.R.I.D.A.Y API",
    message: "Backend API is running",
  });
});

app.use(notFoundMiddleware);
app.use(errorMiddleware);

module.exports = { app };
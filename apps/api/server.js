const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const dotenv = require("dotenv");
const pino = require("pino");

dotenv.config();

const app = express();
const logger = pino({
  transport: {
    target: "pino-pretty",
  },
});

const PORT = process.env.API_PORT || 5000;

app.use(helmet());
app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    success: true,
    service: "F.R.I.D.A.Y API",
    message: "API service is running",
  });
});

app.get("/api/health", (req, res) => {
  res.json({
    success: true,
    service: "F.R.I.D.A.Y API",
    status: "healthy",
    timestamp: new Date().toISOString(),
  });
});

app.listen(PORT, () => {
  logger.info(`F.R.I.D.A.Y API running on http://localhost:${PORT}`);
});
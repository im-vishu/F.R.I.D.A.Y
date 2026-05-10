const dotenv = require("dotenv");

dotenv.config();

const env = {
  NODE_ENV: process.env.NODE_ENV || "development",
  API_PORT: process.env.API_PORT || 5000,

  JWT_SECRET: process.env.JWT_SECRET || "change_this_secret",

  DATABASE_URL: process.env.DATABASE_URL || "",
  REDIS_URL: process.env.REDIS_URL || "",
  QDRANT_URL: process.env.QDRANT_URL || "",

  AI_ORCHESTRATOR_URL:
    process.env.AI_ORCHESTRATOR_URL || "http://localhost:8000",
};

module.exports = { env };
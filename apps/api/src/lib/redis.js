const { createClient } = require("redis");
const { env } = require("../config/env");
const { logger } = require("../config/logger");

const redis = createClient({
  url: env.REDIS_URL,
});

redis.on("error", (error) => {
  logger.error({ error }, "Redis connection error");
});

redis.on("connect", () => {
  logger.info("Redis connected");
});

async function connectRedis() {
  if (!redis.isOpen) {
    await redis.connect();
  }
}

module.exports = {
  redis,
  connectRedis,
};
const { redis } = require("../lib/redis");
const { prisma } = require("../lib/prisma");

async function getHealth(req, res) {
  const health = {
    success: true,
    service: "F.R.I.D.A.Y API",
    status: "healthy",
    modules: {
      api: "online",
      database: "checking",
      redis: "checking",
      auth: "ready",
      security: "enabled",
      rateLimit: "enabled",
    },
    timestamp: new Date().toISOString(),
  };

  try {
    await prisma.$queryRaw`SELECT 1`;
    health.modules.database = "connected";
  } catch {
    health.modules.database = "disconnected";
    health.status = "degraded";
  }

  try {
    await redis.ping();
    health.modules.redis = "connected";
  } catch {
    health.modules.redis = "disconnected";
    health.status = "degraded";
  }

  res.json(health);
}

module.exports = { getHealth };
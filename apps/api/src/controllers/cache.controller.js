const { redis } = require("../lib/redis");

async function getCacheHealth(req, res, next) {
  try {
    await redis.set("friday:cache:health", "online", {
      EX: 60,
    });

    const status = await redis.get("friday:cache:health");

    res.json({
      success: true,
      service: "F.R.I.D.A.Y Redis Cache",
      status,
      ttlSeconds: await redis.ttl("friday:cache:health"),
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    next(error);
  }
}

async function setCacheValue(req, res, next) {
  try {
    const { key, value, ttl = 300 } = req.body;

    if (!key || !value) {
      return res.status(400).json({
        success: false,
        message: "key and value are required",
      });
    }

    const redisKey = `friday:cache:${key}`;

    await redis.set(redisKey, JSON.stringify(value), {
      EX: Number(ttl),
    });

    res.status(201).json({
      success: true,
      message: "Cache value saved",
      key: redisKey,
      ttl,
    });
  } catch (error) {
    next(error);
  }
}

async function getCacheValue(req, res, next) {
  try {
    const { key } = req.params;
    const redisKey = `friday:cache:${key}`;

    const value = await redis.get(redisKey);

    if (!value) {
      return res.status(404).json({
        success: false,
        message: "Cache key not found",
      });
    }

    res.json({
      success: true,
      key: redisKey,
      value: JSON.parse(value),
      ttlSeconds: await redis.ttl(redisKey),
    });
  } catch (error) {
    next(error);
  }
}

module.exports = {
  getCacheHealth,
  setCacheValue,
  getCacheValue,
};
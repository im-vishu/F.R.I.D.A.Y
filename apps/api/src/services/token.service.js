const jwt = require("jsonwebtoken");
const { redis } = require("../lib/redis");
const { env } = require("../config/env");

function getTokenFromHeader(authHeader) {
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return null;
  }

  return authHeader.split(" ")[1];
}

function verifyToken(token) {
  return jwt.verify(token, env.JWT_SECRET);
}

function getTokenTTL(decodedToken) {
  const nowInSeconds = Math.floor(Date.now() / 1000);
  return Math.max(decodedToken.exp - nowInSeconds, 0);
}

async function blacklistToken(token) {
  const decodedToken = verifyToken(token);
  const ttl = getTokenTTL(decodedToken);

  if (ttl > 0) {
    await redis.set(`friday:blacklist:${token}`, "blacklisted", {
      EX: ttl,
    });
  }

  return {
    decodedToken,
    ttl,
  };
}

async function isTokenBlacklisted(token) {
  const result = await redis.get(`friday:blacklist:${token}`);
  return Boolean(result);
}

module.exports = {
  getTokenFromHeader,
  verifyToken,
  blacklistToken,
  isTokenBlacklisted,
};
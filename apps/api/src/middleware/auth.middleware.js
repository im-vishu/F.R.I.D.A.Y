const {
  getTokenFromHeader,
  verifyToken,
  isTokenBlacklisted,
} = require("../services/token.service");

async function authMiddleware(req, res, next) {
  const token = getTokenFromHeader(req.headers.authorization);

  if (!token) {
    return res.status(401).json({
      success: false,
      message: "Authorization token missing",
    });
  }

  try {
    const blacklisted = await isTokenBlacklisted(token);

    if (blacklisted) {
      return res.status(401).json({
        success: false,
        message: "Token has been logged out",
      });
    }

    const decoded = verifyToken(token);

    req.token = token;
    req.user = decoded;

    next();
  } catch {
    return res.status(401).json({
      success: false,
      message: "Invalid or expired token",
    });
  }
}

module.exports = { authMiddleware };
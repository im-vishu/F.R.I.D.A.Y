const express = require("express");
const {
  getCacheHealth,
  setCacheValue,
  getCacheValue,
} = require("../controllers/cache.controller");
const { authMiddleware } = require("../middleware/auth.middleware");

const router = express.Router();

router.get("/health", getCacheHealth);

router.post("/", authMiddleware, setCacheValue);

router.get("/:key", authMiddleware, getCacheValue);

module.exports = router;
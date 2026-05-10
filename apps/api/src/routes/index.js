const express = require("express");

const healthRoutes = require("./health.routes");
const authRoutes = require("./auth.routes");
const cacheRoutes = require("./cache.routes");
const aiRoutes = require("./ai.routes");

const router = express.Router();

router.use("/health", healthRoutes);
router.use("/auth", authRoutes);
router.use("/cache", cacheRoutes);
router.use("/ai", aiRoutes);

module.exports = router;
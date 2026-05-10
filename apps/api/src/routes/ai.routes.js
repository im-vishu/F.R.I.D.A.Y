const express = require("express");
const { chatWithAI } = require("../controllers/ai.controller");
const { authMiddleware } = require("../middleware/auth.middleware");

const router = express.Router();

router.post("/chat", authMiddleware, chatWithAI);

module.exports = router;
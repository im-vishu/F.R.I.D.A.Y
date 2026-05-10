const { z } = require("zod");
const { runOrchestrator } = require("../services/ai.service");

const chatSchema = z.object({
  message: z.string().min(1, "Message is required"),
  sessionId: z.string().optional(),
  context: z.record(z.any()).optional(),
});

async function chatWithAI(req, res, next) {
  try {
    const parsed = chatSchema.parse(req.body);

    const result = await runOrchestrator({
      message: parsed.message,
      userId: req.user.id,
      sessionId: parsed.sessionId || "default-session",
      context: {
        ...(parsed.context || {}),
        source: "api-service",
      },
    });

    res.json({
      success: true,
      service: "F.R.I.D.A.Y API AI Gateway",
      result,
    });
  } catch (error) {
    next(error);
  }
}

module.exports = {
  chatWithAI,
};
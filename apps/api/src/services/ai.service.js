const axios = require("axios");
const { env } = require("../config/env");

async function runOrchestrator({ message, userId, sessionId, context }) {
  const response = await axios.post(
    `${env.AI_ORCHESTRATOR_URL}/orchestrator/run`,
    {
      message,
      user_id: userId,
      session_id: sessionId,
      context,
    },
    {
      timeout: 15000,
    }
  );

  return response.data;
}

module.exports = {
  runOrchestrator,
};
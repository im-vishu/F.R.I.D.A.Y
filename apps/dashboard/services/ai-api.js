import axios from "axios";

const API_BASE_URL = "http://localhost:5000";

export async function sendAIChatMessage({ token, message, sessionId, context }) {
  const response = await axios.post(
    `${API_BASE_URL}/api/ai/chat`,
    {
      message,
      sessionId,
      context,
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
}
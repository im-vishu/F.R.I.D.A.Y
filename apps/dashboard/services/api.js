import axios from "axios";

const API_BASE_URL = "http://localhost:5000";
const GATEWAY_BASE_URL = "http://localhost:5001";

export async function checkApiHealth() {
  const response = await axios.get(`${API_BASE_URL}/api/health`);
  return response.data;
}

export async function checkGatewayHealth() {
  const response = await axios.get(`${GATEWAY_BASE_URL}/gateway/health`);
  return response.data;
}
const express = require("express");
const http = require("http");
const cors = require("cors");
const dotenv = require("dotenv");
const { Server } = require("socket.io");
const pino = require("pino");

dotenv.config();

const app = express();
const server = http.createServer(app);

const logger = pino({
  transport: {
    target: "pino-pretty",
  },
});

const PORT = process.env.REALTIME_GATEWAY_PORT || 5001;

app.use(cors());
app.use(express.json());

const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
  },
});

app.get("/gateway/health", (req, res) => {
  res.json({
    success: true,
    service: "F.R.I.D.A.Y Realtime Gateway",
    status: "healthy",
    timestamp: new Date().toISOString(),
  });
});

io.on("connection", (socket) => {
  logger.info(`Client connected: ${socket.id}`);

  socket.emit("gateway:connected", {
    message: "Connected to F.R.I.D.A.Y realtime gateway",
    socketId: socket.id,
  });

  socket.on("chat:message", (payload) => {
    logger.info(payload);

    socket.emit("chat:response", {
      role: "assistant",
      message: `F.R.I.D.A.Y received: ${payload.message}`,
      timestamp: new Date().toISOString(),
    });
  });

  socket.on("disconnect", () => {
    logger.info(`Client disconnected: ${socket.id}`);
  });
});

server.listen(PORT, () => {
  logger.info(`Realtime Gateway running on http://localhost:${PORT}`);
});
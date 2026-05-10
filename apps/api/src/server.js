const { app } = require("./app");
const { env } = require("./config/env");
const { logger } = require("./config/logger");
const { connectRedis } = require("./lib/redis");

async function startServer() {
  try {
    await connectRedis();

    app.listen(env.API_PORT, () => {
      logger.info(`F.R.I.D.A.Y API running on http://localhost:${env.API_PORT}`);
    });
  } catch (error) {
    logger.error({ error }, "Failed to start server");
    process.exit(1);
  }
}

startServer();
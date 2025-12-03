import express, { Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { setupSwaggerRoutes } from './routes/swagger.routes';
import exampleRoutes from './routes/example.routes';
import prisma from './database';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 6173;

// Middleware
app.use(cors());
app.use(express.json());

// Setup Swagger/OpenAPI routes
app.use('/api', setupSwaggerRoutes(PORT));

// Setup API routes
app.use('/api/examples', exampleRoutes);

/**
 * @swagger
 * /api/health:
 *   get:
 *     summary: Health check endpoint
 *     description: Returns the health status of the API
 *     tags:
 *       - Health
 *     responses:
 *       200:
 *         description: API is healthy
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: string
 *                   example: ok
 *                 timestamp:
 *                   type: string
 *                   format: date-time
 *                   example: 2025-12-02T10:30:00.000Z
 */
app.get('/api/health', (req: Request, res: Response) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
  });
});

// Start server
const server = app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log(`Swagger UI available at http://localhost:${PORT}/api/swagger`);
  console.log(`OpenAPI JSON available at http://localhost:${PORT}/api/openapi.json`);
  console.log(`OpenAPI YAML available at http://localhost:${PORT}/api/openapi.yaml`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM signal received: closing HTTP server');
  await prisma.$disconnect();
  server.close(() => {
    console.log('HTTP server closed');
  });
});

process.on('SIGINT', async () => {
  console.log('SIGINT signal received: closing HTTP server');
  await prisma.$disconnect();
  server.close(() => {
    console.log('HTTP server closed');
    process.exit(0);
  });
});

export default app;

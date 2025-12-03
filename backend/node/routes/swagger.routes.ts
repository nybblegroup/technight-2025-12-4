import { Router, Request, Response } from 'express';
import swaggerJsdoc from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';
import yaml from 'js-yaml';

const router = Router();

/**
 * Configure and export Swagger specification
 */
export function configureSwagger(port: number | string) {
  const swaggerOptions = {
    definition: {
      openapi: '3.0.0',
      info: {
        title: 'Backend API',
        version: '1.0.0',
        description: 'Minimal backend API with health check endpoint',
      },
      servers: [
        {
          url: `http://localhost:${port}`,
          description: 'Development server',
        },
      ],
    },
    apis: ['./server.ts', './routes/*.ts'], // Path to the API docs
  };

  return swaggerJsdoc(swaggerOptions);
}

/**
 * Setup Swagger UI and OpenAPI endpoints
 */
export function setupSwaggerRoutes(port: number | string) {
  const swaggerSpec = configureSwagger(port);

  // Serve Swagger UI
  router.use('/swagger', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

  // Serve OpenAPI spec as JSON
  router.get('/openapi.json', (req: Request, res: Response) => {
    res.setHeader('Content-Type', 'application/json');
    res.send(swaggerSpec);
  });

  // Serve OpenAPI spec as YAML
  router.get('/openapi.yaml', (req: Request, res: Response) => {
    res.setHeader('Content-Type', 'text/yaml');
    const yamlSpec = yaml.dump(swaggerSpec);
    res.send(yamlSpec);
  });

  return router;
}


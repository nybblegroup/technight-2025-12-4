# Node.js Backend - Example Entity Implementation

## Overview

This backend now includes an `Example` entity with full CRUD operations, matching the implementation in the Spring Boot and .NET backends.

## Project Structure

The codebase is organized into modules for better maintainability:

```
backend/node/
├── server.ts              # Main server entry point
├── database.ts            # Shared Prisma client instance
├── routes/
│   ├── swagger.routes.ts  # Swagger/OpenAPI configuration and endpoints
│   └── example.routes.ts  # Example CRUD endpoints
├── prisma/
│   ├── schema.prisma      # Database schema
│   └── migrations/        # Database migrations
└── package.json
```

## Architecture

### Modular Design

The application follows a clean modular architecture:

- **`server.ts`**: Main application entry point - sets up Express, middleware, and routes
- **`database.ts`**: Shared Prisma client instance to avoid multiple connections
- **`routes/swagger.routes.ts`**: Swagger/OpenAPI configuration and documentation endpoints
- **`routes/example.routes.ts`**: All Example entity CRUD operations and their Swagger documentation

This separation makes the code more maintainable, testable, and easier to extend with new features.

## Database Schema

The `Example` entity has the following fields:
- `id`: Auto-incrementing integer primary key
- `name`: String (max 200 characters)
- `title`: String (max 200 characters)
- `entryDate`: Timestamp with default value of current timestamp
- `description`: Optional string (max 1000 characters)
- `isActive`: Boolean with default value of true

An index is created on `entry_date` for better query performance.

## Migrations

Two migrations have been created and applied:

1. **20251203150629_add_example_entity**: Creates the `example` table with all fields and index
2. **20251203150630_seed_example_data**: Inserts two sample records for testing

## API Endpoints

All endpoints are available at `/api/examples` with full Swagger documentation:

### GET /api/examples
Get all examples, ordered by entry date (descending)

### GET /api/examples/search?name={name}
Search examples by name (case-insensitive)

### GET /api/examples/:id
Get a specific example by ID

### POST /api/examples
Create a new example
- Required fields: `name`, `title`
- Optional fields: `description`, `isActive`

### PUT /api/examples/:id
Update an existing example (partial update supported)

### DELETE /api/examples/:id
Delete an example by ID

## Environment Setup

A `.env.example` file has been created with the database configuration:

```env
DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5432/technightdb-node?schema=public"
PORT=6173
```

Copy this to `.env` to configure your local environment.

## Running the Backend

```bash
# Install dependencies
npm install

# Generate Prisma client
npx prisma generate

# Run migrations (if not already applied)
npx prisma migrate deploy

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Swagger Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:6173/api/swagger
- OpenAPI JSON: http://localhost:6173/api/openapi.json
- OpenAPI YAML: http://localhost:6173/api/openapi.yaml

## Testing

The seed data provides two sample records for testing:
1. "First Example" - Introduction
2. "Second Example" - Advanced Topics

You can test the API using curl:

```bash
# Get all examples
curl http://localhost:6173/api/examples

# Get example by ID
curl http://localhost:6173/api/examples/1

# Search examples
curl http://localhost:6173/api/examples/search?name=First

# Create new example
curl -X POST http://localhost:6173/api/examples \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","title":"Test Title","description":"A test example","isActive":true}'

# Update example
curl -X PUT http://localhost:6173/api/examples/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title"}'

# Delete example
curl -X DELETE http://localhost:6173/api/examples/1
```


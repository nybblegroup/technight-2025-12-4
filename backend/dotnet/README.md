# TechnightApi - .NET 10 Backend

A .NET 10 Web API with PostgreSQL database using Entity Framework Core.

## Features

- ✅ .NET 10 Web API with minimal APIs
- ✅ Entity Framework Core with PostgreSQL
- ✅ **Swagger UI** - Interactive API documentation
- ✅ OpenAPI specification support
- ✅ CRUD operations for Example entities
- ✅ Database migrations support
- ✅ CORS configured for frontend development

## Prerequisites

- .NET 10 SDK
- PostgreSQL database

## Getting Started

### 1. Install Dependencies

The packages are already included in the project:
- `Npgsql.EntityFrameworkCore.PostgreSQL` - PostgreSQL provider for EF Core
- `Microsoft.EntityFrameworkCore.Design` - Design-time tools for EF Core

### 2. Configure Database Connection

Update the connection string in `appsettings.json` or `appsettings.Development.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=technightdb;Username=postgres;Password=postgres"
  }
}
```

Or use environment variables (recommended for production):

```bash
export ConnectionStrings__DefaultConnection="Host=localhost;Port=5432;Database=technightdb;Username=your-user;Password=your-password"
```

### 3. Create Database and Apply Migrations

```bash
cd TechnightApi

# Create the initial migration
dotnet ef migrations add InitialCreate

# Apply migrations to create the database
dotnet ef database update
```

### 4. Run the Application

```bash
# Development mode with hot reload
dotnet watch run

# Or standard run
dotnet run
```

The API will be available at:
- HTTP: `http://localhost:8080`
- HTTPS: `https://localhost:8080`
- **Swagger UI**: `http://localhost:8080/api/swagger` (in development mode)

## API Endpoints

### Health Check
- `GET /api/health` - Health check endpoint

### Examples API

All example endpoints are under `/api/examples`:

- `GET /api/examples` - Get all examples
- `GET /api/examples/{id}` - Get example by ID
- `GET /api/examples/search?name={name}` - Search examples by name
- `POST /api/examples` - Create a new example
- `PUT /api/examples/{id}` - Update an example
- `DELETE /api/examples/{id}` - Delete an example

### Swagger/OpenAPI Documentation

- **Swagger UI**: `http://localhost:8080/api/swagger` (interactive documentation)
- **OpenAPI JSON**: `http://localhost:8080/swagger/v1/swagger.json`

The Swagger UI provides an interactive interface where you can:
- Browse all available endpoints
- Test endpoints directly from your browser
- View request/response schemas
- See example values

## Example Entity

The `Example` entity has the following properties:

- `Id` (int) - Primary key, auto-generated
- `Name` (string) - Name of the example (required, max 200 chars)
- `Title` (string) - Title of the example (required, max 200 chars)
- `EntryDate` (DateTime) - Date when the entry was created
- `Description` (string?) - Optional description (max 1000 chars)
- `IsActive` (bool) - Active status (default: true)

## Database Schema

The `example` table in PostgreSQL:

```sql
CREATE TABLE example (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    title VARCHAR(200) NOT NULL,
    entry_date TIMESTAMP NOT NULL,
    description VARCHAR(1000),
    is_active BOOLEAN NOT NULL DEFAULT true
);

CREATE INDEX ix_example_entry_date ON example(entry_date);
```

## DTOs

### CreateExampleDto
Used for creating new examples:
```json
{
  "name": "Example Name",
  "title": "Example Title",
  "description": "Optional description",
  "isActive": true
}
```

### UpdateExampleDto
Used for updating existing examples (all fields optional):
```json
{
  "name": "Updated Name",
  "title": "Updated Title",
  "description": "Updated description",
  "isActive": false
}
```

## Entity Framework Commands

```bash
# Add a new migration
dotnet ef migrations add MigrationName

# Apply migrations to database
dotnet ef database update

# Rollback to a specific migration
dotnet ef database update PreviousMigrationName

# Remove last migration (if not applied)
dotnet ef migrations remove

# Drop the database
dotnet ef database drop
```

## Project Structure

```
TechnightApi/
├── Data/
│   └── ApplicationDbContext.cs    # EF Core DbContext
├── Models/
│   └── Example.cs                 # Example entity
├── DTOs/
│   ├── CreateExampleDto.cs        # DTO for creating examples
│   └── UpdateExampleDto.cs        # DTO for updating examples
├── Endpoints/
│   └── ExampleEndpoints.cs        # API endpoints
├── Migrations/                     # EF Core migrations
├── Program.cs                      # Application entry point
├── appsettings.json               # Configuration
└── TechnightApi.csproj            # Project file
```

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (React dev server)

Update the CORS policy in `Program.cs` to add more origins if needed.

## Production Considerations

For production deployment:

1. Use environment variables for sensitive configuration
2. Enable HTTPS
3. Configure proper CORS policies
4. Set up proper logging
5. Use connection pooling
6. Configure health checks
7. Add authentication/authorization as needed

## Troubleshooting

### Cannot connect to PostgreSQL
- Ensure PostgreSQL is running
- Verify connection string credentials
- Check firewall settings

### Migration errors
- Ensure you're in the TechnightApi directory
- Check database connection
- Verify EF Core tools are installed: `dotnet tool install --global dotnet-ef`

### Port already in use
- Change the port in `launchSettings.json` or use environment variable:
  ```bash
  export ASPNETCORE_URLS="http://localhost:8081"
  ```


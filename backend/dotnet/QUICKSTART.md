# TechnightApi - Quick Start Guide

## 🚀 What's Been Created

A complete .NET 10 Web API with PostgreSQL integration featuring:

- **Example Entity** with fields: Id, Name, Title, EntryDate, Description, IsActive
- **Full CRUD API** endpoints for Example operations
- **Entity Framework Core** with PostgreSQL provider
- **Database migrations** ready to apply
- **OpenAPI documentation** support
- **CORS** configured for frontend development

## 📦 Project Structure

```
TechnightApi/
├── Data/
│   └── ApplicationDbContext.cs       # EF Core DbContext with Example configuration
├── Models/
│   └── Example.cs                    # Example entity (maps to "example" table)
├── DTOs/
│   ├── CreateExampleDto.cs           # DTO for POST requests
│   └── UpdateExampleDto.cs           # DTO for PUT requests
├── Endpoints/
│   └── ExampleEndpoints.cs           # All API endpoints
├── Migrations/
│   └── 20251202131042_InitialCreate  # Initial database migration
├── Program.cs                        # App configuration and startup
├── appsettings.json                  # Configuration with connection string
└── run.sh                            # Quick start script
```

## 🔧 Quick Setup

### 1. Prerequisites

- .NET 10 SDK ✅ (already installed)
- PostgreSQL database running
- Default connection: `localhost:5432`

### 2. Configure Database

Update the connection string in `TechnightApi/appsettings.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=technightdb;Username=postgres;Password=postgres"
  }
}
```

### 3. Apply Migrations

```bash
cd TechnightApi
dotnet ef database update
```

This will:
- Create the `technightdb` database
- Create the `example` table
- Seed 2 initial example records

### 4. Run the API

```bash
# Option 1: Use the provided script
./run.sh

# Option 2: Run manually
dotnet run

# Option 3: Development mode with hot reload
dotnet watch run
```

The API will start on:
- **HTTP**: http://localhost:8080
- **HTTPS**: https://localhost:8080

## 🌐 API Endpoints

### Health Check
```
GET /api/health
```

### Examples CRUD

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/examples` | Get all examples |
| GET | `/api/examples/{id}` | Get example by ID |
| GET | `/api/examples/search?name=xxx` | Search examples by name |
| POST | `/api/examples` | Create new example |
| PUT | `/api/examples/{id}` | Update example |
| DELETE | `/api/examples/{id}` | Delete example |

### Example Request/Response

**Create Example (POST /api/examples)**
```json
Request:
{
  "name": "My Example",
  "title": "Example Title",
  "description": "Optional description",
  "isActive": true
}

Response (201 Created):
{
  "id": 3,
  "name": "My Example",
  "title": "Example Title",
  "entryDate": "2025-12-02T13:10:42.123Z",
  "description": "Optional description",
  "isActive": true
}
```

**Get All Examples (GET /api/examples)**
```json
Response (200 OK):
[
  {
    "id": 1,
    "name": "First Example",
    "title": "Introduction",
    "entryDate": "2025-12-02T13:10:42.123Z",
    "description": "This is the first example entry",
    "isActive": true
  },
  {
    "id": 2,
    "name": "Second Example",
    "title": "Advanced Topics",
    "entryDate": "2025-12-01T13:10:42.123Z",
    "description": "This is the second example entry",
    "isActive": true
  }
]
```

**Update Example (PUT /api/examples/1)**
```json
Request (all fields optional):
{
  "name": "Updated Name",
  "isActive": false
}

Response (200 OK):
{
  "id": 1,
  "name": "Updated Name",
  "title": "Introduction",
  "entryDate": "2025-12-02T13:10:42.123Z",
  "description": "This is the first example entry",
  "isActive": false
}
```

## 📖 API Documentation

### Swagger UI

Once the API is running, navigate to:
- **Swagger UI**: http://localhost:8080/api/swagger

The Swagger UI provides:
- Interactive API documentation
- Ability to test endpoints directly from the browser
- Request/response schemas
- Example values for all endpoints

You can try out any endpoint by clicking on it, filling in the parameters, and clicking "Execute".

## 🧪 Testing the API

### Using Swagger UI (Recommended)

1. Run the API: `dotnet run`
2. Open browser to http://localhost:8080/api/swagger
3. Click on any endpoint to expand it
4. Click "Try it out" button
5. Fill in required parameters
6. Click "Execute" to see the response

### Using curl

```bash
# Health check
curl http://localhost:8080/api/health

# Get all examples
curl http://localhost:8080/api/examples

# Get example by ID
curl http://localhost:8080/api/examples/1

# Search examples
curl http://localhost:8080/api/examples/search?name=First

# Create example
curl -X POST http://localhost:8080/api/examples \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","title":"Test Title","description":"Test description"}'

# Update example
curl -X PUT http://localhost:8080/api/examples/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Name"}'

# Delete example
curl -X DELETE http://localhost:8080/api/examples/1
```

## 🗄️ Database Schema

The `example` table:

| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| name | VARCHAR(200) | NOT NULL |
| title | VARCHAR(200) | NOT NULL |
| entry_date | TIMESTAMP | NOT NULL |
| description | VARCHAR(1000) | NULL |
| is_active | BOOLEAN | NOT NULL, DEFAULT true |

Indexes:
- `PRIMARY KEY` on `id`
- `ix_example_entry_date` on `entry_date`

## 🔄 Entity Framework Commands

```bash
# Create a new migration
dotnet ef migrations add MigrationName

# Apply migrations
dotnet ef database update

# Rollback to previous migration
dotnet ef database update PreviousMigrationName

# Remove last migration (if not applied)
dotnet ef migrations remove

# Drop database
dotnet ef database drop
```

## 🌍 CORS Configuration

CORS is enabled for:
- `http://localhost:5173` (Vite frontend)
- `http://localhost:3000` (React frontend)

Configured in `Program.cs` - modify as needed.

## 📝 Next Steps

1. **Connect Frontend**: Use the endpoints from your React/Vite frontend
2. **Add Authentication**: Implement JWT or other auth mechanisms
3. **Add Swagger UI**: Install `Swashbuckle.AspNetCore` for interactive API docs
4. **Add Logging**: Configure Serilog or other logging frameworks
5. **Add Validation**: Enhance DTOs with more validation attributes
6. **Add Tests**: Create unit and integration tests

## 🐛 Troubleshooting

### "Could not execute because dotnet-ef does not exist"
```bash
dotnet tool install --global dotnet-ef
export PATH="$PATH:/Users/nybblegroup/.dotnet/tools"
```

### "Cannot connect to database"
- Ensure PostgreSQL is running
- Verify connection string in `appsettings.json`
- Check credentials and port

### "Port already in use"
Change port in `Properties/launchSettings.json` or:
```bash
export ASPNETCORE_URLS="http://localhost:5002"
dotnet run
```

## 📚 Technology Stack

- **.NET 10** - Latest stable version
- **ASP.NET Core** - Minimal APIs
- **Entity Framework Core** - ORM
- **Npgsql** - PostgreSQL provider
- **PostgreSQL** - Database

## ✅ What Works

- ✅ All CRUD operations
- ✅ Database migrations
- ✅ **Swagger UI** - Interactive API documentation
- ✅ OpenAPI specifications
- ✅ CORS for frontend
- ✅ Health check endpoint
- ✅ Proper error responses (404, 400, etc.)
- ✅ Search functionality
- ✅ Data validation
- ✅ Seeded data
- ✅ Zero build warnings

## 🎨 Swagger/OpenAPI

The project includes Swashbuckle.AspNetCore for automatic API documentation:

**Packages installed:**
- `Swashbuckle.AspNetCore` (v10.0.1) - Complete Swagger toolchain
- `Microsoft.OpenApi` (v2.3.0) - OpenAPI specifications

**Access Swagger UI:**
```
http://localhost:5291/swagger
```

**Swagger JSON spec:**
```
http://localhost:5291/swagger/v1/swagger.json
```

### Customizing Swagger

To add more details to your Swagger documentation, you can enhance the configuration in `Program.cs`:

```csharp
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new()
    {
        Title = "TechnightApi",
        Version = "v1",
        Description = "Your custom description",
        TermsOfService = new Uri("https://example.com/terms"),
        Contact = new()
        {
            Name = "Your Name",
            Email = "your@email.com",
            Url = new Uri("https://example.com")
        },
        License = new()
        {
            Name = "MIT",
            Url = new Uri("https://opensource.org/licenses/MIT")
        }
    });
    
    // Enable XML comments for more detailed documentation
    // var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    // var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    // options.IncludeXmlComments(xmlPath);
});
```


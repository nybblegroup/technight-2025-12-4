using Microsoft.EntityFrameworkCore;
using TechnightApi.Data;
using TechnightApi.Endpoints;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new()
    {
        Title = "TechnightApi",
        Version = "v1",
        Description = "A .NET 10 Web API with PostgreSQL and Entity Framework Core"
    });
});

// Add DbContext with PostgreSQL
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection")
    ?? "Host=localhost;Port=5432;Database=technightdb;Username=postgres;Password=postgres";

builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseNpgsql(connectionString));

// Add CORS for frontend development
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins("http://localhost:5173", "http://localhost:3000")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(options =>
    {
        options.SwaggerEndpoint("/swagger/v1/swagger.json", "TechnightApi v1");
        options.RoutePrefix = "api/swagger";
        options.DocumentTitle = "TechnightApi - Swagger UI";
    });
}

app.UseCors("AllowFrontend");

app.UseHttpsRedirection();

// Map Example endpoints
app.MapExampleEndpoints();

// Health check endpoint
app.MapGet("/api/health", () => Results.Ok(new
{
    status = "healthy",
    timestamp = DateTime.UtcNow,
    service = "TechnightApi"
}))
.WithName("HealthCheck")
.WithTags("Health")
.WithSummary("Health check endpoint");

app.Run();

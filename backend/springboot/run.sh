#!/bin/bash

# TechnightApi Spring Boot - Run Script
# This script builds and runs the Spring Boot application

set -e

echo "🚀 Starting TechnightApi (Spring Boot)..."
echo ""

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo "❌ Error: Java is not installed or not in PATH"
    echo "Please install Java 25 or higher"
    exit 1
fi

# Check Java version
JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}' | cut -d'.' -f1)
echo "☕ Java version: $(java -version 2>&1 | head -n 1)"

# Check if Maven is installed
if ! command -v mvn &> /dev/null; then
    echo "❌ Error: Maven is not installed or not in PATH"
    echo "Please install Maven 3.9 or higher"
    exit 1
fi

echo "📦 Maven version: $(mvn -version | head -n 1)"
echo ""

# Check if PostgreSQL is running
echo "🗄️  Checking database connection..."
if ! nc -z localhost 5432 2>/dev/null; then
    echo "⚠️  Warning: Cannot connect to PostgreSQL on localhost:5432"
    echo "Make sure PostgreSQL is running:"
    echo ""
    echo "Using Docker:"
    echo "  docker run --name postgres-technight-springboot \\"
    echo "    -e POSTGRES_DB=technightdb-springboot \\"
    echo "    -e POSTGRES_USER=postgres \\"
    echo "    -e POSTGRES_PASSWORD=mysecretpassword \\"
    echo "    -p 5432:5432 -d postgres:17"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ PostgreSQL is running on localhost:5432"
fi

echo ""
echo "🔨 Building application..."
mvn clean install -DskipTests

echo ""
echo "🏃 Starting Spring Boot application..."
echo "📍 API will be available at: http://localhost:8080"
echo "📚 Swagger UI: http://localhost:8080/api/swagger"
echo "🏥 Health Check: http://localhost:8080/api/health"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run the application with dev profile
mvn spring-boot:run -Dspring-boot.run.profiles=dev


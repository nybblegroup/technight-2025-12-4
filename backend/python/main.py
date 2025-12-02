from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from datetime import datetime
import os
import yaml
from dotenv import load_dotenv
import signal
import sys

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Backend API",
    version="1.0.0",
    description="Minimal backend API with health check endpoint",
    docs_url="/api/swagger",
    openapi_url="/api/openapi.json",
)

PORT = int(os.getenv("PORT", 6174))

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint

    Returns the health status of the API

    Returns:
        dict: Health status with timestamp
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/api/openapi.yaml", include_in_schema=False)
async def get_openapi_yaml():
    """
    Serve OpenAPI spec as YAML
    """
    openapi_schema = app.openapi()
    yaml_content = yaml.dump(openapi_schema, default_flow_style=False)
    return Response(content=yaml_content, media_type="text/yaml")


# Graceful shutdown handlers
def handle_shutdown(signum, frame):
    """Handle graceful shutdown on SIGTERM/SIGINT"""
    print(f"\n{'SIGTERM' if signum == signal.SIGTERM else 'SIGINT'} signal received: closing server")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


if __name__ == "__main__":
    import uvicorn

    print(f"Server is running on http://localhost:{PORT}")
    print(f"Swagger UI available at http://localhost:{PORT}/api/swagger")
    print(f"OpenAPI JSON available at http://localhost:{PORT}/api/openapi.json")
    print(f"OpenAPI YAML available at http://localhost:{PORT}/api/openapi.yaml")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
        log_level="info"
    )

#!/bin/bash

# Script to setup and start development environment with Python backend and frontend
# Usage: ./start-dev.sh

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_BACKEND_DIR="$SCRIPT_DIR"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
VENV_DIR="$PYTHON_BACKEND_DIR/venv"

echo -e "${BLUE}=== Technight 2025-12 Development Setup ===${NC}\n"

# Step 1: Check Python installation
echo -e "${BLUE}[1/7] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.12+ first.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Step 2: Setup Python virtual environment
echo -e "\n${BLUE}[2/7] Setting up Python virtual environment...${NC}"
cd "$PYTHON_BACKEND_DIR"

if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Step 2.5: Install system dependencies for psycopg2-binary
echo -e "\n${BLUE}[2.5/7] Installing system dependencies for PostgreSQL...${NC}"

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)
        echo -e "${YELLOW}Detected Linux. Checking for PostgreSQL dependencies...${NC}"
        if command -v apt-get &> /dev/null; then
            # Debian/Ubuntu
            if ! dpkg -l | grep -q libpq-dev; then
                echo -e "${YELLOW}Installing libpq-dev (requires sudo)...${NC}"
                sudo apt-get update -qq && sudo apt-get install -y -qq libpq-dev || {
                    echo -e "${YELLOW}⚠ Could not install libpq-dev automatically. Please run: sudo apt-get install libpq-dev${NC}"
                }
            else
                echo -e "${GREEN}✓ libpq-dev already installed${NC}"
            fi
        elif command -v yum &> /dev/null; then
            # RHEL/CentOS
            if ! rpm -qa | grep -q postgresql-devel; then
                echo -e "${YELLOW}Installing postgresql-devel (requires sudo)...${NC}"
                sudo yum install -y -q postgresql-devel || {
                    echo -e "${YELLOW}⚠ Could not install postgresql-devel automatically. Please run: sudo yum install postgresql-devel${NC}"
                }
            else
                echo -e "${GREEN}✓ postgresql-devel already installed${NC}"
            fi
        else
            echo -e "${YELLOW}⚠ Unknown Linux distribution. Please install PostgreSQL development libraries manually.${NC}"
        fi
        ;;
    Darwin*)
        echo -e "${YELLOW}Detected macOS. Checking for PostgreSQL dependencies...${NC}"
        if ! command -v brew &> /dev/null; then
            echo -e "${RED}❌ Homebrew is not installed. Please install Homebrew first:${NC}"
            echo -e "${YELLOW}   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"${NC}"
            echo -e "${YELLOW}⚠ Continuing without system dependencies. psycopg2-binary installation may fail.${NC}"
        else
            # Check and install libpq
            set +e
            brew list libpq &> /dev/null 2>&1
            LIBPQ_INSTALLED=$?
            set -e
            
            if [ $LIBPQ_INSTALLED -eq 0 ]; then
                echo -e "${GREEN}✓ libpq already installed${NC}"
            else
                echo -e "${YELLOW}Installing libpq via Homebrew...${NC}"
                brew install libpq || {
                    echo -e "${YELLOW}⚠ Could not install libpq automatically. Please run: brew install libpq${NC}"
                }
                echo -e "${GREEN}✓ libpq installation attempted${NC}"
            fi
            
            # Check and install OpenSSL (required for psycopg2-binary)
            set +e
            brew list openssl@3 &> /dev/null 2>&1 || brew list openssl@1.1 &> /dev/null 2>&1
            OPENSSL_INSTALLED=$?
            set -e
            
            if [ $OPENSSL_INSTALLED -eq 0 ]; then
                echo -e "${GREEN}✓ OpenSSL already installed${NC}"
            else
                echo -e "${YELLOW}Installing OpenSSL via Homebrew...${NC}"
                brew install openssl@3 || brew install openssl@1.1 || {
                    echo -e "${YELLOW}⚠ Could not install OpenSSL automatically. Please run: brew install openssl@3${NC}"
                }
                echo -e "${GREEN}✓ OpenSSL installation attempted${NC}"
            fi
            
            # Find libpq path
            LIBPQ_PATH=""
            for path in "$(brew --prefix libpq 2>/dev/null)" "/opt/homebrew/opt/libpq" "/usr/local/opt/libpq"; do
                if [ -d "$path" ]; then
                    LIBPQ_PATH="$path"
                    break
                fi
            done
            
            # Find OpenSSL path (try openssl@3 first, then openssl@1.1)
            OPENSSL_PATH=""
            for path in "$(brew --prefix openssl@3 2>/dev/null)" "$(brew --prefix openssl@1.1 2>/dev/null)" "/opt/homebrew/opt/openssl@3" "/opt/homebrew/opt/openssl@1.1" "/usr/local/opt/openssl@3" "/usr/local/opt/openssl@1.1"; do
                if [ -d "$path" ]; then
                    OPENSSL_PATH="$path"
                    break
                fi
            done
            
            # Set environment variables for psycopg2 compilation
            if [ -n "$LIBPQ_PATH" ] && [ -d "$LIBPQ_PATH" ]; then
                export PATH="$LIBPQ_PATH/bin:$PATH"
                export LDFLAGS="-L$LIBPQ_PATH/lib $LDFLAGS"
                export CPPFLAGS="-I$LIBPQ_PATH/include $CPPFLAGS"
                export PKG_CONFIG_PATH="$LIBPQ_PATH/lib/pkgconfig:$PKG_CONFIG_PATH"
                echo -e "${GREEN}✓ Configured environment for libpq at $LIBPQ_PATH${NC}"
            else
                echo -e "${YELLOW}⚠ Could not find libpq installation path.${NC}"
            fi
            
            if [ -n "$OPENSSL_PATH" ] && [ -d "$OPENSSL_PATH" ]; then
                export PATH="$OPENSSL_PATH/bin:$PATH"
                export LDFLAGS="-L$OPENSSL_PATH/lib $LDFLAGS"
                export CPPFLAGS="-I$OPENSSL_PATH/include $CPPFLAGS"
                export PKG_CONFIG_PATH="$OPENSSL_PATH/lib/pkgconfig:$PKG_CONFIG_PATH"
                echo -e "${GREEN}✓ Configured environment for OpenSSL at $OPENSSL_PATH${NC}"
            else
                echo -e "${YELLOW}⚠ Could not find OpenSSL installation path. psycopg2-binary may fail to compile.${NC}"
                echo -e "${YELLOW}   Try: brew install openssl@3${NC}"
            fi
        fi
        ;;
    *)
        echo -e "${YELLOW}⚠ Unknown OS: ${OS}. Please install PostgreSQL development libraries manually.${NC}"
        ;;
esac

# Step 3: Activate virtual environment and install Python dependencies
echo -e "\n${BLUE}[3/7] Installing Python dependencies...${NC}"
source venv/bin/activate

# Upgrade pip
pip install --quiet --upgrade pip

# Install Python dependencies
echo -e "${YELLOW}Installing Python packages (this may take a moment)...${NC}"
pip install --quiet -r requirements.txt || {
    echo -e "${RED}❌ Failed to install Python dependencies${NC}"
    echo -e "${YELLOW}If psycopg2-binary failed, make sure you have:${NC}"
    echo -e "${YELLOW}  - macOS: libpq installed via Homebrew${NC}"
    echo -e "${YELLOW}  - Linux: libpq-dev or postgresql-devel installed${NC}"
    exit 1
}
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Step 4: Install Node dependencies (root and frontend)
echo -e "\n${BLUE}[4/7] Installing Node dependencies...${NC}"
cd "$PROJECT_ROOT"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 20.19.4+ first.${NC}"
    exit 1
fi

# Install root dependencies
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing root dependencies...${NC}"
    npm install --silent
    echo -e "${GREEN}✓ Root dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Root dependencies already installed${NC}"
fi

# Install frontend dependencies
cd "$FRONTEND_DIR"
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    npm install --silent
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Frontend dependencies already installed${NC}"
fi

# Step 5: Check for .env file
echo -e "\n${BLUE}[5/7] Checking environment configuration...${NC}"
cd "$PYTHON_BACKEND_DIR"

if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠ .env file not found. Creating from example...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠ Please edit backend/python/.env with your DATABASE_URL${NC}"
    else
        echo -e "${YELLOW}⚠ Creating basic .env file...${NC}"
        cat > .env << EOF
PORT=8080
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
EOF
        echo -e "${YELLOW}⚠ Please edit backend/python/.env with your DATABASE_URL${NC}"
    fi
else
    echo -e "${GREEN}✓ .env file found${NC}"
fi

# Check frontend .env
cd "$FRONTEND_DIR"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠ Frontend .env not found. Creating...${NC}"
    echo "VITE_API_BASE_URL=http://localhost:8080" > .env
    echo -e "${GREEN}✓ Frontend .env created${NC}"
else
    echo -e "${GREEN}✓ Frontend .env found${NC}"
fi

# Step 6: Generate SDK (if needed)
echo -e "\n${BLUE}[6/7] Checking SDK...${NC}"
cd "$PROJECT_ROOT"

if [ ! -d "sdk/ts/src" ]; then
    echo -e "${YELLOW}SDK not found. Generating SDK from Python backend...${NC}"
    echo -e "${YELLOW}(This requires Java or Docker. If it fails, install Java or configure Docker)${NC}"
    npm run sdk:generate:python || {
        echo -e "${RED}⚠ SDK generation failed. You can continue without it, but the frontend may not work.${NC}"
        echo -e "${YELLOW}To fix: Install Java or configure Docker in openapitools.json${NC}"
    }
else
    echo -e "${GREEN}✓ SDK found${NC}"
fi

# Final step: Start services
echo -e "\n${GREEN}=== Starting Development Servers ===${NC}\n"
echo -e "${BLUE}Starting Python backend and Frontend...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}\n"

cd "$PROJECT_ROOT"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Stopping servers...${NC}"
    kill $PYTHON_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Python backend in background
cd "$PYTHON_BACKEND_DIR"
source venv/bin/activate
python3 main.py &
PYTHON_PID=$!
echo -e "${GREEN}✓ Python backend started (PID: $PYTHON_PID)${NC}"
echo -e "${BLUE}   → http://localhost:8080${NC}"
echo -e "${BLUE}   → Swagger: http://localhost:8080/api/swagger${NC}"

# Wait a moment for Python backend to start
sleep 2

# Start frontend in background
cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo -e "${BLUE}   → http://localhost:5173${NC}"

echo -e "\n${GREEN}=== Servers Running ===${NC}"
echo -e "${BLUE}Python Backend:${NC} http://localhost:8080"
echo -e "${BLUE}Frontend:${NC}       http://localhost:5173"
echo -e "${BLUE}Swagger UI:${NC}     http://localhost:8080/api/swagger"
echo -e "\n${YELLOW}Press Ctrl+C to stop all servers${NC}\n"

# Wait for both processes
wait $PYTHON_PID $FRONTEND_PID


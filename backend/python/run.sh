#!/bin/bash

# Script to setup and start Python backend development environment
# Usage: ./run.sh

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Project directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BACKEND_DIR="$SCRIPT_DIR"
VENV_DIR="$PYTHON_BACKEND_DIR/venv"

echo -e "${BLUE}=== Python Backend Development Setup ===${NC}\n"

# Step 1: Check Python installation
echo -e "${BLUE}[1/5] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.12+ first.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Step 2: Setup Python virtual environment
echo -e "\n${BLUE}[2/5] Setting up Python virtual environment...${NC}"
cd "$PYTHON_BACKEND_DIR"

if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Step 2.5: Install system dependencies for psycopg2-binary
echo -e "\n${BLUE}[2.5/5] Installing system dependencies for PostgreSQL...${NC}"

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
echo -e "\n${BLUE}[3/5] Installing Python dependencies...${NC}"
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

# Step 4: Check for .env file
echo -e "\n${BLUE}[4/5] Checking environment configuration...${NC}"
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

# Step 4.5: Auto-detect and apply database migrations intelligently
echo -e "\n${BLUE}[4.5/5] Running database migrations (auto-detect changes)...${NC}"
cd "$PYTHON_BACKEND_DIR"
source venv/bin/activate

# Function to load DATABASE_URL from .env file safely
load_database_url() {
    if [ -f ".env" ]; then
        # Use grep and sed to extract DATABASE_URL, handling quoted and unquoted values
        DATABASE_URL=$(grep -E "^DATABASE_URL=" .env | sed -E 's/^DATABASE_URL=["'\'']?([^"'\'']*)["'\'']?$/\1/' | head -1)
        if [ -n "$DATABASE_URL" ]; then
            export DATABASE_URL
            return 0
        fi
    fi
    return 1
}

# Load DATABASE_URL from .env if not already set
if [ -z "$DATABASE_URL" ]; then
    load_database_url
fi

# Check if DATABASE_URL is configured and not the default placeholder
if [ -n "$DATABASE_URL" ] && [ "$DATABASE_URL" != "postgresql://user:password@localhost:5432/mydb" ]; then
    echo -e "${YELLOW}DATABASE_URL found: ${DATABASE_URL%%@*}@***${NC}"
    
    # Check if Alembic is initialized
    if [ ! -d "alembic/versions" ]; then
        echo -e "${YELLOW}⚠ Alembic not initialized. Initializing...${NC}"
        alembic init alembic 2>/dev/null || {
            echo -e "${RED}❌ Failed to initialize Alembic${NC}"
        }
    fi
    
    # Function to generate migration message from model changes
    generate_migration_message() {
        # Try to detect what changed by comparing models with database
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        echo "Auto migration ${TIMESTAMP}"
    }
    
    # Step 1: Check if there are any migration files in the directory
    MIGRATION_COUNT=$(find alembic/versions -name "*.py" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo -e "${BLUE}Found $MIGRATION_COUNT migration file(s) in alembic/versions/${NC}"
    
    # Step 2: Check current migration status in database
    echo -e "${YELLOW}Checking current migration status in database...${NC}"
    CURRENT_OUTPUT=$(alembic current 2>&1)
    CURRENT_EXIT=$?
    
    # Use sed instead of grep -P for macOS compatibility
    CURRENT_VERSION=$(echo "$CURRENT_OUTPUT" | sed -n 's/.*\([0-9a-f]\{12\}\).*/\1/p' | head -1 || echo "")
    
    # Check if database is completely empty (no alembic_version table or no records)
    DB_IS_EMPTY=false
    if [ $CURRENT_EXIT -ne 0 ] || [ -z "$CURRENT_VERSION" ]; then
        # Try to check if alembic_version table exists
        if python3 -c "
from database import engine
from sqlalchemy import inspect, text
if engine:
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if 'alembic_version' not in tables:
        print('EMPTY')
        exit(0)
    # Check if table has any records
    with engine.connect() as conn:
        result = conn.execute(text('SELECT COUNT(*) FROM alembic_version'))
        count = result.scalar()
        if count == 0:
            print('EMPTY')
            exit(0)
        else:
            print('HAS_DATA')
            exit(1)
else:
    exit(1)
" 2>/dev/null | grep -q "EMPTY"; then
            DB_IS_EMPTY=true
            echo -e "${YELLOW}Database is empty (no migrations applied)${NC}"
        else
            echo -e "${YELLOW}No migrations applied yet (fresh database)${NC}"
        fi
    else
        echo -e "${GREEN}Current migration version: ${CURRENT_VERSION}${NC}"
    fi
    
    # Step 3: Apply existing migrations first (if database is empty and migrations exist)
    if [ "$MIGRATION_COUNT" -gt 0 ] && [ "$DB_IS_EMPTY" = true ]; then
        echo -e "${YELLOW}Database is empty but migration files exist. Applying existing migrations first...${NC}"
        if alembic upgrade head 2>&1 | tee /tmp/alembic_initial_upgrade.log; then
            echo -e "${GREEN}✓ Existing migrations applied successfully${NC}"
            # Update current version after applying
            CURRENT_VERSION=$(alembic current 2>/dev/null | sed -n 's/.*\([0-9a-f]\{12\}\).*/\1/p' | head -1 || echo "")
            rm -f /tmp/alembic_initial_upgrade.log
        else
            INIT_ERROR=$(cat /tmp/alembic_initial_upgrade.log 2>/dev/null || echo "")
            echo -e "${YELLOW}⚠ Could not apply existing migrations:${NC}"
            echo "$INIT_ERROR" | head -10
            rm -f /tmp/alembic_initial_upgrade.log
        fi
    fi
    
    # Step 4: Auto-detect model changes and generate NEW migration if needed
    # Only generate if there are actual differences between models and database
    echo -e "${YELLOW}Auto-detecting model changes...${NC}"
    
    MIGRATION_MSG=$(generate_migration_message)
    MIGRATION_COUNT_BEFORE=$MIGRATION_COUNT
    
    # Attempt to create migration with autogenerate
    # This will only create a migration if there are actual changes
    echo -e "${BLUE}Running: alembic revision --autogenerate -m \"$MIGRATION_MSG\"${NC}"
    AUTOGEN_OUTPUT=$(alembic revision --autogenerate -m "$MIGRATION_MSG" 2>&1)
    AUTOGEN_EXIT=$?
    
    # Always show output for debugging
    if [ $AUTOGEN_EXIT -ne 0 ]; then
        echo -e "${YELLOW}Autogenerate output:${NC}"
        echo "$AUTOGEN_OUTPUT" | head -20
    fi
    
    if [ $AUTOGEN_EXIT -eq 0 ]; then
        # Check if a migration file was actually created
        MIGRATION_COUNT_AFTER=$(find alembic/versions -name "*.py" -type f 2>/dev/null | wc -l | tr -d ' ')
        
        if [ "$MIGRATION_COUNT_AFTER" -gt "$MIGRATION_COUNT_BEFORE" ]; then
            NEW_MIGRATION=$(ls -t alembic/versions/*.py 2>/dev/null | head -1)
            echo -e "${GREEN}✓ Detected model changes! New migration generated automatically${NC}"
            if [ -n "$NEW_MIGRATION" ]; then
                echo -e "${BLUE}   Migration file: $(basename "$NEW_MIGRATION")${NC}"
            fi
        elif echo "$AUTOGEN_OUTPUT" | grep -q "Generating.*alembic/versions"; then
            echo -e "${GREEN}✓ Detected model changes! Migration generated automatically${NC}"
        else
            echo -e "${GREEN}✓ No model changes detected (database schema matches models)${NC}"
        fi
    else
        # Check if error is because database doesn't exist or connection issue
        if echo "$AUTOGEN_OUTPUT" | grep -q "connection\|refused\|could not connect\|does not exist"; then
            echo -e "${RED}❌ Cannot connect to database for migration detection${NC}"
            echo -e "${YELLOW}   Error details:${NC}"
            echo "$AUTOGEN_OUTPUT" | grep -i "error\|connection\|refused" | head -5
            echo -e "${YELLOW}   Please verify:${NC}"
            echo -e "${YELLOW}   1. PostgreSQL is running${NC}"
            echo -e "${YELLOW}   2. DATABASE_URL is correct in .env${NC}"
            echo -e "${YELLOW}   3. Database exists and credentials are valid${NC}"
            echo -e "${YELLOW}   Continuing anyway... (migrations will be skipped, server will still start)${NC}"
        else
            echo -e "${YELLOW}⚠ Could not auto-detect changes${NC}"
            echo -e "${YELLOW}   Output: ${AUTOGEN_OUTPUT:0:200}...${NC}"
            echo -e "${YELLOW}   This is OK if no changes exist${NC}"
        fi
    fi
    
    # Step 5: Apply all pending migrations (including any newly generated)
    echo -e "${YELLOW}Applying all pending migrations...${NC}"
    
    # Re-check migration count (might have changed after autogenerate)
    MIGRATION_FILES=$(find alembic/versions -name "*.py" -type f 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$MIGRATION_FILES" -eq 0 ]; then
        echo -e "${RED}❌ No migration files found at all!${NC}"
        echo -e "${YELLOW}   Attempting to generate initial migration...${NC}"
        MIGRATION_MSG="Initial migration - create all tables"
        AUTOGEN_INIT_OUTPUT=$(alembic revision --autogenerate -m "$MIGRATION_MSG" 2>&1)
        AUTOGEN_INIT_EXIT=$?
        
        if [ $AUTOGEN_INIT_EXIT -eq 0 ]; then
            echo -e "${GREEN}✓ Initial migration generated${NC}"
            echo "$AUTOGEN_INIT_OUTPUT" | grep -i "generating\|created" | head -3
            MIGRATION_FILES=$(find alembic/versions -name "*.py" -type f 2>/dev/null | wc -l | tr -d ' ')
        else
            echo -e "${RED}❌ Failed to generate initial migration${NC}"
            echo -e "${YELLOW}   Error output:${NC}"
            echo "$AUTOGEN_INIT_OUTPUT" | head -15
            echo -e "${YELLOW}   The server will start, but database tables may not exist.${NC}"
            echo -e "${YELLOW}   You may need to create tables manually or check database connection.${NC}"
        fi
    fi
    
    if [ "$MIGRATION_FILES" -gt 0 ]; then
        echo -e "${BLUE}Applying $MIGRATION_FILES migration(s) to database...${NC}"
        if alembic upgrade head 2>&1 | tee /tmp/alembic_upgrade.log; then
            echo -e "${GREEN}✓ All migrations applied successfully${NC}"
            
            # Verify database schema
            if python3 -c "
from database import engine
from sqlalchemy import inspect
if engine:
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if 'example' in tables:
        print('✓ Example table exists')
        exit(0)
    else:
        print('⚠ Example table not found')
        exit(1)
else:
    exit(1)
" 2>/dev/null; then
                echo -e "${GREEN}✓ Database schema verified${NC}"
            else
                echo -e "${YELLOW}⚠ Warning: Could not verify database schema${NC}"
            fi
        else
            ERROR_OUTPUT=$(cat /tmp/alembic_upgrade.log 2>/dev/null || echo "")
            
            echo -e "${RED}❌ Migration application failed${NC}"
            echo -e "${YELLOW}Error output:${NC}"
            echo "$ERROR_OUTPUT" | head -30
            
            # Check for specific error types
            if echo "$ERROR_OUTPUT" | grep -q "Target database is not up to date"; then
                echo -e "${YELLOW}⚠ Database is not up to date. Retrying upgrade...${NC}"
                alembic upgrade head 2>&1 && echo -e "${GREEN}✓ Migrations applied${NC}" || echo -e "${YELLOW}⚠ Please check migration status manually${NC}"
            elif echo "$ERROR_OUTPUT" | grep -q "Can't locate revision\|No such revision"; then
                echo -e "${YELLOW}⚠ Migration revision issue detected.${NC}"
                echo -e "${YELLOW}   This might be a fresh database. Will continue anyway.${NC}"
                echo -e "${YELLOW}   Run 'alembic history' to see available migrations${NC}"
            elif echo "$ERROR_OUTPUT" | grep -q "connection\|refused\|could not connect"; then
                echo -e "${RED}❌ Cannot connect to database${NC}"
                echo -e "${YELLOW}   Please verify database connection and credentials${NC}"
                echo -e "${YELLOW}   Continuing anyway... (server will start but database features may not work)${NC}"
            elif echo "$ERROR_OUTPUT" | grep -q "relation.*does not exist\|table.*does not exist"; then
                echo -e "${YELLOW}⚠ Database tables don't exist yet. This is normal for a fresh database.${NC}"
                echo -e "${YELLOW}   The server will start. Tables will be created on first use or next migration run.${NC}"
            else
                echo -e "${YELLOW}⚠ Migration had issues. See error output above.${NC}"
                echo -e "${YELLOW}   You can run 'alembic upgrade head' manually if needed.${NC}"
                echo -e "${YELLOW}   Continuing anyway... (server will start)${NC}"
            fi
            rm -f /tmp/alembic_upgrade.log
        fi
    else
        echo -e "${YELLOW}⚠ No migrations to apply. Server will start anyway.${NC}"
    fi
else
    echo -e "${YELLOW}⚠ DATABASE_URL not configured or using default placeholder.${NC}"
    echo -e "${YELLOW}   Skipping migrations. Set DATABASE_URL in .env to enable database features.${NC}"
fi

# Final step: Start Python backend
echo -e "\n${GREEN}=== Starting Python Backend ===${NC}\n"
echo -e "${BLUE}Starting Python backend server...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}\n"

cd "$PYTHON_BACKEND_DIR"
source venv/bin/activate

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Stopping server...${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Python backend
echo -e "${GREEN}✓ Starting Python backend...${NC}"
echo -e "${BLUE}   → http://localhost:8080${NC}"
echo -e "${BLUE}   → Swagger: http://localhost:8080/api/swagger${NC}"
echo -e "\n${GREEN}=== Server Running ===${NC}"
echo -e "${BLUE}Python Backend:${NC} http://localhost:8080"
echo -e "${BLUE}Swagger UI:${NC}     http://localhost:8080/api/swagger"
echo -e "\n${YELLOW}Press Ctrl+C to stop the server${NC}\n"

# Run Python backend in foreground
python3 main.py


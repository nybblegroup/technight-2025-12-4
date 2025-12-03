"""
Database migration helper script using Alembic
This script provides a simple interface to run Alembic migrations
"""
import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_alembic_command(command: str, *args):
    """
    Run an Alembic command
    """
    try:
        # Change to the directory containing alembic.ini
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Build the command
        cmd = ["alembic"] + command.split() + list(args)
        
        # Run the command
        result = subprocess.run(cmd, check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running Alembic: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 migrations.py <command> [args]")
        print("\nAvailable commands:")
        print("  upgrade head    - Apply all pending migrations")
        print("  downgrade -1    - Rollback last migration")
        print("  revision --autogenerate -m 'message' - Create new migration from model changes")
        print("  current         - Show current migration version")
        print("  history         - Show migration history")
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    # Check DATABASE_URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url or database_url == "postgresql://user:password@localhost:5432/mydb":
        print("⚠ Warning: DATABASE_URL not configured or using default value.")
        print("   Set DATABASE_URL in .env file to use migrations.")
        if command not in ["history", "current"]:
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)
    
    success = run_alembic_command(command, *args)
    sys.exit(0 if success else 1)


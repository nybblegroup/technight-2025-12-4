#!/usr/bin/env python3
"""
Drop ALL tables in the database (complete reset)
"""
from database import engine
from sqlalchemy import text, inspect

print("=" * 60)
print("  COMPLETE DATABASE RESET")
print("=" * 60)
print()
print("⚠️  WARNING: This will delete ALL tables in the database!")
print()

# Get confirmation
confirm = input("Type 'yes' to continue: ").strip().lower()
if confirm != 'yes':
    print("❌ Aborted")
    exit(0)

print()
print("🗑️ Dropping ALL tables...")

with engine.begin() as conn:
    # Get all table names
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    if not table_names:
        print("   ℹ️  No tables found")
    else:
        # Drop each table (CASCADE will handle foreign keys)
        for table_name in table_names:
            try:
                conn.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE'))
                print(f"   ✓ Dropped table: {table_name}")
            except Exception as e:
                print(f"   ✗ Failed to drop {table_name}: {e}")
        
        # Drop alembic_version table
        try:
            conn.execute(text('DROP TABLE IF EXISTS alembic_version CASCADE'))
            print(f"   ✓ Dropped table: alembic_version")
        except:
            pass

print()
print("✅ All tables dropped successfully!")
print()
print("📝 Next steps:")
print("   1. alembic upgrade head")
print("   2. python3 seed_data.py")
print()


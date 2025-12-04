"""
Reset database - Drop all Event Hub tables and recreate from migrations
"""
from sqlalchemy import text
from database import engine
import os


def reset_database():
    """Drop all Event Hub tables and reset migrations"""
    
    print("🗑️  Dropping existing Event Hub tables...")
    
    with engine.connect() as conn:
        # Drop tables in correct order (respecting foreign keys)
        tables_to_drop = [
            'participant_badges',
            'responses',
            'messages',
            'questions',
            'participants',
            'badges',
            'events',
        ]
        
        for table in tables_to_drop:
            try:
                conn.execute(text(f'DROP TABLE IF EXISTS {table} CASCADE'))
                print(f"   ✓ Dropped table: {table}")
            except Exception as e:
                print(f"   ⚠️  Could not drop {table}: {e}")
        
        conn.commit()
    
    print("\n✅ Database reset complete!")
    print("\n📝 Now run:")
    print("   alembic upgrade head")
    print("   python seed_data.py")


if __name__ == "__main__":
    print("=" * 60)
    print("  DATABASE RESET - Event Hub Tables")
    print("=" * 60)
    print("\n⚠️  WARNING: This will delete all Event Hub data!")
    
    confirm = input("\nContinue? (yes/no): ")
    
    if confirm.lower() in ['yes', 'y']:
        reset_database()
    else:
        print("❌ Cancelled")






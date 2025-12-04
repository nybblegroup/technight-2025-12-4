"""
Reset responses for a participant - allows re-testing the event
"""
from sqlalchemy import text
from database import engine


def reset_participant_responses(participant_id: int = None, event_id: int = 1):
    """
    Reset responses for a participant or all participants in an event
    
    Args:
        participant_id: Specific participant to reset (None = all participants)
        event_id: Event ID to reset
    """
    
    print("🔄 Resetting responses...")
    
    with engine.connect() as conn:
        if participant_id:
            # Reset specific participant
            conn.execute(text(f"""
                DELETE FROM responses 
                WHERE participant_id = {participant_id}
            """))
            
            conn.execute(text(f"""
                UPDATE participants 
                SET points = 0, 
                    responses_count = 0,
                    quality_score = 0.0,
                    sentiment_score = 0.0
                WHERE id = {participant_id}
            """))
            
            print(f"   ✓ Reset participant #{participant_id}")
        else:
            # Reset all participants in event
            conn.execute(text(f"""
                DELETE FROM responses 
                WHERE participant_id IN (
                    SELECT id FROM participants WHERE event_id = {event_id}
                )
            """))
            
            conn.execute(text(f"""
                UPDATE participants 
                SET points = 0, 
                    responses_count = 0,
                    quality_score = 0.0,
                    sentiment_score = 0.0
                WHERE event_id = {event_id}
            """))
            
            print(f"   ✓ Reset all participants in event #{event_id}")
        
        # Delete only user messages (keep bot messages with questions)
        conn.execute(text(f"""
            DELETE FROM messages 
            WHERE event_id = {event_id}
            AND message_type = 'user'
        """))
        
        # Keep only the initial 2 bot messages (welcome + first question)
        conn.execute(text(f"""
            DELETE FROM messages 
            WHERE event_id = {event_id}
            AND message_type = 'bot'
            AND id NOT IN (
                SELECT id FROM messages 
                WHERE event_id = {event_id} 
                AND message_type = 'bot'
                ORDER BY created_at ASC 
                LIMIT 2
            )
        """))
        
        print(f"   ✓ Deleted user messages and extra bot messages")
        
        conn.commit()
    
    print("\n✅ Reset complete!")
    print("🔄 Refresh the page at http://localhost:5173/events/1 to start over")


if __name__ == "__main__":
    print("=" * 60)
    print("  RESET PARTICIPANT RESPONSES")
    print("=" * 60)
    print("\nThis will delete all responses and reset points.")
    print("You'll be able to answer all questions again.\n")
    
    confirm = input("Continue? (yes/no): ")
    
    if confirm.lower() in ['yes', 'y']:
        reset_participant_responses(participant_id=None, event_id=1)
    else:
        print("❌ Cancelled")


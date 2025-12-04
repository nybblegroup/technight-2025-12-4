"""
Seed script to populate the database with sample data for testing
"""
import asyncio
from datetime import datetime, timedelta
from database import SessionLocal
from models import Event, Participant, Question, Badge
from services.gamification_service import gamification_service


async def seed_database():
    """Seed the database with sample data"""
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seed...")
        
        # 1. Seed badges
        print("  ✅ Seeding badges...")
        await gamification_service.seed_badges(db)
        
        # 2. Create sample event
        print("  ✅ Creating sample event...")
        event = Event(
            title="Tech Night: AI en Producción",
            description="Aprende cómo llevar modelos de IA a producción con casos reales y mejores prácticas.",
            event_date=datetime.now(),
            status="live",
            max_participants=100,
            speaker_name="Juan Pérez",
            speaker_avatar="https://i.pravatar.cc/150?img=12",
            event_type="tech_night"
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        print(f"     Event ID: {event.id}")
        
        # 3. Create sample participants
        print("  ✅ Creating sample participants...")
        participants_data = [
            {
                "user_id": "1",
                "name": "María González",
                "email": "maria.gonzalez@nybble.com.ar",
                "avatar_url": "https://i.pravatar.cc/150?img=1",
                "points": 1250,
                "streak": 8
            },
            {
                "user_id": "2",
                "name": "Carlos Ruiz",
                "email": "carlos.ruiz@nybble.com.ar",
                "avatar_url": "https://i.pravatar.cc/150?img=2",
                "points": 1180,
                "streak": 5
            },
            {
                "user_id": "3",
                "name": "Ana Martínez",
                "email": "ana.martinez@nybble.com.ar",
                "avatar_url": "https://i.pravatar.cc/150?img=3",
                "points": 1050,
                "streak": 3
            },
            {
                "user_id": "4",
                "name": "Luis Torres",
                "email": "luis.torres@nybble.com.ar",
                "avatar_url": "https://i.pravatar.cc/150?img=4",
                "points": 920,
                "streak": 2
            },
        ]
        
        for p_data in participants_data:
            participant = Participant(
                event_id=event.id,
                **p_data,
                responses_count=5,
                quality_score=0.8,
                sentiment_score=0.6,
                joined_at=datetime.now() - timedelta(minutes=30)
            )
            db.add(participant)
        
        db.commit()
        print(f"     Created {len(participants_data)} participants")
        
        # 4. Create sample questions
        print("  ✅ Creating sample questions...")
        questions_data = [
            {
                "text": "¿Qué te motivó a unirte a este evento hoy?",
                "question_type": "quick_options",
                "order": 1,
                "options": ["💡 Aprender sobre IA", "🤝 Networking", "🎤 El speaker", "✍️ Escribir mi respuesta"]
            },
            {
                "text": "¿Qué aspecto técnico te resultó más interesante de la presentación?",
                "question_type": "open",
                "order": 2,
                "options": None
            },
            {
                "text": "Del 1 al 5, ¿qué tan clara fue la explicación sobre embeddings?",
                "question_type": "rating",
                "order": 3,
                "options": None
            },
            {
                "text": "¿Implementarías alguna de las técnicas mostradas en tu proyecto actual?",
                "question_type": "quick_options",
                "order": 4,
                "options": ["Definitivamente sí", "Probablemente", "Necesito investigar más", "No aplica a mi caso"]
            },
            {
                "text": "¿Qué te gustaría que profundicemos en la próxima sesión?",
                "question_type": "open",
                "order": 5,
                "options": None
            }
        ]
        
        created_questions = []
        for q_data in questions_data:
            question = Question(
                event_id=event.id,
                **q_data,
                is_ai_generated=False,
                asked_at=datetime.now() - timedelta(minutes=25)
            )
            db.add(question)
            created_questions.append(question)
        
        db.commit()
        print(f"     Created {len(questions_data)} questions")
        
        # 4.5. Create initial bot messages
        print("  ✅ Creating initial bot messages...")
        from models import Message
        
        # Welcome message
        welcome_msg = Message(
            event_id=event.id,
            text="¡Hola! 👋 Bienvenido al Tech Night de hoy. Soy tu asistente IA y voy a guiarte en esta experiencia.<br><br>Tus respuestas nos ayudan a mejorar y vos ganás puntos para el ranking. ¡Empecemos! 🚀",
            message_type="bot"
        )
        db.add(welcome_msg)
        
        # First question message
        first_question = created_questions[0]
        first_question_msg = Message(
            event_id=event.id,
            text=f"Pregunta 1 de {len(questions_data)}:<br><strong>{first_question.text}</strong>",
            message_type="bot"
        )
        db.add(first_question_msg)
        
        db.commit()
        print(f"     Created {2} initial messages")
        
        # 6. Update rankings
        print("  ✅ Updating rankings...")
        await gamification_service.recalculate_rankings(db, event.id)
        
        print("✨ Database seeding completed successfully!")
        print(f"\n📌 Sample Event Created:")
        print(f"   ID: {event.id}")
        print(f"   Title: {event.title}")
        print(f"   URL: http://localhost:5173/events/{event.id}")
        print(f"\n🚀 Start the frontend with: npm run dev:frontend")
        print(f"🔧 Backend should be running on: http://localhost:8080")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  NYBBLE EVENT HUB - DATABASE SEED")
    print("=" * 60)
    asyncio.run(seed_database())


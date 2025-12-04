"""
Participant-related API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime
from database import get_db
from models import Participant, Event
from schemas import (
    CreateParticipantDto, ParticipantResponse,
    ParticipantStatsResponse, BadgeResponse, ParticipantBadgeResponse
)
from services.mock_apis import people_force_service

router = APIRouter(prefix="/api/participants", tags=["Participants"])


@router.post("", response_model=ParticipantResponse, status_code=201)
async def join_event(
    participant_data: CreateParticipantDto,
    db: Session = Depends(get_db)
):
    """Join an event as a participant"""
    # Check if event exists
    event = db.query(Event).filter(Event.id == participant_data.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if already joined
    existing = db.query(Participant).filter(
        Participant.event_id == participant_data.event_id,
        Participant.user_id == participant_data.user_id
    ).first()
    
    if existing:
        # Ensure initial messages exist for this event
        await _ensure_initial_messages(db, participant_data.event_id)
        return ParticipantResponse.from_orm(existing)
    
    # Get Nybbler data from People Force (mock)
    nybbler = await people_force_service.get_nybbler_by_id(participant_data.user_id)
    if not nybbler:
        nybbler = await people_force_service.get_nybbler_by_email(participant_data.email)
    
    # Create participant
    participant = Participant(
        event_id=participant_data.event_id,
        user_id=participant_data.user_id,
        name=participant_data.name,
        email=participant_data.email,
        avatar_url=participant_data.avatar_url or (nybbler.avatar_url if nybbler else None),
        points=0,
        streak=0,
        responses_count=0,
        quality_score=0.0,
        sentiment_score=0.0,
        last_activity_at=datetime.now()
    )
    
    db.add(participant)
    db.commit()
    db.refresh(participant)
    
    # Ensure initial messages exist
    await _ensure_initial_messages(db, participant_data.event_id)
    
    return ParticipantResponse.from_orm(participant)


async def _ensure_initial_messages(db: Session, event_id: int):
    """Ensure initial bot messages exist for the event"""
    from models import Message, Question
    
    # Check if initial messages already exist
    message_count = db.query(Message).filter(
        Message.event_id == event_id,
        Message.message_type == 'bot'
    ).count()
    
    if message_count >= 2:
        return  # Already have initial messages
    
    # Get first question
    first_question = db.query(Question).filter(
        Question.event_id == event_id
    ).order_by(Question.order).first()
    
    if not first_question:
        return  # No questions yet
    
    # Get total questions count
    total_questions = db.query(Question).filter(
        Question.event_id == event_id
    ).count()
    
    # Delete existing messages to recreate them properly
    db.query(Message).filter(
        Message.event_id == event_id,
        Message.message_type == 'bot'
    ).delete()
    
    # Create welcome message
    welcome_msg = Message(
        event_id=event_id,
        text="¡Hola! 👋 Bienvenido al Tech Night de hoy. Soy tu asistente IA y voy a guiarte en esta experiencia.<br><br>Tus respuestas nos ayudan a mejorar y vos ganás puntos para el ranking. ¡Empecemos! 🚀",
        message_type="bot"
    )
    db.add(welcome_msg)
    
    # Create first question message
    first_question_msg = Message(
        event_id=event_id,
        text=f"Pregunta 1 de {total_questions}:<br><strong>{first_question.text}</strong>",
        message_type="bot"
    )
    db.add(first_question_msg)
    
    db.commit()


@router.get("/{participant_id}", response_model=ParticipantResponse)
async def get_participant(
    participant_id: int,
    db: Session = Depends(get_db)
):
    """Get participant details"""
    participant = db.query(Participant).filter(Participant.id == participant_id).first()
    
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    return ParticipantResponse.from_orm(participant)


@router.get("/{participant_id}/stats", response_model=ParticipantStatsResponse)
async def get_participant_stats(
    participant_id: int,
    db: Session = Depends(get_db)
):
    """Get participant statistics across all events"""
    participant = db.query(Participant).filter(Participant.id == participant_id).first()
    
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    # Get all participations for this user
    all_participations = db.query(Participant).filter(
        Participant.user_id == participant.user_id
    ).all()
    
    total_events = len(all_participations)
    total_points = sum(p.points for p in all_participations)
    total_responses = sum(p.responses_count for p in all_participations)
    
    avg_quality = 0.0
    if all_participations:
        avg_quality = sum(p.quality_score for p in all_participations) / total_events
    
    # Get all badges
    all_badges = []
    for p in all_participations:
        for pb in p.badges:
            badge_response = BadgeResponse.from_orm(pb.badge)
            if badge_response not in all_badges:
                all_badges.append(badge_response)
    
    # Rank history (simplified - just current ranks)
    rank_history = [
        {
            "event_id": p.event_id,
            "rank": p.rank_position,
            "points": p.points
        }
        for p in all_participations
    ]
    
    return ParticipantStatsResponse(
        participant_id=participant_id,
        total_events=total_events,
        total_points=total_points,
        total_responses=total_responses,
        average_quality_score=round(avg_quality, 2),
        current_streak=participant.streak,
        badges_earned=all_badges,
        rank_history=rank_history
    )


@router.get("/{participant_id}/badges", response_model=List[ParticipantBadgeResponse])
async def get_participant_badges(
    participant_id: int,
    db: Session = Depends(get_db)
):
    """Get participant's earned badges"""
    participant = db.query(Participant).filter(Participant.id == participant_id).first()
    
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    return [ParticipantBadgeResponse.from_orm(pb) for pb in participant.badges]


@router.post("/{participant_id}/reset")
async def reset_participant_responses(
    participant_id: int,
    db: Session = Depends(get_db)
):
    """Reset participant's responses, points, and stats (for testing)"""
    participant = db.query(Participant).filter(Participant.id == participant_id).first()
    
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    from models import Response, Message
    
    # Delete all responses
    db.query(Response).filter(Response.participant_id == participant_id).delete()
    
    # Delete user messages
    db.query(Message).filter(
        Message.participant_id == participant_id,
        Message.message_type == 'user'
    ).delete()
    
    # Reset participant stats
    participant.points = 0
    participant.responses_count = 0
    participant.quality_score = 0.0
    participant.sentiment_score = 0.0
    participant.rank_position = None
    
    db.commit()
    db.refresh(participant)
    
    return {
        "message": "Participant responses reset successfully",
        "participant_id": participant_id,
        "points": participant.points
    }


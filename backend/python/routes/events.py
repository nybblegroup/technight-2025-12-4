"""
Event-related API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List
from database import get_db
from models import Event, Participant
from schemas import (
    CreateEventDto, UpdateEventDto, EventResponse,
    EventStatsResponse, RankingResponse, ParticipantResponse
)
from services.mock_apis import google_calendar_service, slack_service

router = APIRouter(prefix="/api/events", tags=["Events"])


@router.get("", response_model=List[EventResponse])
async def get_events(
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get all events, optionally filtered by status"""
    query = db.query(Event)
    
    if status:
        query = query.filter(Event.status == status)
    
    events = query.order_by(desc(Event.event_date)).all()
    
    # Add participant count
    result = []
    for event in events:
        event_dict = EventResponse.from_orm(event).dict()
        event_dict["participant_count"] = len(event.participants)
        result.append(EventResponse(**event_dict))
    
    return result


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific event by ID"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event_dict = EventResponse.from_orm(event).dict()
    event_dict["participant_count"] = len(event.participants)
    
    return EventResponse(**event_dict)


@router.post("", response_model=EventResponse, status_code=201)
async def create_event(
    event_data: CreateEventDto,
    db: Session = Depends(get_db)
):
    """Create a new event"""
    event = Event(
        title=event_data.title,
        description=event_data.description,
        event_date=event_data.event_date,
        max_participants=event_data.max_participants,
        speaker_name=event_data.speaker_name,
        speaker_avatar=event_data.speaker_avatar,
        event_type=event_data.event_type,
        status="upcoming"
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    # Create Google Calendar event (mock)
    calendar_event = await google_calendar_service.create_event(
        title=event.title,
        start_time=event.event_date,
        end_time=event.event_date,
        attendees=[]
    )
    
    event.google_calendar_id = calendar_event.id
    db.commit()
    db.refresh(event)
    
    event_dict = EventResponse.from_orm(event).dict()
    event_dict["participant_count"] = 0
    
    return EventResponse(**event_dict)


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_data: UpdateEventDto,
    db: Session = Depends(get_db)
):
    """Update an event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Update fields
    update_data = event_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    db.commit()
    db.refresh(event)
    
    event_dict = EventResponse.from_orm(event).dict()
    event_dict["participant_count"] = len(event.participants)
    
    return EventResponse(**event_dict)


@router.delete("/{event_id}", status_code=204)
async def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Delete an event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Delete Google Calendar event (mock)
    if event.google_calendar_id:
        await google_calendar_service.delete_event(event.google_calendar_id)
    
    db.delete(event)
    db.commit()


@router.get("/{event_id}/stats", response_model=EventStatsResponse)
async def get_event_stats(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get event statistics"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Calculate statistics
    participants = event.participants
    total_participants = len(participants)
    
    total_responses = sum(p.responses_count for p in participants)
    
    avg_quality = 0.0
    avg_sentiment = 0.0
    if participants:
        avg_quality = sum(p.quality_score for p in participants) / total_participants
        avg_sentiment = sum(p.sentiment_score for p in participants) / total_participants
    
    # Calculate completion rate
    from models import Question
    total_questions = db.query(Question).filter(
        Question.event_id == event_id
    ).count()
    
    completion_rate = 0.0
    if total_questions > 0 and total_participants > 0:
        completion_rate = (total_responses / (total_questions * total_participants)) * 100
    
    # Get top participants
    top_participants = db.query(Participant).filter(
        Participant.event_id == event_id
    ).order_by(desc(Participant.points)).limit(10).all()
    
    top_rankings = []
    for i, p in enumerate(top_participants, start=1):
        participant_response = ParticipantResponse.from_orm(p)
        ranking = RankingResponse(
            position=i,
            participant=participant_response,
            badges=[pb.badge.icon for pb in p.badges]
        )
        top_rankings.append(ranking)
    
    return EventStatsResponse(
        event_id=event_id,
        total_participants=total_participants,
        total_responses=total_responses,
        average_quality_score=round(avg_quality, 2),
        average_sentiment_score=round(avg_sentiment, 2),
        completion_rate=round(completion_rate, 2),
        top_participants=top_rankings
    )


@router.get("/{event_id}/rankings", response_model=List[RankingResponse])
async def get_event_rankings(
    event_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get event rankings/leaderboard"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    participants = db.query(Participant).filter(
        Participant.event_id == event_id
    ).order_by(desc(Participant.points)).limit(limit).all()
    
    rankings = []
    for i, p in enumerate(participants, start=1):
        participant_response = ParticipantResponse.from_orm(p)
        ranking = RankingResponse(
            position=i,
            participant=participant_response,
            badges=[pb.badge.icon for pb in p.badges]
        )
        rankings.append(ranking)
    
    return rankings


@router.post("/{event_id}/start")
async def start_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Start an event (change status to live)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event.status = "live"
    db.commit()
    
    # Send Slack notification (mock)
    await slack_service.notify_event_start(
        event_title=event.title,
        event_url=f"http://localhost:5173/events/{event_id}"
    )
    
    return {"message": "Event started", "status": "live"}


@router.post("/{event_id}/complete")
async def complete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Complete an event (change status to completed)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event.status = "completed"
    db.commit()
    
    # Send thank you emails (mock)
    from services.mock_apis import email_service
    for participant in event.participants:
        await email_service.send_thank_you_email(
            email=participant.email,
            participant_name=participant.name,
            event_title=event.title,
            points_earned=participant.points
        )
    
    return {"message": "Event completed", "status": "completed"}






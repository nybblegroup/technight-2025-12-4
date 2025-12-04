"""
Response-related API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime
from database import get_db
from models import Response, Question, Participant
from schemas import CreateResponseDto, ResponseResponse
from services.gemini_service import gemini_service
from services.gamification_service import gamification_service
from services.mock_apis import slack_service

router = APIRouter(prefix="/api/responses", tags=["Responses"])


@router.get("", response_model=List[ResponseResponse])
async def get_responses(
    question_id: int = None,
    participant_id: int = None,
    db: Session = Depends(get_db)
):
    """Get all responses, optionally filtered by question or participant"""
    query = db.query(Response)
    
    if question_id:
        query = query.filter(Response.question_id == question_id)
    
    if participant_id:
        query = query.filter(Response.participant_id == participant_id)
    
    responses = query.order_by(desc(Response.created_at)).all()
    
    # Add participant name to each response
    result = []
    for response in responses:
        response_dict = ResponseResponse.from_orm(response).dict()
        response_dict["participant_name"] = response.participant.name
        result.append(ResponseResponse(**response_dict))
    
    return result


@router.get("/{response_id}", response_model=ResponseResponse)
async def get_response(
    response_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific response"""
    response = db.query(Response).filter(Response.id == response_id).first()
    
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    
    response_dict = ResponseResponse.from_orm(response).dict()
    response_dict["participant_name"] = response.participant.name
    
    return ResponseResponse(**response_dict)


@router.post("", response_model=ResponseResponse, status_code=201)
async def create_response(
    response_data: CreateResponseDto,
    db: Session = Depends(get_db)
):
    """Create a new response to a question"""
    # Check if question exists
    question = db.query(Question).filter(Question.id == response_data.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check if participant exists
    participant = db.query(Participant).filter(Participant.id == response_data.participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    # Check if participant already responded to this question
    existing = db.query(Response).filter(
        Response.question_id == response_data.question_id,
        Response.participant_id == response_data.participant_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Participant already responded to this question")
    
    # Analyze sentiment with Gemini AI
    sentiment_analysis = await gemini_service.analyze_sentiment(response_data.text)
    
    # Calculate quality score
    quality_score = await gemini_service.calculate_quality_score(
        text=response_data.text,
        question_text=question.text
    )
    
    # Check if this is the first response
    is_first_response = db.query(Response).filter(
        Response.question_id == response_data.question_id
    ).count() == 0
    
    # Calculate points
    points_awarded = gamification_service.calculate_response_points(
        text=response_data.text,
        is_quick_option=response_data.is_quick_option,
        quality_score=quality_score,
        sentiment=sentiment_analysis.sentiment,
        response_time_seconds=None,
        is_first_response=is_first_response
    )
    
    # Create response
    response = Response(
        question_id=response_data.question_id,
        participant_id=response_data.participant_id,
        text=response_data.text,
        rating=response_data.rating,
        sentiment=sentiment_analysis.sentiment,
        sentiment_score=sentiment_analysis.score,
        quality_score=quality_score,
        is_quick_option=response_data.is_quick_option,
        points_awarded=points_awarded
    )
    
    db.add(response)
    db.commit()
    db.refresh(response)
    
    # Update participant points
    await gamification_service.update_participant_points(
        db=db,
        participant=participant,
        points=points_awarded
    )
    
    # Update participant stats
    if sentiment_analysis.score != 0:
        # Update running average of sentiment
        total_responses = participant.responses_count
        participant.sentiment_score = (
            (participant.sentiment_score * (total_responses - 1)) + sentiment_analysis.score
        ) / total_responses
        
        participant.quality_score = (
            (participant.quality_score * (total_responses - 1)) + quality_score
        ) / total_responses
    
    participant.last_activity_at = datetime.now()
    db.commit()
    
    # Check and award badges
    new_badges = await gamification_service.check_and_award_badges(
        db=db,
        participant=participant,
        response=response
    )
    
    # If high quality response, notify on Slack (mock)
    if quality_score >= 0.7 and len(response_data.text) > 50:
        await slack_service.notify_new_response(
            participant_name=participant.name,
            response_text=response_data.text
        )
    
    # Prepare response
    response_dict = ResponseResponse.from_orm(response).dict()
    response_dict["participant_name"] = participant.name
    
    return ResponseResponse(**response_dict)


@router.get("/top/quality", response_model=List[ResponseResponse])
async def get_top_quality_responses(
    event_id: int,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """Get top quality responses for an event"""
    from models import Question as Q
    
    responses = db.query(Response).join(Q).filter(
        Q.event_id == event_id,
        Response.quality_score >= 0.7
    ).order_by(
        desc(Response.quality_score),
        desc(Response.created_at)
    ).limit(limit).all()
    
    result = []
    for response in responses:
        response_dict = ResponseResponse.from_orm(response).dict()
        response_dict["participant_name"] = response.participant.name
        result.append(ResponseResponse(**response_dict))
    
    return result






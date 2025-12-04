"""
Question-related API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models import Question, Event
from schemas import CreateQuestionDto, QuestionResponse, GenerateQuestionRequest, GenerateQuestionResponse
from services.gemini_service import gemini_service

router = APIRouter(prefix="/api/questions", tags=["Questions"])


@router.get("", response_model=List[QuestionResponse])
async def get_questions(
    event_id: int = None,
    db: Session = Depends(get_db)
):
    """Get all questions, optionally filtered by event"""
    query = db.query(Question)
    
    if event_id:
        query = query.filter(Question.event_id == event_id)
    
    questions = query.order_by(Question.order).all()
    return [QuestionResponse.from_orm(q) for q in questions]


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific question"""
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return QuestionResponse.from_orm(question)


@router.post("", response_model=QuestionResponse, status_code=201)
async def create_question(
    question_data: CreateQuestionDto,
    db: Session = Depends(get_db)
):
    """Create a new question"""
    # Check if event exists
    event = db.query(Event).filter(Event.id == question_data.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    question = Question(
        event_id=question_data.event_id,
        text=question_data.text,
        question_type=question_data.question_type,
        order=question_data.order,
        options=question_data.options,
        is_ai_generated=question_data.is_ai_generated,
        ai_context=question_data.ai_context,
        asked_at=datetime.now()
    )
    
    db.add(question)
    db.commit()
    db.refresh(question)
    
    return QuestionResponse.from_orm(question)


@router.post("/generate", response_model=GenerateQuestionResponse)
async def generate_question_with_ai(
    request: GenerateQuestionRequest,
    db: Session = Depends(get_db)
):
    """Generate a question using Gemini AI"""
    # Check if event exists
    event = db.query(Event).filter(Event.id == request.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Generate question with AI
    generated = await gemini_service.generate_question(
        context=request.context or event.title,
        previous_questions=request.previous_questions,
        question_type="open"
    )
    
    return generated


@router.delete("/{question_id}", status_code=204)
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Delete a question"""
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db.delete(question)
    db.commit()






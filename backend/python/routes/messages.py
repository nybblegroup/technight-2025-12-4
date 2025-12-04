"""
Message-related API endpoints (for chat interface)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from database import get_db
from models import Message, Event, Participant
from schemas import CreateMessageDto, MessageResponse

router = APIRouter(prefix="/api/messages", tags=["Messages"])


@router.get("", response_model=List[MessageResponse])
async def get_messages(
    event_id: int,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get messages for an event (chat history)"""
    messages = db.query(Message).filter(
        Message.event_id == event_id
    ).order_by(Message.created_at).limit(limit).all()
    
    result = []
    for message in messages:
        message_dict = MessageResponse.from_orm(message).dict()
        
        if message.participant_id:
            participant = db.query(Participant).filter(
                Participant.id == message.participant_id
            ).first()
            if participant:
                message_dict["participant_name"] = participant.name
                message_dict["participant_avatar"] = participant.avatar_url
        
        result.append(MessageResponse(**message_dict))
    
    return result


@router.post("", response_model=MessageResponse, status_code=201)
async def create_message(
    message_data: CreateMessageDto,
    db: Session = Depends(get_db)
):
    """Create a new message in the chat"""
    # Check if event exists
    event = db.query(Event).filter(Event.id == message_data.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # If participant_id is provided, check if participant exists
    if message_data.participant_id:
        participant = db.query(Participant).filter(
            Participant.id == message_data.participant_id
        ).first()
        if not participant:
            raise HTTPException(status_code=404, detail="Participant not found")
    
    # Create message
    message = Message(
        event_id=message_data.event_id,
        participant_id=message_data.participant_id,
        text=message_data.text,
        message_type=message_data.message_type
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    # Prepare response
    message_dict = MessageResponse.from_orm(message).dict()
    
    if message.participant_id:
        participant = db.query(Participant).filter(
            Participant.id == message.participant_id
        ).first()
        if participant:
            message_dict["participant_name"] = participant.name
            message_dict["participant_avatar"] = participant.avatar_url
    
    return MessageResponse(**message_dict)


@router.delete("/{message_id}", status_code=204)
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    """Delete a message"""
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    db.delete(message)
    db.commit()






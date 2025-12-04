"""
Pydantic schemas (DTOs) for Nybble Event Engagement Hub
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Any
from datetime import datetime


# ========== EVENT SCHEMAS ==========

class EventBase(BaseModel):
    """Base Event schema"""
    title: str = Field(..., min_length=1, max_length=300)
    description: Optional[str] = None
    event_date: datetime
    max_participants: Optional[int] = None
    speaker_name: Optional[str] = None
    speaker_avatar: Optional[str] = None
    event_type: Optional[str] = "tech_night"


class CreateEventDto(EventBase):
    """DTO for creating a new Event"""
    pass


class UpdateEventDto(BaseModel):
    """DTO for updating an Event"""
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    status: Optional[str] = None
    max_participants: Optional[int] = None
    speaker_name: Optional[str] = None
    speaker_avatar: Optional[str] = None
    event_type: Optional[str] = None


class EventResponse(EventBase):
    """Response schema for Event"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    google_calendar_id: Optional[str] = None
    participant_count: Optional[int] = 0
    
    class Config:
        from_attributes = True


# ========== PARTICIPANT SCHEMAS ==========

class ParticipantBase(BaseModel):
    """Base Participant schema"""
    user_id: str
    name: str
    email: EmailStr
    avatar_url: Optional[str] = None


class CreateParticipantDto(ParticipantBase):
    """DTO for creating/joining a participant to an event"""
    event_id: int


class ParticipantResponse(ParticipantBase):
    """Response schema for Participant"""
    id: int
    event_id: int
    points: int
    streak: int
    rank_position: Optional[int] = None
    responses_count: int
    quality_score: float
    sentiment_score: float
    joined_at: datetime
    last_activity_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RankingResponse(BaseModel):
    """Response schema for Rankings/Leaderboard"""
    position: int
    participant: ParticipantResponse
    badges: List[str] = []  # Badge icons


# ========== QUESTION SCHEMAS ==========

class QuestionBase(BaseModel):
    """Base Question schema"""
    text: str
    question_type: str = "open"  # open, rating, multiple_choice, quick_options
    options: Optional[List[str]] = None


class CreateQuestionDto(QuestionBase):
    """DTO for creating a Question"""
    event_id: int
    order: int = 1
    is_ai_generated: bool = False
    ai_context: Optional[str] = None


class QuestionResponse(QuestionBase):
    """Response schema for Question"""
    id: int
    event_id: int
    order: int
    is_ai_generated: bool
    asked_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ========== RESPONSE SCHEMAS ==========

class CreateResponseDto(BaseModel):
    """DTO for creating a Response"""
    question_id: int
    participant_id: int
    text: str
    rating: Optional[int] = Field(None, ge=1, le=5)
    is_quick_option: bool = False


class ResponseResponse(BaseModel):
    """Response schema for Response"""
    id: int
    question_id: int
    participant_id: int
    text: str
    rating: Optional[int] = None
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    quality_score: Optional[float] = None
    points_awarded: int
    created_at: datetime
    participant_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# ========== MESSAGE SCHEMAS ==========

class CreateMessageDto(BaseModel):
    """DTO for creating a Message"""
    event_id: int
    participant_id: Optional[int] = None
    text: str
    message_type: str = "user"  # bot, user, system, notification


class MessageResponse(BaseModel):
    """Response schema for Message"""
    id: int
    event_id: int
    participant_id: Optional[int] = None
    text: str
    message_type: str
    created_at: datetime
    participant_name: Optional[str] = None
    participant_avatar: Optional[str] = None
    
    class Config:
        from_attributes = True


# ========== BADGE SCHEMAS ==========

class BadgeBase(BaseModel):
    """Base Badge schema"""
    name: str
    display_name: str
    description: str
    icon: str  # Emoji
    criteria_type: str
    criteria_value: int
    rarity: str = "common"


class CreateBadgeDto(BadgeBase):
    """DTO for creating a Badge"""
    pass


class BadgeResponse(BadgeBase):
    """Response schema for Badge"""
    id: int
    
    class Config:
        from_attributes = True


class ParticipantBadgeResponse(BaseModel):
    """Response schema for Participant's earned badges"""
    id: int
    badge: BadgeResponse
    earned_at: datetime
    
    class Config:
        from_attributes = True


# ========== GEMINI AI SCHEMAS ==========

class SentimentAnalysisRequest(BaseModel):
    """Request for sentiment analysis"""
    text: str


class SentimentAnalysisResponse(BaseModel):
    """Response from sentiment analysis"""
    sentiment: str  # positive, negative, neutral
    score: float  # -1.0 to 1.0
    confidence: float  # 0.0 to 1.0


class GenerateQuestionRequest(BaseModel):
    """Request for AI-generated question"""
    event_id: int
    context: str
    previous_questions: List[str] = []


class GenerateQuestionResponse(BaseModel):
    """Response with AI-generated question"""
    text: str
    question_type: str
    options: Optional[List[str]] = None
    reasoning: str


# ========== STATS & ANALYTICS SCHEMAS ==========

class EventStatsResponse(BaseModel):
    """Event statistics"""
    event_id: int
    total_participants: int
    total_responses: int
    average_quality_score: float
    average_sentiment_score: float
    completion_rate: float
    top_participants: List[RankingResponse]


class ParticipantStatsResponse(BaseModel):
    """Participant statistics"""
    participant_id: int
    total_events: int
    total_points: int
    total_responses: int
    average_quality_score: float
    current_streak: int
    badges_earned: List[BadgeResponse]
    rank_history: List[dict]


# ========== MOCK API SCHEMAS ==========

class NybblerDto(BaseModel):
    """Nybbler from People Force (mock)"""
    id: str
    name: str
    email: str
    avatar_url: str
    department: Optional[str] = None
    position: Optional[str] = None


class CalendarEventDto(BaseModel):
    """Calendar event (mock)"""
    id: str
    title: str
    start_time: datetime
    end_time: datetime
    attendees: List[str] = []


class SlackNotificationDto(BaseModel):
    """Slack notification (mock)"""
    channel: str
    message: str
    user_id: Optional[str] = None


# Keep Example schemas for backward compatibility
class ExampleResponse(BaseModel):
    """Response schema for Example entity"""
    id: int
    name: str
    title: str
    entryDate: datetime = Field(..., alias="entry_date")
    description: Optional[str] = None
    isActive: bool = Field(..., alias="is_active")
    
    class Config:
        from_attributes = True
        populate_by_name = True


class CreateExampleDto(BaseModel):
    """DTO for creating a new Example"""
    name: str = Field(..., min_length=1, max_length=200)
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    isActive: Optional[bool] = Field(True)


class UpdateExampleDto(BaseModel):
    """DTO for updating an existing Example"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    isActive: Optional[bool] = None


"""
SQLAlchemy models for the Nybble Event Engagement Hub
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Event(Base):
    """
    Event entity representing a Nybble event (Tech Night, Workshop, etc.)
    """
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), nullable=False, default='upcoming')  # upcoming, live, completed, cancelled
    max_participants = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    # Event metadata
    speaker_name = Column(String(200), nullable=True)
    speaker_avatar = Column(String(500), nullable=True)
    event_type = Column(String(100), nullable=True)  # tech_night, workshop, webinar, etc.
    
    # Google Calendar integration (mock)
    google_calendar_id = Column(String(300), nullable=True)
    
    # Relations
    participants = relationship("Participant", back_populates="event", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="event", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="event", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_events_status', 'status'),
        Index('ix_events_event_date', 'event_date'),
    )


class Participant(Base):
    """
    Participant in an event
    """
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    
    # User info (from People Force mock)
    user_id = Column(String(100), nullable=False)  # External ID from People Force
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    
    # Gamification
    points = Column(Integer, nullable=False, default=0)
    streak = Column(Integer, nullable=False, default=0)  # Consecutive events
    rank_position = Column(Integer, nullable=True)
    
    # Stats
    responses_count = Column(Integer, nullable=False, default=0)
    quality_score = Column(Float, nullable=False, default=0.0)  # AI-calculated quality
    sentiment_score = Column(Float, nullable=False, default=0.0)  # Positive/Negative/Neutral
    
    # Timestamps
    joined_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_activity_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relations
    event = relationship("Event", back_populates="participants")
    responses = relationship("Response", back_populates="participant", cascade="all, delete-orphan")
    badges = relationship("ParticipantBadge", back_populates="participant", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_participants_event_id', 'event_id'),
        Index('ix_participants_user_id', 'user_id'),
        Index('ix_participants_points', 'points'),
    )


class Question(Base):
    """
    Question asked during an event
    """
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    
    # Question content
    text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # open, rating, multiple_choice, quick_options
    order = Column(Integer, nullable=False)  # Question order in the sequence
    
    # Options for multiple choice / quick options
    options = Column(JSON, nullable=True)  # ["Option 1", "Option 2", ...]
    
    # AI-generated or manual
    is_ai_generated = Column(Boolean, nullable=False, default=False)
    ai_context = Column(Text, nullable=True)  # Context used for AI generation
    
    # Timing
    asked_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relations
    event = relationship("Event", back_populates="questions")
    responses = relationship("Response", back_populates="question", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_questions_event_id', 'event_id'),
        Index('ix_questions_order', 'order'),
    )


class Response(Base):
    """
    Participant's response to a question
    """
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    participant_id = Column(Integer, ForeignKey('participants.id', ondelete='CASCADE'), nullable=False)
    
    # Response content
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)  # For rating type questions (1-5)
    
    # AI Analysis
    sentiment = Column(String(50), nullable=True)  # positive, negative, neutral
    sentiment_score = Column(Float, nullable=True)  # -1.0 to 1.0
    quality_score = Column(Float, nullable=True)  # 0.0 to 1.0
    ai_summary = Column(Text, nullable=True)  # AI-generated summary
    
    # Metadata
    response_time_seconds = Column(Integer, nullable=True)  # Time taken to respond
    is_quick_option = Column(Boolean, nullable=False, default=False)
    
    # Points awarded for this response
    points_awarded = Column(Integer, nullable=False, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Relations
    question = relationship("Question", back_populates="responses")
    participant = relationship("Participant", back_populates="responses")
    
    __table_args__ = (
        Index('ix_responses_question_id', 'question_id'),
        Index('ix_responses_participant_id', 'participant_id'),
        Index('ix_responses_sentiment', 'sentiment'),
    )


class Message(Base):
    """
    Chat message in the conversational interface
    """
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    participant_id = Column(Integer, ForeignKey('participants.id', ondelete='CASCADE'), nullable=True)
    
    # Message content
    text = Column(Text, nullable=False)
    message_type = Column(String(50), nullable=False)  # bot, user, system, notification
    
    # Metadata
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Relations
    event = relationship("Event", back_populates="messages")
    
    __table_args__ = (
        Index('ix_messages_event_id', 'event_id'),
        Index('ix_messages_created_at', 'created_at'),
    )


class Badge(Base):
    """
    Badge definition (template)
    """
    __tablename__ = "badges"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Badge info
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(10), nullable=False)  # Emoji icon
    
    # Requirements
    criteria_type = Column(String(50), nullable=False)  # points_threshold, streak, responses_count, quality_score, etc.
    criteria_value = Column(Integer, nullable=False)
    
    # Rarity
    rarity = Column(String(50), nullable=False, default='common')  # common, rare, epic, legendary
    
    # Relations
    participant_badges = relationship("ParticipantBadge", back_populates="badge")
    
    __table_args__ = (
        Index('ix_badges_name', 'name'),
    )


class ParticipantBadge(Base):
    """
    Badges earned by participants
    """
    __tablename__ = "participant_badges"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    participant_id = Column(Integer, ForeignKey('participants.id', ondelete='CASCADE'), nullable=False)
    badge_id = Column(Integer, ForeignKey('badges.id', ondelete='CASCADE'), nullable=False)
    
    # When earned
    earned_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Relations
    participant = relationship("Participant", back_populates="badges")
    badge = relationship("Badge", back_populates="participant_badges")
    
    __table_args__ = (
        Index('ix_participant_badges_participant_id', 'participant_id'),
        Index('ix_participant_badges_badge_id', 'badge_id'),
    )


# Keep Example model for backward compatibility (can be removed later)
class Example(Base):
    """
    Example entity representing a sample record
    """
    __tablename__ = "example"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    title = Column(String(200), nullable=False)
    entry_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    description = Column(String(1000), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    
    __table_args__ = (
        Index('ix_example_entry_date', 'entry_date'),
    )
    


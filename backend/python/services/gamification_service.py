"""
Gamification Service for points, badges, and rankings
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from models import Participant, Badge, ParticipantBadge, Response
from schemas import BadgeResponse, ParticipantBadgeResponse


class GamificationService:
    """Service for gamification logic"""
    
    # Points configuration
    POINTS_CONFIG = {
        "quick_option": 10,
        "short_response": 15,  # < 50 chars
        "medium_response": 25,  # 50-100 chars
        "long_response": 40,   # 100+ chars
        "quality_bonus": 20,    # High quality response
        "positive_sentiment_bonus": 10,
        "first_response": 50,   # First to respond
        "rating_response": 10,
    }
    
    # Badge criteria
    BADGE_DEFINITIONS = [
        {
            "name": "first_voice",
            "display_name": "First Voice",
            "description": "Primera respuesta en un evento",
            "icon": "🎤",
            "criteria_type": "first_response",
            "criteria_value": 1,
            "rarity": "common"
        },
        {
            "name": "on_fire",
            "display_name": "On Fire",
            "description": "Racha de 5 eventos consecutivos",
            "icon": "🔥",
            "criteria_type": "streak",
            "criteria_value": 5,
            "rarity": "rare"
        },
        {
            "name": "insight_master",
            "display_name": "Insight Master",
            "description": "10 respuestas de alta calidad",
            "icon": "💎",
            "criteria_type": "quality_responses",
            "criteria_value": 10,
            "rarity": "epic"
        },
        {
            "name": "community_leader",
            "display_name": "Community Leader",
            "description": "1000 puntos acumulados",
            "icon": "👑",
            "criteria_type": "total_points",
            "criteria_value": 1000,
            "rarity": "legendary"
        },
        {
            "name": "perfectionist",
            "display_name": "Perfectionist",
            "description": "Completa todas las preguntas de un evento",
            "icon": "🎯",
            "criteria_type": "completion_rate",
            "criteria_value": 100,
            "rarity": "rare"
        },
        {
            "name": "speed_demon",
            "display_name": "Speed Demon",
            "description": "Responde en menos de 10 segundos",
            "icon": "⚡",
            "criteria_type": "fast_response",
            "criteria_value": 10,
            "rarity": "rare"
        },
        {
            "name": "wordsmith",
            "display_name": "Wordsmith",
            "description": "Respuesta de más de 200 caracteres",
            "icon": "✍️",
            "criteria_type": "long_response",
            "criteria_value": 200,
            "rarity": "common"
        },
        {
            "name": "positive_vibes",
            "display_name": "Positive Vibes",
            "description": "10 respuestas con sentimiento positivo",
            "icon": "😊",
            "criteria_type": "positive_sentiment",
            "criteria_value": 10,
            "rarity": "common"
        }
    ]
    
    def calculate_response_points(
        self, 
        text: str,
        is_quick_option: bool,
        quality_score: float,
        sentiment: str,
        response_time_seconds: Optional[int],
        is_first_response: bool = False
    ) -> int:
        """
        Calculate points for a response
        
        Args:
            text: Response text
            is_quick_option: Whether it's a quick option
            quality_score: Quality score from AI
            sentiment: Sentiment (positive/negative/neutral)
            response_time_seconds: Time taken to respond
            is_first_response: Whether this is the first response to the question
            
        Returns:
            Total points awarded
        """
        points = 0
        
        # Base points
        if is_quick_option:
            points += self.POINTS_CONFIG["quick_option"]
        else:
            text_length = len(text)
            if text_length < 50:
                points += self.POINTS_CONFIG["short_response"]
            elif text_length < 100:
                points += self.POINTS_CONFIG["medium_response"]
            else:
                points += self.POINTS_CONFIG["long_response"]
        
        # Quality bonus
        if quality_score >= 0.7:
            points += self.POINTS_CONFIG["quality_bonus"]
        
        # Sentiment bonus
        if sentiment == "positive":
            points += self.POINTS_CONFIG["positive_sentiment_bonus"]
        
        # First response bonus
        if is_first_response:
            points += self.POINTS_CONFIG["first_response"]
        
        return points
    
    async def update_participant_points(
        self, 
        db: Session, 
        participant: Participant, 
        points: int
    ) -> Participant:
        """
        Update participant points and recalculate ranking
        
        Args:
            db: Database session
            participant: Participant to update
            points: Points to add
            
        Returns:
            Updated participant
        """
        participant.points += points
        participant.responses_count += 1
        
        # Recalculate ranking for this event
        await self.recalculate_rankings(db, participant.event_id)
        
        db.commit()
        db.refresh(participant)
        
        return participant
    
    async def recalculate_rankings(self, db: Session, event_id: int):
        """
        Recalculate rankings for an event
        
        Args:
            db: Database session
            event_id: Event ID
        """
        participants = db.query(Participant).filter(
            Participant.event_id == event_id
        ).order_by(desc(Participant.points)).all()
        
        for index, participant in enumerate(participants, start=1):
            participant.rank_position = index
        
        db.commit()
    
    async def check_and_award_badges(
        self, 
        db: Session, 
        participant: Participant,
        response: Optional[Response] = None
    ) -> List[Badge]:
        """
        Check if participant earned any new badges
        
        Args:
            db: Database session
            participant: Participant to check
            response: Recent response (if any)
            
        Returns:
            List of newly earned badges
        """
        awarded_badges = []
        
        # Get existing badges for participant
        existing_badge_names = {
            pb.badge.name for pb in participant.badges
        }
        
        # Check each badge criteria
        for badge_def in self.BADGE_DEFINITIONS:
            if badge_def["name"] in existing_badge_names:
                continue  # Already has this badge
            
            # Get or create badge
            badge = db.query(Badge).filter(Badge.name == badge_def["name"]).first()
            if not badge:
                badge = Badge(**badge_def)
                db.add(badge)
                db.commit()
                db.refresh(badge)
            
            # Check criteria
            earned = await self._check_badge_criteria(
                db, participant, badge, response
            )
            
            if earned:
                # Award badge
                participant_badge = ParticipantBadge(
                    participant_id=participant.id,
                    badge_id=badge.id
                )
                db.add(participant_badge)
                awarded_badges.append(badge)
        
        if awarded_badges:
            db.commit()
        
        return awarded_badges
    
    async def _check_badge_criteria(
        self, 
        db: Session, 
        participant: Participant,
        badge: Badge,
        response: Optional[Response]
    ) -> bool:
        """Check if badge criteria is met"""
        
        if badge.criteria_type == "total_points":
            return participant.points >= badge.criteria_value
        
        elif badge.criteria_type == "streak":
            return participant.streak >= badge.criteria_value
        
        elif badge.criteria_type == "first_response":
            if response:
                # Check if this is the first response to this question
                first_response = db.query(Response).filter(
                    Response.question_id == response.question_id
                ).order_by(Response.created_at).first()
                return first_response.id == response.id
            return False
        
        elif badge.criteria_type == "quality_responses":
            quality_responses = db.query(Response).filter(
                Response.participant_id == participant.id,
                Response.quality_score >= 0.7
            ).count()
            return quality_responses >= badge.criteria_value
        
        elif badge.criteria_type == "positive_sentiment":
            positive_responses = db.query(Response).filter(
                Response.participant_id == participant.id,
                Response.sentiment == "positive"
            ).count()
            return positive_responses >= badge.criteria_value
        
        elif badge.criteria_type == "fast_response":
            if response and response.response_time_seconds:
                return response.response_time_seconds <= badge.criteria_value
            return False
        
        elif badge.criteria_type == "long_response":
            if response:
                return len(response.text) >= badge.criteria_value
            return False
        
        elif badge.criteria_type == "completion_rate":
            # Check if participant answered all questions in event
            from models import Question
            total_questions = db.query(Question).filter(
                Question.event_id == participant.event_id
            ).count()
            participant_responses = participant.responses_count
            
            if total_questions > 0:
                completion = (participant_responses / total_questions) * 100
                return completion >= badge.criteria_value
            return False
        
        return False
    
    async def get_top_participants(
        self, 
        db: Session, 
        event_id: int, 
        limit: int = 10
    ) -> List[Participant]:
        """
        Get top participants by points
        
        Args:
            db: Database session
            event_id: Event ID
            limit: Number of participants to return
            
        Returns:
            List of top participants
        """
        return db.query(Participant).filter(
            Participant.event_id == event_id
        ).order_by(
            desc(Participant.points)
        ).limit(limit).all()
    
    async def seed_badges(self, db: Session):
        """Seed initial badges into database"""
        for badge_def in self.BADGE_DEFINITIONS:
            existing = db.query(Badge).filter(Badge.name == badge_def["name"]).first()
            if not existing:
                badge = Badge(**badge_def)
                db.add(badge)
        
        db.commit()


# Singleton instance
gamification_service = GamificationService()






"""
Mock API services for Calendar, Slack, People Force, and Email
"""
from typing import List, Optional
from datetime import datetime, timedelta
from schemas import NybblerDto, CalendarEventDto, SlackNotificationDto


class PeopleForceService:
    """Mock People Force API for Nybbler data"""
    
    # Mock Nybblers data
    NYBBLERS = [
        NybblerDto(
            id="1",
            name="María González",
            email="maria.gonzalez@nybble.com.ar",
            avatar_url="https://i.pravatar.cc/150?img=1",
            department="Engineering",
            position="Senior Developer"
        ),
        NybblerDto(
            id="2",
            name="Carlos Ruiz",
            email="carlos.ruiz@nybble.com.ar",
            avatar_url="https://i.pravatar.cc/150?img=2",
            department="Engineering",
            position="Tech Lead"
        ),
        NybblerDto(
            id="3",
            name="Ana Martínez",
            email="ana.martinez@nybble.com.ar",
            avatar_url="https://i.pravatar.cc/150?img=3",
            department="Product",
            position="Product Manager"
        ),
        NybblerDto(
            id="4",
            name="Luis Torres",
            email="luis.torres@nybble.com.ar",
            avatar_url="https://i.pravatar.cc/150?img=4",
            department="Engineering",
            position="Full Stack Developer"
        ),
        NybblerDto(
            id="5",
            name="Sofia Fernández",
            email="sofia.fernandez@nybble.com.ar",
            avatar_url="https://i.pravatar.cc/150?img=5",
            department="Design",
            position="UX Designer"
        ),
        NybblerDto(
            id="6",
            name="Diego López",
            email="diego.lopez@nybble.com.ar",
            avatar_url="https://i.pravatar.cc/150?img=6",
            department="Engineering",
            position="Backend Developer"
        ),
        NybblerDto(
            id="7",
            name="Valentina Romero",
            email="valentina.romero@nybble.com.ar",
            avatar_url="https://i.pravatar.cc/150?img=7",
            department="Marketing",
            position="Marketing Manager"
        ),
        NybblerDto(
            id="8",
            name="Martín Silva",
            email="martin.silva@nybble.com.ar",
            avatar_url="https://i.pravatar.cc/150?img=8",
            department="Engineering",
            position="DevOps Engineer"
        ),
        NybblerDto(
            id="9",
            name="Camila Rodríguez",
            email="camila.rodriguez@nybble.com.ar",
            avatar_url="https://i.pravatar.cc/150?img=9",
            department="People & Culture",
            position="HR Manager"
        ),
        NybblerDto(
            id="10",
            name="Francisco Gómez",
            email="francisco.gomez@nybble.com.ar",
            avatar_url="https://i.pravatar.cc/150?img=10",
            department="Engineering",
            position="Frontend Developer"
        ),
    ]
    
    async def get_all_nybblers(self) -> List[NybblerDto]:
        """Get all Nybblers"""
        return self.NYBBLERS
    
    async def search_nybblers(self, query: str) -> List[NybblerDto]:
        """Search Nybblers by name or email"""
        query_lower = query.lower()
        return [
            n for n in self.NYBBLERS 
            if query_lower in n.name.lower() or query_lower in n.email.lower()
        ]
    
    async def get_nybbler_by_id(self, user_id: str) -> Optional[NybblerDto]:
        """Get Nybbler by ID"""
        for nybbler in self.NYBBLERS:
            if nybbler.id == user_id:
                return nybbler
        return None
    
    async def get_nybbler_by_email(self, email: str) -> Optional[NybblerDto]:
        """Get Nybbler by email"""
        for nybbler in self.NYBBLERS:
            if nybbler.email.lower() == email.lower():
                return nybbler
        return None


class GoogleCalendarService:
    """Mock Google Calendar API"""
    
    async def create_event(
        self, 
        title: str, 
        start_time: datetime, 
        end_time: datetime,
        attendees: List[str] = None
    ) -> CalendarEventDto:
        """Create a calendar event (mock)"""
        event_id = f"mock_event_{int(datetime.now().timestamp())}"
        
        return CalendarEventDto(
            id=event_id,
            title=title,
            start_time=start_time,
            end_time=end_time,
            attendees=attendees or []
        )
    
    async def update_event(self, event_id: str, **kwargs) -> CalendarEventDto:
        """Update a calendar event (mock)"""
        # Mock implementation
        return CalendarEventDto(
            id=event_id,
            title=kwargs.get("title", "Updated Event"),
            start_time=kwargs.get("start_time", datetime.now()),
            end_time=kwargs.get("end_time", datetime.now() + timedelta(hours=1)),
            attendees=kwargs.get("attendees", [])
        )
    
    async def delete_event(self, event_id: str) -> bool:
        """Delete a calendar event (mock)"""
        print(f"[MOCK] Deleted calendar event: {event_id}")
        return True
    
    async def get_event(self, event_id: str) -> Optional[CalendarEventDto]:
        """Get a calendar event (mock)"""
        return CalendarEventDto(
            id=event_id,
            title="Mock Event",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            attendees=[]
        )


class SlackService:
    """Mock Slack API"""
    
    async def send_notification(
        self, 
        channel: str, 
        message: str,
        user_id: Optional[str] = None
    ) -> dict:
        """Send a Slack notification (mock)"""
        notification = SlackNotificationDto(
            channel=channel,
            message=message,
            user_id=user_id
        )
        
        print(f"[MOCK SLACK] Channel: {channel}")
        print(f"[MOCK SLACK] Message: {message}")
        if user_id:
            print(f"[MOCK SLACK] User: {user_id}")
        
        return {
            "success": True,
            "ts": str(datetime.now().timestamp()),
            "channel": channel
        }
    
    async def send_dm(self, user_id: str, message: str) -> dict:
        """Send a direct message (mock)"""
        print(f"[MOCK SLACK DM] To: {user_id}")
        print(f"[MOCK SLACK DM] Message: {message}")
        
        return {
            "success": True,
            "ts": str(datetime.now().timestamp())
        }
    
    async def notify_event_start(self, event_title: str, event_url: str) -> dict:
        """Notify about event start (mock)"""
        message = f"🎉 ¡{event_title} está por comenzar! Únete aquí: {event_url}"
        return await self.send_notification("#tech-events", message)
    
    async def notify_new_response(self, participant_name: str, response_text: str) -> dict:
        """Notify about new top response (mock)"""
        message = f"💎 Top respuesta de {participant_name}: \"{response_text[:100]}...\""
        return await self.send_notification("#tech-events", message)


class EmailService:
    """Mock Email Service (SendGrid/AWS SES)"""
    
    async def send_email(
        self, 
        to: str, 
        subject: str, 
        body: str,
        html_body: Optional[str] = None
    ) -> dict:
        """Send an email (mock)"""
        print(f"[MOCK EMAIL] To: {to}")
        print(f"[MOCK EMAIL] Subject: {subject}")
        print(f"[MOCK EMAIL] Body: {body[:100]}...")
        
        return {
            "success": True,
            "message_id": f"mock_email_{int(datetime.now().timestamp())}",
            "to": to
        }
    
    async def send_event_reminder(self, email: str, event_title: str, event_date: datetime) -> dict:
        """Send event reminder email (mock)"""
        subject = f"Recordatorio: {event_title}"
        body = f"""
        Hola!
        
        Te recordamos que {event_title} será el {event_date.strftime('%d/%m/%Y a las %H:%M')}.
        
        ¡No te lo pierdas!
        
        Saludos,
        Equipo Nybble
        """
        
        return await self.send_email(email, subject, body)
    
    async def send_thank_you_email(
        self, 
        email: str, 
        participant_name: str,
        event_title: str, 
        points_earned: int
    ) -> dict:
        """Send thank you email after event (mock)"""
        subject = f"Gracias por participar en {event_title}"
        body = f"""
        Hola {participant_name}!
        
        Gracias por participar en {event_title}.
        
        Ganaste {points_earned} puntos en esta sesión. 
        
        ¡Esperamos verte en el próximo evento!
        
        Saludos,
        Equipo Nybble
        """
        
        return await self.send_email(email, subject, body)


# Singleton instances
people_force_service = PeopleForceService()
google_calendar_service = GoogleCalendarService()
slack_service = SlackService()
email_service = EmailService()






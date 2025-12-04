import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api, EventResponse, ParticipantResponse, QuestionResponse, MessageResponse, RankingResponse } from '../utils/api';
import { RankingSidebar } from '../components/eventhub/RankingSidebar';
import { ChatContainer } from '../components/eventhub/ChatContainer';
import { StatsSidebar } from '../components/eventhub/StatsSidebar';
import '../styles/eventhub.css';

export function EventHub() {
  const { eventId } = useParams<{ eventId: string }>();
  const [event, setEvent] = useState<EventResponse | null>(null);
  const [participant, setParticipant] = useState<ParticipantResponse | null>(null);
  const [rankings, setRankings] = useState<RankingResponse[]>([]);
  const [questions, setQuestions] = useState<QuestionResponse[]>([]);
  const [messages, setMessages] = useState<MessageResponse[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState<QuestionResponse | null>(null);
  const [sentiment, setSentiment] = useState<'positive' | 'negative' | 'neutral'>('neutral');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false); // Prevent double submissions

  useEffect(() => {
    if (eventId) {
      loadEventData();
    }
  }, [eventId]);

  const loadEventData = async () => {
    try {
      setLoading(true);
      
      // Load event details
      const eventData = await api.events.getById(Number(eventId));
      setEvent(eventData);

      // Load rankings
      const rankingsData = await api.events.getRankings(Number(eventId), 10);
      setRankings(rankingsData);

      // Load questions
      const questionsData = await api.questions.getAll(Number(eventId));
      setQuestions(questionsData);
      
      if (questionsData.length > 0) {
        setCurrentQuestion(questionsData[0]);
      }

      // Load messages
      const messagesData = await api.messages.getAll(Number(eventId), 100);
      setMessages(messagesData);

      // Join as participant (generate unique user ID for each session)
      // This allows testing multiple times without resetting the database
      const sessionUserId = `test_${Date.now()}`;
      const participantData = await api.participants.join({
        event_id: Number(eventId),
        user_id: sessionUserId,
        name: "Tú",
        email: `test_${Date.now()}@nybble.com.ar`,
        avatar_url: "https://i.pravatar.cc/150?img=5"
      });
      setParticipant(participantData);

    } catch (error) {
      console.error('Error loading event data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (text: string, isQuickOption: boolean = false) => {
    if (!participant || !currentQuestion || sending) return;

    try {
      setSending(true); // Prevent double submissions

      // 1. Add user message to UI immediately (optimistic update)
      const userMessage: MessageResponse = {
        id: Date.now(), // Temporary ID
        event_id: Number(eventId),
        participant_id: participant.id,
        text: text,
        message_type: 'user',
        created_at: new Date().toISOString(),
        participant_name: participant.name,
        participant_avatar: participant.avatar_url
      };
      setMessages(prev => [...prev, userMessage]);

      // 2. Save the current question BEFORE creating response
      const questionToAnswer = currentQuestion;
      const currentIndex = questions.findIndex(q => q.id === currentQuestion.id);

      // 3. Move to next question immediately (prevents double submission)
      if (currentIndex < questions.length - 1) {
        const nextQuestion = questions[currentIndex + 1];
        setCurrentQuestion(nextQuestion);
      } else {
        setCurrentQuestion(null); // All questions answered
      }

      // 4. Create response in backend
      const response = await api.responses.create({
        question_id: questionToAnswer.id,
        participant_id: participant.id,
        text: text,
        is_quick_option: isQuickOption
      });

      // 5. Create message in backend (for persistence)
      await api.messages.create({
        event_id: Number(eventId),
        participant_id: participant.id,
        text: text,
        message_type: 'user'
      });

      // 6. Update sentiment based on response
      if (response.sentiment) {
        setSentiment(response.sentiment as 'positive' | 'negative' | 'neutral');
      }

      // 7. Update participant points
      const updatedParticipant = await api.participants.getById(participant.id);
      setParticipant(updatedParticipant);

      // 8. Reload rankings
      const rankingsData = await api.events.getRankings(Number(eventId), 10);
      setRankings(rankingsData);

      // 9. Add bot response after delay
      setTimeout(async () => {
        if (currentIndex < questions.length - 1) {
          const nextQuestion = questions[currentIndex + 1];
          
          // Add bot message to UI
          const botMessage: MessageResponse = {
            id: Date.now() + 1,
            event_id: Number(eventId),
            participant_id: null,
            text: `Pregunta ${currentIndex + 2} de ${questions.length}:<br/><strong>${nextQuestion.text}</strong>`,
            message_type: 'bot',
            created_at: new Date().toISOString(),
            participant_name: null,
            participant_avatar: null
          };
          setMessages(prev => [...prev, botMessage]);

          // Save bot message to backend
          await api.messages.create({
            event_id: Number(eventId),
            text: botMessage.text,
            message_type: 'bot'
          });
        } else {
          // All questions answered - completion message
          const completionMessage: MessageResponse = {
            id: Date.now() + 1,
            event_id: Number(eventId),
            participant_id: null,
            text: `🎊 ¡Encuesta completada! Muchas gracias por tu feedback.<br/><br/>
                   <strong>Resumen:</strong><br/>
                   • Ganaste ${response.points_awarded} puntos en esta respuesta<br/>
                   • Total de puntos: ${updatedParticipant.points}<br/>
                   • Tu posición en el ranking: #${updatedParticipant.rank_position || 'TBD'}<br/><br/>
                   Tu opinión nos ayuda a mejorar. ¡Nos vemos en el próximo evento! 🚀`,
            message_type: 'bot',
            created_at: new Date().toISOString(),
            participant_name: null,
            participant_avatar: null
          };
          setMessages(prev => [...prev, completionMessage]);

          await api.messages.create({
            event_id: Number(eventId),
            text: completionMessage.text,
            message_type: 'bot'
          });
        }
      }, 1500);

    } catch (error) {
      console.error('Error sending message:', error);
      alert('Error al enviar mensaje. Por favor intenta de nuevo.');
      
      // Reload messages to sync state
      try {
        const messagesData = await api.messages.getAll(Number(eventId), 100);
        setMessages(messagesData);
      } catch (e) {
        console.error('Error reloading messages:', e);
      }
    } finally {
      setSending(false);
    }
  };

  const handleRating = async (rating: number) => {
    await handleSendMessage(`⭐ ${rating} de 5`, false);
  };

  const handleReset = async () => {
    if (!participant) return;

    const confirmed = window.confirm(
      '¿Estás seguro que quieres reiniciar? Se borrarán todas tus respuestas y puntos.'
    );

    if (!confirmed) return;

    try {
      setLoading(true);

      // Call reset endpoint
      await api.participants.reset(participant.id);

      // Reload event data
      await loadEventData();

      alert('✅ Reiniciado con éxito! Puedes responder todas las preguntas de nuevo.');
    } catch (error) {
      console.error('Error resetting:', error);
      alert('❌ Error al reiniciar. Por favor recarga la página.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <p>Cargando evento...</p>
      </div>
    );
  }

  if (!event || !participant) {
    return (
      <div className="error-screen">
        <h2>Evento no encontrado</h2>
        <p>No se pudo cargar la información del evento.</p>
      </div>
    );
  }

  return (
    <div className={`event-hub ${sentiment}`}>
      <div className="container">
        <RankingSidebar 
          rankings={rankings} 
          topResponses={[]}
        />

        <ChatContainer
          event={event}
          participant={participant}
          messages={messages}
          currentQuestion={currentQuestion}
          onSendMessage={handleSendMessage}
          onRating={handleRating}
          onReset={handleReset}
          progress={(questions.findIndex(q => q.id === currentQuestion?.id) + 1) / questions.length * 100}
          sending={sending}
        />

        <StatsSidebar
          participant={participant}
          eventsCompleted={12}
          streak={participant.streak}
          badges={[
            { id: 1, icon: "🎤", name: "FIRST VOICE", unlocked: true },
            { id: 2, icon: "🔥", name: "ON FIRE", unlocked: true },
            { id: 3, icon: "💎", name: "INSIGHT MASTER", unlocked: false },
            { id: 4, icon: "👑", name: "COMMUNITY LEADER", unlocked: false },
            { id: 5, icon: "🎯", name: "PERFECTIONIST", unlocked: false },
            { id: 6, icon: "⚡", name: "SPEED DEMON", unlocked: false },
          ]}
        />
      </div>
    </div>
  );
}


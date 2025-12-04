import { useState, useEffect, useRef } from 'react';
import { EventResponse, ParticipantResponse, MessageResponse, QuestionResponse } from '../../utils/api';
import { QuickOptions } from './QuickOptions';
import { RatingStars } from './RatingStars';
import { TypingIndicator } from './TypingIndicator';

interface ChatContainerProps {
  event: EventResponse;
  participant: ParticipantResponse;
  messages: MessageResponse[];
  currentQuestion: QuestionResponse | null;
  onSendMessage: (text: string, isQuickOption: boolean) => void;
  onRating: (rating: number) => void;
  onReset: () => void;
  progress: number;
  sending?: boolean;
}

export function ChatContainer({
  event,
  participant,
  messages,
  currentQuestion,
  onSendMessage,
  onRating,
  onReset,
  progress,
  sending = false
}: ChatContainerProps) {
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() || sending) return;

    onSendMessage(inputText.trim(), false);
    setInputText('');

    // Show typing indicator
    setIsTyping(true);
    setTimeout(() => setIsTyping(false), 2000);
  };

  const handleQuickOption = (option: string) => {
    if (sending) return;
    
    onSendMessage(option, true);
    
    setIsTyping(true);
    setTimeout(() => setIsTyping(false), 1500);
  };

  const handleRatingClick = (rating: number) => {
    if (sending) return;
    
    onRating(rating);
    
    setIsTyping(true);
    setTimeout(() => setIsTyping(false), 1500);
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <main className="chat-container">
      <header className="chat-header">
        <div className="event-info">
          <h1>{event.title}</h1>
          <div className="event-meta">
            <span>📅 {new Date(event.event_date).toLocaleDateString('es-AR')}</span>
            <span>👥 {event.participant_count} participantes</span>
            <span>⏱️ {event.status === 'live' ? 'En vivo' : 'Evento'}</span>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button
            onClick={onReset}
            style={{
              background: 'rgba(255, 255, 255, 0.2)',
              border: '2px solid rgba(255, 255, 255, 0.5)',
              color: 'white',
              padding: '8px 16px',
              borderRadius: '12px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '600',
              transition: 'all 0.3s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(255, 255, 255, 0.3)';
              e.currentTarget.style.transform = 'translateY(-2px)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
              e.currentTarget.style.transform = 'translateY(0)';
            }}
          >
            🔄 Reiniciar
          </button>
          <div className="user-score">
            <span className="score-number" id="userScore">{participant.points}</span>
            <span className="score-label">Puntos</span>
          </div>
        </div>
      </header>

      <div className="progress-container">
        <div className="progress-bar" style={{ width: `${progress}%` }}></div>
      </div>

      <div className="chat-messages" id="chatMessages">
        {messages.map((message, index) => {
          // Only show interactive components on the very last message (which should be a bot message with a question)
          const shouldShowInteractive = message.message_type === 'bot' && 
            index === messages.length - 1 &&
            currentQuestion !== null;

          return (
            <div key={message.id} className={`message ${message.message_type}`}>
              {message.message_type === 'bot' && (
                <div className="message-avatar">🤖</div>
              )}
              <div className="message-content">
                <div 
                  className="message-bubble"
                  dangerouslySetInnerHTML={{ __html: message.text }}
                />
                {shouldShowInteractive && currentQuestion.question_type === 'quick_options' && (
                  <QuickOptions 
                    options={currentQuestion.options || []}
                    onSelect={handleQuickOption}
                    disabled={sending}
                  />
                )}
                {shouldShowInteractive && currentQuestion.question_type === 'rating' && (
                  <RatingStars onSelect={handleRatingClick} disabled={sending} />
                )}
                <div className="message-time">{formatTime(message.created_at)}</div>
              </div>
              {message.message_type === 'user' && message.participant_avatar && (
                <img 
                  src={message.participant_avatar}
                  alt={message.participant_name || 'User'}
                  className="message-avatar"
                  style={{ width: '40px', height: '40px', borderRadius: '50%' }}
                />
              )}
            </div>
          );
        })}

        {isTyping && <TypingIndicator />}
        
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input" onSubmit={handleSubmit}>
        <div className="input-wrapper">
          <input
            type="text"
            id="messageInput"
            placeholder="Escribe tu respuesta..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
          <button type="submit" className="send-button" disabled={!inputText.trim() || sending}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
            </svg>
          </button>
        </div>
      </form>
    </main>
  );
}


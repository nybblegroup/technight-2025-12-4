import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api, EventResponse } from '../utils/api';

export function Home() {
  const [events, setEvents] = useState<EventResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadEvents();
  }, []);

  const loadEvents = async () => {
    try {
      setLoading(true);
      const data = await api.events.getAll();
      setEvents(data);
    } catch (error) {
      console.error('Error loading events:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '40px 20px',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{
          background: 'white',
          borderRadius: '20px',
          padding: '40px',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.15)'
        }}>
          <h1 style={{
            fontSize: '48px',
            fontWeight: '700',
            marginBottom: '16px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            🎉 Nybble Event Hub
          </h1>
          <p style={{
            fontSize: '20px',
            color: '#6b7280',
            marginBottom: '40px'
          }}>
            Plataforma de engagement con IA para eventos Nybble
          </p>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '20px',
            marginBottom: '40px'
          }}>
            {loading ? (
              <div style={{ textAlign: 'center', padding: '40px' }}>
                <div style={{
                  width: '40px',
                  height: '40px',
                  border: '4px solid #e5e7eb',
                  borderTopColor: '#667eea',
                  borderRadius: '50%',
                  animation: 'spin 1s linear infinite',
                  margin: '0 auto'
                }}></div>
                <p style={{ marginTop: '16px', color: '#6b7280' }}>Cargando eventos...</p>
              </div>
            ) : events.length > 0 ? (
              events.map((event) => (
                <Link
                  key={event.id}
                  to={`/events/${event.id}`}
                  style={{
                    textDecoration: 'none',
                    background: '#f9fafb',
                    borderRadius: '16px',
                    padding: '24px',
                    border: '2px solid #e5e7eb',
                    transition: 'all 0.3s ease',
                    cursor: 'pointer'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-4px)';
                    e.currentTarget.style.boxShadow = '0 12px 24px rgba(0, 0, 0, 0.1)';
                    e.currentTarget.style.borderColor = '#667eea';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = 'none';
                    e.currentTarget.style.borderColor = '#e5e7eb';
                  }}
                >
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    marginBottom: '12px'
                  }}>
                    <h3 style={{
                      fontSize: '20px',
                      fontWeight: '600',
                      color: '#1f2937'
                    }}>
                      {event.title}
                    </h3>
                    <span style={{
                      padding: '4px 12px',
                      borderRadius: '12px',
                      fontSize: '12px',
                      fontWeight: '600',
                      textTransform: 'uppercase',
                      background: event.status === 'live' ? '#10b981' : 
                                 event.status === 'upcoming' ? '#3b82f6' : '#6b7280',
                      color: 'white'
                    }}>
                      {event.status}
                    </span>
                  </div>
                  {event.description && (
                    <p style={{
                      fontSize: '14px',
                      color: '#6b7280',
                      marginBottom: '12px',
                      lineHeight: '1.6'
                    }}>
                      {event.description}
                    </p>
                  )}
                  <div style={{
                    display: 'flex',
                    gap: '16px',
                    fontSize: '14px',
                    color: '#9ca3af'
                  }}>
                    <span>📅 {new Date(event.event_date).toLocaleDateString('es-AR')}</span>
                    <span>👥 {event.participant_count} participantes</span>
                  </div>
                </Link>
              ))
            ) : (
              <div style={{
                textAlign: 'center',
                padding: '40px',
                gridColumn: '1 / -1'
              }}>
                <p style={{ fontSize: '18px', color: '#6b7280' }}>
                  No hay eventos disponibles
                </p>
              </div>
            )}
          </div>

          <div style={{
            borderTop: '2px solid #e5e7eb',
            paddingTop: '32px',
            marginTop: '32px'
          }}>
            <h2 style={{
              fontSize: '24px',
              fontWeight: '600',
              marginBottom: '16px',
              color: '#1f2937'
            }}>
              Otras opciones
            </h2>
            <Link
              to="/examples"
              style={{
                display: 'inline-block',
                padding: '12px 24px',
                background: '#f3f4f6',
                border: '2px solid #e5e7eb',
                borderRadius: '12px',
                textDecoration: 'none',
                color: '#1f2937',
                fontWeight: '600',
                transition: 'all 0.3s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = '#e5e7eb';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = '#f3f4f6';
              }}
            >
              📝 Ver Ejemplos (Demo anterior)
            </Link>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}






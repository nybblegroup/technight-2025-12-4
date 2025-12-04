import { ParticipantResponse } from '../../utils/api';

interface Badge {
  id: number;
  icon: string;
  name: string;
  unlocked: boolean;
}

interface StatsSidebarProps {
  participant: ParticipantResponse;
  eventsCompleted: number;
  streak: number;
  badges: Badge[];
}

export function StatsSidebar({ participant, eventsCompleted, streak, badges }: StatsSidebarProps) {
  const unlockedCount = badges.filter(b => b.unlocked).length;
  const nextBadge = badges.find(b => !b.unlocked);
  
  return (
    <aside className="stats-sidebar">
      <h2>📊 Tu Progreso</h2>

      <div className="stat-card">
        <div className="stat-label">Eventos Completados</div>
        <div className="stat-value">{eventsCompleted}</div>
      </div>

      <div className="stat-card">
        <div className="stat-label">Racha Actual</div>
        <div className="stat-value" style={{ color: '#f59e0b' }}>{streak} 🔥</div>
      </div>

      <div className="stat-card">
        <div className="stat-label">Calidad Promedio</div>
        <div className="stat-value" style={{ fontSize: '24px' }}>
          {(participant.quality_score * 100).toFixed(0)}%
        </div>
      </div>

      {nextBadge && (
        <div className="stat-card">
          <div className="stat-label">Próximo Badge</div>
          <div style={{ fontSize: '14px', marginTop: '8px', color: 'var(--text-secondary)' }}>
            {nextBadge.icon} <strong>{nextBadge.name}</strong><br />
            Sigue participando para desbloquearlo
            <div className="progress-container" style={{ marginTop: '8px' }}>
              <div className="progress-bar" style={{ width: `${(unlockedCount / badges.length) * 100}%` }}></div>
            </div>
            <small>{unlockedCount} de {badges.length} badges</small>
          </div>
        </div>
      )}

      <h2 style={{ marginTop: '32px' }}>🏅 Tus Badges</h2>
      <div className="badge-grid">
        {badges.map((badge) => (
          <div
            key={badge.id}
            className={`badge ${badge.unlocked ? 'unlocked' : 'locked'}`}
          >
            <div className="badge-icon">{badge.icon}</div>
            <div className="badge-name">{badge.name}</div>
          </div>
        ))}
      </div>

      <h2 style={{ marginTop: '32px' }}>📈 Tus Stats</h2>
      <div className="stat-card" style={{ fontSize: '13px' }}>
        <strong>Respuestas enviadas</strong><br />
        <span style={{ fontSize: '20px', color: 'var(--primary-color)' }}>
          {participant.responses_count}
        </span>
      </div>
      <div className="stat-card" style={{ fontSize: '13px' }}>
        <strong>Sentimiento promedio</strong><br />
        <span style={{ fontSize: '20px' }}>
          {participant.sentiment_score > 0.3 ? '😊 Positivo' : 
           participant.sentiment_score < -0.3 ? '😐 Neutral' : '🤔 Variado'}
        </span>
      </div>
    </aside>
  );
}






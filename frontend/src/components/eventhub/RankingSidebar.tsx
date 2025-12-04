import { RankingResponse, ResponseResponse } from '../../utils/api';

interface RankingSidebarProps {
  rankings: RankingResponse[];
  topResponses: ResponseResponse[];
}

export function RankingSidebar({ rankings, topResponses }: RankingSidebarProps) {
  return (
    <aside className="sidebar">
      <h2>🏆 Top 10 Participantes</h2>
      <div id="rankingList">
        {rankings.map((ranking, index) => (
          <div 
            key={ranking.participant.id}
            className={`ranking-item ${index < 3 ? 'top-3' : ''}`}
          >
            <div className="ranking-number">{ranking.position}</div>
            <img 
              src={ranking.participant.avatar_url || `https://i.pravatar.cc/150?img=${index + 1}`}
              alt="Avatar" 
              className="ranking-avatar"
            />
            <div className="ranking-info">
              <div className="ranking-name">{ranking.participant.name}</div>
              <div className="ranking-points">
                {ranking.participant.points} pts
                {ranking.participant.streak > 0 && ` • 🔥 Racha ${ranking.participant.streak}`}
                {ranking.badges.length > 0 && ` • ${ranking.badges[0]}`}
              </div>
            </div>
          </div>
        ))}
      </div>

      {topResponses.length > 0 && (
        <>
          <h2 style={{ marginTop: '32px' }}>💎 Top Respuestas</h2>
          {topResponses.slice(0, 2).map((response) => (
            <div key={response.id} className="stat-card" style={{ fontSize: '13px', lineHeight: '1.6' }}>
              <strong>{response.participant_name}:</strong> "{response.text.substring(0, 150)}..."
            </div>
          ))}
        </>
      )}
    </aside>
  );
}






import { useEffect, useState } from 'react';
import { api } from './utils/api';

interface HealthStatus {
  status: 'loading' | 'success' | 'error';
  message: string;
  timestamp?: string;
}

function App() {
  const [backendHealth, setBackendHealth] = useState<HealthStatus>({
    status: 'loading',
    message: 'Checking...'
  });

  useEffect(() => {
    // Check backend health using direct API client
    api.health.get()
      .then(data => {
        console.log('Backend health check successful:', data);
        setBackendHealth({
          status: 'success',
          message: 'Connected successfully',
          timestamp: data.timestamp
        });
      })
      .catch(err => {
        console.error('Backend health check failed:', err);
        setBackendHealth({
          status: 'error',
          message: `Connection failed: ${err.message}`
        });
      });
  }, []);

  const getStatusStyle = (status: HealthStatus['status']) => {
    const baseStyle = {
      padding: '20px',
      borderRadius: '8px',
      marginBottom: '16px',
      border: '2px solid'
    };

    switch (status) {
      case 'loading':
        return { ...baseStyle, borderColor: '#999', backgroundColor: '#f5f5f5' };
      case 'success':
        return { ...baseStyle, borderColor: '#4caf50', backgroundColor: '#e8f5e9' };
      case 'error':
        return { ...baseStyle, borderColor: '#f44336', backgroundColor: '#ffebee' };
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      padding: '20px',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      backgroundColor: '#fafafa'
    }}>
      <h1 style={{ marginBottom: '40px' }}>Welcome to Technight 2025</h1>

      <div style={{ maxWidth: '600px', width: '100%' }}>
        <h2 style={{ marginBottom: '20px' }}>Backend Health Status</h2>

        {/* Backend Status */}
        <div style={getStatusStyle(backendHealth.status)}>
          <h3 style={{ margin: '0 0 8px 0' }}>
            Backend (Port 8080)
            {backendHealth.status === 'loading' && ' 🔄'}
            {backendHealth.status === 'success' && ' ✅'}
            {backendHealth.status === 'error' && ' ❌'}
          </h3>
          <p style={{ margin: '4px 0' }}>{backendHealth.message}</p>
          {backendHealth.timestamp && (
            <p style={{ margin: '4px 0', fontSize: '14px', color: '#666' }}>
              Timestamp: {backendHealth.timestamp}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

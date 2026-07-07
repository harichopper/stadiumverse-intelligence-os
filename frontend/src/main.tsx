import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './styles/globals.css'

// Catch-all error boundary for debugging
class ErrorBoundary extends React.Component<{ children: React.ReactNode }, { error: string | null }> {
  state = { error: null };
  static getDerivedStateFromError(error: Error) {
    return { error: error.message + '\n' + error.stack };
  }
  render() {
    if (this.state.error) {
      return (
        <div style={{
          position: 'fixed', inset: 0, background: '#050816', color: '#EF4444',
          fontFamily: 'monospace', fontSize: 12, padding: 32, overflow: 'auto', zIndex: 9999
        }}>
          <div style={{ color: '#F59E0B', fontSize: 18, marginBottom: 16 }}>⚠️ StadiumVerse Intelligence OS — Render Error</div>
          <pre style={{ whiteSpace: 'pre-wrap', color: '#EF4444' }}>{this.state.error}</pre>
          <button
            onClick={() => this.setState({ error: null })}
            style={{ marginTop: 16, padding: '8px 16px', background: '#3B82F6', color: 'white', border: 'none', borderRadius: 8, cursor: 'pointer' }}
          >
            Retry
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
)

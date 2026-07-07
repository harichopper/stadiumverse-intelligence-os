import React from 'react';

interface State { error: string | null }

export class PageBoundary extends React.Component<{ name: string; children: React.ReactNode }, State> {
  state: State = { error: null };

  static getDerivedStateFromError(err: Error): State {
    return { error: err.message + '\n' + (err.stack ?? '') };
  }

  render() {
    if (this.state.error) {
      return (
        <div style={{
          flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexDirection: 'column', gap: 16, padding: 32,
          background: 'rgba(239,68,68,.05)', borderRadius: 16,
          border: '1px solid rgba(239,68,68,.2)', margin: 16,
        }}>
          <div style={{ fontSize: 32 }}>⚠️</div>
          <div style={{ fontSize: 14, fontWeight: 600, color: '#EF4444' }}>
            {this.props.name} crashed
          </div>
          <pre style={{
            fontSize: 10, color: '#94A3B8', whiteSpace: 'pre-wrap',
            maxWidth: 600, maxHeight: 200, overflow: 'auto',
            background: 'rgba(0,0,0,.3)', padding: 12, borderRadius: 8,
          }}>
            {this.state.error}
          </pre>
          <button
            onClick={() => this.setState({ error: null })}
            style={{ padding: '6px 16px', background: '#3B82F6', color: 'white', border: 'none', borderRadius: 8, cursor: 'pointer', fontSize: 12 }}
          >
            Retry
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAppStore } from '../../store/appStore';

const Clock: React.FC = () => {
  const [t, setT] = useState(() => new Date());
  useEffect(() => { const iv = setInterval(() => setT(new Date()), 1000); return () => clearInterval(iv); }, []);
  return <span style={{ fontFamily: 'monospace', fontSize: 12, color: '#CBD5E1' }}>{t.toLocaleTimeString('en-US', { hour12: false })}</span>;
};

export const TopBar: React.FC = () => {
  const { riskLevel, crowdCount, matchMinute, setCommandBarOpen } = useAppStore();
  const [voice, setVoice] = useState(false);

  const riskColor = riskLevel === 'healthy' ? '#10B981' : riskLevel === 'warning' ? '#F59E0B' : '#EF4444';
  const riskLabel = riskLevel === 'healthy' ? 'OPTIMAL' : riskLevel === 'warning' ? 'MONITOR' : 'CRITICAL';

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); setCommandBarOpen(true); } };
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
  }, [setCommandBarOpen]);

  return (
    <header style={{
      height: 52, flexShrink: 0, display: 'flex', alignItems: 'center',
      padding: '0 14px', gap: 12, position: 'relative', zIndex: 30,
      background: 'rgba(5,8,22,.92)', borderBottom: '1px solid rgba(255,255,255,.06)',
      backdropFilter: 'blur(20px)',
    }} role="banner">

      {/* LOGO */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
        <div style={{ position: 'relative', width: 28, height: 28 }} aria-hidden="true">
          <motion.div animate={{ scale: [1, 1.5, 1] }} transition={{ duration: 2.5, repeat: Infinity }}
            style={{ position: 'absolute', inset: 0, borderRadius: '50%', background: 'rgba(59,130,246,.25)' }} />
          <svg viewBox="0 0 28 28" width="28" height="28" fill="none" style={{ position: 'relative', zIndex: 1 }} aria-hidden="true">
            <circle cx="14" cy="14" r="12" stroke="#3B82F6" strokeWidth="1" fill="rgba(59,130,246,.15)" />
            <circle cx="14" cy="14" r="4" fill="rgba(59,130,246,.4)" />
            <circle cx="14" cy="14" r="2" fill="#3B82F6" />
          </svg>
        </div>
        <div>
          <div style={{ fontSize: 11, fontWeight: 600, color: '#F8FAFC', letterSpacing: '.1em', textTransform: 'uppercase' }}>StadiumVerse</div>
          <div style={{ fontSize: 8, color: '#3B82F6', letterSpacing: '.2em', textTransform: 'uppercase' }}>INTELLIGENCE OS</div>
        </div>
      </div>

      <div style={{ width: 1, height: 28, background: 'rgba(255,255,255,.08)', flexShrink: 0 }} aria-hidden="true" />

      {/* BRAIN STATUS */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }} aria-live="polite">
        <motion.div animate={{ scale: [1, 1.4, 1] }} transition={{ duration: 1.5, repeat: Infinity }}
          style={{ width: 7, height: 7, borderRadius: '50%', background: riskColor, boxShadow: `0 0 8px ${riskColor}` }} 
          aria-hidden="true"
        />
        <span style={{ fontSize: 10, fontWeight: 600, color: riskColor }}>BRAIN {riskLabel}</span>
        {/* heartbeat path */}
        <svg width="56" height="20" viewBox="0 0 56 20" fill="none" aria-hidden="true">
          <motion.path d="M0,10 L7,10 L11,3 L15,17 L19,3 L22,14 L26,10 L34,10 L38,4 L42,16 L46,10 L56,10"
            stroke={riskColor} strokeWidth="1.5" fill="none" strokeLinecap="round"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: [0, 1, 1], opacity: [0, 1, 0] }}
            transition={{ duration: 1.6, repeat: Infinity, ease: 'easeInOut' }}
          />
        </svg>
      </div>

      {/* MATCH */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '3px 10px', background: 'rgba(255,255,255,.04)', border: '1px solid rgba(255,255,255,.06)', borderRadius: 8, flexShrink: 0 }}>
        <span style={{ fontSize: 11, color: '#64748B' }} aria-hidden="true">⚽</span>
        <span style={{ fontSize: 11, fontWeight: 600, color: '#F8FAFC' }}>BRA 2 – 1 ARG</span>
        <motion.span animate={{ opacity: [1, .5, 1] }} transition={{ duration: 1.3, repeat: Infinity }}
          style={{ fontSize: 9, fontWeight: 700, background: '#EF4444', color: '#fff', padding: '1px 5px', borderRadius: 4 }}>
          {matchMinute}'
        </motion.span>
      </div>

      {/* SEARCH / CMD BAR */}
      <motion.button
        onClick={() => setCommandBarOpen(true)}
        whileHover={{ borderColor: 'rgba(59,130,246,.5)' }}
        aria-label="Open command bar (Ctrl+K)"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            setCommandBarOpen(true);
          }
        }}
        style={{
          flex: 1, maxWidth: 280, display: 'flex', alignItems: 'center', gap: 8,
          padding: '5px 12px', background: 'rgba(255,255,255,.04)', border: '1px solid rgba(255,255,255,.08)',
          borderRadius: 10, color: '#64748B', fontSize: 12, cursor: 'pointer',
          outline: 'none',
        }}
        onFocus={(e) => {
          e.currentTarget.style.borderColor = 'rgba(59,130,246,.6)';
          e.currentTarget.style.boxShadow = '0 0 0 2px rgba(59,130,246,.3)';
        }}
        onBlur={(e) => {
          e.currentTarget.style.borderColor = 'rgba(255,255,255,.08)';
          e.currentTarget.style.boxShadow = 'none';
        }}
      >
        <span aria-hidden="true">🔍</span>
        <span style={{ flex: 1, textAlign: 'left' }}>Ask Intelligence OS...</span>
        <span style={{ fontSize: 9, fontFamily: 'monospace', background: 'rgba(255,255,255,.06)', padding: '1px 5px', borderRadius: 4 }} aria-label="Keyboard shortcut">⌘K</span>
      </motion.button>

      <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 12 }}>
        {/* crowd */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
          <span style={{ fontSize: 9, color: '#64748B', textTransform: 'uppercase', letterSpacing: '.06em' }}>Crowd</span>
          <motion.span key={crowdCount} initial={{ scale: 1.1 }} animate={{ scale: 1 }}
            style={{ fontSize: 12, fontWeight: 600, color: '#3B82F6', fontVariantNumeric: 'tabular-nums' }}>
            {crowdCount.toLocaleString()}
          </motion.span>
        </div>

        {/* weather */}
        <span style={{ fontSize: 11, color: '#CBD5E1' }} aria-label="Weather: partly cloudy, 22 degrees Celsius">🌤 22°C</span>

        {/* clock */}
        <Clock />

        {/* voice */}
        <motion.button 
          onClick={() => setVoice(v => !v)} 
          whileHover={{ scale: 1.1 }} 
          whileTap={{ scale: .93 }}
          aria-label={voice ? 'Turn off voice control' : 'Turn on voice control'}
          aria-pressed={voice}
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              setVoice(v => !v);
            }
          }}
          style={{ 
            width: 30, height: 30, borderRadius: 8, 
            background: voice ? 'rgba(59,130,246,.2)' : 'rgba(255,255,255,.04)', 
            border: '1px solid rgba(255,255,255,.08)', 
            cursor: 'pointer', fontSize: 13, display: 'flex', alignItems: 'center', justifyContent: 'center',
            outline: 'none',
          }}
          onFocus={(e) => {
            e.currentTarget.style.borderColor = 'rgba(59,130,246,.6)';
            e.currentTarget.style.boxShadow = '0 0 0 2px rgba(59,130,246,.3)';
          }}
          onBlur={(e) => {
            e.currentTarget.style.borderColor = 'rgba(255,255,255,.08)';
            e.currentTarget.style.boxShadow = 'none';
          }}
        >
          🎤
        </motion.button>

        {/* settings */}
        <motion.button 
          whileHover={{ scale: 1.1, rotate: 60 }} 
          transition={{ type: 'spring', stiffness: 300 }}
          aria-label="Open settings"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              useAppStore.getState().setCurrentPage('settings');
            }
          }}
          style={{ 
            width: 30, height: 30, borderRadius: 8, 
            background: 'rgba(255,255,255,.04)', 
            border: '1px solid rgba(255,255,255,.08)', 
            cursor: 'pointer', fontSize: 13, display: 'flex', alignItems: 'center', justifyContent: 'center',
            outline: 'none',
          }}
          onFocus={(e) => {
            e.currentTarget.style.borderColor = 'rgba(100,116,139,.6)';
            e.currentTarget.style.boxShadow = '0 0 0 2px rgba(100,116,139,.3)';
          }}
          onBlur={(e) => {
            e.currentTarget.style.borderColor = 'rgba(255,255,255,.08)';
            e.currentTarget.style.boxShadow = 'none';
          }}
        >
          ⚙️
        </motion.button>

        {/* avatar */}
        <div style={{ 
          width: 30, height: 30, borderRadius: '50%', 
          background: 'linear-gradient(135deg,#3B82F6,#8B5CF6)', 
          display: 'flex', alignItems: 'center', justifyContent: 'center', 
          fontSize: 10, fontWeight: 700, color: '#fff', flexShrink: 0 
        }} aria-label="User FC">FC</div>
      </div>
    </header>
  );
};

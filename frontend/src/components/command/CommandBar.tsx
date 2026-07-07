import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAppStore } from '../../store/appStore';

const CMDS = [
  { icon: '🔮', label: 'Predict next 30 minutes',    cat: 'Prediction', color: '#8B5CF6' },
  { icon: '🌧️', label: 'Run rain simulation',        cat: 'Simulation', color: '#3B82F6' },
  { icon: '👤', label: 'Find Fan 204',               cat: 'Search',     color: '#06B6D4' },
  { icon: '🚪', label: 'Open Gate B',               cat: 'Control',    color: '#F59E0B' },
  { icon: '🦺', label: 'Deploy Volunteers',          cat: 'Action',     color: '#10B981' },
  { icon: '🧠', label: 'Explain last decision',      cat: 'Explain',    color: '#8B5CF6' },
  { icon: '📊', label: 'Show crowd analytics',       cat: 'Analytics',  color: '#3B82F6' },
  { icon: '🏥', label: 'Medical status report',      cat: 'Medical',    color: '#EF4444' },
  { icon: '⚡', label: 'Emergency protocol',         cat: 'Emergency',  color: '#EF4444' },
];

const RESPONSES: Record<string, string> = {
  'Predict next 30 minutes': 'Analyzing 87,342 fan trajectories... Gate B congestion likely at +8 min. Rain impact at +15 min. Peak exit flow at +28 min. Confidence: 94%.',
  'Run rain simulation': 'Simulating rainfall... 73% probability of moderate rain at 21:45. Recommend pre-positioning 12 umbrellas at Gate C and alerting Metro coordination.',
  'Find Fan 204': 'Fan #204: Carlos M. 🇧🇷 — Section N7, Row 14. Stress: LOW. Sentiment: EXCITED. No flags raised.',
  'Deploy Volunteers': 'Dispatching 3 volunteers to Gate B... ETA: 2 min. Volunteer IDs: V-041, V-052, V-089. Confirmation sent.',
  'Explain last decision': 'Last decision at 67:23 — Deploy volunteers to Gate B. Based on 23 historical patterns. Confidence 94%. Outcome: -23% congestion in 5 min.',
  'Open Gate B': 'Gate B status: OPEN. Capacity 87%. Flow 2,400/hr. AI recommends soft crowd barriers now.',
};

export const CommandBar: React.FC = () => {
  const { commandBarOpen, setCommandBarOpen } = useAppStore();
  const [q, setQ] = useState('');
  const [sel, setSel] = useState(0);
  const [result, setResult] = useState<string | null>(null);
  const [thinking, setThinking] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const filtered = CMDS.filter(c => c.label.toLowerCase().includes(q.toLowerCase()) || c.cat.toLowerCase().includes(q.toLowerCase()));

  useEffect(() => {
    if (commandBarOpen) { setQ(''); setResult(null); setThinking(false); setSel(0); setTimeout(() => inputRef.current?.focus(), 80); }
  }, [commandBarOpen]);

  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (!commandBarOpen) return;
      if (e.key === 'Escape') setCommandBarOpen(false);
      if (e.key === 'ArrowDown') setSel(s => Math.min(s + 1, filtered.length - 1));
      if (e.key === 'ArrowUp') setSel(s => Math.max(s - 1, 0));
      if (e.key === 'Enter' && filtered[sel]) run(filtered[sel].label);
    };
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
  }, [commandBarOpen, filtered, sel]);

  const run = (label: string) => {
    setThinking(true); setResult(null);
    setTimeout(() => { setThinking(false); setResult(RESPONSES[label] ?? `Executing: "${label}"... Done.`); }, 1400);
  };

  return (
    <AnimatePresence>
      {commandBarOpen && (
        <>
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            style={{ position: 'fixed', inset: 0, zIndex: 900, background: 'rgba(5,8,22,.75)', backdropFilter: 'blur(6px)' }}
            onClick={() => setCommandBarOpen(false)} />

          <motion.div initial={{ opacity: 0, y: -16, scale: .96 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: -16, scale: .96 }}
            transition={{ type: 'spring', stiffness: 380, damping: 28 }}
            style={{ position: 'fixed', zIndex: 901, top: '18%', left: '50%', transform: 'translateX(-50%)', width: '100%', maxWidth: 580 }}>
            <div style={{ background: 'rgba(5,8,22,.98)', border: '1px solid rgba(59,130,246,.35)', borderRadius: 16, overflow: 'hidden', boxShadow: '0 40px 80px rgba(0,0,0,.8),0 0 50px rgba(59,130,246,.08)' }}>

              {/* input */}
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '14px 16px', borderBottom: '1px solid rgba(255,255,255,.06)' }}>
                <span style={{ fontSize: 14 }}>⚡</span>
                <input ref={inputRef} value={q} onChange={e => { setQ(e.target.value); setResult(null); setSel(0); }}
                  placeholder="Ask Intelligence OS anything..."
                  style={{ flex: 1, background: 'none', border: 'none', outline: 'none', color: '#F8FAFC', fontSize: 14 }} />
                <span style={{ fontSize: 10, fontFamily: 'monospace', background: 'rgba(255,255,255,.06)', padding: '2px 6px', borderRadius: 4, color: '#64748B' }}>ESC</span>
              </div>

              {/* thinking */}
              <AnimatePresence>
                {thinking && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                    style={{ padding: '10px 16px', display: 'flex', alignItems: 'center', gap: 8, borderBottom: '1px solid rgba(255,255,255,.04)' }}>
                    {[0,1,2].map(d => (
                      <motion.div key={d} style={{ width: 6, height: 6, borderRadius: '50%', background: '#8B5CF6' }}
                        animate={{ scale: [.5, 1, .5] }} transition={{ duration: .8, repeat: Infinity, delay: d * .16 }} />
                    ))}
                    <span style={{ fontSize: 12, color: '#8B5CF6' }}>Intelligence OS thinking...</span>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* result */}
              <AnimatePresence>
                {result && !thinking && (
                  <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }}
                    style={{ padding: '12px 16px', background: 'rgba(16,185,129,.06)', borderBottom: '1px solid rgba(16,185,129,.15)' }}>
                    <div style={{ fontSize: 9, color: '#10B981', textTransform: 'uppercase', letterSpacing: '.1em', marginBottom: 5 }}>✓ Response</div>
                    <p style={{ fontSize: 13, color: '#CBD5E1', lineHeight: 1.6, margin: 0 }}>{result}</p>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* list */}
              {!result && (
                <div style={{ maxHeight: 300, overflowY: 'auto', padding: '6px 0' }}>
                  {filtered.map((cmd, i) => (
                    <motion.button key={cmd.label} onClick={() => run(cmd.label)} onMouseEnter={() => setSel(i)}
                      whileHover={{ background: 'rgba(59,130,246,.06)' }}
                      style={{ width: '100%', display: 'flex', alignItems: 'center', gap: 12, padding: '9px 16px', background: sel === i ? 'rgba(59,130,246,.08)' : 'transparent', border: 'none', borderLeft: `2px solid ${sel === i ? cmd.color : 'transparent'}`, cursor: 'pointer', textAlign: 'left' }}>
                      <span style={{ fontSize: 18, flexShrink: 0 }}>{cmd.icon}</span>
                      <span style={{ flex: 1, fontSize: 13, color: '#F8FAFC' }}>{cmd.label}</span>
                      <span style={{ fontSize: 9, padding: '2px 7px', borderRadius: 999, background: `${cmd.color}18`, color: cmd.color }}>{cmd.cat}</span>
                    </motion.button>
                  ))}
                </div>
              )}

              {/* footer */}
              <div style={{ display: 'flex', gap: 14, padding: '8px 16px', borderTop: '1px solid rgba(255,255,255,.04)', fontSize: 10, color: '#475569' }}>
                <span>↑↓ Navigate</span><span>↵ Execute</span><span>ESC Close</span>
                <span style={{ marginLeft: 'auto', color: '#3B82F6' }}>⚡ Intelligence OS</span>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

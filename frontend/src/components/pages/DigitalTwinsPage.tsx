import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { api, Fan } from '../../services/api';

const stressColor = (s: number) => s < 30 ? '#10B981' : s < 60 ? '#F59E0B' : '#EF4444';
const stressLabel = (s: number) => s < 30 ? 'LOW' : s < 60 ? 'MODERATE' : 'HIGH';

const emotionEmoji: Record<string, string> = {
  ecstatic:'😄', excited:'🤩', joyful:'😊', calm:'😌', anxious:'😰',
  tense:'😤', fearful:'😨', angry:'😡', tired:'😴', neutral:'😐',
  delighted:'🥳', energetic:'💪', nostalgic:'🥹', curious:'🤔',
};

export const DigitalTwinsPage: React.FC = () => {
  const [fans, setFans] = useState<Fan[]>([]);
  const [selected, setSelected] = useState<Fan | null>(null);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.fans(50).then(r => { setFans(r.fans); setLoading(false); }).catch(() => setLoading(false));
    const iv = setInterval(() => {
      api.fans(50).then(r => setFans(r.fans)).catch(() => {});
    }, 8000);
    return () => clearInterval(iv);
  }, []);

  const filtered = fans.filter(f =>
    f.name.toLowerCase().includes(search.toLowerCase()) ||
    f.country.toLowerCase().includes(search.toLowerCase()) ||
    f.sector?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ height: '100%', display: 'flex', overflow: 'hidden', padding: 12, gap: 12 }}>

      {/* Fan list */}
      <div style={{ width: 340, flexShrink: 0, display: 'flex', flexDirection: 'column', gap: 8 }}>
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
          style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{ width: 32, height: 32, borderRadius: 10, background: 'rgba(6,182,212,.15)', border: '1px solid rgba(6,182,212,.3)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 16 }}>👥</div>
          <div>
            <div style={{ fontSize: 16, fontWeight: 300, color: '#F8FAFC' }}>Digital Twins</div>
            <div style={{ fontSize: 10, color: '#64748B' }}>{fans.length} twins active · DB connected</div>
          </div>
          <motion.div animate={{ opacity: [1, .4, 1] }} transition={{ duration: 2, repeat: Infinity }}
            style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 4, fontSize: 9, color: '#10B981' }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#10B981', display: 'inline-block' }} />
            LIVE
          </motion.div>
        </motion.div>

        {/* Search */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '7px 12px', background: 'rgba(255,255,255,.04)', border: '1px solid rgba(255,255,255,.08)', borderRadius: 10 }}>
          <span style={{ color: '#64748B' }}>🔍</span>
          <input value={search} onChange={e => setSearch(e.target.value)}
            placeholder="Search fans, country, sector..."
            style={{ flex: 1, background: 'none', border: 'none', outline: 'none', color: '#F8FAFC', fontSize: 12 }} />
        </div>

        {/* List */}
        <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 6 }}>
          {loading && <div style={{ textAlign: 'center', color: '#64748B', padding: 32, fontSize: 12 }}>Loading from database...</div>}
          {filtered.map((fan, i) => (
            <motion.div key={fan.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * .05 }}
              onClick={() => setSelected(fan)}
              whileHover={{ borderColor: 'rgba(6,182,212,.3)' }}
              style={{ padding: 10, borderRadius: 12, cursor: 'pointer',
                background: selected?.id === fan.id ? 'rgba(6,182,212,.08)' : 'rgba(255,255,255,.03)',
                border: `1px solid ${selected?.id === fan.id ? 'rgba(6,182,212,.35)' : 'rgba(255,255,255,.06)'}` }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <span style={{ fontSize: 22 }}>{fan.flag}</span>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: 13, fontWeight: 500, color: '#F8FAFC' }}>{fan.name}</span>
                    <span style={{ fontSize: 16 }}>{emotionEmoji[fan.current_emotion] ?? '😐'}</span>
                  </div>
                  <div style={{ fontSize: 9, color: '#64748B', marginTop: 1 }}>
                    {fan.country} · Sector {fan.sector}
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 5 }}>
                    <div style={{ flex: 1, height: 3, borderRadius: 2, background: 'rgba(255,255,255,.06)' }}>
                      <div style={{ height: '100%', borderRadius: 2, width: `${fan.stress_level}%`, background: stressColor(fan.stress_level), transition: 'width .6s' }} />
                    </div>
                    <span style={{ fontSize: 9, fontWeight: 600, color: stressColor(fan.stress_level) }}>{stressLabel(fan.stress_level)}</span>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Inspector */}
      <AnimatePresence>
        {selected ? (
          <motion.div key={selected.id} initial={{ opacity: 0, x: 16 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 16 }}
            style={{ flex: 1, overflowY: 'auto', background: 'rgba(255,255,255,.025)', border: '1px solid rgba(6,182,212,.15)', borderRadius: 14 }}>

            {/* Header */}
            <div style={{ padding: 20, background: 'linear-gradient(135deg,rgba(6,182,212,.12),rgba(139,92,246,.08))' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                <div style={{ width: 72, height: 72, borderRadius: 18, background: 'rgba(255,255,255,.08)', border: '1px solid rgba(255,255,255,.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 36 }}>{selected.flag}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 22, fontWeight: 600, color: '#F8FAFC' }}>{selected.name}</div>
                  <div style={{ fontSize: 12, color: '#94A3B8', marginTop: 2 }}>{selected.country} · Digital Twin #{selected.fan_id}</div>
                  <div style={{ display: 'flex', gap: 12, marginTop: 8 }}>
                    <div style={{ textAlign: 'center' }}>
                      <div style={{ fontSize: 22 }}>{emotionEmoji[selected.current_emotion] ?? '😐'}</div>
                      <div style={{ fontSize: 9, color: '#64748B' }}>Emotion</div>
                      <div style={{ fontSize: 10, fontWeight: 600, color: '#10B981', textTransform: 'capitalize' }}>{selected.current_emotion}</div>
                    </div>
                    <div style={{ textAlign: 'center' }}>
                      <div style={{ fontSize: 18, fontWeight: 700, color: stressColor(selected.stress_level) }}>{selected.stress_level}%</div>
                      <div style={{ fontSize: 9, color: '#64748B' }}>Stress</div>
                      <div style={{ fontSize: 9, fontWeight: 600, color: stressColor(selected.stress_level) }}>{stressLabel(selected.stress_level)}</div>
                    </div>
                    <div style={{ textAlign: 'center' }}>
                      <div style={{ fontSize: 18, fontWeight: 700, color: '#3B82F6' }}>{Math.round(selected.prediction_confidence * 100)}%</div>
                      <div style={{ fontSize: 9, color: '#64748B' }}>AI Confidence</div>
                    </div>
                    <div style={{ textAlign: 'center' }}>
                      <div style={{ fontSize: 18, fontWeight: 700, color: '#F59E0B' }}>{selected.risk_score}</div>
                      <div style={{ fontSize: 9, color: '#64748B' }}>Risk Score</div>
                    </div>
                  </div>
                </div>
                <button onClick={() => setSelected(null)} style={{ padding: '4px 10px', background: 'rgba(255,255,255,.06)', border: 'none', borderRadius: 8, color: '#94A3B8', cursor: 'pointer', fontSize: 11 }}>✕ Close</button>
              </div>
            </div>

            {/* Body */}
            <div style={{ padding: 16, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
              {/* Stress bar */}
              <div style={{ gridColumn: '1/-1', background: 'rgba(255,255,255,.03)', border: '1px solid rgba(255,255,255,.06)', borderRadius: 12, padding: 14 }}>
                <div style={{ fontSize: 9, color: '#64748B', textTransform: 'uppercase', letterSpacing: '.1em', marginBottom: 8 }}>Biometric State</div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 8 }}>
                  {[
                    { label: 'Stress', value: selected.stress_level, color: stressColor(selected.stress_level) },
                    { label: 'Excitement', value: selected.excitement_level, color: '#3B82F6' },
                    { label: 'Hunger', value: selected.hunger_level, color: '#F59E0B' },
                    { label: 'Fatigue', value: selected.fatigue_level, color: '#8B5CF6' },
                  ].map(item => (
                    <div key={item.label} style={{ textAlign: 'center' }}>
                      <div style={{ fontSize: 16, fontWeight: 700, color: item.color }}>{item.value}%</div>
                      <div style={{ fontSize: 9, color: '#64748B', margin: '3px 0' }}>{item.label}</div>
                      <div style={{ height: 3, background: 'rgba(255,255,255,.06)', borderRadius: 2 }}>
                        <motion.div style={{ height: '100%', borderRadius: 2, background: item.color }}
                          initial={{ width: 0 }} animate={{ width: `${item.value}%` }} transition={{ duration: 1 }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {[
                { label: '💭 Current Thought', text: selected.current_thought, color: '#8B5CF6' },
                { label: '🧠 Memory', text: selected.memory_summary, color: '#3B82F6' },
                { label: '🔮 AI Prediction', text: selected.predicted_action, color: '#F59E0B' },
                { label: '📍 Location', text: `Sector ${selected.sector}${selected.seat ? ` · Seat ${selected.seat}` : ''} · Age ${selected.age}`, color: '#10B981' },
              ].map(item => (
                <div key={item.label} style={{ background: 'rgba(255,255,255,.03)', border: `1px solid rgba(255,255,255,.06)`, borderRadius: 12, padding: 12 }}>
                  <div style={{ fontSize: 9, color: '#64748B', textTransform: 'uppercase', letterSpacing: '.08em', marginBottom: 6 }}>{item.label}</div>
                  <p style={{ fontSize: 12, color: '#CBD5E1', margin: 0, lineHeight: 1.6, borderLeft: `2px solid ${item.color}40`, paddingLeft: 8 }}>
                    "{item.text ?? 'No data'}"
                  </p>
                </div>
              ))}

              {/* Confidence bar */}
              <div style={{ gridColumn: '1/-1', background: 'rgba(255,255,255,.03)', border: '1px solid rgba(255,255,255,.06)', borderRadius: 12, padding: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                  <span style={{ fontSize: 9, color: '#64748B', textTransform: 'uppercase', letterSpacing: '.08em' }}>Prediction Confidence</span>
                  <span style={{ fontSize: 16, fontWeight: 700, color: '#3B82F6' }}>{Math.round(selected.prediction_confidence * 100)}%</span>
                </div>
                <div style={{ height: 6, background: 'rgba(255,255,255,.06)', borderRadius: 3, overflow: 'hidden' }}>
                  <motion.div style={{ height: '100%', background: 'linear-gradient(90deg,#3B82F6,#8B5CF6)', borderRadius: 3 }}
                    initial={{ width: 0 }} animate={{ width: `${selected.prediction_confidence * 100}%` }} transition={{ duration: 1.2 }} />
                </div>
                <div style={{ fontSize: 9, color: '#475569', marginTop: 4 }}>
                  Last updated: {selected.updated_at ? new Date(selected.updated_at).toLocaleTimeString() : 'Live'}
                </div>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
            style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 12 }}>
            <span style={{ fontSize: 48 }}>👥</span>
            <p style={{ color: '#475569', fontSize: 13 }}>Select a fan to inspect their digital twin</p>
            <p style={{ color: '#334155', fontSize: 10 }}>{fans.length} digital twins loaded from SQLite</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Users } from 'lucide-react';

const FANS = [
  { id: 'f001', name: 'Carlos M.', flag: '🇧🇷', country: 'Brazil', emotion: 'Ecstatic', emoticon: '😄', stress: 12, thought: 'Goal! One more goal!', memory: 'Saw this team win in 2018', prediction: 'Will stay to celebrate', confidence: 94, sector: 'N7', seat: '14C' },
  { id: 'f002', name: 'Diego R.', flag: '🇦🇷', country: 'Argentina', emotion: 'Anxious', emoticon: '😰', stress: 78, thought: 'Come on, we need to equalize!', memory: 'Lost a final in similar score', prediction: 'May leave early', confidence: 67, sector: 'S3', seat: '28A' },
  { id: 'f003', name: 'Hans K.', flag: '🇩🇪', country: 'Germany', emotion: 'Calm', emoticon: '😌', stress: 22, thought: 'Great technical football', memory: 'First World Cup final', prediction: 'Will watch till end', confidence: 91, sector: 'E12', seat: '5B' },
  { id: 'f004', name: 'Marie D.', flag: '🇫🇷', country: 'France', emotion: 'Excited', emoticon: '🤩', stress: 31, thought: 'Amazing atmosphere!', memory: '2022 WC final atmosphere was similar', prediction: 'Will buy merchandise', confidence: 88, sector: 'W6', seat: '19D' },
  { id: 'f005', name: 'Yuki T.', flag: '🇯🇵', country: 'Japan', emotion: 'Delighted', emoticon: '😊', stress: 8, thought: 'This is history in the making', memory: 'First time attending WC', prediction: 'Will share live on social media', confidence: 97, sector: 'N9', seat: '3A' },
  { id: 'f006', name: 'Ahmed K.', flag: '🇸🇦', country: 'Saudi Arabia', emotion: 'Tense', emoticon: '😤', stress: 55, thought: 'Just a few more minutes...', memory: 'Attended 2002 WC in Korea', prediction: 'Neutral — will enjoy the game', confidence: 79, sector: 'E4', seat: '22C' },
];

const stressColor = (s: number) => s < 30 ? '#10B981' : s < 60 ? '#F59E0B' : '#EF4444';
const stressLabel = (s: number) => s < 30 ? 'LOW' : s < 60 ? 'MODERATE' : 'HIGH';

export const DigitalTwinsPage: React.FC = () => {
  const [selected, setSelected] = useState<typeof FANS[0] | null>(null);
  const [search, setSearch] = useState('');

  const filtered = FANS.filter(f =>
    f.name.toLowerCase().includes(search.toLowerCase()) ||
    f.country.toLowerCase().includes(search.toLowerCase()) ||
    f.sector.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="h-full flex overflow-hidden p-4 gap-4">
      {/* Fan list */}
      <div className="flex flex-col" style={{ width: 360, flexShrink: 0 }}>
        <motion.div className="flex items-center gap-3 mb-4" initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
          <div className="w-8 h-8 rounded-xl flex items-center justify-center" style={{ background: 'rgba(6,182,212,0.15)', border: '1px solid rgba(6,182,212,0.3)' }}>
            <Users size={16} style={{ color: '#06B6D4' }} />
          </div>
          <div>
            <h2 className="text-lg font-light" style={{ color: '#F8FAFC' }}>Digital Twins</h2>
            <p className="text-[10px]" style={{ color: '#64748B' }}>87,342 active twins · Showing sample</p>
          </div>
        </motion.div>

        {/* Search */}
        <div className="mb-3 px-3 py-2 rounded-xl flex items-center gap-2" style={{ background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)' }}>
          <span style={{ color: '#64748B' }}>🔍</span>
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search fans..."
            className="flex-1 bg-transparent text-xs outline-none"
            style={{ color: '#F8FAFC' }}
          />
        </div>

        {/* Fan cards */}
        <div className="flex-1 overflow-y-auto space-y-2 pr-1">
          {filtered.map((fan, i) => (
            <motion.div
              key={fan.id}
              className="rounded-2xl p-3 cursor-pointer"
              style={{
                background: selected?.id === fan.id ? 'rgba(6,182,212,0.08)' : 'rgba(255,255,255,0.03)',
                border: `1px solid ${selected?.id === fan.id ? 'rgba(6,182,212,0.3)' : 'rgba(255,255,255,0.06)'}`,
              }}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              whileHover={{ borderColor: 'rgba(6,182,212,0.2)' }}
              onClick={() => setSelected(fan)}
            >
              <div className="flex items-center gap-3">
                <div className="text-2xl">{fan.flag}</div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium" style={{ color: '#F8FAFC' }}>{fan.name}</span>
                    <span className="text-lg">{fan.emoticon}</span>
                  </div>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-[10px]" style={{ color: '#64748B' }}>{fan.country}</span>
                    <span className="text-[10px]" style={{ color: '#475569' }}>·</span>
                    <span className="text-[10px]" style={{ color: '#475569' }}>Sector {fan.sector}</span>
                  </div>
                  <div className="flex items-center gap-2 mt-1.5">
                    <div className="flex-1 h-1 rounded-full" style={{ background: 'rgba(255,255,255,0.06)' }}>
                      <div
                        className="h-full rounded-full transition-all"
                        style={{ width: `${fan.stress}%`, background: stressColor(fan.stress) }}
                      />
                    </div>
                    <span className="text-[9px] font-semibold" style={{ color: stressColor(fan.stress) }}>
                      {stressLabel(fan.stress)}
                    </span>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Fan Inspector */}
      <AnimatePresence>
        {selected ? (
          <motion.div
            className="flex-1 overflow-y-auto"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            key={selected.id}
          >
            {/* Apple Health-style profile */}
            <div className="rounded-2xl overflow-hidden" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(6,182,212,0.15)' }}>
              {/* Header */}
              <div
                className="p-6"
                style={{ background: 'linear-gradient(135deg, rgba(6,182,212,0.12) 0%, rgba(139,92,246,0.08) 100%)' }}
              >
                <div className="flex items-center gap-5">
                  <div
                    className="w-20 h-20 rounded-3xl flex items-center justify-center text-4xl"
                    style={{ background: 'rgba(255,255,255,0.08)', border: '1px solid rgba(255,255,255,0.15)' }}
                  >
                    {selected.flag}
                  </div>
                  <div className="flex-1">
                    <h2 className="text-2xl font-semibold" style={{ color: '#F8FAFC' }}>{selected.name}</h2>
                    <p className="text-sm mt-0.5" style={{ color: '#94A3B8' }}>{selected.country} · Digital Twin #{selected.id}</p>
                    <div className="flex items-center gap-3 mt-3">
                      <span className="text-2xl">{selected.emoticon}</span>
                      <div>
                        <div className="text-sm font-semibold" style={{ color: '#F8FAFC' }}>{selected.emotion}</div>
                        <div className="text-[10px]" style={{ color: '#64748B' }}>Current Emotion</div>
                      </div>
                      <div className="ml-6">
                        <div className="text-sm font-semibold" style={{ color: '#F8FAFC' }}>Sector {selected.sector}, {selected.seat}</div>
                        <div className="text-[10px]" style={{ color: '#64748B' }}>Location</div>
                      </div>
                    </div>
                  </div>
                  <button
                    className="text-xs px-3 py-1.5 rounded-xl"
                    style={{ background: 'rgba(255,255,255,0.06)', color: '#94A3B8' }}
                    onClick={() => setSelected(null)}
                  >
                    Close
                  </button>
                </div>
              </div>

              {/* Stats */}
              <div className="p-4 grid grid-cols-2 gap-3">
                {/* Stress gauge */}
                <div className="rounded-2xl p-4" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
                  <div className="text-[10px] uppercase tracking-wider mb-3" style={{ color: '#64748B' }}>Stress Level</div>
                  <div className="flex items-center gap-3">
                    <div className="relative w-16 h-16">
                      <svg viewBox="0 0 64 64" className="w-16 h-16 -rotate-90">
                        <circle cx="32" cy="32" r="26" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="6" />
                        <motion.circle
                          cx="32" cy="32" r="26"
                          fill="none"
                          stroke={stressColor(selected.stress)}
                          strokeWidth="6"
                          strokeLinecap="round"
                          strokeDasharray={`${2 * Math.PI * 26}`}
                          initial={{ strokeDashoffset: 2 * Math.PI * 26 }}
                          animate={{ strokeDashoffset: 2 * Math.PI * 26 * (1 - selected.stress / 100) }}
                          transition={{ duration: 1.5 }}
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-sm font-bold" style={{ color: stressColor(selected.stress) }}>{selected.stress}%</span>
                      </div>
                    </div>
                    <div>
                      <div className="text-lg font-bold" style={{ color: stressColor(selected.stress) }}>{stressLabel(selected.stress)}</div>
                      <div className="text-[10px]" style={{ color: '#64748B' }}>Biometric reading</div>
                    </div>
                  </div>
                </div>

                {/* Confidence */}
                <div className="rounded-2xl p-4" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
                  <div className="text-[10px] uppercase tracking-wider mb-3" style={{ color: '#64748B' }}>AI Confidence</div>
                  <div className="text-3xl font-bold mb-1" style={{ color: '#3B82F6' }}>{selected.confidence}%</div>
                  <div className="text-[10px]" style={{ color: '#64748B' }}>Prediction accuracy</div>
                  <div className="w-full h-1.5 rounded-full mt-2" style={{ background: 'rgba(255,255,255,0.06)' }}>
                    <motion.div
                      className="h-full rounded-full"
                      style={{ background: 'linear-gradient(90deg, #3B82F6, #8B5CF6)' }}
                      initial={{ width: 0 }}
                      animate={{ width: `${selected.confidence}%` }}
                      transition={{ duration: 1.5 }}
                    />
                  </div>
                </div>

                {/* Thought, Memory, Prediction */}
                {[
                  { label: '💭 Current Thought', value: selected.thought, color: '#8B5CF6' },
                  { label: '🧠 Memory', value: selected.memory, color: '#3B82F6' },
                  { label: '🔮 Prediction', value: selected.prediction, color: '#F59E0B' },
                ].map(item => (
                  <div key={item.label} className="rounded-2xl p-4 col-span-2" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
                    <div className="text-[10px] uppercase tracking-wider mb-2 font-medium" style={{ color: '#64748B' }}>{item.label}</div>
                    <p className="text-sm px-3 py-2 rounded-xl" style={{ color: '#CBD5E1', background: `${item.color}08`, borderLeft: `2px solid ${item.color}50` }}>
                      "{item.value}"
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div
            className="flex-1 flex items-center justify-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <div className="text-center">
              <div className="text-5xl mb-4">👥</div>
              <p className="text-sm" style={{ color: '#475569' }}>Select a fan to inspect their digital twin</p>
              <p className="text-[11px] mt-1" style={{ color: '#334155' }}>87,342 twins currently active</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

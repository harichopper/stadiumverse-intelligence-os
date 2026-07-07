import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const BOOT_STEPS = [
  { text: 'Initializing StadiumVerse Intelligence OS...', color: '#3B82F6' },
  { text: 'Loading Stadium Memory...', color: '#8B5CF6' },
  { text: 'Connecting Digital Twins...', color: '#06B6D4' },
  { text: 'Loading 13 AI Agents...', color: '#10B981' },
  { text: 'Synchronizing Collective Intelligence...', color: '#8B5CF6' },
  { text: 'Calibrating Predictive Models...', color: '#3B82F6' },
  { text: 'Predicting Future...', color: '#F59E0B' },
  { text: '🧠 Living Brain Online.', color: '#10B981' },
];

interface Props {
  onComplete: () => void;
}

export const BootSequence: React.FC<Props> = ({ onComplete }) => {
  const [step, setStep] = useState(0);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    if (step < BOOT_STEPS.length) {
      const t = setTimeout(() => setStep(s => s + 1), step === 0 ? 400 : 600);
      return () => clearTimeout(t);
    } else {
      // All steps shown — fade out then call onComplete
      const t = setTimeout(() => {
        setVisible(false);
        setTimeout(onComplete, 600);
      }, 800);
      return () => clearTimeout(t);
    }
  }, [step, onComplete]);

  const progress = Math.round((step / BOOT_STEPS.length) * 100);

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: '#050816',
        zIndex: 999,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        opacity: visible ? 1 : 0,
        transition: 'opacity 0.6s ease',
        pointerEvents: visible ? 'all' : 'none',
      }}
    >
      {/* Background glow */}
      <div style={{
        position: 'absolute', inset: 0, pointerEvents: 'none',
        background: 'radial-gradient(ellipse at 50% 50%, rgba(59,130,246,0.07) 0%, transparent 70%)',
      }} />

      {/* Grid overlay */}
      <div style={{
        position: 'absolute', inset: 0, pointerEvents: 'none', opacity: 0.15,
        backgroundImage: 'linear-gradient(rgba(59,130,246,0.15) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,0.15) 1px, transparent 1px)',
        backgroundSize: '60px 60px',
      }} />

      {/* Scan line */}
      <motion.div
        style={{
          position: 'absolute', left: 0, right: 0, height: 2,
          background: 'linear-gradient(90deg, transparent, rgba(59,130,246,0.5), transparent)',
          pointerEvents: 'none',
        }}
        animate={{ top: ['0%', '100%'] }}
        transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
      />

      <div style={{ position: 'relative', zIndex: 10, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 48, width: '100%', maxWidth: 560, padding: '0 32px' }}>

        {/* Logo / Brain */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16 }}
        >
          {/* Brain SVG */}
          <div style={{ position: 'relative', width: 88, height: 88 }}>
            <motion.div
              style={{
                position: 'absolute', inset: 0, borderRadius: '50%',
                background: 'radial-gradient(circle, rgba(59,130,246,0.25) 0%, transparent 70%)',
              }}
              animate={{ scale: [1, 1.4, 1] }}
              transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
            />
            <svg viewBox="0 0 88 88" width="88" height="88" fill="none">
              <circle cx="44" cy="44" r="38" stroke="rgba(59,130,246,0.2)" strokeWidth="1" fill="rgba(59,130,246,0.06)" />
              <motion.circle cx="44" cy="44" r="38"
                stroke="#3B82F6" strokeWidth="1.5" fill="none"
                strokeDasharray="240" strokeLinecap="round"
                animate={{ strokeDashoffset: [240, 0] }}
                transition={{ duration: 2, ease: 'easeInOut' }}
              />
              {/* Brain nodes */}
              {[
                [28, 30], [44, 22], [60, 30],
                [22, 46], [44, 40], [66, 46],
                [28, 62], [44, 58], [60, 62],
              ].map(([cx, cy], i) => (
                <motion.circle key={i} cx={cx} cy={cy} r="3.5"
                  fill="#3B82F6"
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: [0, 1, 0.7] }}
                  transition={{ delay: 0.8 + i * 0.12, duration: 0.4 }}
                />
              ))}
              {/* Connections */}
              {[
                [28,30,44,22],[44,22,60,30],
                [28,30,22,46],[60,30,66,46],
                [22,46,44,40],[44,40,66,46],
                [22,46,28,62],[66,46,60,62],
                [28,62,44,58],[44,58,60,62],
                [44,40,44,22],[44,40,44,58],
              ].map(([x1,y1,x2,y2], i) => (
                <motion.line key={i} x1={x1} y1={y1} x2={x2} y2={y2}
                  stroke="rgba(59,130,246,0.35)" strokeWidth="0.8"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 1 + i * 0.08 }}
                />
              ))}
            </svg>
          </div>

          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 28, fontWeight: 200, letterSpacing: '0.25em', color: '#F8FAFC', textTransform: 'uppercase', fontFamily: 'Inter, sans-serif' }}>
              StadiumVerse
            </div>
            <div style={{ fontSize: 11, letterSpacing: '0.45em', color: '#3B82F6', textTransform: 'uppercase', marginTop: 4, fontFamily: 'Inter, sans-serif', fontWeight: 400 }}>
              Intelligence OS
            </div>
            <div style={{ fontSize: 10, color: '#475569', marginTop: 6, letterSpacing: '0.1em' }}>
              ⚽ FIFA WORLD CUP 2026 · COMMAND CENTER
            </div>
          </div>
        </motion.div>

        {/* Boot log */}
        <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: 8, fontFamily: 'monospace' }}>
          {BOOT_STEPS.slice(0, step).map((s, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.35 }}
              style={{ display: 'flex', alignItems: 'center', gap: 10 }}
            >
              <span style={{ color: s.color, fontSize: 11 }}>
                {i === BOOT_STEPS.length - 1 ? '●' : '✓'}
              </span>
              <span style={{
                fontSize: 13,
                color: i === BOOT_STEPS.length - 1 ? s.color : '#94A3B8',
                fontWeight: i === BOOT_STEPS.length - 1 ? 600 : 400,
              }}>
                {s.text}
              </span>
              {/* Thinking dots on last visible step */}
              {i === step - 1 && step < BOOT_STEPS.length && (
                <span style={{ display: 'flex', gap: 3, marginLeft: 4 }}>
                  {[0, 1, 2].map(d => (
                    <motion.span key={d}
                      style={{ width: 4, height: 4, borderRadius: '50%', background: s.color, display: 'block' }}
                      animate={{ opacity: [0, 1, 0] }}
                      transition={{ duration: 0.9, repeat: Infinity, delay: d * 0.2 }}
                    />
                  ))}
                </span>
              )}
            </motion.div>
          ))}
        </div>

        {/* Progress bar */}
        <div style={{ width: '100%' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
            <span style={{ fontSize: 10, color: '#475569', letterSpacing: '0.1em', textTransform: 'uppercase' }}>System Boot</span>
            <span style={{ fontSize: 10, color: '#3B82F6', fontFamily: 'monospace' }}>{progress}%</span>
          </div>
          <div style={{ width: '100%', height: 3, background: 'rgba(255,255,255,0.06)', borderRadius: 2 }}>
            <motion.div
              style={{ height: '100%', borderRadius: 2, background: 'linear-gradient(90deg, #3B82F6, #8B5CF6, #06B6D4)' }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.4 }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

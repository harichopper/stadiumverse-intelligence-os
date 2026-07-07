import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useAppStore } from '../../store/appStore';

const EVENTS = [
  { t: -20, label: 'Gate A opened',         type: 'info',       icon: '🚪' },
  { t: -15, label: 'Crowd surge',           type: 'warn',       icon: '⚠️' },
  { t: -5,  label: 'Volunteers deployed',   type: 'success',    icon: '✅' },
  { t: 0,   label: 'NOW',                   type: 'now',        icon: '📍' },
  { t: 5,   label: 'Predicted congestion',  type: 'prediction', icon: '🔮' },
  { t: 10,  label: 'Rain expected',         type: 'prediction', icon: '🌧️' },
  { t: 20,  label: 'Peak fan exit',         type: 'prediction', icon: '📊' },
  { t: 30,  label: 'Stadium clear',         type: 'prediction', icon: '✨' },
];

const COLORS: Record<string, string> = {
  info: '#3B82F6', warn: '#F59E0B', success: '#10B981',
  now: '#EF4444', prediction: '#8B5CF6',
};

export const Timeline: React.FC = () => {
  const { timelineOffset, setTimelineOffset } = useAppStore();
  const [tip, setTip] = useState<number | null>(null);

  return (
    <div style={{
      height: 68, flexShrink: 0, display: 'flex', alignItems: 'center',
      padding: '0 14px', gap: 12, position: 'relative', zIndex: 20,
      background: 'rgba(5,8,22,.95)', borderTop: '1px solid rgba(255,255,255,.06)',
    }}>
      {/* label */}
      <div style={{ flexShrink: 0, width: 52 }}>
        <div style={{ fontSize: 9, color: '#64748B', textTransform: 'uppercase', letterSpacing: '.06em' }}>Timeline</div>
        <div style={{ fontSize: 11, fontWeight: 600, color: '#3B82F6', marginTop: 2 }}>
          {timelineOffset === 0 ? 'NOW' : timelineOffset > 0 ? `+${timelineOffset}m` : `${timelineOffset}m`}
        </div>
      </div>

      {/* track */}
      <div style={{ flex: 1, position: 'relative', height: 40, display: 'flex', alignItems: 'center' }}>
        {/* bg line */}
        <div style={{ position: 'absolute', left: 0, right: 0, height: 2, background: 'rgba(255,255,255,.06)', borderRadius: 1 }} />
        {/* progress */}
        <div style={{ position: 'absolute', left: 0, height: 2, borderRadius: 1, background: 'linear-gradient(90deg,#3B82F6,#8B5CF6)', width: `${((timelineOffset + 30) / 60) * 100}%` }} />

        {/* events */}
        {EVENTS.map((ev, i) => {
          const pos = ((ev.t + 30) / 60) * 100;
          const color = COLORS[ev.type];
          const isNow = ev.type === 'now';
          return (
            <div key={i} style={{ position: 'absolute', left: `${pos}%`, transform: 'translateX(-50%)', cursor: 'pointer' }}
              onMouseEnter={() => setTip(i)} onMouseLeave={() => setTip(null)}>
              {isNow && (
                <motion.div animate={{ scale: [1, 2, 1] }} transition={{ duration: 1.5, repeat: Infinity }}
                  style={{ position: 'absolute', width: 14, height: 14, borderRadius: '50%', background: color, opacity: .25, top: '50%', left: '50%', transform: 'translate(-50%,-50%)' }} />
              )}
              <div style={{ width: isNow ? 10 : 7, height: isNow ? 10 : 7, borderRadius: '50%', background: ev.t <= timelineOffset ? color : 'rgba(255,255,255,.1)', border: `1px solid ${ev.t <= timelineOffset ? color : 'rgba(255,255,255,.15)'}`, position: 'relative', zIndex: 1 }} />
              <div style={{ position: 'absolute', bottom: -16, left: '50%', transform: 'translateX(-50%)', fontSize: 8, color: isNow ? color : '#475569', whiteSpace: 'nowrap' }}>
                {ev.t === 0 ? 'NOW' : ev.t > 0 ? `+${ev.t}m` : `${ev.t}m`}
              </div>
              {/* tooltip */}
              {tip === i && (
                <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }}
                  style={{ position: 'absolute', bottom: 20, left: '50%', transform: 'translateX(-50%)', background: 'rgba(5,8,22,.97)', border: `1px solid ${color}30`, borderRadius: 6, padding: '4px 8px', whiteSpace: 'nowrap', fontSize: 10, color: '#F8FAFC', zIndex: 10 }}>
                  {ev.icon} {ev.label}
                </motion.div>
              )}
            </div>
          );
        })}

        {/* drag input */}
        <input type="range" min={-30} max={30} step={5} value={timelineOffset}
          onChange={e => setTimelineOffset(+e.target.value)}
          style={{ position: 'absolute', inset: 0, width: '100%', opacity: 0, cursor: 'pointer', zIndex: 5 }} />
      </div>

      {/* jump buttons */}
      <div style={{ display: 'flex', gap: 4, flexShrink: 0 }}>
        {[-10, 0, 10, 20, 30].map(t => (
          <motion.button key={t} onClick={() => setTimelineOffset(t)} whileHover={{ scale: 1.08 }} whileTap={{ scale: .94 }}
            style={{ fontSize: 9, padding: '3px 8px', borderRadius: 6, cursor: 'pointer', fontWeight: 500,
              background: timelineOffset === t ? 'rgba(59,130,246,.2)' : 'rgba(255,255,255,.04)',
              color: timelineOffset === t ? '#3B82F6' : '#475569',
              border: `1px solid ${timelineOffset === t ? 'rgba(59,130,246,.3)' : 'rgba(255,255,255,.06)'}` }}>
            {t === 0 ? 'NOW' : t > 0 ? `+${t}` : t}
          </motion.button>
        ))}
      </div>
    </div>
  );
};

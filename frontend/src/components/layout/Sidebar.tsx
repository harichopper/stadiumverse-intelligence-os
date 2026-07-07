import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAppStore, Page } from '../../store/appStore';

const NAV: { id: Page; emoji: string; label: string; color: string; badge?: string }[] = [
  { id: 'dashboard',  emoji: '⊞',  label: 'Dashboard',       color: '#3B82F6' },
  { id: 'brain',      emoji: '🧠', label: 'AI Brain',         color: '#8B5CF6', badge: 'LIVE' },
  { id: 'twins',      emoji: '👥', label: 'Digital Twins',    color: '#06B6D4' },
  { id: 'simulation', emoji: '⚙️', label: 'Simulation',       color: '#10B981' },
  { id: 'future',     emoji: '🔮', label: 'Future Branches',  color: '#F59E0B' },
  { id: 'analytics',  emoji: '📊', label: 'Analytics',        color: '#3B82F6' },
  { id: 'debate',     emoji: '🗣️', label: 'AI Debate',        color: '#EF4444', badge: '4' },
  { id: 'memory',     emoji: '🗄️', label: 'Memory',           color: '#8B5CF6' },
  { id: 'reports',    emoji: '📋', label: 'Reports',          color: '#06B6D4' },
  { id: 'settings',   emoji: '⚙️', label: 'Settings',         color: '#64748B' },
];

export const Sidebar: React.FC = () => {
  const { currentPage, setCurrentPage } = useAppStore();
  const [hovered, setHovered] = useState<Page | null>(null);

  return (
    <nav style={{
      width: 60, flexShrink: 0,
      background: 'rgba(5,8,22,.95)',
      borderRight: '1px solid rgba(255,255,255,.06)',
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      padding: '10px 0', gap: 2, position: 'relative', zIndex: 20,
    }} aria-label="Main navigation">
      {/* top pulse */}
      <motion.div
        style={{ width: 8, height: 8, borderRadius: '50%', background: '#3B82F6', marginBottom: 8, flexShrink: 0 }}
        animate={{ boxShadow: ['0 0 4px #3B82F6', '0 0 14px #3B82F6', '0 0 4px #3B82F6'] }}
        transition={{ duration: 2.5, repeat: Infinity }}
        role="presentation"
      />

      {NAV.map(item => {
        const active = currentPage === item.id;
        return (
          <div key={item.id} style={{ position: 'relative', width: '100%', display: 'flex', justifyContent: 'center' }}
            onMouseEnter={() => setHovered(item.id)}
            onMouseLeave={() => setHovered(null)}>

            <motion.button
              onClick={() => setCurrentPage(item.id)}
              whileHover={{ scale: 1.12 }}
              whileTap={{ scale: 0.94 }}
              aria-label={`Go to ${item.label} page`}
              aria-current={active ? 'page' : 'false'}
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  setCurrentPage(item.id);
                }
              }}
              style={{
                width: 38, height: 38, borderRadius: 10, border: 'none', cursor: 'pointer',
                background: active ? `${item.color}20` : 'transparent',
                outline: 'none',
                boxShadow: active ? `0 0 0 2px ${item.color}40` : 'none',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 16, position: 'relative',
                transition: 'box-shadow 0.2s ease',
              }}
              onFocus={(e) => {
                e.currentTarget.style.boxShadow = `0 0 0 2px ${item.color}80`;
              }}
              onBlur={(e) => {
                e.currentTarget.style.boxShadow = active ? `0 0 0 2px ${item.color}40` : 'none';
              }}
            >
              {/* active left bar */}
              {active && (
                <motion.div layoutId="activeBar"
                  style={{ position: 'absolute', left: -11, width: 3, height: 20, borderRadius: 2, background: item.color }}
                  transition={{ type: 'spring', stiffness: 350 }}
                />
              )}
              <span style={{ fontSize: 15 }}>{item.emoji}</span>
              {/* badge */}
              {item.badge && (
                <span style={{
                  position: 'absolute', top: -2, right: -2,
                  fontSize: 7, fontWeight: 700, padding: '1px 3px', borderRadius: 999,
                  background: item.badge === 'LIVE' ? '#10B981' : '#EF4444', color: 'white',
                }} aria-label={`${item.badge} badge`}>{item.badge}</span>
              )}
            </motion.button>

            {/* tooltip */}
            <AnimatePresence>
              {hovered === item.id && (
                <motion.div
                  initial={{ opacity: 0, x: -6 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -6 }}
                  transition={{ duration: 0.15 }}
                  style={{
                    position: 'absolute', left: 50, top: '50%', transform: 'translateY(-50%)',
                    background: 'rgba(5,8,22,.97)', border: `1px solid ${item.color}30`,
                    borderRadius: 8, padding: '5px 10px', whiteSpace: 'nowrap', zIndex: 100,
                    fontSize: 11, fontWeight: 500, color: item.color,
                    boxShadow: '0 8px 24px rgba(0,0,0,.5)',
                    pointerEvents: 'none',
                  }}
                  role="tooltip"
                >
                  {item.label}
                  {item.badge && (
                    <span style={{ marginLeft: 6, fontSize: 8, fontWeight: 700, background: item.badge === 'LIVE' ? '#10B981' : '#EF4444', color: 'white', padding: '1px 4px', borderRadius: 4 }}>
                      {item.badge}
                    </span>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        );
      })}

      {/* bottom online dot */}
      <div style={{ marginTop: 'auto' }}>
        <motion.div style={{ width: 6, height: 6, borderRadius: '50%', background: '#10B981' }}
          animate={{ opacity: [1, 0.4, 1] }} transition={{ duration: 2, repeat: Infinity }} 
          role="presentation"
          aria-hidden="true"
        />
      </div>
    </nav>
  );
};

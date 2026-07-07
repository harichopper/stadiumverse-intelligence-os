import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

interface MetricCardProps {
  title: string;
  value: string | number;
  unit?: string;
  icon: React.ReactNode;
  color: string;
  trend?: number;
  status?: 'good' | 'warn' | 'bad';
  subtitle?: string;
  sparkData?: number[];
  delay?: number;
}

const Sparkline: React.FC<{ data: number[]; color: string }> = ({ data, color }) => {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const w = 60, h = 24;
  const pts = data.map((v, i) => {
    const x = (i / (data.length - 1)) * w;
    const y = h - ((v - min) / range) * h;
    return `${x},${y}`;
  }).join(' ');

  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} fill="none">
      <polyline points={pts} stroke={color} strokeWidth="1.5" fill="none" strokeLinecap="round" strokeLinejoin="round" opacity="0.8" />
      <polyline points={`0,${h} ${pts} ${w},${h}`} fill={`${color}20`} stroke="none" />
    </svg>
  );
};

export const MetricCard: React.FC<MetricCardProps> = ({
  title, value, unit, icon, color, trend, status = 'good', subtitle, sparkData, delay = 0
}) => {
  const [displayValue, setDisplayValue] = useState(0);
  const numVal = typeof value === 'number' ? value : parseFloat(String(value).replace(/,/g, ''));

  useEffect(() => {
    let start = 0;
    const end = numVal;
    const duration = 1500;
    const startTime = Date.now();
    const tick = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplayValue(Math.round(start + (end - start) * eased));
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, [numVal]);

  const statusColors = { good: '#10B981', warn: '#F59E0B', bad: '#EF4444' };
  const statusColor = statusColors[status];

  const formatVal = (v: number) => {
    if (typeof value === 'string' && value.includes(',')) return v.toLocaleString();
    return v;
  };

  return (
    <motion.div
      className="relative overflow-hidden rounded-2xl p-4 cursor-pointer group"
      style={{
        background: 'rgba(255,255,255,0.04)',
        border: '1px solid rgba(255,255,255,0.07)',
        backdropFilter: 'blur(20px)',
      }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5, ease: 'easeOut' }}
      whileHover={{
        y: -4,
        boxShadow: `0 20px 60px rgba(0,0,0,0.4), 0 0 30px ${color}20`,
        borderColor: `${color}30`,
      }}
    >
      {/* Background glow */}
      <div
        className="absolute -top-8 -right-8 w-24 h-24 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-500"
        style={{ background: `radial-gradient(circle, ${color}15 0%, transparent 70%)` }}
      />

      {/* Status bar at top */}
      <div
        className="absolute top-0 left-0 right-0 h-0.5 rounded-t-2xl"
        style={{ background: `linear-gradient(90deg, transparent, ${color}60, transparent)` }}
      />

      <div className="relative z-10">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2">
            <div
              className="flex items-center justify-center w-8 h-8 rounded-xl"
              style={{ background: `${color}15`, color }}
            >
              {icon}
            </div>
            <div>
              <div className="text-[10px] uppercase tracking-wider font-medium" style={{ color: '#64748B' }}>
                {title}
              </div>
              {subtitle && (
                <div className="text-[9px]" style={{ color: '#475569' }}>{subtitle}</div>
              )}
            </div>
          </div>

          {sparkData && <Sparkline data={sparkData} color={color} />}

          {trend !== undefined && !sparkData && (
            <div
              className="text-xs font-medium flex items-center gap-0.5"
              style={{ color: trend >= 0 ? '#10B981' : '#EF4444' }}
            >
              <span>{trend >= 0 ? '↑' : '↓'}</span>
              <span>{Math.abs(trend)}%</span>
            </div>
          )}
        </div>

        <div className="flex items-end gap-1">
          <motion.span
            className="text-2xl font-semibold tabular-nums"
            style={{ color: '#F8FAFC', letterSpacing: '-0.02em' }}
            key={displayValue}
          >
            {formatVal(displayValue)}
          </motion.span>
          {unit && (
            <span className="text-sm mb-0.5" style={{ color: '#64748B' }}>{unit}</span>
          )}
        </div>

        {/* Status indicator */}
        <div className="flex items-center gap-1.5 mt-2">
          <motion.div
            className="w-1.5 h-1.5 rounded-full"
            style={{ background: statusColor }}
            animate={{ opacity: status === 'bad' ? [1, 0.3, 1] : 1 }}
            transition={{ duration: 0.8, repeat: Infinity }}
          />
          <span className="text-[10px]" style={{ color: statusColor }}>
            {status === 'good' ? 'NOMINAL' : status === 'warn' ? 'MONITOR' : 'ALERT'}
          </span>
        </div>
      </div>
    </motion.div>
  );
};

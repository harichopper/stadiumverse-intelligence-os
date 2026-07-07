import React, { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAppStore } from '../../store/appStore';

interface Entity {
  id: string;
  x: number;
  y: number;
  vx: number;
  vy: number;
  type: 'fan' | 'volunteer' | 'medical' | 'security';
  section: string;
}

interface FanDetail {
  id: string;
  country: string;
  flag: string;
  name: string;
  emotion: string;
  stress: number;
  thought: string;
  memory: string;
  prediction: string;
  confidence: number;
  sector: string;
}

const SECTIONS = [
  { id: 'N', label: 'North', cx: 200, cy: 60, color: '#3B82F6' },
  { id: 'S', label: 'South', cx: 200, cy: 300, color: '#3B82F6' },
  { id: 'E', label: 'East', cx: 340, cy: 180, color: '#8B5CF6' },
  { id: 'W', label: 'West', cx: 60, cy: 180, color: '#8B5CF6' },
  { id: 'VIP', label: 'VIP', cx: 200, cy: 155, color: '#F59E0B' },
];

const FANS: FanDetail[] = [
  { id: 'f1', country: 'Brazil', flag: '🇧🇷', name: 'Carlos M.', emotion: 'Ecstatic', stress: 12, thought: 'Goal! We need one more!', memory: 'Similar game in 2018 WC final', prediction: 'Will stay 30 more mins', confidence: 88, sector: 'N' },
  { id: 'f2', country: 'Argentina', flag: '🇦🇷', name: 'Diego R.', emotion: 'Anxious', stress: 67, thought: 'Come on, equalize!', memory: 'This exact score at 67th min before', prediction: 'Might leave early if no goal', confidence: 72, sector: 'S' },
  { id: 'f3', country: 'Germany', flag: '🇩🇪', name: 'Hans K.', emotion: 'Calm', stress: 23, thought: 'Great match quality', memory: 'First time at WC final', prediction: 'Will watch till end', confidence: 95, sector: 'E' },
  { id: 'f4', country: 'France', flag: '🇫🇷', name: 'Marie D.', emotion: 'Excited', stress: 31, thought: 'Amazing atmosphere!', memory: '2022 WC final comparison', prediction: 'Will buy merchandise', confidence: 91, sector: 'W' },
];

export const LivingStadium: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const entitiesRef = useRef<Entity[]>([]);
  const animFrameRef = useRef<number>(0);
  const [hoveredFan, setHoveredFan] = useState<FanDetail | null>(null);
  const [heatmapVisible, setHeatmapVisible] = useState(true);
  const { setSelectedFanId } = useAppStore();

  const W = 400, H = 360;

  // Init entities
  useEffect(() => {
    const entities: Entity[] = [];

    // Fans - spread around stadium sections
    for (let i = 0; i < 120; i++) {
      const angle = (i / 120) * Math.PI * 2;
      const r = 80 + Math.random() * 60;
      entities.push({
        id: `fan-${i}`,
        x: W / 2 + Math.cos(angle) * r * 0.9 + (Math.random() - 0.5) * 30,
        y: H / 2 + Math.sin(angle) * r * 0.6 + (Math.random() - 0.5) * 30,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.3,
        type: 'fan',
        section: SECTIONS[Math.floor(Math.random() * SECTIONS.length)].id,
      });
    }

    // Volunteers
    for (let i = 0; i < 8; i++) {
      entities.push({
        id: `vol-${i}`,
        x: W / 2 + (Math.random() - 0.5) * 200,
        y: H / 2 + (Math.random() - 0.5) * 160,
        vx: (Math.random() - 0.5) * 0.8,
        vy: (Math.random() - 0.5) * 0.6,
        type: 'volunteer',
        section: 'patrol',
      });
    }

    // Medical
    for (let i = 0; i < 4; i++) {
      entities.push({
        id: `med-${i}`,
        x: 40 + i * 100,
        y: H - 40,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        type: 'medical',
        section: 'medical',
      });
    }

    // Security
    for (let i = 0; i < 12; i++) {
      const angle = (i / 12) * Math.PI * 2;
      entities.push({
        id: `sec-${i}`,
        x: W / 2 + Math.cos(angle) * 155,
        y: H / 2 + Math.sin(angle) * 115,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.3,
        type: 'security',
        section: 'perimeter',
      });
    }

    entitiesRef.current = entities;
  }, []);

  // Animation loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = W;
    canvas.height = H;

    const typeColors = {
      fan: '#3B82F6',
      volunteer: '#10B981',
      medical: '#EF4444',
      security: '#F59E0B',
    };

    let time = 0;

    const draw = () => {
      ctx.clearRect(0, 0, W, H);
      time += 0.01;

      // Draw stadium shape
      // Field
      const fieldGrad = ctx.createRadialGradient(W/2, H/2, 10, W/2, H/2, 80);
      fieldGrad.addColorStop(0, 'rgba(16,185,129,0.12)');
      fieldGrad.addColorStop(1, 'rgba(16,185,129,0.04)');
      ctx.fillStyle = fieldGrad;
      ctx.beginPath();
      ctx.ellipse(W/2, H/2, 80, 55, 0, 0, Math.PI * 2);
      ctx.fill();

      // Field outline
      ctx.strokeStyle = 'rgba(16,185,129,0.3)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.ellipse(W/2, H/2, 80, 55, 0, 0, Math.PI * 2);
      ctx.stroke();

      // Center circle
      ctx.strokeStyle = 'rgba(16,185,129,0.2)';
      ctx.lineWidth = 0.5;
      ctx.beginPath();
      ctx.arc(W/2, H/2, 20, 0, Math.PI * 2);
      ctx.stroke();

      // Goal boxes
      ctx.strokeStyle = 'rgba(255,255,255,0.1)';
      ctx.strokeRect(W/2 - 25, H/2 - 55, 50, 15);
      ctx.strokeRect(W/2 - 25, H/2 + 40, 50, 15);

      // Stadium seats (elliptical stand)
      ctx.strokeStyle = 'rgba(59,130,246,0.15)';
      ctx.lineWidth = 18;
      ctx.beginPath();
      ctx.ellipse(W/2, H/2, 150, 105, 0, 0, Math.PI * 2);
      ctx.stroke();

      // Outer perimeter ring
      ctx.strokeStyle = 'rgba(59,130,246,0.06)';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(W/2, H/2, 168, 118, 0, 0, Math.PI * 2);
      ctx.stroke();

      // Entrances
      const entrances = [0, Math.PI/2, Math.PI, Math.PI*3/2];
      entrances.forEach(angle => {
        const ex = W/2 + Math.cos(angle) * 168;
        const ey = H/2 + Math.sin(angle) * 118;
        ctx.fillStyle = 'rgba(6,182,212,0.6)';
        ctx.beginPath();
        ctx.arc(ex, ey, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = 'rgba(6,182,212,0.15)';
        ctx.beginPath();
        ctx.arc(ex, ey, 8, 0, Math.PI * 2);
        ctx.fill();
      });

      // Heatmap overlay
      if (heatmapVisible) {
        const fanEntities = entitiesRef.current.filter(e => e.type === 'fan');
        fanEntities.forEach(fan => {
          const grad = ctx.createRadialGradient(fan.x, fan.y, 0, fan.x, fan.y, 20);
          grad.addColorStop(0, 'rgba(239,68,68,0.03)');
          grad.addColorStop(1, 'transparent');
          ctx.fillStyle = grad;
          ctx.beginPath();
          ctx.arc(fan.x, fan.y, 20, 0, Math.PI * 2);
          ctx.fill();
        });
      }

      // Update and draw entities
      entitiesRef.current.forEach(entity => {
        // Constrain to stadium bounds (ellipse)
        const dx = entity.x - W/2;
        const dy = entity.y - H/2;
        const dist = Math.sqrt((dx/150)**2 + (dy/105)**2);
        if (dist > 0.95) {
          entity.vx -= dx * 0.01;
          entity.vy -= dy * 0.01;
        }
        if (dist < 0.35 && entity.type === 'fan') {
          entity.vx += dx * 0.01;
          entity.vy += dy * 0.01;
        }

        entity.x += entity.vx + Math.sin(time + entity.id.charCodeAt(3)) * 0.1;
        entity.y += entity.vy + Math.cos(time + entity.id.charCodeAt(3)) * 0.08;
        entity.vx *= 0.98;
        entity.vy *= 0.98;

        const color = typeColors[entity.type];
        const size = entity.type === 'fan' ? 2.5 : 4;

        // Glow
        const glowGrad = ctx.createRadialGradient(entity.x, entity.y, 0, entity.x, entity.y, size * 3);
        glowGrad.addColorStop(0, `${color}60`);
        glowGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = glowGrad;
        ctx.beginPath();
        ctx.arc(entity.x, entity.y, size * 3, 0, Math.PI * 2);
        ctx.fill();

        // Dot
        ctx.fillStyle = color;
        ctx.globalAlpha = entity.type === 'fan' ? 0.7 : 1;
        ctx.beginPath();
        ctx.arc(entity.x, entity.y, size, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
      });

      // Labels — used for section identification

      // Section labels
      SECTIONS.forEach(sec => {
        ctx.font = '8px Inter';
        ctx.fillStyle = 'rgba(255,255,255,0.3)';
        ctx.textAlign = 'center';
        ctx.fillText(sec.label, sec.cx, sec.cy);
      });

      // POIs (Food, Restrooms, etc.)
      const pois = [
        { x: 30, y: 30, icon: '🍔', label: 'Food' },
        { x: W - 30, y: 30, icon: '🚻', label: 'WC' },
        { x: 30, y: H - 30, icon: '🅿️', label: 'Park' },
        { x: W - 30, y: H - 30, icon: '🚇', label: 'Metro' },
      ];
      pois.forEach(poi => {
        ctx.font = '12px serif';
        ctx.textAlign = 'center';
        ctx.fillText(poi.icon, poi.x, poi.y);
        ctx.font = '7px Inter';
        ctx.fillStyle = 'rgba(255,255,255,0.3)';
        ctx.fillText(poi.label, poi.x, poi.y + 10);
      });

      animFrameRef.current = requestAnimationFrame(draw);
    };

    draw();
    return () => cancelAnimationFrame(animFrameRef.current);
  }, [heatmapVisible]);

  return (
    <div className="relative w-full h-full flex flex-col">
      {/* Controls */}
      <div className="flex items-center justify-between mb-2 px-1">
        <div className="flex items-center gap-3">
          <span className="text-xs font-medium" style={{ color: '#F8FAFC' }}>Living Stadium</span>
          <motion.div
            className="flex items-center gap-1.5 text-[10px]"
            style={{ color: '#10B981' }}
            animate={{ opacity: [1, 0.5, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <div className="w-1.5 h-1.5 rounded-full bg-green-400" />
            LIVE
          </motion.div>
        </div>
        <div className="flex items-center gap-2">
          {/* Legend */}
          {[
            { color: '#3B82F6', label: 'Fans' },
            { color: '#10B981', label: 'Volunteers' },
            { color: '#EF4444', label: 'Medical' },
            { color: '#F59E0B', label: 'Security' },
          ].map(item => (
            <div key={item.label} className="flex items-center gap-1">
              <div className="w-2 h-2 rounded-full" style={{ background: item.color }} />
              <span className="text-[9px]" style={{ color: '#64748B' }}>{item.label}</span>
            </div>
          ))}
          <button
            className="text-[9px] px-2 py-0.5 rounded"
            style={{
              background: heatmapVisible ? 'rgba(239,68,68,0.15)' : 'rgba(255,255,255,0.04)',
              color: heatmapVisible ? '#EF4444' : '#64748B',
              border: `1px solid ${heatmapVisible ? 'rgba(239,68,68,0.3)' : 'rgba(255,255,255,0.08)'}`,
            }}
            onClick={() => setHeatmapVisible(!heatmapVisible)}
          >
            HEAT
          </button>
        </div>
      </div>

      {/* Canvas */}
      <div className="relative flex-1 flex items-center justify-center">
        <canvas
          ref={canvasRef}
          className="rounded-xl cursor-crosshair"
          style={{
            background: 'rgba(5,8,22,0.6)',
            border: '1px solid rgba(59,130,246,0.15)',
            maxWidth: '100%',
            maxHeight: '100%',
          }}
          onClick={() => {
            // x and y were not used

            // Find nearest fan to click
            const nearestFan = FANS[Math.floor(Math.random() * FANS.length)];
            setSelectedFanId(nearestFan.id);
            setHoveredFan(nearestFan);
          }}
        />

        {/* Floating POI tooltips */}
        <div className="absolute top-2 right-2 space-y-1">
          <div className="text-[9px] px-2 py-1 rounded" style={{ background: 'rgba(5,8,22,0.8)', color: '#06B6D4', border: '1px solid rgba(6,182,212,0.2)' }}>
            ✈️ Airport: 2 flights landed
          </div>
          <div className="text-[9px] px-2 py-1 rounded" style={{ background: 'rgba(5,8,22,0.8)', color: '#10B981', border: '1px solid rgba(16,185,129,0.2)' }}>
            🚇 Metro: 340/min influx
          </div>
        </div>
      </div>

      {/* Fan Inspector Panel */}
      <AnimatePresence>
        {hoveredFan && (
          <motion.div
            className="absolute top-0 right-0 w-72 rounded-2xl overflow-hidden z-20"
            style={{
              background: 'rgba(5,8,22,0.95)',
              border: '1px solid rgba(59,130,246,0.2)',
              backdropFilter: 'blur(20px)',
              boxShadow: '0 20px 60px rgba(0,0,0,0.6), 0 0 30px rgba(59,130,246,0.1)',
            }}
            initial={{ opacity: 0, x: 20, scale: 0.95 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: 20, scale: 0.95 }}
            transition={{ type: 'spring', stiffness: 300 }}
          >
            {/* Header */}
            <div
              className="p-4"
              style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.15), rgba(139,92,246,0.1))' }}
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div
                    className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
                    style={{ background: 'rgba(59,130,246,0.1)', border: '1px solid rgba(59,130,246,0.2)' }}
                  >
                    {hoveredFan.flag}
                  </div>
                  <div>
                    <div className="font-semibold text-sm" style={{ color: '#F8FAFC' }}>{hoveredFan.name}</div>
                    <div className="text-xs" style={{ color: '#64748B' }}>{hoveredFan.country} · Sector {hoveredFan.sector}</div>
                    <div className="text-xs mt-0.5" style={{ color: '#10B981' }}>Digital Twin #{hoveredFan.id}</div>
                  </div>
                </div>
                <button
                  className="text-xs px-2 py-1 rounded-lg"
                  style={{ background: 'rgba(255,255,255,0.06)', color: '#64748B' }}
                  onClick={() => setHoveredFan(null)}
                >
                  ✕
                </button>
              </div>

              <div className="flex gap-2">
                <div className="flex-1 text-center py-2 rounded-lg" style={{ background: 'rgba(255,255,255,0.04)' }}>
                  <div className="text-lg">😊</div>
                  <div className="text-[9px]" style={{ color: '#64748B' }}>Emotion</div>
                  <div className="text-[11px] font-medium" style={{ color: '#10B981' }}>{hoveredFan.emotion}</div>
                </div>
                <div className="flex-1 text-center py-2 rounded-lg" style={{ background: 'rgba(255,255,255,0.04)' }}>
                  <div className="text-sm font-bold" style={{ color: hoveredFan.stress < 40 ? '#10B981' : hoveredFan.stress < 70 ? '#F59E0B' : '#EF4444' }}>
                    {hoveredFan.stress}%
                  </div>
                  <div className="text-[9px]" style={{ color: '#64748B' }}>Stress</div>
                  <div className="w-full h-1 rounded-full mt-1" style={{ background: 'rgba(255,255,255,0.06)' }}>
                    <div
                      className="h-full rounded-full"
                      style={{
                        width: `${hoveredFan.stress}%`,
                        background: hoveredFan.stress < 40 ? '#10B981' : hoveredFan.stress < 70 ? '#F59E0B' : '#EF4444',
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Body */}
            <div className="p-4 space-y-3">
              {[
                { label: '💭 Current Thought', value: hoveredFan.thought, color: '#3B82F6' },
                { label: '🧠 Memory', value: hoveredFan.memory, color: '#8B5CF6' },
                { label: '🔮 Prediction', value: hoveredFan.prediction, color: '#F59E0B' },
              ].map(item => (
                <div key={item.label}>
                  <div className="text-[10px] mb-1 font-medium" style={{ color: '#64748B' }}>{item.label}</div>
                  <div className="text-xs px-2 py-2 rounded-lg" style={{ background: 'rgba(255,255,255,0.03)', color: '#CBD5E1', borderLeft: `2px solid ${item.color}` }}>
                    "{item.value}"
                  </div>
                </div>
              ))}

              <div className="flex items-center justify-between pt-1">
                <span className="text-[10px]" style={{ color: '#64748B' }}>Confidence</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 h-1.5 rounded-full" style={{ background: 'rgba(255,255,255,0.06)' }}>
                    <motion.div
                      className="h-full rounded-full"
                      style={{ background: 'linear-gradient(90deg, #3B82F6, #8B5CF6)', width: `${hoveredFan.confidence}%` }}
                      initial={{ width: 0 }}
                      animate={{ width: `${hoveredFan.confidence}%` }}
                    />
                  </div>
                  <span className="text-xs font-semibold" style={{ color: '#3B82F6' }}>{hoveredFan.confidence}%</span>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

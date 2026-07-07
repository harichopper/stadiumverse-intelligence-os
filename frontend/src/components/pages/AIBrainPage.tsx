import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, Zap, Clock, Cpu, Activity, Database, TrendingUp, ChevronRight } from 'lucide-react';

const ReasoningChain: React.FC = () => {
  const steps = [
    { icon: '👁️', label: 'Perceive', desc: 'Ingesting 87K+ fan data streams', color: '#3B82F6', time: '0.12s' },
    { icon: '🔗', label: 'Retrieve', desc: 'Querying 23 similar historical events', color: '#8B5CF6', time: '0.23s' },
    { icon: '⚖️', label: 'Debate', desc: '4 specialized agents deliberating', color: '#06B6D4', time: '1.4s' },
    { icon: '🧮', label: 'Compute', desc: 'Running 156 probability branches', color: '#F59E0B', time: '0.31s' },
    { icon: '✅', label: 'Decide', desc: 'Confidence 94% — action triggered', color: '#10B981', time: '0.08s' },
  ];

  const [active, setActive] = useState(0);
  useEffect(() => {
    const interval = setInterval(() => setActive(a => (a + 1) % steps.length), 1800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-center gap-2 overflow-x-auto pb-2">
      {steps.map((step, i) => (
        <React.Fragment key={step.label}>
          <motion.div
            className="flex-shrink-0 flex flex-col items-center gap-2 px-4 py-3 rounded-xl min-w-28"
            style={{
              background: active === i ? `${step.color}15` : 'rgba(255,255,255,0.03)',
              border: `1px solid ${active === i ? step.color + '40' : 'rgba(255,255,255,0.06)'}`,
            }}
            animate={{ scale: active === i ? 1.05 : 1 }}
          >
            <span className="text-xl">{step.icon}</span>
            <div className="text-center">
              <div className="text-xs font-semibold" style={{ color: active === i ? step.color : '#F8FAFC' }}>{step.label}</div>
              <div className="text-[9px] mt-0.5" style={{ color: '#64748B' }}>{step.desc}</div>
              <div className="text-[9px] mt-1 font-mono" style={{ color: step.color }}>{step.time}</div>
            </div>
            {active === i && (
              <motion.div
                className="w-full h-0.5 rounded-full"
                style={{ background: step.color }}
                animate={{ scaleX: [0, 1] }}
                transition={{ duration: 1.8 }}
              />
            )}
          </motion.div>
          {i < steps.length - 1 && (
            <ChevronRight size={16} style={{ color: '#334155', flexShrink: 0 }} />
          )}
        </React.Fragment>
      ))}
    </div>
  );
};

const NeuralVisualization: React.FC = () => {
  const [pulses, setPulses] = useState<number[]>([]);

  useEffect(() => {
    const interval = setInterval(() => {
      setPulses(prev => {
        const next = [...prev, Date.now()];
        return next.slice(-5);
      });
    }, 800);
    return () => clearInterval(interval);
  }, []);

  const nodes = [
    { x: 60, y: 120, label: 'Input Layer', color: '#3B82F6' },
    { x: 150, y: 60, label: 'Memory', color: '#8B5CF6' },
    { x: 150, y: 120, label: 'Reasoning', color: '#8B5CF6' },
    { x: 150, y: 180, label: 'Prediction', color: '#8B5CF6' },
    { x: 240, y: 90, label: 'Debate', color: '#06B6D4' },
    { x: 240, y: 150, label: 'Planning', color: '#06B6D4' },
    { x: 320, y: 120, label: 'Output', color: '#10B981' },
  ];

  const connections = [
    [0, 1], [0, 2], [0, 3],
    [1, 4], [2, 4], [2, 5], [3, 5],
    [4, 6], [5, 6],
  ];

  return (
    <svg viewBox="0 0 380 240" className="w-full h-full" style={{ opacity: 0.8 }}>
      {connections.map(([from, to], i) => (
        <motion.line
          key={i}
          x1={nodes[from].x} y1={nodes[from].y}
          x2={nodes[to].x} y2={nodes[to].y}
          stroke="rgba(59,130,246,0.2)"
          strokeWidth="1"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ delay: i * 0.1, duration: 0.5 }}
        />
      ))}
      {nodes.map((node, i) => (
        <g key={i}>
          <motion.circle
            cx={node.x} cy={node.y} r="16"
            fill={`${node.color}15`}
            stroke={node.color}
            strokeWidth="1"
            animate={{
              r: [16, 18, 16],
              opacity: [0.7, 1, 0.7],
            }}
            transition={{ duration: 2 + i * 0.3, repeat: Infinity, delay: i * 0.2 }}
          />
          <text x={node.x} y={node.y + 4} textAnchor="middle" fill={node.color} fontSize="7" fontWeight="600">
            {node.label.split(' ')[0]}
          </text>
        </g>
      ))}
    </svg>
  );
};

export const AIBrainPage: React.FC = () => {
  const [tokenUsage, setTokenUsage] = useState(24819);
  const [responseTime, setResponseTime] = useState(0.43);
  const [memUsed, setMemUsed] = useState(78);

  useEffect(() => {
    const interval = setInterval(() => {
      setTokenUsage(t => t + Math.floor(Math.random() * 150));
      setResponseTime(parseFloat((0.3 + Math.random() * 0.4).toFixed(2)));
      setMemUsed(m => Math.min(100, Math.max(60, m + Math.floor((Math.random() - 0.5) * 2))));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const stats = [
    { label: 'Model', value: 'LLaMA 3.1 70B', icon: <Brain size={14} />, color: '#8B5CF6' },
    { label: 'Response Time', value: `${responseTime}s`, icon: <Clock size={14} />, color: '#3B82F6' },
    { label: 'Tokens Used', value: tokenUsage.toLocaleString(), icon: <Cpu size={14} />, color: '#06B6D4' },
    { label: 'Memory Used', value: `${memUsed}%`, icon: <Database size={14} />, color: '#F59E0B' },
    { label: 'Confidence', value: '94%', icon: <TrendingUp size={14} />, color: '#10B981' },
    { label: 'Active Agents', value: '13', icon: <Activity size={14} />, color: '#EF4444' },
  ];

  return (
    <div className="h-full overflow-y-auto p-4 space-y-4">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <div className="flex items-center gap-3 mb-1">
          <div
            className="w-10 h-10 rounded-2xl flex items-center justify-center"
            style={{ background: 'rgba(139,92,246,0.2)', border: '1px solid rgba(139,92,246,0.4)' }}
          >
            <Brain size={20} style={{ color: '#8B5CF6' }} />
          </div>
          <div>
            <h1 className="text-2xl font-light" style={{ color: '#F8FAFC', letterSpacing: '-0.02em' }}>
              AI Brain
            </h1>
            <p className="text-xs" style={{ color: '#64748B' }}>JARVIS-class Intelligence Engine · All systems nominal</p>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <motion.div
              className="w-2 h-2 rounded-full"
              style={{ background: '#10B981' }}
              animate={{ scale: [1, 1.5, 1] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            />
            <span className="text-xs font-semibold" style={{ color: '#10B981' }}>ONLINE</span>
          </div>
        </div>
      </motion.div>

      {/* Stats grid */}
      <div className="grid grid-cols-3 lg:grid-cols-6 gap-3">
        {stats.map((stat, i) => (
          <motion.div
            key={stat.label}
            className="rounded-2xl p-3 text-center"
            style={{ background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.07)' }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            whileHover={{ y: -2, borderColor: `${stat.color}30` }}
          >
            <div className="flex justify-center mb-2" style={{ color: stat.color }}>{stat.icon}</div>
            <div className="text-sm font-semibold tabular-nums" style={{ color: '#F8FAFC' }}>{stat.value}</div>
            <div className="text-[9px] mt-0.5 uppercase tracking-wider" style={{ color: '#475569' }}>{stat.label}</div>
          </motion.div>
        ))}
      </div>

      {/* Two column layout */}
      <div className="grid grid-cols-2 gap-4">
        {/* Neural Network Visualization */}
        <motion.div
          className="rounded-2xl p-4"
          style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(139,92,246,0.15)' }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <div className="flex items-center gap-2 mb-4">
            <div className="w-2 h-2 rounded-full bg-purple-400" />
            <span className="text-xs font-semibold" style={{ color: '#F8FAFC' }}>Neural Architecture</span>
          </div>
          <div style={{ height: 200 }}>
            <NeuralVisualization />
          </div>
        </motion.div>

        {/* Reasoning chain */}
        <motion.div
          className="rounded-2xl p-4"
          style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(59,130,246,0.15)' }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <div className="flex items-center gap-2 mb-4">
            <div className="w-2 h-2 rounded-full bg-blue-400" />
            <span className="text-xs font-semibold" style={{ color: '#F8FAFC' }}>Live Reasoning Chain</span>
          </div>
          <ReasoningChain />
        </motion.div>
      </div>

      {/* Current learning */}
      <motion.div
        className="rounded-2xl p-4"
        style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(16,185,129,0.15)' }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <div className="flex items-center gap-2 mb-4">
          <div className="w-2 h-2 rounded-full bg-green-400" />
          <span className="text-xs font-semibold" style={{ color: '#F8FAFC' }}>Current Learning</span>
          <span className="text-[10px] px-2 py-0.5 rounded-full" style={{ background: 'rgba(16,185,129,0.15)', color: '#10B981' }}>
            Active training
          </span>
        </div>
        <div className="grid grid-cols-3 gap-3">
          {[
            { event: 'Gate B congestion resolved in 6 min', pattern: 'Volunteer deployment effective', confidence: 96, color: '#10B981' },
            { event: 'Rain impact on crowd flow: -15%', pattern: 'Historical rain pattern matched', confidence: 88, color: '#3B82F6' },
            { event: 'Medical response time: 3.2min avg', pattern: 'Zone C coverage optimal', confidence: 91, color: '#EF4444' },
          ].map((item, i) => (
            <div
              key={i}
              className="rounded-xl p-3"
              style={{ background: 'rgba(255,255,255,0.03)', border: `1px solid ${item.color}20` }}
            >
              <div className="text-[10px] font-medium mb-1" style={{ color: '#F8FAFC' }}>{item.event}</div>
              <div className="text-[9px] mb-2" style={{ color: '#64748B' }}>{item.pattern}</div>
              <div className="flex items-center gap-2">
                <div className="flex-1 h-1 rounded-full" style={{ background: 'rgba(255,255,255,0.06)' }}>
                  <div className="h-full rounded-full" style={{ width: `${item.confidence}%`, background: item.color }} />
                </div>
                <span className="text-[9px]" style={{ color: item.color }}>{item.confidence}%</span>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Black Box Recorder */}
      <motion.div
        className="rounded-2xl p-4"
        style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(239,68,68,0.15)' }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-red-400" />
            <span className="text-xs font-semibold" style={{ color: '#F8FAFC' }}>Black Box Recorder</span>
          </div>
          <span className="text-[10px]" style={{ color: '#64748B' }}>Last 5 decisions</span>
        </div>
        <div className="space-y-2">
          {[
            { time: '67:23', decision: 'Deploy 3 volunteers to Gate B', confidence: 94, outcome: 'SUCCESS', color: '#10B981' },
            { time: '65:14', decision: 'Activate digital signage at Exit C', confidence: 87, outcome: 'SUCCESS', color: '#10B981' },
            { time: '62:08', decision: 'Alert medical team Zone D', confidence: 91, outcome: 'SUCCESS', color: '#10B981' },
            { time: '58:44', decision: 'Reroute 400 fans to Metro Line 3', confidence: 89, outcome: 'PARTIAL', color: '#F59E0B' },
            { time: '52:31', decision: 'Adjust energy in North Stand lighting', confidence: 79, outcome: 'SUCCESS', color: '#10B981' },
          ].map((item, i) => (
            <motion.div
              key={i}
              className="flex items-center gap-4 px-3 py-2 rounded-xl"
              style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.04)' }}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.6 + i * 0.06 }}
              whileHover={{ background: 'rgba(255,255,255,0.04)' }}
            >
              <span className="font-mono text-[10px]" style={{ color: '#475569', width: 40 }}>{item.time}</span>
              <span className="flex-1 text-xs" style={{ color: '#CBD5E1' }}>{item.decision}</span>
              <span className="text-[10px] w-8 text-right" style={{ color: '#64748B' }}>{item.confidence}%</span>
              <span
                className="text-[9px] px-2 py-0.5 rounded-full font-semibold"
                style={{ background: `${item.color}15`, color: item.color }}
              >
                {item.outcome}
              </span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

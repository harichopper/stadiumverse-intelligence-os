import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, Zap, Target, TrendingUp, MessageSquare, Lightbulb, CheckCircle, Clock } from 'lucide-react';
import { useAppStore } from '../../store/appStore';

const TypingText: React.FC<{ text: string; speed?: number; color?: string }> = ({ text, speed = 30, color = '#F8FAFC' }) => {
  const [displayed, setDisplayed] = useState('');
  const [cursor, setCursor] = useState(true);

  useEffect(() => {
    setDisplayed('');
    let i = 0;
    const interval = setInterval(() => {
      if (i < text.length) {
        setDisplayed(text.slice(0, i + 1));
        i++;
      } else {
        clearInterval(interval);
      }
    }, speed);
    return () => clearInterval(interval);
  }, [text, speed]);

  useEffect(() => {
    const cursorInterval = setInterval(() => setCursor(c => !c), 500);
    return () => clearInterval(cursorInterval);
  }, []);

  return (
    <span style={{ color }}>
      {displayed}
      {cursor && displayed.length < text.length && (
        <span style={{ color: '#3B82F6', fontWeight: 'bold' }}>|</span>
      )}
    </span>
  );
};

const AgentDebate: React.FC = () => {
  const [agents, setAgents] = React.useState([
    { id: 'nav', name: 'Navigation', icon: '🗺️', color: '#3B82F6', status: 'thinking', message: '' },
    { id: 'med', name: 'Medical', icon: '🏥', color: '#EF4444', status: 'waiting', message: '' },
    { id: 'sec', name: 'Security', icon: '🛡️', color: '#F59E0B', status: 'waiting', message: '' },
    { id: 'tra', name: 'Transport', icon: '🚇', color: '#10B981', status: 'waiting', message: '' },
    { id: 'coord', name: 'Coordinator', icon: '🧠', color: '#8B5CF6', status: 'waiting', message: '' },
  ]);

  const agentMessages = React.useRef([
    { id: 'nav', msg: 'Gate B flow rate: 2,400/hr. Projecting 94% capacity in 8 min.' },
    { id: 'med', msg: 'No medical incidents in Zone B. Capacity to absorb 200 more attendees.' },
    { id: 'sec', msg: 'Perimeter secure. Recommend soft barriers at Gate B entrance.' },
    { id: 'tra', msg: 'Metro Station 2 at 78%. Suggest diverting 400 fans to Metro 3.' },
    { id: 'coord', msg: '⚡ Decision: Deploy 3 volunteers to Gate B. Activate digital signage rerouting. Expected impact: -23% congestion.' },
  ]);

  React.useEffect(() => {
    const msgs = agentMessages.current;
    let delay = 0;
    const timers: ReturnType<typeof setTimeout>[] = [];
    msgs.forEach((m, i) => {
      const t1 = setTimeout(() => {
        setAgents(prev => prev.map(a =>
          a.id === m.id ? { ...a, status: 'speaking', message: m.msg } : a
        ));
        const t2 = setTimeout(() => {
          setAgents(prev => prev.map(a =>
            a.id === m.id ? { ...a, status: 'done' } : a
          ));
          if (i + 1 < msgs.length) {
            setAgents(prev => prev.map(a =>
              a.id === msgs[i + 1].id ? { ...a, status: 'thinking' } : a
            ));
          }
        }, 2500);
        timers.push(t2);
      }, delay);
      timers.push(t1);
      delay += 3000;
    });
    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <div className="space-y-2">
      {agents.map((agent) => (
        <AnimatePresence key={agent.id}>
          {(agent.status !== 'waiting' || agent.message) && (
            <motion.div
              className="flex items-start gap-3"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ type: 'spring', stiffness: 300 }}
            >
              <div
                className="flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center text-sm"
                style={{ background: `${agent.color}15`, border: `1px solid ${agent.color}30` }}
              >
                {agent.icon}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-semibold" style={{ color: agent.color }}>{agent.name}</span>
                  {agent.status === 'thinking' && (
                    <div className="flex gap-1">
                      {[0, 1, 2].map(d => (
                        <motion.div
                          key={d}
                          className="w-1.5 h-1.5 rounded-full"
                          style={{ background: agent.color }}
                          animate={{ opacity: [0, 1, 0], scale: [0.5, 1, 0.5] }}
                          transition={{ duration: 1, repeat: Infinity, delay: d * 0.2 }}
                        />
                      ))}
                    </div>
                  )}
                  {agent.status === 'done' && (
                    <CheckCircle size={10} style={{ color: '#10B981' }} />
                  )}
                </div>
                {agent.message && (
                  <div
                    className="text-xs px-3 py-2 rounded-xl rounded-tl-sm"
                    style={{
                      background: agent.id === 'coord' ? `${agent.color}15` : 'rgba(255,255,255,0.04)',
                      border: `1px solid ${agent.id === 'coord' ? agent.color + '30' : 'rgba(255,255,255,0.06)'}`,
                      color: agent.id === 'coord' ? '#F8FAFC' : '#CBD5E1',
                    }}
                  >
                    {agent.status === 'speaking' ? (
                      <TypingText text={agent.message} speed={20} color={agent.id === 'coord' ? '#F8FAFC' : '#CBD5E1'} />
                    ) : agent.message}
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      ))}
    </div>
  );
};

export const LivingBrainPanel: React.FC = () => {
  const { currentThought, currentPrediction, confidence, isThinking } = useAppStore();
  const [activeTab, setActiveTab] = useState<'thoughts' | 'debate' | 'storyteller'>('thoughts');
  const [storyPhase, setStoryPhase] = useState(0);

  const story = {
    situation: 'At 67th minute, Gate B crowd density is at 87% capacity with 2,400 fans/hour flow rate.',
    prediction: 'In 8 minutes, Gate B will reach critical capacity (>95%), potentially causing crowd pressure.',
    reasoning: 'Historical data from 23 similar matches shows this pattern leads to congestion 84% of the time. Current volunteer coverage is insufficient.',
    recommendation: 'Deploy 3 additional volunteers to Gate B immediately. Activate digital signage to redirect fans to Gate C.',
    outcome: 'Expected 23% reduction in Gate B density within 5 minutes. Risk level drops from WARNING to NOMINAL.',
  };

  const storySteps = [
    { key: 'situation', label: '📍 Situation', color: '#3B82F6', text: story.situation },
    { key: 'prediction', label: '🔮 Prediction', color: '#F59E0B', text: story.prediction },
    { key: 'reasoning', label: '🧠 Reasoning', color: '#8B5CF6', text: story.reasoning },
    { key: 'recommendation', label: '⚡ Recommendation', color: '#10B981', text: story.recommendation },
    { key: 'outcome', label: '✅ Expected Outcome', color: '#06B6D4', text: story.outcome },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setStoryPhase(p => (p + 1) % storySteps.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const tabs = [
    { id: 'thoughts', label: 'Brain', icon: <Brain size={12} /> },
    { id: 'debate', label: 'Debate', icon: <MessageSquare size={12} /> },
    { id: 'storyteller', label: 'Story', icon: <Lightbulb size={12} /> },
  ];

  return (
    <div className="flex flex-col h-full">
      {/* Panel Header */}
      <div
        className="flex items-center justify-between px-4 py-3"
        style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}
      >
        <div className="flex items-center gap-2">
          <motion.div
            className="w-6 h-6 rounded-lg flex items-center justify-center"
            style={{ background: 'rgba(139,92,246,0.2)', border: '1px solid rgba(139,92,246,0.4)' }}
            animate={{ boxShadow: ['0 0 8px rgba(139,92,246,0.3)', '0 0 20px rgba(139,92,246,0.6)', '0 0 8px rgba(139,92,246,0.3)'] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <Brain size={12} style={{ color: '#8B5CF6' }} />
          </motion.div>
          <span className="text-xs font-semibold" style={{ color: '#F8FAFC' }}>Living Brain</span>
          <motion.span
            className="text-[9px] px-1.5 py-0.5 rounded-full font-bold"
            style={{ background: '#10B981', color: 'white' }}
            animate={{ opacity: [1, 0.7, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            ONLINE
          </motion.span>
        </div>
        <div className="flex items-center gap-1">
          <motion.div
            className="w-1.5 h-1.5 rounded-full bg-purple-400"
            animate={{ scale: [1, 1.4, 1] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          />
          <span className="text-[10px]" style={{ color: '#8B5CF6' }}>Thinking...</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 px-4 py-2">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className="flex items-center gap-1 px-3 py-1.5 rounded-lg text-[11px] font-medium transition-all"
            style={{
              background: activeTab === tab.id ? 'rgba(139,92,246,0.2)' : 'transparent',
              color: activeTab === tab.id ? '#8B5CF6' : '#64748B',
              border: `1px solid ${activeTab === tab.id ? 'rgba(139,92,246,0.3)' : 'transparent'}`,
            }}
            onClick={() => setActiveTab(tab.id as any)}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto px-4 pb-4 space-y-3">
        <AnimatePresence mode="wait">
          {activeTab === 'thoughts' && (
            <motion.div
              key="thoughts"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-3"
            >
              {/* Current Thought */}
              <div
                className="rounded-xl p-3"
                style={{ background: 'rgba(139,92,246,0.08)', border: '1px solid rgba(139,92,246,0.15)' }}
              >
                <div className="flex items-center gap-2 mb-2">
                  <Zap size={12} style={{ color: '#8B5CF6' }} />
                  <span className="text-[10px] uppercase tracking-wider font-medium" style={{ color: '#8B5CF6' }}>Current Thought</span>
                </div>
                <p className="text-xs leading-relaxed" style={{ color: '#CBD5E1' }}>
                  <TypingText text={currentThought} speed={25} color="#CBD5E1" />
                </p>
              </div>

              {/* Prediction */}
              <div
                className="rounded-xl p-3"
                style={{ background: 'rgba(245,158,11,0.06)', border: '1px solid rgba(245,158,11,0.15)' }}
              >
                <div className="flex items-center gap-2 mb-2">
                  <Target size={12} style={{ color: '#F59E0B' }} />
                  <span className="text-[10px] uppercase tracking-wider font-medium" style={{ color: '#F59E0B' }}>Prediction</span>
                </div>
                <p className="text-xs leading-relaxed" style={{ color: '#CBD5E1' }}>
                  {currentPrediction}
                </p>
              </div>

              {/* Confidence */}
              <div
                className="rounded-xl p-3"
                style={{ background: 'rgba(16,185,129,0.06)', border: '1px solid rgba(16,185,129,0.15)' }}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <TrendingUp size={12} style={{ color: '#10B981' }} />
                    <span className="text-[10px] uppercase tracking-wider font-medium" style={{ color: '#10B981' }}>Confidence</span>
                  </div>
                  <motion.span
                    className="text-xl font-bold"
                    style={{ color: '#10B981' }}
                    key={confidence}
                    initial={{ scale: 1.2 }}
                    animate={{ scale: 1 }}
                  >
                    {confidence}%
                  </motion.span>
                </div>
                <div className="w-full h-2 rounded-full overflow-hidden" style={{ background: 'rgba(255,255,255,0.06)' }}>
                  <motion.div
                    className="h-full rounded-full"
                    style={{ background: 'linear-gradient(90deg, #10B981, #3B82F6)' }}
                    animate={{ width: `${confidence}%` }}
                    transition={{ duration: 0.8 }}
                  />
                </div>
              </div>

              {/* Memory */}
              <div
                className="rounded-xl p-3"
                style={{ background: 'rgba(59,130,246,0.06)', border: '1px solid rgba(59,130,246,0.15)' }}
              >
                <div className="flex items-center gap-2 mb-2">
                  <Clock size={12} style={{ color: '#3B82F6' }} />
                  <span className="text-[10px] uppercase tracking-wider font-medium" style={{ color: '#3B82F6' }}>Memory</span>
                </div>
                <p className="text-xs" style={{ color: '#94A3B8' }}>
                  "Similar crowd pattern detected at 2022 WC Quarterfinals. Gate B congestion resolved in 7 min with 4 volunteers."
                </p>
              </div>

              {/* Recommendation */}
              <div
                className="rounded-xl p-3"
                style={{
                  background: 'rgba(16,185,129,0.08)',
                  border: '1px solid rgba(16,185,129,0.25)',
                  boxShadow: '0 0 20px rgba(16,185,129,0.05)',
                }}
              >
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle size={12} style={{ color: '#10B981' }} />
                  <span className="text-[10px] uppercase tracking-wider font-medium" style={{ color: '#10B981' }}>Recommendation</span>
                </div>
                <p className="text-xs font-medium mb-2" style={{ color: '#F8FAFC' }}>
                  Deploy 3 volunteers to Gate B. Activate digital signage.
                </p>
                <div className="flex items-center gap-3 text-[10px]" style={{ color: '#64748B' }}>
                  <span>Impact: <span style={{ color: '#10B981' }}>-23% congestion</span></span>
                  <span>ROI: <span style={{ color: '#3B82F6' }}>4.2x</span></span>
                </div>
                <motion.button
                  className="w-full mt-3 py-2 rounded-xl text-xs font-semibold"
                  style={{ background: 'linear-gradient(135deg, #10B981, #3B82F6)', color: 'white' }}
                  whileHover={{ scale: 1.02, boxShadow: '0 0 20px rgba(16,185,129,0.4)' }}
                  whileTap={{ scale: 0.98 }}
                >
                  ⚡ Execute Recommendation
                </motion.button>
              </div>
            </motion.div>
          )}

          {activeTab === 'debate' && (
            <motion.div
              key="debate"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <div className="mb-3">
                <div className="text-xs font-medium mb-1" style={{ color: '#F8FAFC' }}>Active Debate</div>
                <div className="text-[10px]" style={{ color: '#64748B' }}>Gate B Congestion Response</div>
              </div>
              <AgentDebate />
            </motion.div>
          )}

          {activeTab === 'storyteller' && (
            <motion.div
              key="storyteller"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-2"
            >
              <div className="text-[10px] mb-2" style={{ color: '#64748B' }}>AI Narrative Intelligence</div>
              {storySteps.map((step, i) => (
                <motion.div
                  key={step.key}
                  className="rounded-xl p-3"
                  style={{
                    background: i <= storyPhase ? `${step.color}08` : 'rgba(255,255,255,0.02)',
                    border: `1px solid ${i <= storyPhase ? step.color + '25' : 'rgba(255,255,255,0.04)'}`,
                    opacity: i <= storyPhase ? 1 : 0.3,
                  }}
                  animate={{ opacity: i <= storyPhase ? 1 : 0.3 }}
                >
                  <div className="text-[10px] font-semibold mb-1" style={{ color: step.color }}>
                    {step.label}
                  </div>
                  {i <= storyPhase && (
                    <p className="text-xs leading-relaxed" style={{ color: '#CBD5E1' }}>
                      {i === storyPhase ? (
                        <TypingText text={step.text} speed={20} color="#CBD5E1" />
                      ) : step.text}
                    </p>
                  )}
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

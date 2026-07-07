import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { GitBranch, TrendingUp, TrendingDown, Minus, ChevronRight } from 'lucide-react';

interface Branch {
  id: string;
  label: string;
  type: 'best' | 'likely' | 'worst';
  probability: number;
  description: string;
  impact: string;
  children?: Branch[];
}

const TREE: Branch[] = [
  {
    id: 'now', label: 'Current State', type: 'likely', probability: 100,
    description: 'Gate B at 87% capacity, 67th minute',
    impact: 'Nominal operations',
    children: [
      {
        id: 'best', label: 'Best Scenario', type: 'best', probability: 34,
        description: 'Early volunteer deployment resolves congestion',
        impact: '✅ Gate B drops to 65%. Zero incidents. Fan satisfaction +12%.',
        children: [
          {
            id: 'best-1', label: 'Smooth Exit Flow', type: 'best', probability: 28,
            description: 'All gates operating at optimal capacity',
            impact: '✅ Full stadium cleared in 22 minutes post-match.',
          },
        ],
      },
      {
        id: 'likely', label: 'Likely Scenario', type: 'likely', probability: 47,
        description: 'Standard response with minor delays',
        impact: '⚠️ Gate B peaks at 96%. 2-minute delay at turnstiles. Minor queuing.',
        children: [
          {
            id: 'likely-1', label: 'Metro Overflow', type: 'likely', probability: 38,
            description: 'Post-match metro capacity exceeded',
            impact: '⚠️ Metro Station 2 queue: 8-12 min wait. Additional shuttle needed.',
          },
        ],
      },
      {
        id: 'worst', label: 'Worst Scenario', type: 'worst', probability: 19,
        description: 'No intervention + rain event triggers panic',
        impact: '🔴 Gate B critical. Crowd pressure risk. Emergency protocol required.',
        children: [
          {
            id: 'worst-1', label: 'Crowd Incident', type: 'worst', probability: 8,
            description: 'Structural crowd pressure at Gate B',
            impact: '🔴 Medical deployment. Evacuation protocol. Match suspension risk.',
          },
        ],
      },
    ],
  },
];

const branchStyles = {
  best: { color: '#10B981', bg: 'rgba(16,185,129,0.08)', border: 'rgba(16,185,129,0.3)', icon: <TrendingUp size={12} /> },
  likely: { color: '#3B82F6', bg: 'rgba(59,130,246,0.08)', border: 'rgba(59,130,246,0.3)', icon: <Minus size={12} /> },
  worst: { color: '#EF4444', bg: 'rgba(239,68,68,0.08)', border: 'rgba(239,68,68,0.3)', icon: <TrendingDown size={12} /> },
};

const BranchNode: React.FC<{ branch: Branch; depth: number; onSelect: (b: Branch) => void; selectedId: string }> = ({
  branch, depth, onSelect, selectedId
}) => {
  const style = branchStyles[branch.type];
  const isSelected = selectedId === branch.id;
  const isRoot = depth === 0;

  return (
    <div className={`flex ${isRoot ? 'flex-col items-center' : ''}`}>
      <div className="flex items-start gap-4">
        {depth > 0 && (
          <div className="flex items-center pt-5">
            <div style={{ width: 32, height: 1, background: `${style.color}40` }} />
          </div>
        )}
        <motion.div
          className="rounded-2xl p-3 cursor-pointer"
          style={{
            background: isSelected ? style.bg : 'rgba(255,255,255,0.03)',
            border: `1px solid ${isSelected ? style.border : 'rgba(255,255,255,0.06)'}`,
            minWidth: isRoot ? 200 : 180,
            boxShadow: isSelected ? `0 0 20px ${style.color}15` : 'none',
          }}
          whileHover={{ scale: 1.02, borderColor: style.border }}
          whileTap={{ scale: 0.98 }}
          onClick={() => onSelect(branch)}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ type: 'spring', stiffness: 300 }}
        >
          <div className="flex items-center gap-2 mb-2">
            <span style={{ color: style.color }}>{style.icon}</span>
            <span className="text-xs font-semibold" style={{ color: style.color }}>{branch.label}</span>
            <span
              className="ml-auto text-[10px] px-1.5 py-0.5 rounded-full font-bold"
              style={{ background: `${style.color}20`, color: style.color }}
            >
              {branch.probability}%
            </span>
          </div>
          <p className="text-[10px] leading-relaxed" style={{ color: '#94A3B8' }}>{branch.description}</p>
        </motion.div>
      </div>

      {/* Children */}
      {branch.children && (
        <div className={`flex ${isRoot ? 'flex-row justify-center gap-8 mt-6' : 'flex-col gap-4 mt-4 ml-12'}`}>
          {/* Connecting lines for root */}
          {isRoot && branch.children.map((child) => (
            <div key={child.id} className="flex flex-col items-center">
              <div style={{ width: 1, height: 24, background: `${branchStyles[child.type].color}40` }} />
              <BranchNode branch={child} depth={depth + 1} onSelect={onSelect} selectedId={selectedId} />
              {child.children?.map(grandchild => (
                <div key={grandchild.id} className="flex flex-col items-center mt-4">
                  <div style={{ width: 1, height: 24, background: `${branchStyles[grandchild.type].color}30` }} />
                  <BranchNode branch={grandchild} depth={depth + 2} onSelect={onSelect} selectedId={selectedId} />
                </div>
              ))}
            </div>
          ))}

          {/* Non-root children */}
          {!isRoot && branch.children.map(child => (
            <BranchNode key={child.id} branch={child} depth={depth + 1} onSelect={onSelect} selectedId={selectedId} />
          ))}
        </div>
      )}
    </div>
  );
};

export const FuturePage: React.FC = () => {
  const [selectedBranch, setSelectedBranch] = useState<Branch | null>(null);

  return (
    <div className="h-full flex flex-col overflow-hidden p-4">
      {/* Header */}
      <motion.div className="flex items-center gap-3 mb-4" initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <div className="w-10 h-10 rounded-2xl flex items-center justify-center" style={{ background: 'rgba(245,158,11,0.15)', border: '1px solid rgba(245,158,11,0.3)' }}>
          <GitBranch size={18} style={{ color: '#F59E0B' }} />
        </div>
        <div>
          <h1 className="text-2xl font-light" style={{ color: '#F8FAFC', letterSpacing: '-0.02em' }}>Future Branches</h1>
          <p className="text-xs" style={{ color: '#64748B' }}>156 probability branches computed · Horizon: +30 minutes</p>
        </div>
        <div className="ml-auto flex gap-2">
          {['Best', 'Likely', 'Worst'].map((label, i) => {
            const colors = ['#10B981', '#3B82F6', '#EF4444'];
            const probs = ['34%', '47%', '19%'];
            return (
              <div key={label} className="flex items-center gap-2 px-3 py-2 rounded-xl" style={{ background: `${colors[i]}10`, border: `1px solid ${colors[i]}25` }}>
                <div className="w-2 h-2 rounded-full" style={{ background: colors[i] }} />
                <span className="text-xs font-medium" style={{ color: colors[i] }}>{label}</span>
                <span className="text-xs font-bold" style={{ color: colors[i] }}>{probs[i]}</span>
              </div>
            );
          })}
        </div>
      </motion.div>

      <div className="flex flex-1 gap-4 overflow-hidden">
        {/* Tree */}
        <div className="flex-1 overflow-auto rounded-2xl p-6" style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.06)' }}>
          <BranchNode
            branch={TREE[0]}
            depth={0}
            onSelect={(b) => setSelectedBranch(b)}
            selectedId={selectedBranch?.id ?? ''}
          />
        </div>

        {/* Detail panel */}
        <AnimatePresence>
          {selectedBranch && (
            <motion.div
              className="w-64 rounded-2xl p-4 overflow-y-auto"
              style={{
                background: 'rgba(5,8,22,0.95)',
                border: `1px solid ${branchStyles[selectedBranch.type].border}`,
                backdropFilter: 'blur(20px)',
              }}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
            >
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm font-semibold" style={{ color: branchStyles[selectedBranch.type].color }}>
                  {selectedBranch.label}
                </span>
                <button onClick={() => setSelectedBranch(null)} style={{ color: '#64748B' }}>✕</button>
              </div>

              <div
                className="text-4xl font-bold text-center py-4 rounded-xl mb-4"
                style={{
                  background: `${branchStyles[selectedBranch.type].color}10`,
                  color: branchStyles[selectedBranch.type].color,
                }}
              >
                {selectedBranch.probability}%
              </div>

              <div className="space-y-3">
                <div>
                  <div className="text-[10px] uppercase tracking-wider mb-1" style={{ color: '#64748B' }}>Description</div>
                  <p className="text-xs" style={{ color: '#CBD5E1' }}>{selectedBranch.description}</p>
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-wider mb-1" style={{ color: '#64748B' }}>Predicted Impact</div>
                  <p className="text-xs" style={{ color: '#CBD5E1' }}>{selectedBranch.impact}</p>
                </div>
                <motion.button
                  className="w-full py-2 rounded-xl text-xs font-semibold"
                  style={{ background: `${branchStyles[selectedBranch.type].color}20`, color: branchStyles[selectedBranch.type].color, border: `1px solid ${branchStyles[selectedBranch.type].border}` }}
                  whileHover={{ scale: 1.02 }}
                >
                  Simulate This Branch
                </motion.button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

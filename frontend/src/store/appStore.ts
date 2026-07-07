import { create } from 'zustand';

export type Page = 'dashboard' | 'brain' | 'twins' | 'simulation' | 'future' | 'analytics' | 'debate' | 'memory' | 'reports' | 'settings';

export type RiskLevel = 'healthy' | 'warning' | 'critical';

interface AppStore {
  // Navigation
  currentPage: Page;
  setCurrentPage: (page: Page) => void;

  // Stadium state
  crowdCount: number;
  setCrowdCount: (n: number) => void;

  riskLevel: RiskLevel;
  setRiskLevel: (r: RiskLevel) => void;

  matchMinute: number;
  setMatchMinute: (m: number) => void;

  timelineOffset: number;
  setTimelineOffset: (t: number) => void;

  // UI state
  commandBarOpen: boolean;
  setCommandBarOpen: (open: boolean) => void;

  selectedFanId: string | null;
  setSelectedFanId: (id: string | null) => void;

  isDemoRunning: boolean;
  setIsDemoRunning: (running: boolean) => void;

  // AI Brain state
  currentThought: string;
  setCurrentThought: (t: string) => void;

  currentPrediction: string;
  setCurrentPrediction: (p: string) => void;

  confidence: number;
  setConfidence: (c: number) => void;

  isThinking: boolean;
  setIsThinking: (t: boolean) => void;

  // Sidebar
  sidebarExpanded: boolean;
  setSidebarExpanded: (e: boolean) => void;
}

export const useAppStore = create<AppStore>((set) => ({
  currentPage: 'dashboard',
  setCurrentPage: (page) => set({ currentPage: page }),

  crowdCount: 87342,
  setCrowdCount: (n) => set({ crowdCount: n }),

  riskLevel: 'healthy',
  setRiskLevel: (r) => set({ riskLevel: r }),

  matchMinute: 67,
  setMatchMinute: (m) => set({ matchMinute: m }),

  timelineOffset: 0,
  setTimelineOffset: (t) => set({ timelineOffset: t }),

  commandBarOpen: false,
  setCommandBarOpen: (open) => set({ commandBarOpen: open }),

  selectedFanId: null,
  setSelectedFanId: (id) => set({ selectedFanId: id }),

  isDemoRunning: false,
  setIsDemoRunning: (running) => set({ isDemoRunning: running }),

  currentThought: 'I predict Gate B congestion in 8 minutes based on crowd flow patterns from 23 similar historical events.',
  setCurrentThought: (t) => set({ currentThought: t }),

  currentPrediction: 'Crowd density at North Stand will reach 94% capacity in 12 minutes.',
  setCurrentPrediction: (p) => set({ currentPrediction: p }),

  confidence: 94,
  setConfidence: (c) => set({ confidence: c }),

  isThinking: false,
  setIsThinking: (t) => set({ isThinking: t }),

  sidebarExpanded: false,
  setSidebarExpanded: (e) => set({ sidebarExpanded: e }),
}));

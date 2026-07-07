import { useEffect, useRef } from 'react';
import { useAppStore } from '../store/appStore';

const thoughts = [
  'I predict Gate B congestion in 8 minutes based on crowd flow patterns.',
  'Analyzing 87,342 fan positions in real-time. Detecting 3 anomalies.',
  'Weather radar shows 73% probability of rain in 15 minutes. Preparing contingency.',
  'Medical team at Zone C should be redeployed — no incidents in last 40 minutes.',
  'Transport congestion at Metro Station 2 detected. Redirecting 1,200 fans.',
  'Volunteer allocation optimal at 94% efficiency. No action required.',
  'Historical match data: similar crowd patterns led to Gate A overload 3 times.',
  'Energy consumption trending 12% above baseline. Recommend lighting adjustment.',
  'Fan sentiment analysis: 89% positive. Excitement spike detected at 67th minute.',
  'Security perimeter intact. All 48 access points operating normally.',
];

export const useLiveData = () => {
  const store = useAppStore;

  useEffect(() => {
    const interval = setInterval(() => {
      const state = store.getState();

      // Tick match minute
      if (state.matchMinute < 90) {
        state.setMatchMinute(state.matchMinute + 1);
      }

      // Fluctuate crowd
      state.setCrowdCount(87342 + Math.floor((Math.random() - 0.5) * 300));

      // Change thought occasionally
      if (Math.random() < 0.2) {
        state.setCurrentThought(thoughts[Math.floor(Math.random() * thoughts.length)]);
        state.setConfidence(Math.floor(Math.random() * 15) + 82);
      }

      // Risk level
      const rand = Math.random();
      if (rand < 0.04) state.setRiskLevel('critical');
      else if (rand < 0.18) state.setRiskLevel('warning');
      else state.setRiskLevel('healthy');
    }, 3000);

    return () => clearInterval(interval);
  }, []);
};

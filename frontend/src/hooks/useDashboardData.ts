/**
 * Polls /api/stadium/dashboard every 5 s and syncs into Zustand store.
 * Falls back gracefully if backend is offline (simulated data stays active).
 */
import { useEffect, useRef } from 'react';
import { api } from '../services/api';
import { useAppStore } from '../store/appStore';

export const useDashboardData = () => {
  const {
    setCrowdCount, setRiskLevel, setCurrentThought,
    setConfidence, setCurrentPrediction,
  } = useAppStore();

  const failCount = useRef(0);

  const fetchDash = async () => {
    try {
      const data = await api.dashboard();
      failCount.current = 0;

      if (data.crowd?.total_fans) setCrowdCount(data.crowd.total_fans);
      if (data.crowd?.risk_level) {
        setRiskLevel(data.crowd.risk_level as 'healthy' | 'warning' | 'critical');
      }
      if (data.recent_decisions?.length) {
        const latest = data.recent_decisions[0];
        setCurrentThought(latest.decision);
        setConfidence(Math.round(latest.confidence * 100));
        if (data.crowd?.gate_densities?.B) {
          const gB = data.crowd.gate_densities.B;
          setCurrentPrediction(
            `Gate B density at ${gB.toFixed(0)}%. ${gB > 90 ? 'Critical — action required.' : gB > 75 ? 'Monitor closely.' : 'Nominal.'}`
          );
        }
      }
    } catch {
      failCount.current += 1;
      if (failCount.current === 1) {
        console.info('[StadiumOS] Backend offline — running on simulated data');
      }
    }
  };

  useEffect(() => {
    fetchDash();
    const iv = setInterval(fetchDash, 5000);
    return () => clearInterval(iv);
  }, []);
};

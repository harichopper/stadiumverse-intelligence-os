import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import type { ECharts, EChartsOption } from 'echarts';
import { api, CrowdSnap, AIDecisionData } from '../../services/api';

const EChart: React.FC<{ option: EChartsOption; style?: React.CSSProperties }> = ({ option, style }) => {
  const ref = useRef<HTMLDivElement>(null);
  const chartRef = useRef<ECharts | null>(null);

  useEffect(() => {
    let mounted = true;
    import('echarts').then(ec => {
      if (!mounted || !ref.current) return;
      if (!chartRef.current) chartRef.current = ec.init(ref.current, 'dark');
      chartRef.current?.setOption(option, true);
    });
    return () => { mounted = false; };
  }, [option]);

  useEffect(() => {
    const obs = new ResizeObserver(() => chartRef.current?.resize());
    if (ref.current) obs.observe(ref.current);
    return () => obs.disconnect();
  }, []);

  return <div ref={ref} style={{ width: '100%', height: '100%', ...style }} />;
};

export const AnalyticsPage: React.FC = () => {
  const [snapshots, setSnapshots] = useState<CrowdSnap[]>([]);
  const [decisions, setDecisions] = useState<AIDecisionData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.crowdHistory(90), api.decisions(20)])
      .then(([histRes, decRes]) => {
        setSnapshots(histRes.snapshots);
        setDecisions(decRes.decisions);
        setLoading(false);
      })
      .catch(() => setLoading(false));
    const iv = setInterval(() => {
      api.crowdHistory(90).then(r => setSnapshots(r.snapshots)).catch(() => {});
    }, 10000);
    return () => clearInterval(iv);
  }, []);

  // crowd over time
  const crowdOption = {
    backgroundColor: 'transparent',
    grid: { left: 48, right: 16, top: 16, bottom: 36 },
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(5,8,22,.9)', borderColor: '#3B82F6', textStyle: { color: '#F8FAFC', fontSize: 11 } },
    xAxis: {
      type: 'category',
      data: snapshots.map(s => new Date(s.timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })),
      axisLabel: { color: '#475569', fontSize: 9, interval: Math.max(1, Math.floor(snapshots.length / 8)) },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,.1)' } },
      splitLine: { show: false },
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#475569', fontSize: 9, formatter: (v: number) => (v / 1000).toFixed(0) + 'K' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,.04)' } },
    },
    series: [{
      type: 'line', data: snapshots.map(s => s.total_fans), smooth: true, symbol: 'none',
      lineStyle: { color: '#3B82F6', width: 2 },
      areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(59,130,246,.3)' }, { offset: 1, color: 'rgba(59,130,246,.02)' }] } },
    }],
  };

  // gate densities
  const latestSnap = snapshots[snapshots.length - 1];
  const gateOption = {
    backgroundColor: 'transparent',
    grid: { left: 48, right: 16, top: 16, bottom: 36 },
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(5,8,22,.9)', borderColor: '#3B82F6', textStyle: { color: '#F8FAFC', fontSize: 11 } },
    xAxis: {
      type: 'value', max: 100,
      axisLabel: { color: '#475569', fontSize: 9, formatter: (v: number) => v + '%' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,.04)' } },
    },
    yAxis: {
      type: 'category', data: ['Gate D', 'Gate C', 'Gate A', 'Gate B'],
      axisLabel: { color: '#94A3B8', fontSize: 10 }, axisLine: { show: false },
    },
    series: [{
      type: 'bar', barMaxWidth: 18,
      data: latestSnap ? [
        { value: latestSnap.gate_densities.D, itemStyle: { color: '#3B82F6', borderRadius: [0,4,4,0] } },
        { value: latestSnap.gate_densities.C, itemStyle: { color: '#10B981', borderRadius: [0,4,4,0] } },
        { value: latestSnap.gate_densities.A, itemStyle: { color: '#F59E0B', borderRadius: [0,4,4,0] } },
        { value: latestSnap.gate_densities.B, itemStyle: { color: latestSnap.gate_densities.B > 85 ? '#EF4444' : '#F59E0B', borderRadius: [0,4,4,0] } },
      ] : [],
    }],
  };

  // stress over time
  const stressOption = {
    backgroundColor: 'transparent',
    grid: { left: 40, right: 16, top: 16, bottom: 36 },
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(5,8,22,.9)', borderColor: '#8B5CF6', textStyle: { color: '#F8FAFC', fontSize: 11 } },
    xAxis: {
      type: 'category',
      data: snapshots.map(s => new Date(s.timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })),
      axisLabel: { color: '#475569', fontSize: 9, interval: Math.max(1, Math.floor(snapshots.length / 8)) },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,.1)' } }, splitLine: { show: false },
    },
    yAxis: { type: 'value', max: 100, axisLabel: { color: '#475569', fontSize: 9, formatter: (v: number) => v + '%' }, splitLine: { lineStyle: { color: 'rgba(255,255,255,.04)' } } },
    series: [
      {
        name: 'Stress', type: 'line', data: snapshots.map(s => s.avg_stress.toFixed(1)), smooth: true, symbol: 'none',
        lineStyle: { color: '#EF4444', width: 1.5 },
        areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(239,68,68,.25)' }, { offset: 1, color: 'transparent' }] } },
      },
      {
        name: 'Excitement', type: 'line', data: snapshots.map(s => s.avg_excitement.toFixed(1)), smooth: true, symbol: 'none',
        lineStyle: { color: '#3B82F6', width: 1.5 },
      },
    ],
    legend: { data: ['Stress', 'Excitement'], textStyle: { color: '#94A3B8', fontSize: 10 }, bottom: 0 },
  };

  // AI decisions confidence
  const decisionOption = {
    backgroundColor: 'transparent',
    grid: { left: 48, right: 16, top: 16, bottom: 36 },
    tooltip: {
      trigger: 'axis', backgroundColor: 'rgba(5,8,22,.9)', borderColor: '#10B981',
      textStyle: { color: '#F8FAFC', fontSize: 11 },
      formatter: (params: { dataIndex: number }[]) => {
        const p = params[0];
        if (!p || typeof p.dataIndex !== 'number') return '';
        const d = decisions[p.dataIndex];
        return d ? `${d.agent}: ${d.decision.slice(0, 40)}...` : '';
      },
    },
    xAxis: {
      type: 'category',
      data: decisions.slice().reverse().map(d => `${d.match_minute}'`),
      axisLabel: { color: '#475569', fontSize: 9 },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,.1)' } }, splitLine: { show: false },
    },
    yAxis: { type: 'value', min: 0, max: 1, axisLabel: { color: '#475569', fontSize: 9, formatter: (v: number) => (v * 100).toFixed(0) + '%' }, splitLine: { lineStyle: { color: 'rgba(255,255,255,.04)' } } },
    series: [{
      type: 'bar', barMaxWidth: 20,
      data: decisions.slice().reverse().map(d => ({
        value: d.confidence,
        itemStyle: { color: d.outcome === 'SUCCESS' ? '#10B981' : d.outcome === 'PARTIAL' ? '#F59E0B' : '#EF4444', borderRadius: [4, 4, 0, 0] },
      })),
    }],
  };

  const cardStyle = { background: 'rgba(255,255,255,.03)', border: '1px solid rgba(255,255,255,.06)', borderRadius: 14, padding: 14 };

  return (
    <div style={{ height: '100%', overflowY: 'auto', padding: 12 }}>
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
        style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 12 }}>
        <div style={{ width: 32, height: 32, borderRadius: 10, background: 'rgba(59,130,246,.15)', border: '1px solid rgba(59,130,246,.3)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 16 }}>📊</div>
        <div>
          <div style={{ fontSize: 18, fontWeight: 300, color: '#F8FAFC' }}>Analytics</div>
          <div style={{ fontSize: 10, color: '#64748B' }}>
            {loading ? 'Loading from database...' : `${snapshots.length} crowd snapshots · ${decisions.length} AI decisions · SQLite`}
          </div>
        </div>
        <motion.div animate={{ opacity: [1, .5, 1] }} transition={{ duration: 2, repeat: Infinity }}
          style={{ marginLeft: 'auto', fontSize: 9, color: '#10B981', display: 'flex', alignItems: 'center', gap: 4 }}>
          <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#10B981', display: 'inline-block' }} />
          DB LIVE
        </motion.div>
      </motion.div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>

        {/* Crowd over time — full width */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: .1 }}
          style={{ ...cardStyle, gridColumn: '1/-1', height: 200 }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: '#F8FAFC', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 6 }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#3B82F6', display: 'inline-block' }} />
            Crowd Flow — Match Duration ({snapshots.length} data points)
          </div>
          <div style={{ height: 160 }}><EChart option={crowdOption} /></div>
        </motion.div>

        {/* Gate density */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: .2 }}
          style={{ ...cardStyle, height: 200 }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: '#F8FAFC', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 6 }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#EF4444', display: 'inline-block' }} />
            Live Gate Density
          </div>
          <div style={{ height: 160 }}><EChart option={gateOption} /></div>
        </motion.div>

        {/* Stress / excitement */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: .3 }}
          style={{ ...cardStyle, height: 200 }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: '#F8FAFC', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 6 }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#8B5CF6', display: 'inline-block' }} />
            Crowd Emotion Trends
          </div>
          <div style={{ height: 160 }}><EChart option={stressOption} /></div>
        </motion.div>

        {/* AI decision confidence */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: .4 }}
          style={{ ...cardStyle, height: 200 }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: '#F8FAFC', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 6 }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#10B981', display: 'inline-block' }} />
            AI Decisions — Confidence by Minute
          </div>
          <div style={{ height: 160 }}><EChart option={decisionOption} /></div>
        </motion.div>

        {/* Decisions table — full width */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: .5 }}
          style={{ ...cardStyle, gridColumn: '1/-1' }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: '#F8FAFC', marginBottom: 10, display: 'flex', alignItems: 'center', gap: 6 }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#F59E0B', display: 'inline-block' }} />
            AI Decision Log (Black Box)
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            {decisions.slice(0, 8).map((d, i) => (
              <motion.div key={d.id} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: .5 + i * .05 }}
                style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '7px 10px', background: 'rgba(255,255,255,.02)', border: '1px solid rgba(255,255,255,.04)', borderRadius: 8 }}>
                <span style={{ fontFamily: 'monospace', fontSize: 10, color: '#475569', width: 28, flexShrink: 0 }}>{d.match_minute}'</span>
                <span style={{ fontSize: 10, color: '#94A3B8', width: 80, flexShrink: 0 }}>{d.agent}</span>
                <span style={{ flex: 1, fontSize: 11, color: '#CBD5E1' }}>{d.decision}</span>
                <span style={{ fontSize: 10, color: '#64748B', width: 36, textAlign: 'right' }}>{Math.round(d.confidence * 100)}%</span>
                <span style={{ fontSize: 9, fontWeight: 700, padding: '2px 7px', borderRadius: 999, flexShrink: 0,
                  background: d.outcome === 'SUCCESS' ? 'rgba(16,185,129,.15)' : d.outcome === 'PARTIAL' ? 'rgba(245,158,11,.15)' : 'rgba(100,116,139,.15)',
                  color: d.outcome === 'SUCCESS' ? '#10B981' : d.outcome === 'PARTIAL' ? '#F59E0B' : '#94A3B8' }}>
                  {d.outcome}
                </span>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Latest stats cards */}
        {latestSnap && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: .6 }}
            style={{ ...cardStyle, gridColumn: '1/-1' }}>
            <div style={{ fontSize: 11, fontWeight: 600, color: '#F8FAFC', marginBottom: 10 }}>⚡ Collective Intelligence — Current State</div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 8 }}>
              {[
                { label: 'Total Fans', value: latestSnap.total_fans.toLocaleString(), color: '#3B82F6' },
                { label: 'Avg Queue', value: `${latestSnap.queue_avg_min.toFixed(1)} min`, color: '#F59E0B' },
                { label: 'Gate B Density', value: `${latestSnap.gate_densities.B?.toFixed(0)}%`, color: latestSnap.gate_densities.B > 85 ? '#EF4444' : '#10B981' },
                { label: 'Weather', value: `${latestSnap.weather.temp.toFixed(1)}°C · ${latestSnap.weather.rain_pct.toFixed(0)}% rain`, color: '#06B6D4' },
              ].map(item => (
                <div key={item.label} style={{ background: `${item.color}08`, border: `1px solid ${item.color}20`, borderRadius: 10, padding: '10px 12px', textAlign: 'center' }}>
                  <div style={{ fontSize: 16, fontWeight: 700, color: item.color }}>{item.value}</div>
                  <div style={{ fontSize: 9, color: '#64748B', marginTop: 3, textTransform: 'uppercase', letterSpacing: '.06em' }}>{item.label}</div>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

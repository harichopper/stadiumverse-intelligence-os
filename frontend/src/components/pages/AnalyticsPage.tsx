import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { BarChart3 } from 'lucide-react';

// ECharts dynamic import
let echarts: any = null;

const EChart: React.FC<{ option: any; style?: React.CSSProperties }> = ({ option, style }) => {
  const ref = useRef<HTMLDivElement>(null);
  const chartRef = useRef<any>(null);

  useEffect(() => {
    let mounted = true;
    import('echarts').then((ec) => {
      if (!mounted || !ref.current) return;
      echarts = ec;
      if (!chartRef.current) {
        chartRef.current = ec.init(ref.current, 'dark');
      }
      chartRef.current.setOption(option);
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
  const [minute, setMinute] = useState(67);

  useEffect(() => {
    const t = setInterval(() => setMinute(m => m < 90 ? m + 1 : 90), 5000);
    return () => clearInterval(t);
  }, []);

  const crowdData = Array.from({ length: minute }, (_, i) => ({
    min: i + 1,
    crowd: 50000 + Math.round(37342 * (1 - Math.exp(-(i + 1) / 20)) + (Math.random() - 0.5) * 2000),
  }));

  const crowdOption = {
    backgroundColor: 'transparent',
    grid: { left: 40, right: 20, top: 20, bottom: 40 },
    xAxis: {
      type: 'category',
      data: crowdData.map(d => d.min + "'"),
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      axisLabel: { color: '#475569', fontSize: 9 },
      splitLine: { show: false },
    },
    yAxis: {
      type: 'value',
      min: 40000,
      axisLine: { show: false },
      axisLabel: { color: '#475569', fontSize: 9, formatter: (v: number) => (v / 1000).toFixed(0) + 'K' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.04)' } },
    },
    series: [{
      type: 'line',
      data: crowdData.map(d => d.crowd),
      smooth: true,
      symbol: 'none',
      lineStyle: { color: '#3B82F6', width: 2 },
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [{ offset: 0, color: 'rgba(59,130,246,0.3)' }, { offset: 1, color: 'rgba(59,130,246,0.0)' }],
        },
      },
    }],
    animation: true,
    animationDuration: 800,
  };

  const gateOption = {
    backgroundColor: 'transparent',
    grid: { left: 50, right: 20, top: 20, bottom: 40 },
    xAxis: {
      type: 'value',
      axisLabel: { color: '#475569', fontSize: 9, formatter: (v: number) => v + '/hr' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.04)' } },
    },
    yAxis: {
      type: 'category',
      data: ['Gate A', 'Gate B', 'Gate C', 'Gate D', 'VIP', 'Press'],
      axisLabel: { color: '#94A3B8', fontSize: 10 },
      axisLine: { show: false },
    },
    series: [{
      type: 'bar',
      data: [1800, 2400, 1200, 900, 600, 300].map((v, i) => ({
        value: v,
        itemStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 1, y2: 0,
            colorStops: [
              { offset: 0, color: i === 1 ? 'rgba(239,68,68,0.8)' : 'rgba(59,130,246,0.8)' },
              { offset: 1, color: i === 1 ? '#EF4444' : '#3B82F6' },
            ],
          },
          borderRadius: [0, 4, 4, 0],
        },
      })),
      barMaxWidth: 16,
    }],
    animation: true,
  };

  const heatOption = {
    backgroundColor: 'transparent',
    grid: { left: 40, right: 20, top: 20, bottom: 40 },
    xAxis: {
      type: 'category',
      data: ['N-Stand', 'S-Stand', 'E-Stand', 'W-Stand', 'VIP'],
      axisLabel: { color: '#475569', fontSize: 9 },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      splitLine: { show: false },
    },
    yAxis: {
      type: 'value',
      max: 100,
      axisLabel: { color: '#475569', fontSize: 9, formatter: (v: number) => v + '%' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.04)' } },
    },
    series: [{
      type: 'bar',
      data: [94, 87, 72, 68, 45].map((v, i) => ({
        value: v,
        itemStyle: {
          color: v > 90 ? '#EF4444' : v > 80 ? '#F59E0B' : '#10B981',
          borderRadius: [4, 4, 0, 0],
        },
      })),
      barMaxWidth: 40,
    }],
    animation: true,
  };

  const sentimentOption = {
    backgroundColor: 'transparent',
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: [
        { value: 89, name: 'Positive', itemStyle: { color: '#10B981' } },
        { value: 7, name: 'Neutral', itemStyle: { color: '#64748B' } },
        { value: 4, name: 'Negative', itemStyle: { color: '#EF4444' } },
      ],
      label: { color: '#94A3B8', fontSize: 10 },
      labelLine: { lineStyle: { color: '#475569' } },
    }],
    animation: true,
  };

  return (
    <div className="h-full overflow-y-auto p-4">
      <motion.div className="flex items-center gap-3 mb-4" initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <div className="w-10 h-10 rounded-2xl flex items-center justify-center" style={{ background: 'rgba(59,130,246,0.15)', border: '1px solid rgba(59,130,246,0.3)' }}>
          <BarChart3 size={18} style={{ color: '#3B82F6' }} />
        </div>
        <div>
          <h1 className="text-2xl font-light" style={{ color: '#F8FAFC', letterSpacing: '-0.02em' }}>Analytics</h1>
          <p className="text-xs" style={{ color: '#64748B' }}>Real-time stadium intelligence · All data streams active</p>
        </div>
      </motion.div>

      <div className="grid grid-cols-2 gap-4">
        {/* Crowd over time */}
        <motion.div
          className="rounded-2xl p-4 col-span-2"
          style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)', height: 220 }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.1 }}
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-blue-400" />
              <span className="text-xs font-semibold" style={{ color: '#F8FAFC' }}>Crowd Flow Over Time</span>
            </div>
            <span className="text-[10px]" style={{ color: '#64748B' }}>Match minute 1–{minute}</span>
          </div>
          <div style={{ height: 150 }}>
            <EChart option={crowdOption} />
          </div>
        </motion.div>

        {/* Gate throughput */}
        <motion.div
          className="rounded-2xl p-4"
          style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)', height: 220 }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="flex items-center gap-2 mb-3">
            <div className="w-2 h-2 rounded-full bg-red-400" />
            <span className="text-xs font-semibold" style={{ color: '#F8FAFC' }}>Gate Throughput</span>
          </div>
          <div style={{ height: 150 }}>
            <EChart option={gateOption} />
          </div>
        </motion.div>

        {/* Stand density */}
        <motion.div
          className="rounded-2xl p-4"
          style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)', height: 220 }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <div className="flex items-center gap-2 mb-3">
            <div className="w-2 h-2 rounded-full bg-yellow-400" />
            <span className="text-xs font-semibold" style={{ color: '#F8FAFC' }}>Stand Occupancy</span>
          </div>
          <div style={{ height: 150 }}>
            <EChart option={heatOption} />
          </div>
        </motion.div>

        {/* Sentiment */}
        <motion.div
          className="rounded-2xl p-4"
          style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)', height: 220 }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <div className="flex items-center gap-2 mb-3">
            <div className="w-2 h-2 rounded-full bg-green-400" />
            <span className="text-xs font-semibold" style={{ color: '#F8FAFC' }}>Fan Sentiment</span>
          </div>
          <div style={{ height: 150 }}>
            <EChart option={sentimentOption} />
          </div>
        </motion.div>

        {/* Collective Intelligence cards */}
        <motion.div
          className="rounded-2xl p-4 col-span-1"
          style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(16,185,129,0.15)' }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <div className="flex items-center gap-2 mb-3">
            <div className="w-2 h-2 rounded-full bg-green-400" />
            <span className="text-xs font-semibold" style={{ color: '#F8FAFC' }}>Collective Intelligence</span>
          </div>
          <div className="space-y-2">
            {[
              { label: 'Smallest Intervention', value: 'Deploy 3 volunteers', icon: '⚡', color: '#10B981' },
              { label: 'Expected Impact', value: '-23% congestion', icon: '📊', color: '#3B82F6' },
              { label: 'ROI', value: '4.2x safety improvement', icon: '💰', color: '#F59E0B' },
              { label: 'Affected Fans', value: '~1,400 fans', icon: '👥', color: '#8B5CF6' },
            ].map((item) => (
              <div key={item.label} className="flex items-center justify-between py-2 px-3 rounded-xl" style={{ background: 'rgba(255,255,255,0.03)' }}>
                <div className="flex items-center gap-2">
                  <span>{item.icon}</span>
                  <span className="text-[10px]" style={{ color: '#94A3B8' }}>{item.label}</span>
                </div>
                <span className="text-[11px] font-semibold" style={{ color: item.color }}>{item.value}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

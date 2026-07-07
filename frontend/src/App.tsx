import React, { useState, useEffect, useRef } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { TopBar } from './components/layout/TopBar';
import { Sidebar } from './components/layout/Sidebar';
import { Dashboard } from './components/layout/Dashboard';
import { Timeline } from './components/timeline/Timeline';
import { CommandBar } from './components/command/CommandBar';
import { AIBrainPage } from './components/pages/AIBrainPage';
import { FuturePage } from './components/pages/FuturePage';
import { AnalyticsPage } from './components/pages/AnalyticsPage';
import { DigitalTwinsPage } from './components/pages/DigitalTwinsPage';
import { PlaceholderPage } from './components/pages/PlaceholderPage';
import { PageBoundary } from './components/common/PageBoundary';
import { useAppStore } from './store/appStore';
import { useLiveData } from './hooks/useLiveData';
import { useDashboardData } from './hooks/useDashboardData';

/* ─────────────────────────────────────────────────────────────
   BACKGROUND CANVAS
───────────────────────────────────────────────────────────── */
const Background: React.FC = () => {
  const ref = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const c = ref.current; if (!c) return;
    const ctx = c.getContext('2d')!;
    let raf = 0;
    const resize = () => { c.width = innerWidth; c.height = innerHeight; };
    resize(); window.addEventListener('resize', resize);
    const COLS = ['#3B82F6','#8B5CF6','#06B6D4','#10B981'];
    const dots = Array.from({length:60}, () => ({
      x: Math.random()*innerWidth, y: Math.random()*innerHeight,
      vx:(Math.random()-.5)*.3, vy:(Math.random()-.5)*.3,
      r:Math.random()*1.5+.3, a:Math.random()*.4+.1,
      c:COLS[Math.floor(Math.random()*4)]
    }));
    const tick = () => {
      const W=c.width, H=c.height; ctx.clearRect(0,0,W,H); t+=.003;
      // orbs
      [[W*.2,H*.3,250,'rgba(59,130,246,.07)'],[W*.8,H*.6,290,'rgba(139,92,246,.05)']].forEach(([bx,by,br,bc])=>{
        const g=ctx.createRadialGradient(bx as number,by as number,0,bx as number,by as number,br as number);
        g.addColorStop(0,bc as string); g.addColorStop(1,'transparent');
        ctx.fillStyle=g; ctx.beginPath(); ctx.arc(bx as number,by as number,br as number,0,Math.PI*2); ctx.fill();
      });
      // grid
      ctx.strokeStyle='rgba(59,130,246,.02)'; ctx.lineWidth=1;
      for(let x=0;x<W;x+=50){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}
      for(let y=0;y<H;y+=50){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
      // particles
      dots.forEach((p,i)=>{
        p.x+=p.vx; p.y+=p.vy;
        if(p.x<0)p.x=W; if(p.x>W)p.x=0; if(p.y<0)p.y=H; if(p.y>H)p.y=0;
        for(let j=i+1;j<dots.length;j++){
          const dx=dots[j].x-p.x,dy=dots[j].y-p.y,d=Math.hypot(dx,dy);
          if(d<100){ctx.strokeStyle=`rgba(59,130,246,${.06*(1-d/100)})`;ctx.lineWidth=.5;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(dots[j].x,dots[j].y);ctx.stroke();}
        }
        ctx.globalAlpha=p.a; ctx.fillStyle=p.c; ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill(); ctx.globalAlpha=1;
      });
      raf=requestAnimationFrame(tick);
    };
    tick();
    return () => { cancelAnimationFrame(raf); window.removeEventListener('resize',resize); };
  }, []);
  return <canvas ref={ref} style={{position:'fixed',inset:0,zIndex:0,pointerEvents:'none'}} />;
};

/* ─────────────────────────────────────────────────────────────
   BOOT SCREEN  – simple timed, no complex state machine
───────────────────────────────────────────────────────────── */
const STEPS = [
  'Initializing StadiumVerse Intelligence OS...',
  'Loading Stadium Memory...',
  'Connecting Digital Twins...',
  'Loading 13 AI Agents...',
  'Synchronizing Collective Intelligence...',
  'Predicting Future...',
  '🧠  Living Brain Online.',
];

const BootScreen: React.FC<{ onDone: () => void }> = ({ onDone }) => {
  const [idx, setIdx] = useState(0);
  const [gone, setGone] = useState(false);
  const cbRef = useRef(onDone);
  cbRef.current = onDone;

  // drive idx 0→N with setInterval, then exit
  useEffect(() => {
    // Show steps one per 450ms
    const iv = setInterval(() => {
      setIdx(prev => {
        const next = prev + 1;
        if (next >= STEPS.length) {
          clearInterval(iv);
          // after last step shown, wait 600ms then fade+call onDone
          setTimeout(() => {
            setGone(true);
            setTimeout(() => cbRef.current(), 550);
          }, 600);
        }
        return next;
      });
    }, 450);
    return () => clearInterval(iv);
  }, []);

  const pct = Math.min(100, Math.round((idx / (STEPS.length - 1)) * 100));

  return (
    <div style={{
      position:'fixed',inset:0,zIndex:9999,background:'#050816',
      display:'flex',alignItems:'center',justifyContent:'center',
      transition:'opacity .55s ease', opacity: gone ? 0 : 1,
      pointerEvents: gone ? 'none' : 'all',
    }}>
      {/* grid bg */}
      <div style={{position:'absolute',inset:0,pointerEvents:'none',opacity:.12,
        backgroundImage:'linear-gradient(rgba(59,130,246,.18) 1px,transparent 1px),linear-gradient(90deg,rgba(59,130,246,.18) 1px,transparent 1px)',
        backgroundSize:'55px 55px'}} />
      {/* glow */}
      <div style={{position:'absolute',inset:0,pointerEvents:'none',
        background:'radial-gradient(ellipse at 50% 50%,rgba(59,130,246,.12) 0%,transparent 60%)'}} />
      {/* scan */}
      <motion.div style={{position:'absolute',left:0,right:0,height:1,background:'linear-gradient(90deg,transparent,rgba(59,130,246,.8),transparent)',pointerEvents:'none'}}
        animate={{top:['0%','100%']}} transition={{duration:2.4,repeat:Infinity,ease:'linear'}} />

      <div style={{position:'relative',zIndex:1,width:'100%',maxWidth:500,padding:'0 32px',
        display:'flex',flexDirection:'column',alignItems:'center',gap:32}}>

        {/* Brain SVG */}
        <div style={{display:'flex',flexDirection:'column',alignItems:'center',gap:12}}>
          <div style={{position:'relative',width:90,height:90}}>
            <motion.div animate={{scale:[1,1.7,1]}} transition={{duration:2.2,repeat:Infinity}}
              style={{position:'absolute',inset:0,borderRadius:'50%',
                background:'radial-gradient(circle,rgba(59,130,246,.35) 0%,transparent 70%)'}} />
            <svg width="90" height="90" viewBox="0 0 90 90" fill="none" style={{position:'relative',zIndex:1}}>
              <circle cx="45" cy="45" r="40" fill="rgba(59,130,246,.1)" stroke="rgba(59,130,246,.3)" strokeWidth="1"/>
              {/* brain nodes */}
              {[[30,30],[45,22],[60,30],[22,45],[45,38],[68,45],[30,60],[45,55],[60,60]].map(([cx,cy],i)=>(
                <motion.circle key={i} cx={cx} cy={cy} r="4" fill="#3B82F6"
                  initial={{opacity:0}} animate={{opacity:[0,.9,.7]}}
                  transition={{delay:.3+i*.12,duration:.4,repeat:Infinity,repeatDelay:2}} />
              ))}
              {/* edges */}
              {[[30,30,45,22],[45,22,60,30],[30,30,22,45],[60,30,68,45],[22,45,45,38],[45,38,68,45],[22,45,30,60],[68,45,60,60],[30,60,45,55],[45,55,60,60],[45,38,45,22],[45,38,45,55]].map(([x1,y1,x2,y2],i)=>(
                <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="rgba(59,130,246,.3)" strokeWidth=".8"/>
              ))}
            </svg>
          </div>
          <div style={{textAlign:'center',fontFamily:'Inter,sans-serif'}}>
            <div style={{fontSize:22,fontWeight:200,letterSpacing:'.2em',color:'#F8FAFC',textTransform:'uppercase'}}>
              StadiumVerse
            </div>
            <div style={{fontSize:10,letterSpacing:'.4em',color:'#3B82F6',textTransform:'uppercase',marginTop:3}}>
              INTELLIGENCE OS
            </div>
            <div style={{fontSize:9,color:'#475569',marginTop:5}}>⚽ FIFA WORLD CUP 2026 · COMMAND CENTER</div>
          </div>
        </div>

        {/* Steps */}
        <div style={{width:'100%',display:'flex',flexDirection:'column',gap:7,fontFamily:'monospace'}}>
          {STEPS.slice(0, idx + 1).map((text, i) => {
            const isLast = i === STEPS.length - 1;
            const isCurrent = i === idx;
            return (
              <motion.div key={i} initial={{opacity:0,x:-8}} animate={{opacity:1,x:0}} transition={{duration:.25}}
                style={{display:'flex',alignItems:'center',gap:9}}>
                <span style={{fontSize:10,color:isLast?'#10B981':'#3B82F6',flexShrink:0}}>{isLast?'●':'✓'}</span>
                <span style={{fontSize:12,color:isLast?'#10B981':isCurrent?'#E2E8F0':'#64748B',
                  fontWeight:isLast||isCurrent?500:400}}>
                  {text}
                </span>
                {isCurrent && !isLast && (
                  <span style={{display:'flex',gap:3}}>
                    {[0,1,2].map(d=>(
                      <motion.span key={d} style={{width:3,height:3,borderRadius:'50%',background:'#3B82F6',display:'inline-block'}}
                        animate={{opacity:[0,1,0]}} transition={{duration:.7,repeat:Infinity,delay:d*.16}} />
                    ))}
                  </span>
                )}
              </motion.div>
            );
          })}
        </div>

        {/* Progress */}
        <div style={{width:'100%'}}>
          <div style={{display:'flex',justifyContent:'space-between',marginBottom:6}}>
            <span style={{fontSize:10,color:'#475569',letterSpacing:'.08em',textTransform:'uppercase'}}>Boot Sequence</span>
            <span style={{fontSize:10,color:'#3B82F6',fontFamily:'monospace'}}>{pct}%</span>
          </div>
          <div style={{width:'100%',height:2,background:'rgba(255,255,255,.07)',borderRadius:2}}>
            <motion.div style={{height:'100%',borderRadius:2,background:'linear-gradient(90deg,#3B82F6,#8B5CF6,#06B6D4)'}}
              animate={{width:`${pct}%`}} transition={{duration:.3}} />
          </div>
        </div>

      </div>
    </div>
  );
};

/* ─────────────────────────────────────────────────────────────
   PAGE ROUTER
───────────────────────────────────────────────────────────── */
const PageRenderer: React.FC = () => {
  const { currentPage } = useAppStore();
  const map: Record<string,React.ReactNode> = {
    dashboard:  <PageBoundary name="Dashboard"><Dashboard /></PageBoundary>,
    brain:      <PageBoundary name="AI Brain"><AIBrainPage /></PageBoundary>,
    twins:      <PageBoundary name="Digital Twins"><DigitalTwinsPage /></PageBoundary>,
    future:     <PageBoundary name="Future"><FuturePage /></PageBoundary>,
    analytics:  <PageBoundary name="Analytics"><AnalyticsPage /></PageBoundary>,
    simulation: <PlaceholderPage title="Simulation Engine"    icon="⚙️"  color="#10B981" description="AI crowd simulation across 156 probability branches." />,
    debate:     <PlaceholderPage title="AI Debate Chamber"    icon="🗣️"  color="#EF4444" description="13 AI agents debating in real-time for optimal decisions." />,
    memory:     <PlaceholderPage title="Memory Database"      icon="🗄️"  color="#8B5CF6" description="Every decision indexed for collective intelligence." />,
    reports:    <PlaceholderPage title="Intelligence Reports" icon="📋"  color="#06B6D4" description="Automated AI-generated stadium event reports." />,
    settings:   <PlaceholderPage title="System Configuration" icon="⚙️"  color="#64748B" description="Configure AI models, streams and alert thresholds." />,
  };
  return (
    <AnimatePresence mode="wait">
      <motion.div key={currentPage}
        style={{flex:1,overflow:'hidden',minWidth:0,minHeight:0,display:'flex',flexDirection:'column'}}
        initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}}
        transition={{duration:.2}}>
        {map[currentPage] ?? <Dashboard />}
      </motion.div>
    </AnimatePresence>
  );
};

/* ─────────────────────────────────────────────────────────────
   SHELL  (TopBar + Sidebar + Page + Timeline)
───────────────────────────────────────────────────────────── */
const Shell: React.FC = () => {
  useLiveData();
  useDashboardData();
  return (
    <div style={{position:'fixed',inset:0,zIndex:10,display:'flex',flexDirection:'column',overflow:'hidden'}}>
      {/* Skip-to-content link */}
      <a
        href="#main-content"
        style={{
          position: 'absolute',
          top: -40,
          left: 0,
          background: '#3B82F6',
          color: 'white',
          padding: '8px 16px',
          zIndex: 9999,
          transition: 'top 0.3s',
        }}
        onFocus={(e) => {
          e.currentTarget.style.top = '0';
        }}
        onBlur={(e) => {
          e.currentTarget.style.top = '-40px';
        }}
      >
        Skip to main content
      </a>
      <TopBar />
      <div style={{flex:1,display:'flex',overflow:'hidden',minHeight:0}}>
        <Sidebar />
        <main id="main-content" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <PageRenderer />
        </main>
      </div>
      <Timeline />
      <CommandBar />
    </div>
  );
};

/* ─────────────────────────────────────────────────────────────
   ROOT
───────────────────────────────────────────────────────────── */
export default function App() {
  const [booted, setBooted] = useState(false);
  return (
    <div style={{position:'fixed',inset:0,background:'#050816',overflow:'hidden'}}>
      <Background />
      <Shell />
      {!booted && <BootScreen onDone={() => setBooted(true)} />}
    </div>
  );
}

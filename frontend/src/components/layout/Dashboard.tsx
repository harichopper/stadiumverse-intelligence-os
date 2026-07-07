import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Users, AlertTriangle, Truck, Heart, Zap, Cloud, Activity, UserCheck, Play } from 'lucide-react';
import { useAppStore } from '../../store/appStore';

/* ── tiny sparkline ─────────────────────────────────────── */
const Spark: React.FC<{data:number[];color:string}> = ({data,color}) => {
  const W=56, H=22, max=Math.max(...data)||1, min=Math.min(...data);
  const range=max-min||1;
  const pts=data.map((v,i)=>`${(i/(data.length-1))*W},${H-((v-min)/range)*H}`).join(' ');
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} fill="none">
      <polyline points={pts} stroke={color} strokeWidth="1.5" fill="none" strokeLinecap="round"/>
    </svg>
  );
};

/* ── metric card ────────────────────────────────────────── */
interface CardProps { title:string; value:string|number; unit?:string; subtitle?:string; icon:React.ReactNode; color:string; status:'good'|'warn'|'bad'; spark:number[]; delay:number }
const Card: React.FC<CardProps> = ({title,value,unit,subtitle,icon,color,status,spark,delay}) => {
  const sc = status==='good'?'#10B981':status==='warn'?'#F59E0B':'#EF4444';
  return (
    <motion.div
      role="region"
      aria-label={`${title} Metric`}
      initial={{opacity:0,y:16}} animate={{opacity:1,y:0}} transition={{delay,duration:.4}}
      whileHover={{y:-3,boxShadow:`0 16px 40px rgba(0,0,0,.4),0 0 20px ${color}18`}}
      style={{background:'rgba(255,255,255,.04)',border:'1px solid rgba(255,255,255,.07)',borderRadius:14,padding:'12px',cursor:'default',position:'relative',overflow:'hidden'}}>
      {/* top accent */}
      <div style={{position:'absolute',top:0,left:0,right:0,height:1.5,background:`linear-gradient(90deg,transparent,${color}60,transparent)`}}/>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',marginBottom:8}}>
        <div style={{display:'flex',alignItems:'center',gap:6}}>
          <div style={{width:28,height:28,borderRadius:8,background:`${color}18`,display:'flex',alignItems:'center',justifyContent:'center',color}}>
            {icon}
          </div>
          <div>
            <div style={{fontSize:9,color:'#64748B',textTransform:'uppercase',letterSpacing:'.08em'}}>{title}</div>
            {subtitle && <div style={{fontSize:9,color:'#475569'}}>{subtitle}</div>}
          </div>
        </div>
        <Spark data={spark} color={color}/>
      </div>
      <div style={{display:'flex',alignItems:'flex-end',gap:3}}>
        <span style={{fontSize:22,fontWeight:600,color:'#F8FAFC',letterSpacing:'-.02em',fontVariantNumeric:'tabular-nums'}}>{typeof value==='number'?value.toLocaleString():value}</span>
        {unit && <span style={{fontSize:12,color:'#64748B',marginBottom:2}}>{unit}</span>}
      </div>
      <div style={{display:'flex',alignItems:'center',gap:5,marginTop:6}}>
        <motion.div style={{width:6,height:6,borderRadius:'50%',background:sc}} animate={{opacity:status==='bad'?[1,.3,1]:1}} transition={{duration:.7,repeat:Infinity}}/>
        <span style={{fontSize:9,color:sc}}>{status==='good'?'NOMINAL':status==='warn'?'MONITOR':'ALERT'}</span>
      </div>
    </motion.div>
  );
};

/* ── simple SVG stadium map ─────────────────────────────── */
const StadiumMap: React.FC = () => {
  const [dots, setDots] = useState(() =>
    Array.from({length:100},(_,i)=>({
      id:i, x:50+Math.cos(i/100*Math.PI*2)*35*(0.6+Math.random()*.4)+Math.random()*8-4,
      y:50+Math.sin(i/100*Math.PI*2)*25*(0.6+Math.random()*.4)+Math.random()*6-3,
      type: i<5?'medical':i<18?'volunteer':i<30?'security':'fan',
    }))
  );

  useEffect(()=>{
    const iv = setInterval(()=>{
      setDots(d=>d.map(p=>({...p,
        x:Math.max(5,Math.min(95,p.x+(Math.random()-.5)*1.2)),
        y:Math.max(5,Math.min(95,p.y+(Math.random()-.5)*.9)),
      })));
    },600);
    return ()=>clearInterval(iv);
  },[]);

  const colors:Record<string,string> = {fan:'#3B82F6',volunteer:'#10B981',medical:'#EF4444',security:'#F59E0B'};

  return (
    <section aria-label="Living Stadium Map" style={{width:'100%',height:'100%',display:'flex',flexDirection:'column'}}>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:8}}>
        <h2 style={{fontSize:11,fontWeight:600,color:'#F8FAFC',margin:0}}>Living Stadium</h2>
        <motion.span style={{fontSize:9,color:'#10B981',display:'flex',alignItems:'center',gap:4}}
          animate={{opacity:[1,.5,1]}} transition={{duration:2,repeat:Infinity}}
          aria-hidden="true">
          <span style={{width:6,height:6,borderRadius:'50%',background:'#10B981',display:'inline-block'}}/>LIVE
        </motion.span>
      </div>
      <div style={{flex:1,position:'relative',background:'rgba(5,8,22,.6)',border:'1px solid rgba(59,130,246,.15)',borderRadius:12,overflow:'hidden'}} aria-hidden="true">
        <svg viewBox="0 0 100 100" style={{width:'100%',height:'100%',position:'absolute',inset:0}}>
          {/* field */}
          <ellipse cx="50" cy="50" rx="22" ry="16" fill="rgba(16,185,129,.1)" stroke="rgba(16,185,129,.3)" strokeWidth=".5"/>
          <ellipse cx="50" cy="50" rx="6" ry="6" fill="none" stroke="rgba(16,185,129,.2)" strokeWidth=".3"/>
          <line x1="50" y1="34" x2="50" y2="66" stroke="rgba(16,185,129,.15)" strokeWidth=".3"/>
          {/* stands */}
          <ellipse cx="50" cy="50" rx="42" ry="30" fill="none" stroke="rgba(59,130,246,.12)" strokeWidth="6"/>
          {/* entrances */}
          {[[50,20],[50,80],[8,50],[92,50]].map(([ex,ey],i)=>(
            <g key={i}><circle cx={ex} cy={ey} r="2.5" fill="rgba(6,182,212,.6)"/>
            <circle cx={ex} cy={ey} r="4.5" fill="rgba(6,182,212,.1)"/></g>
          ))}
          {/* dots */}
          {dots.map(p=>(
            <motion.circle key={p.id} cx={p.x} cy={p.y} r={p.type==='fan'?1.2:2}
              fill={colors[p.type]}
              animate={{cx:p.x,cy:p.y}} transition={{duration:.5,ease:'easeInOut'}}
              style={{opacity:p.type==='fan'?.65:1}}/>
          ))}
        </svg>
        {/* legend */}
        <div style={{position:'absolute',bottom:8,left:8,display:'flex',gap:8}}>
          {Object.entries(colors).map(([type,color])=>(
            <div key={type} style={{display:'flex',alignItems:'center',gap:3}}>
              <div style={{width:6,height:6,borderRadius:'50%',background:color}}/>
              <span style={{fontSize:8,color:'#64748B',textTransform:'capitalize'}}>{type}</span>
            </div>
          ))}
        </div>
        {/* POI labels */}
        <div style={{position:'absolute',top:6,right:6,display:'flex',flexDirection:'column',gap:3}}>
          {['✈️ Airport','🚇 Metro','🅿️ Parking'].map(l=>(
            <div key={l} style={{fontSize:8,color:'#475569',background:'rgba(5,8,22,.7)',padding:'1px 5px',borderRadius:4}}>{l}</div>
          ))}
        </div>
      </div>
      {/* heatmap legend */}
      <div style={{display:'flex',gap:12,marginTop:6,justifyContent:'center'}} aria-label="Gate Congestion Heatmap">
        {[['Gate A','#10B981','72%'],['Gate B','#EF4444','94%'],['Gate C','#F59E0B','81%'],['Gate D','#3B82F6','68%']].map(([g,c,pct])=>(
          <div key={g} style={{textAlign:'center'}}>
            <div style={{fontSize:9,color:'#64748B'}}>{g}</div>
            <div style={{fontSize:11,fontWeight:600,color:c}}>{pct}</div>
          </div>
        ))}
      </div>
    </section>
  );
};

/* ── living brain panel ─────────────────────────────────── */
const BrainPanel: React.FC = () => {
  const { currentThought, currentPrediction, confidence } = useAppStore();
  const [charIdx, setCharIdx] = useState(0);

  useEffect(()=>{
    setCharIdx(0);
    let i=0;
    const iv=setInterval(()=>{
      i++;
      setCharIdx(i);
      if(i>=currentThought.length) clearInterval(iv);
    },22);
    return ()=>clearInterval(iv);
  },[currentThought]);

  return (
    <section aria-label="Living Brain Panel" style={{display:'flex',flexDirection:'column',height:'100%'}}>
      {/* header */}
      <header style={{display:'flex',alignItems:'center',gap:8,padding:'12px 14px',borderBottom:'1px solid rgba(255,255,255,.06)'}}>
        <motion.div animate={{scale:[1,1.3,1],boxShadow:['0 0 6px rgba(139,92,246,.3)','0 0 18px rgba(139,92,246,.7)','0 0 6px rgba(139,92,246,.3)']}} transition={{duration:2,repeat:Infinity}}
          style={{width:8,height:8,borderRadius:'50%',background:'#8B5CF6'}} aria-hidden="true"/>
        <h2 style={{fontSize:12,fontWeight:600,color:'#F8FAFC',margin:0}}>Living Brain</h2>
        <motion.span style={{fontSize:9,fontWeight:700,background:'#10B981',color:'#fff',padding:'1px 6px',borderRadius:999,marginLeft:'auto'}}
          animate={{opacity:[1,.7,1]}} transition={{duration:2,repeat:Infinity}}>ONLINE</motion.span>
      </header>

      {/* content */}
      <div style={{flex:1,overflow:'auto',padding:'10px 14px',display:'flex',flexDirection:'column',gap:10}} role="log" aria-live="polite">

        {/* thought */}
        <div style={{background:'rgba(139,92,246,.08)',border:'1px solid rgba(139,92,246,.15)',borderRadius:10,padding:'10px'}}>
          <div style={{fontSize:9,color:'#8B5CF6',textTransform:'uppercase',letterSpacing:'.1em',marginBottom:5}}>⚡ Current Thought</div>
          <p style={{fontSize:11,lineHeight:1.6,color:'#CBD5E1',margin:0,minHeight:36}}>
            {currentThought.slice(0,charIdx)}
            <motion.span animate={{opacity:[1,0,1]}} transition={{duration:.6,repeat:Infinity}} style={{color:'#3B82F6',fontWeight:'bold'}}>|</motion.span>
          </p>
        </div>

        {/* prediction */}
        <div style={{background:'rgba(245,158,11,.06)',border:'1px solid rgba(245,158,11,.15)',borderRadius:10,padding:'10px'}}>
          <div style={{fontSize:9,color:'#F59E0B',textTransform:'uppercase',letterSpacing:'.1em',marginBottom:5}}>🔮 Prediction</div>
          <p style={{fontSize:11,lineHeight:1.6,color:'#CBD5E1',margin:0}}>{currentPrediction}</p>
        </div>

        {/* confidence */}
        <div style={{background:'rgba(16,185,129,.06)',border:'1px solid rgba(16,185,129,.15)',borderRadius:10,padding:'10px'}}>
          <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:6}}>
            <span style={{fontSize:9,color:'#10B981',textTransform:'uppercase',letterSpacing:'.1em'}}>📊 Confidence</span>
            <motion.span style={{fontSize:20,fontWeight:700,color:'#10B981'}} key={confidence} initial={{scale:1.2}} animate={{scale:1}}>{confidence}%</motion.span>
          </div>
          <div style={{height:6,background:'rgba(255,255,255,.06)',borderRadius:3,overflow:'hidden'}}>
            <motion.div style={{height:'100%',background:'linear-gradient(90deg,#10B981,#3B82F6)',borderRadius:3}}
              animate={{width:`${confidence}%`}} transition={{duration:.8}}/>
          </div>
        </div>

        {/* memory */}
        <div style={{background:'rgba(59,130,246,.06)',border:'1px solid rgba(59,130,246,.15)',borderRadius:10,padding:'10px'}}>
          <div style={{fontSize:9,color:'#3B82F6',textTransform:'uppercase',letterSpacing:'.1em',marginBottom:5}}>🧠 Memory</div>
          <p style={{fontSize:11,lineHeight:1.6,color:'#94A3B8',margin:0,fontStyle:'italic'}}>
            "Similar pattern at 2022 WC — Gate B resolved in 7 min with 4 volunteers."
          </p>
        </div>

        {/* recommendation */}
        <div style={{background:'rgba(16,185,129,.1)',border:'1px solid rgba(16,185,129,.3)',borderRadius:10,padding:'10px'}}>
          <div style={{fontSize:9,color:'#10B981',textTransform:'uppercase',letterSpacing:'.1em',marginBottom:6}}>✅ Recommendation</div>
          <p style={{fontSize:12,fontWeight:600,color:'#F8FAFC',margin:'0 0 8px'}}>Deploy 3 volunteers → Gate B</p>
          <div style={{display:'flex',gap:12,fontSize:9,color:'#64748B',marginBottom:8}}>
            <span>Impact: <span style={{color:'#10B981'}}>-23% congestion</span></span>
            <span>ROI: <span style={{color:'#3B82F6'}}>4.2×</span></span>
          </div>
          <motion.button whileHover={{scale:1.02}} whileTap={{scale:.97}}
            style={{width:'100%',padding:'8px',background:'linear-gradient(135deg,#10B981,#3B82F6)',border:'none',borderRadius:8,color:'#fff',fontSize:11,fontWeight:600,cursor:'pointer'}}>
            ⚡ Execute
          </motion.button>
        </div>

        {/* debate */}
        <div style={{background:'rgba(255,255,255,.02)',border:'1px solid rgba(255,255,255,.06)',borderRadius:10,padding:'10px'}}>
          <div style={{fontSize:9,color:'#94A3B8',textTransform:'uppercase',letterSpacing:'.1em',marginBottom:8}}>🗣 Agent Debate</div>
          {[
            {name:'Navigation',icon:'🗺️',color:'#3B82F6',msg:'Gate B: 94% cap in 8 min.'},
            {name:'Medical',icon:'🏥',color:'#EF4444',msg:'Zone B clear. No incidents.'},
            {name:'Security',icon:'🛡️',color:'#F59E0B',msg:'Soft barriers recommended.'},
            {name:'Coordinator',icon:'🧠',color:'#8B5CF6',msg:'Decision: Deploy 3 volunteers.'},
          ].map((a,i)=>(
            <motion.div key={a.name} initial={{opacity:0,y:6}} animate={{opacity:1,y:0}} transition={{delay:i*.3+1}}
              style={{display:'flex',gap:7,marginBottom:7,alignItems:'flex-start'}}>
              <div style={{width:24,height:24,borderRadius:6,background:`${a.color}15`,border:`1px solid ${a.color}30`,display:'flex',alignItems:'center',justifyContent:'center',fontSize:12,flexShrink:0}}>{a.icon}</div>
              <div style={{flex:1}}>
                <span style={{fontSize:9,fontWeight:600,color:a.color}}>{a.name}</span>
                <div style={{fontSize:10,color:'#94A3B8',background:`${a.color}08`,borderRadius:6,padding:'3px 6px',marginTop:2,borderLeft:`2px solid ${a.color}40`}}>{a.msg}</div>
              </div>
            </motion.div>
          ))}
        </div>

      </div>
    </section>
  );
};

/* ── main dashboard ─────────────────────────────────────── */
export const Dashboard: React.FC = () => {
  const { isDemoRunning, setIsDemoRunning, matchMinute } = useAppStore();
  const [metrics, setMetrics] = useState({crowd:87342,queue:2400,risk:34,volunteers:142,transport:78,medical:3,energy:87,temp:22});
  const [demoStep, setDemoStep] = useState(0);
  const DEMO = ['⚽ Goal scored! Crowd peaks...','🌧️ Rain detected — redirecting fans.','⚠️ Gate B: 94% — congestion risk!','🧠 AI debate — 4 agents deliberating...','⚡ Decision: Deploy 3 volunteers.','✅ Congestion -23%. Risk NOMINAL.'];

  useEffect(()=>{
    const iv=setInterval(()=>{
      setMetrics(m=>({
        crowd:87342+Math.floor((Math.random()-.5)*200),
        queue:Math.max(800,m.queue+Math.floor((Math.random()-.5)*150)),
        risk:Math.min(99,Math.max(0,m.risk+Math.floor((Math.random()-.5)*4))),
        volunteers:m.volunteers+Math.floor((Math.random()-.5)*3),
        transport:Math.min(99,Math.max(20,m.transport+Math.floor((Math.random()-.5)*2))),
        medical:Math.max(0,m.medical+(Math.random()<.05?1:Math.random()<.05?-1:0)),
        energy:Math.min(99,Math.max(50,m.energy+Math.floor((Math.random()-.5)*1))),
        temp:Math.max(18,Math.min(30,m.temp+(Math.random()-.5)*.3)),
      }));
    },3000);
    return ()=>clearInterval(iv);
  },[]);

  useEffect(()=>{
    if(!isDemoRunning) return;
    if(demoStep>=DEMO.length){setIsDemoRunning(false);setDemoStep(0);return;}
    const t=setTimeout(()=>setDemoStep(s=>s+1),2200);
    return()=>clearTimeout(t);
  },[isDemoRunning, demoStep, DEMO.length, setIsDemoRunning]);

  const cards:CardProps[] = [
    {title:'Crowd',value:metrics.crowd,icon:<Users size={13}/>,color:'#3B82F6',status:'good',spark:[78,82,85,83,87,89,87],delay:.05},
    {title:'Queue',value:metrics.queue,unit:'/hr',icon:<Activity size={13}/>,color:'#06B6D4',status:metrics.queue>2000?'warn':'good',spark:[1200,1800,2200,2000,2400,2100,metrics.queue],delay:.1},
    {title:'Risk',value:metrics.risk,unit:'%',icon:<AlertTriangle size={13}/>,color:'#EF4444',status:metrics.risk>70?'bad':metrics.risk>40?'warn':'good',spark:[20,30,45,38,34,40,metrics.risk],delay:.15},
    {title:'Volunteers',value:metrics.volunteers,icon:<UserCheck size={13}/>,color:'#10B981',status:'good',spark:[138,140,142,141,143,142,metrics.volunteers],delay:.2},
    {title:'Transport',value:metrics.transport,unit:'%',icon:<Truck size={13}/>,color:'#F59E0B',status:metrics.transport>90?'warn':'good',spark:[65,70,75,78,80,78,metrics.transport],delay:.25},
    {title:'Medical',value:metrics.medical,subtitle:'incidents',icon:<Heart size={13}/>,color:'#EF4444',status:metrics.medical>5?'warn':'good',spark:[1,2,3,2,3,3,metrics.medical],delay:.3},
    {title:'Energy',value:metrics.energy,unit:'%',icon:<Zap size={13}/>,color:'#8B5CF6',status:'good',spark:[85,86,87,86,88,87,metrics.energy],delay:.35},
    {title:'Weather',value:Math.round(metrics.temp),unit:'°C',subtitle:'18% rain',icon:<Cloud size={13}/>,color:'#06B6D4',status:'good',spark:[21,22,22,23,22,22,Math.round(metrics.temp)],delay:.4},
  ];

  return (
    <div style={{display:'flex',flexDirection:'column',height:'100%',overflow:'hidden'}}>
      {/* demo banner */}
      <AnimatePresence>
        {isDemoRunning && demoStep<DEMO.length && (
          <motion.div initial={{opacity:0,y:-10}} animate={{opacity:1,y:0}} exit={{opacity:0,y:-10}}
            key={demoStep}
            style={{margin:'8px 12px 0',padding:'8px 14px',background:'rgba(139,92,246,.12)',border:'1px solid rgba(139,92,246,.3)',borderRadius:10,display:'flex',alignItems:'center',gap:10}}>
            <motion.div style={{width:7,height:7,borderRadius:'50%',background:'#8B5CF6',flexShrink:0}} animate={{scale:[1,1.4,1]}} transition={{duration:.8,repeat:Infinity}}/>
            <span style={{fontSize:12,fontWeight:500,color:'#E2D9F3'}}>DEMO: {DEMO[demoStep]}</span>
            <div style={{marginLeft:'auto',display:'flex',gap:3}}>
              {DEMO.map((_,i)=><div key={i} style={{width:5,height:5,borderRadius:'50%',background:i<=demoStep?'#8B5CF6':'rgba(255,255,255,.1)'}}/>)}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 3-col layout */}
      <div style={{flex:1,display:'flex',gap:10,padding:10,overflow:'hidden',minHeight:0}}>

        {/* LEFT — match card + metrics grid */}
        <div style={{width:234,flexShrink:0,display:'flex',flexDirection:'column',gap:8,overflow:'auto'}}>
          {/* match */}
          <motion.div initial={{opacity:0,x:-16}} animate={{opacity:1,x:0}}
            style={{background:'linear-gradient(135deg,rgba(59,130,246,.12),rgba(139,92,246,.08))',border:'1px solid rgba(59,130,246,.2)',borderRadius:14,padding:'12px'}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:8}}>
              <span style={{fontSize:9,color:'#3B82F6',textTransform:'uppercase',letterSpacing:'.1em'}}>Live Match</span>
              <motion.span style={{fontSize:8,fontWeight:700,background:'#EF4444',color:'#fff',padding:'1px 5px',borderRadius:999}}
                animate={{opacity:[1,.5,1]}} transition={{duration:1.2,repeat:Infinity}}>● LIVE</motion.span>
            </div>
            <div style={{display:'flex',alignItems:'center',justifyContent:'space-between'}}>
              <div style={{textAlign:'center'}}><div style={{fontSize:24}}>🇧🇷</div><div style={{fontSize:9,color:'#94A3B8',marginTop:2}}>Brazil</div></div>
              <div style={{textAlign:'center'}}>
                <div style={{fontSize:26,fontWeight:700,color:'#F8FAFC',letterSpacing:'-.04em'}}>2 – 1</div>
                <motion.div style={{fontSize:9,background:'rgba(239,68,68,.2)',color:'#FCA5A5',padding:'1px 8px',borderRadius:999,marginTop:3}}
                  animate={{opacity:[1,.5,1]}} transition={{duration:1.5,repeat:Infinity}}>{matchMinute}'</motion.div>
              </div>
              <div style={{textAlign:'center'}}><div style={{fontSize:24}}>🇦🇷</div><div style={{fontSize:9,color:'#94A3B8',marginTop:2}}>Argentina</div></div>
            </div>
          </motion.div>

          {/* metrics */}
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:6,flex:1}}>
            {cards.map(c=><Card key={c.title} {...c}/>)}
          </div>

          {/* demo btn */}
          <motion.button whileHover={{scale:1.02}} whileTap={{scale:.97}}
            onClick={()=>{setIsDemoRunning(!isDemoRunning);setDemoStep(0);}}
            style={{padding:'10px',background:isDemoRunning?'rgba(239,68,68,.15)':'linear-gradient(135deg,rgba(59,130,246,.2),rgba(139,92,246,.2))',
              border:`1px solid ${isDemoRunning?'rgba(239,68,68,.3)':'rgba(59,130,246,.3)'}`,borderRadius:12,
              color:isDemoRunning?'#EF4444':'#F8FAFC',fontSize:12,fontWeight:600,cursor:'pointer',
              display:'flex',alignItems:'center',justifyContent:'center',gap:6}}>
            <Play size={13} style={{fill:isDemoRunning?'none':'currentColor'}}/>
            {isDemoRunning?'STOP DEMO':'▶ RUN DEMO'}
          </motion.button>
        </div>

        {/* CENTER — stadium map */}
        <motion.div initial={{opacity:0,scale:.98}} animate={{opacity:1,scale:1}} transition={{delay:.2}}
          style={{flex:1,background:'rgba(255,255,255,.025)',border:'1px solid rgba(255,255,255,.06)',borderRadius:14,padding:12,overflow:'hidden',display:'flex',flexDirection:'column'}}>
          <StadiumMap/>
        </motion.div>

        {/* RIGHT — brain */}
        <motion.div initial={{opacity:0,x:16}} animate={{opacity:1,x:0}} transition={{delay:.3}}
          style={{width:270,flexShrink:0,background:'rgba(255,255,255,.025)',border:'1px solid rgba(139,92,246,.15)',borderRadius:14,overflow:'hidden',display:'flex',flexDirection:'column'}}>
          <BrainPanel/>
        </motion.div>

      </div>
    </div>
  );
};

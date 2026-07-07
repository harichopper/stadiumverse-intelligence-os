"""
StadiumVerse Intelligence OS — Database Seeder
Populates SQLite with realistic demo data
"""

import math
import random
from datetime import datetime, timedelta
from .database import SessionLocal
from .db_models import (
    DigitalFan, Volunteer, VolunteerTask,
    CrowdSnapshot, AIDecision, StadiumEvent
)

FANS_DATA = [
    ("F001","Carlos Mendoza","BRA","🇧🇷","pt",29,"Brazil","N7","14C","ecstatic",12,95,"Goal! We need one more!","Saw Brazil win in 2018","Will stay to celebrate",0.94),
    ("F002","Diego Ramirez","ARG","🇦🇷","es",34,"Argentina","S3","28A","anxious",78,45,"Come on, equalize!","Lost a final at similar score","May leave early",0.67),
    ("F003","Hans Kellner","DEU","🇩🇪","de",41,"Germany","E12","5B","calm",22,60,"Great football quality","First World Cup final","Will watch till end",0.91),
    ("F004","Marie Dupont","FRA","🇫🇷","fr",27,"France","W6","19D","excited",31,80,"Amazing atmosphere!","2022 WC final comparison","Will buy merchandise",0.88),
    ("F005","Yuki Tanaka","JPN","🇯🇵","ja",25,"Japan","N9","3A","delighted",8,90,"This is history","First time at WC","Will share on social media",0.97),
    ("F006","Ahmed Al-Rashid","SAU","🇸🇦","ar",38,"Saudi Arabia","E4","22C","tense",55,65,"Just a few more minutes","Attended 2002 WC Korea","Neutral — enjoying game",0.79),
    ("F007","Priya Sharma","IND","🇮🇳","en",23,"India","S8","11F","joyful",18,85,"Incredible experience!","Never been to WC before","Will explore stadium",0.92),
    ("F008","Marco Rossi","ITA","🇮🇹","it",45,"Italy","W2","7B","nostalgic",35,70,"Reminds me of 2006","Attended 2006 WC Germany","Will leave at final whistle",0.83),
    ("F009","Liu Wei","CHN","🇨🇳","zh",31,"China","N3","33D","curious",25,75,"Everything is so organised","Seen lots of WC footage","Will take many photos",0.89),
    ("F010","Aisha Okonkwo","NGA","🇳🇬","en",28,"Nigeria","S11","9A","energetic",20,88,"The crowd energy is amazing!","Followed tournament from Africa","Will attend post-match show",0.93),
]

VOLUNTEER_DATA = [
    ("V001","Rashid Al-Amiri","ar,en","crowd_control,multilingual",True,"Gate B"),
    ("V002","Sofia Petrov","ru,en","first_aid,multilingual",True,"Medical Zone C"),
    ("V003","James Okafor","en,fr","crowd_control",False,"Gate A"),
    ("V004","Mei Chen","zh,en","information,multilingual",False,"Info Desk North"),
    ("V005","Pablo Hernandez","es,en,pt","multilingual,accessibility",False,"Gate D"),
    ("V006","Anna Kowalski","pl,en","first_aid",True,"Medical Zone A"),
    ("V007","Tariq Hassan","ar,en,fr","crowd_control,multilingual",False,"Gate C"),
    ("V008","Ingrid Larsen","no,en","accessibility,information",False,"South Stand"),
]


def seed_fans(db):
    if db.query(DigitalFan).count() > 0:
        return
    for i, (fan_id,name,country,flag,lang,age,team,sector,seat,emotion,stress,excitement,thought,memory,prediction,confidence) in enumerate(FANS_DATA):
        angle = (i / len(FANS_DATA)) * math.pi * 2
        lx = 50 + 35 * (0.6 + random.random() * 0.4) * round(math.cos(angle), 3)
        ly = 50 + 25 * (0.6 + random.random() * 0.4) * round(math.sin(angle), 3)
        db.add(DigitalFan(
            fan_id=fan_id, name=name, country=country, flag=flag,
            language=lang, age=age, favorite_team=team,
            sector=sector, seat=seat,
            current_emotion=emotion,
            stress_level=stress, excitement_level=excitement,
            hunger_level=random.randint(10,60),
            fatigue_level=random.randint(5,40),
            loc_x=round(lx,1), loc_y=round(ly,1),
            current_thought=thought,
            memory_summary=memory,
            predicted_action=prediction,
            prediction_confidence=confidence,
            risk_score=max(0, stress - 30),
        ))
    db.commit()
    print(f"✅ Seeded {len(FANS_DATA)} digital fans")


def seed_volunteers(db):
    if db.query(Volunteer).count() > 0:
        return
    positions = [(15,50),(85,50),(50,15),(50,85),(20,30),(80,30),(20,70),(80,70)]
    for i, (vid,name,langs,skills,medical,zone) in enumerate(VOLUNTEER_DATA):
        lx, ly = positions[i % len(positions)]
        db.add(Volunteer(
            volunteer_id=vid, name=name,
            languages=langs, skills=skills,
            medical_training=medical,
            availability=random.choice(["available","available","available","busy"]),
            zone_assignment=zone,
            loc_x=lx+random.uniform(-3,3),
            loc_y=ly+random.uniform(-3,3),
            tasks_today=random.randint(0,5),
        ))
    db.commit()
    print(f"✅ Seeded {len(VOLUNTEER_DATA)} volunteers")


def seed_crowd_snapshots(db):
    if db.query(CrowdSnapshot).count() > 0:
        return
    now = datetime.utcnow()
    for i in range(90):  # 90 match minutes
        ts = now - timedelta(minutes=90-i)
        total = int(40000 + 47342 * (1 - math.exp(-i/15)) + random.randint(-500,500))
        db.add(CrowdSnapshot(
            timestamp=ts,
            total_fans=total,
            avg_stress=30 + 40*(i/90) + random.uniform(-5,5),
            avg_excitement=50 + 30*(i/90) + random.uniform(-8,8),
            risk_level="critical" if i>80 else "warning" if i>60 else "healthy",
            gate_a_density=60+random.uniform(-10,10),
            gate_b_density=min(99,70+i*0.3+random.uniform(-8,8)),
            gate_c_density=55+random.uniform(-10,10),
            gate_d_density=50+random.uniform(-10,10),
            queue_avg_min=3+i*0.15+random.uniform(-1,1),
            weather_temp=22+random.uniform(-1,1),
            weather_rain_pct=max(0,i*0.5-20+random.uniform(-5,5)),
        ))
    db.commit()
    print("✅ Seeded 90 crowd snapshots")


def seed_ai_decisions(db):
    if db.query(AIDecision).count() > 0:
        return
    decisions = [
        (15,"Navigation","Open Gate C overflow lane","Gate A density reached 75%. Pre-emptive measure.",0.88,"SUCCESS",2800,18.0),
        (28,"Medical","Deploy medic to Section S-East","Fan reported dizziness. High heat index.",0.95,"SUCCESS",1,100.0),
        (42,"Coordinator","Deploy 2 volunteers to food court","Queue > 8 min. Efficiency dropped.",0.82,"SUCCESS",420,31.0),
        (55,"Transport","Alert Metro Station 2 incoming surge","Model predicts 1,200 fans in 12 min.",0.91,"SUCCESS",1200,24.0),
        (62,"Security","Soft barriers at Gate B",  "Crowd pressure rising. Safety threshold.",0.87,"SUCCESS",3400,19.0),
        (67,"Coordinator","Deploy 3 volunteers → Gate B","Gate B at 94% capacity. 8-min prediction.",0.94,"SUCCESS",1400,23.0),
        (72,"Navigation","Activate digital rerouting → Gate C","Complement volunteer deployment.",0.89,"PARTIAL",600,12.0),
        (78,"Medical","Pre-position medical at South Exit","Post-match exit pattern from history.",0.85,"PENDING",5000,0.0),
    ]
    for min,agent,dec,reason,conf,outcome,fans,impact in decisions:
        db.add(AIDecision(
            timestamp=datetime.utcnow()-timedelta(minutes=90-min),
            match_minute=min, agent=agent,
            decision=dec, reasoning=reason,
            confidence=conf, outcome=outcome,
            affected_fans=fans, impact_pct=impact,
        ))
    db.commit()
    print(f"✅ Seeded {len(decisions)} AI decisions")


def seed_events(db):
    if db.query(StadiumEvent).count() > 0:
        return
    events = [
        (5,"match","Kick-off — BRA vs ARG","FIFA World Cup 2026 Final begins",1,"Field",True),
        (23,"goal","GOAL — Neymar Jr. (Brazil 1-0)","Brazilian fans surge in celebration",2,"N-Stand",True),
        (38,"crowd","Gate B congestion warning","Flow rate exceeds threshold",3,"Gate B",True),
        (44,"weather","Rain advisory issued","73% rain probability next 20 min",2,"Stadium-wide",False),
        (61,"goal","GOAL — Lautaro (Argentina 1-1)","Argentine sector erupts",2,"S-Stand",True),
        (67,"ai_action","AI deployed 3 volunteers","Gate B congestion resolved",1,"Gate B",True),
        (74,"goal","GOAL — Vinicius Jr. (Brazil 2-1)","Brazilian fans celebrate",2,"N-Stand",True),
        (85,"crowd","Post-match exit preparation","AI pre-positioning teams",2,"All Gates",False),
    ]
    for min,etype,title,desc,severity,zone,resolved in events:
        db.add(StadiumEvent(
            timestamp=datetime.utcnow()-timedelta(minutes=90-min),
            event_type=etype, title=title, description=desc,
            severity=severity, zone=zone, resolved=resolved,
            resolved_at=datetime.utcnow()-timedelta(minutes=90-min-5) if resolved else None,
        ))
    db.commit()
    print(f"✅ Seeded {len(events)} stadium events")


def run_seed():
    db = SessionLocal()
    try:
        seed_fans(db)
        seed_volunteers(db)
        seed_crowd_snapshots(db)
        seed_ai_decisions(db)
        seed_events(db)
        print("🌱 Database seeding complete")
    finally:
        db.close()

#!/usr/bin/env python3
"""
StadiumVerse AI - Demo Data Generator
Generate realistic mock data for FIFA World Cup 2026 stadium simulation
"""

import asyncio
import random
from datetime import datetime, timedelta
from typing import List
import uuid

# Ensure we can import from the backend
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.database import AsyncSessionLocal, init_database
from app.models.fan import DigitalFan, FanEmotion, AccessibilityNeed, TransportMode
from app.models.volunteer import Volunteer, VolunteerSkill, VolunteerStatus
from app.models.stadium import StadiumZone, StadiumFacility
from app.models.event import WeatherData
from app.config import STADIUM_ZONES
from geoalchemy2 import WKTElement

# FIFA World Cup 2026 Teams
WORLD_CUP_TEAMS = [
    "Argentina",
    "Brazil",
    "France",
    "England",
    "Spain",
    "Germany",
    "Netherlands",
    "Portugal",
    "Belgium",
    "Croatia",
    "Italy",
    "Morocco",
    "Mexico",
    "USA",
    "Canada",
    "Japan",
    "South Korea",
    "Australia",
    "Senegal",
    "Ghana",
    "Nigeria",
    "Egypt",
    "Saudi Arabia",
    "Iran",
    "Qatar",
    "Ecuador",
    "Uruguay",
    "Chile",
    "Colombia",
    "Peru",
]

# Popular first names by country
NAMES_BY_COUNTRY = {
    "US": [
        "James",
        "Mary",
        "John",
        "Patricia",
        "Robert",
        "Jennifer",
        "Michael",
        "Linda",
        "David",
        "Elizabeth",
    ],
    "CA": [
        "Liam",
        "Emma",
        "Noah",
        "Olivia",
        "William",
        "Ava",
        "James",
        "Isabella",
        "Benjamin",
        "Sophia",
    ],
    "MX": [
        "José",
        "María",
        "Luis",
        "Guadalupe",
        "Juan",
        "Margarita",
        "Antonio",
        "Juana",
        "Francisco",
        "Rosa",
    ],
    "BR": [
        "Miguel",
        "Alice",
        "Arthur",
        "Laura",
        "Heitor",
        "Manuela",
        "Bernardo",
        "Luiza",
        "Théo",
        "Valentina",
    ],
    "AR": [
        "Santiago",
        "Emma",
        "Mateo",
        "Olivia",
        "Sebastián",
        "Mía",
        "Matías",
        "Isabella",
        "Nicolás",
        "Sofía",
    ],
    "FR": [
        "Gabriel",
        "Emma",
        "Raphaël",
        "Louise",
        "Arthur",
        "Alice",
        "Louis",
        "Chloé",
        "Jules",
        "Inès",
    ],
    "DE": [
        "Ben",
        "Emma",
        "Paul",
        "Hannah",
        "Leon",
        "Mia",
        "Finn",
        "Sofia",
        "Noah",
        "Emilia",
    ],
    "GB": [
        "Oliver",
        "Olivia",
        "George",
        "Amelia",
        "Harry",
        "Isla",
        "Jack",
        "Ava",
        "Jacob",
        "Emily",
    ],
    "IT": [
        "Leonardo",
        "Sofia",
        "Francesco",
        "Giulia",
        "Lorenzo",
        "Aurora",
        "Alessandro",
        "Ginevra",
        "Andrea",
        "Alice",
    ],
    "ES": [
        "Hugo",
        "Lucía",
        "Martín",
        "Sofía",
        "Lucas",
        "Martina",
        "Mateo",
        "María",
        "Leo",
        "Paula",
    ],
    "JP": [
        "Hiroto",
        "Himari",
        "Haruto",
        "Koharu",
        "Yuto",
        "Yui",
        "Sota",
        "Rei",
        "Hayato",
        "Ichika",
    ],
    "KR": [
        "Minjun",
        "Soeun",
        "Seoung",
        "Seoyeon",
        "Yejun",
        "Jiwoo",
        "Dohyun",
        "Chaeyeon",
        "Eunwoo",
        "Dayeon",
    ],
}

# Languages by country
LANGUAGES_BY_COUNTRY = {
    "US": "en",
    "CA": "en",
    "MX": "es",
    "BR": "pt",
    "AR": "es",
    "FR": "fr",
    "DE": "de",
    "GB": "en",
    "IT": "it",
    "ES": "es",
    "JP": "ja",
    "KR": "ko",
    "MA": "ar",
    "EG": "ar",
    "SA": "ar",
    "IR": "fa",
    "SN": "fr",
    "GH": "en",
    "NG": "en",
    "AU": "en",
    "QA": "ar",
    "EC": "es",
    "UY": "es",
    "CL": "es",
    "CO": "es",
    "PE": "es",
}


async def generate_digital_fans(count: int = 100) -> List[DigitalFan]:
    """Generate realistic digital fans for the simulation"""
    fans = []

    # Stadium bounds (MetLife Stadium)
    stadium_bounds = {
        "north": 40.8155,
        "south": 40.8115,
        "east": -74.0720,
        "west": -74.0770,
    }

    for i in range(count):
        # Random country selection
        country_code = random.choice(list(WORLD_CUP_TEAMS))
        country_iso = {
            "Argentina": "AR",
            "Brazil": "BR",
            "France": "FR",
            "England": "GB",
            "Spain": "ES",
            "Germany": "DE",
            "Netherlands": "NL",
            "Portugal": "PT",
            "Belgium": "BE",
            "Croatia": "HR",
            "Italy": "IT",
            "Morocco": "MA",
            "Mexico": "MX",
            "USA": "US",
            "Canada": "CA",
            "Japan": "JP",
            "South Korea": "KR",
            "Australia": "AU",
            "Senegal": "SN",
            "Ghana": "GH",
            "Nigeria": "NG",
            "Egypt": "EG",
            "Saudi Arabia": "SA",
            "Iran": "IR",
            "Qatar": "QA",
            "Ecuador": "EC",
            "Uruguay": "UY",
            "Chile": "CL",
            "Colombia": "CO",
            "Peru": "PE",
        }.get(country_code, "US")

        # Generate name based on country
        names = NAMES_BY_COUNTRY.get(country_iso, NAMES_BY_COUNTRY["US"])
        name = random.choice(names)

        # Add surname
        if country_iso in ["ES", "MX", "AR", "CL", "CO", "PE", "EC", "UY"]:
            surnames = [
                "García",
                "Rodríguez",
                "González",
                "Fernández",
                "López",
                "Martínez",
                "Sánchez",
                "Pérez",
                "Gómez",
                "Martín",
            ]
        elif country_iso in ["BR"]:
            surnames = [
                "Silva",
                "Santos",
                "Oliveira",
                "Souza",
                "Rodrigues",
                "Ferreira",
                "Alves",
                "Pereira",
                "Lima",
                "Gomes",
            ]
        elif country_iso in ["FR"]:
            surnames = [
                "Martin",
                "Bernard",
                "Dubois",
                "Thomas",
                "Robert",
                "Richard",
                "Petit",
                "Durand",
                "Leroy",
                "Moreau",
            ]
        elif country_iso in ["DE"]:
            surnames = [
                "Müller",
                "Schmidt",
                "Schneider",
                "Fischer",
                "Weber",
                "Meyer",
                "Wagner",
                "Becker",
                "Schulz",
                "Hoffmann",
            ]
        else:
            surnames = [
                "Smith",
                "Johnson",
                "Williams",
                "Brown",
                "Jones",
                "Garcia",
                "Miller",
                "Davis",
                "Rodriguez",
                "Martinez",
            ]

        full_name = f"{name} {random.choice(surnames)}"

        # Random location within stadium
        lat = random.uniform(stadium_bounds["south"], stadium_bounds["north"])
        lng = random.uniform(stadium_bounds["west"], stadium_bounds["east"])

        # Age distribution - more young adults at football
        age = random.choices(
            population=list(range(16, 80)),
            weights=[
                1 if a < 25 else 3 if a < 40 else 2 if a < 60 else 1
                for a in range(16, 80)
            ],
            k=1,
        )[0]

        # Accessibility needs (10% have some form of accessibility need)
        accessibility = random.choices(
            population=list(AccessibilityNeed),
            weights=[85, 5, 3, 3, 4],  # Most have no needs
            k=1,
        )[0]

        # Emotional state - varied but generally positive at stadium
        emotion_weights = [
            15,
            20,
            5,
            10,
            5,
            10,
            5,
            30,
        ]  # excited, joyful, angry, stressed, confused, tired, fearful, neutral
        current_emotion = random.choices(
            population=list(FanEmotion), weights=emotion_weights, k=1
        )[0]

        # Generate behavioral characteristics
        base_stress = random.randint(20, 80)
        base_excitement = (
            random.randint(30, 90)
            if current_emotion in [FanEmotion.EXCITED, FanEmotion.JOYFUL]
            else random.randint(20, 60)
        )

        fan = DigitalFan(
            fan_id=f"F{i + 1:03d}",
            name=full_name,
            country=country_iso,
            language=LANGUAGES_BY_COUNTRY.get(country_iso, "en"),
            age=age,
            accessibility_needs=accessibility,
            favorite_team=country_code,
            # Current state
            current_emotion=current_emotion,
            stress_level=base_stress,
            excitement_level=base_excitement,
            walking_speed=random.uniform(0.8, 1.8),
            hunger_level=random.randint(20, 80),
            fatigue_level=random.randint(10, 60),
            battery_level=random.randint(30, 100),
            # Location
            current_location=WKTElement(f"POINT({lng} {lat})", srid=4326),
            transportation=random.choice(list(TransportMode)),
            # Behavioral patterns
            purchase_intent=random.randint(20, 90),
            medical_risk_score=random.randint(5, 30) + (age - 40)
            if age > 40
            else random.randint(5, 20),
            lost_probability=random.uniform(0.01, 0.15),
            queue_tolerance=random.randint(30, 90),
            risk_score=random.randint(10, 40),
            # Predictions
            predicted_next_action=random.choice(
                [
                    "Moving to food court",
                    "Heading to restroom",
                    "Finding seat",
                    "Exploring stadium",
                    "Meeting friends",
                    "Taking photos",
                ]
            ),
            prediction_confidence=random.uniform(0.4, 0.9),
        )

        fans.append(fan)

    return fans


async def generate_volunteers(count: int = 20) -> List[Volunteer]:
    """Generate volunteers for stadium operations"""
    volunteers = []

    volunteer_names = [
        "Alex Johnson",
        "Maria Rodriguez",
        "David Smith",
        "Sarah Kim",
        "Carlos Mendez",
        "Jennifer Liu",
        "Michael Brown",
        "Ana Santos",
        "James Wilson",
        "Lisa Chen",
        "Roberto Garcia",
        "Emma Davis",
        "Ahmed Hassan",
        "Sophie Martin",
        "Juan Lopez",
        "Rachel Green",
        "Pierre Dubois",
        "Yuki Tanaka",
        "Marco Rossi",
        "Elena Petrov",
    ]

    # Volunteer positions around the stadium
    volunteer_positions = [
        (40.8140, -74.0750),
        (40.8135, -74.0740),
        (40.8130, -74.0745),
        (40.8125, -74.0755),
        (40.8145, -74.0745),
        (40.8125, -74.0745),
        (40.8135, -74.0735),
        (40.8135, -74.0755),
        (40.8142, -74.0752),
        (40.8142, -74.0738),
        (40.8128, -74.0752),
        (40.8128, -74.0738),
        (40.8135, -74.0745),
        (40.8145, -74.0745),
        (40.8125, -74.0745),
        (40.8140, -74.0760),
        (40.8130, -74.0730),
        (40.8138, -74.0748),
        (40.8132, -74.0742),
        (40.8141, -74.0747),
    ]

    for i in range(min(count, len(volunteer_names))):
        # Random skills for each volunteer
        num_skills = random.randint(1, 3)
        skills = random.sample(list(VolunteerSkill), num_skills)

        # Languages - most know English + one other
        languages = ["en"]
        if random.random() > 0.3:  # 70% know additional language
            additional_lang = random.choice(["es", "fr", "pt", "de", "ar", "ja", "ko"])
            languages.append(additional_lang)

        # Position
        lat, lng = volunteer_positions[i % len(volunteer_positions)]

        volunteer = Volunteer(
            volunteer_id=f"V{i + 1:03d}",
            name=volunteer_names[i],
            languages=languages,
            skills=skills,
            medical_training=VolunteerSkill.FIRST_AID in skills,
            current_location=WKTElement(f"POINT({lng} {lat})", srid=4326),
            availability_status=random.choices(
                population=list(VolunteerStatus),
                weights=[60, 25, 10, 5],  # Most available
                k=1,
            )[0],
            shift_start=datetime.utcnow() - timedelta(hours=random.randint(1, 4)),
            shift_end=datetime.utcnow() + timedelta(hours=random.randint(2, 6)),
            tasks_completed_today=random.randint(0, 8),
            average_response_time=random.randint(120, 600),  # 2-10 minutes
            satisfaction_rating=random.uniform(4.0, 5.0),
        )

        volunteers.append(volunteer)

    return volunteers


async def generate_stadium_zones_and_facilities():
    """Generate stadium zones and facilities"""
    zones = []
    facilities = []

    # Create zones based on configuration
    zone_id_map = {}

    for zone_type, zone_data in STADIUM_ZONES.items():
        for zone_name, zone_info in zone_data.items():
            # Create zone
            zone_id = str(uuid.uuid4())
            zone_id_map[f"{zone_type}_{zone_name}"] = zone_id

            # Create polygon coordinates for the zone (simple square around the point)
            lat, lng = zone_info["coordinates"]
            size = 0.001  # Roughly 100m x 100m

            polygon_coords = f"POLYGON(({lng - size} {lat - size}, {lng + size} {lat - size}, {lng + size} {lat + size}, {lng - size} {lat + size}, {lng - size} {lat - size}))"

            zone = StadiumZone(
                id=zone_id,
                name=f"{zone_name} {zone_type.replace('_', ' ').title()}",
                zone_type=zone_type,
                capacity=zone_info.get("capacity", 100),
                coordinates=WKTElement(polygon_coords, srid=4326),
                level=1,
                accessibility_features=["wheelchair_accessible", "elevator"]
                if random.random() > 0.5
                else [],
            )
            zones.append(zone)

            # Create facility within zone
            facility = StadiumFacility(
                zone_id=zone_id,
                facility_type=zone_type.replace("s", ""),  # Remove plural
                name=zone_name,
                location=WKTElement(f"POINT({lng} {lat})", srid=4326),
                capacity=zone_info.get("capacity", 100),
                current_queue_length=random.randint(0, 20),
                average_service_time=random.randint(30, 300),  # 30 seconds to 5 minutes
                is_operational=random.random() > 0.05,  # 95% operational
                accessibility_features=["wheelchair_accessible"]
                if random.random() > 0.3
                else [],
            )
            facilities.append(facility)

    return zones, facilities


async def generate_weather_data():
    """Generate realistic weather data"""
    # Simulate weather for MetLife Stadium area (New Jersey)
    base_temp = 22.0  # 22°C (nice summer day)

    weather_conditions = ["clear", "partly_cloudy", "cloudy", "light_rain"]
    current_condition = random.choice(weather_conditions)

    weather = WeatherData(
        temperature=base_temp + random.uniform(-5, 5),
        humidity=random.randint(40, 80),
        wind_speed=random.uniform(0, 20),
        wind_direction=random.randint(0, 360),
        precipitation=random.uniform(0, 5) if "rain" in current_condition else 0,
        visibility=random.uniform(8, 15),
        weather_conditions=current_condition,
        air_quality_index=random.randint(20, 120),
        predicted_changes={
            "next_hour": {
                "temperature_change": random.uniform(-2, 2),
                "precipitation_probability": random.uniform(0, 40),
                "condition": current_condition,
            }
        },
    )

    return weather


async def main():
    """Main function to generate all demo data"""
    print("🏟️  Generating StadiumVerse AI Demo Data")
    print("FIFA World Cup 2026 - MetLife Stadium")
    print("=" * 50)

    try:
        # Initialize database
        print("📊 Initializing database...")
        await init_database()

        async with AsyncSessionLocal() as session:
            # Generate digital fans
            print("👥 Generating 100 digital fans...")
            fans = await generate_digital_fans(100)
            for fan in fans:
                session.add(fan)

            # Generate volunteers
            print("🙋 Generating 20 volunteers...")
            volunteers = await generate_volunteers(20)
            for volunteer in volunteers:
                session.add(volunteer)

            # Generate stadium zones and facilities
            print("🏗️  Generating stadium zones and facilities...")
            zones, facilities = await generate_stadium_zones_and_facilities()
            for zone in zones:
                session.add(zone)
            for facility in facilities:
                session.add(facility)

            # Generate weather data
            print("🌤️  Generating weather data...")
            weather = await generate_weather_data()
            session.add(weather)

            # Commit all data
            await session.commit()
            print("✅ All demo data saved to database")

        print("\n🎉 Demo data generation completed successfully!")
        print("\nGenerated:")
        print("  • 100 Digital Fans with realistic behaviors")
        print("  • 20 Volunteers with various skills")
        print(f"  • {len(zones)} Stadium zones")
        print(f"  • {len(facilities)} Stadium facilities")
        print("  • Current weather conditions")
        print(
            "\n🚀 You can now start the application and see the simulation in action!"
        )

    except Exception as e:
        print(f"❌ Error generating demo data: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

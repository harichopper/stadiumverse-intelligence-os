"""
StadiumVerse AI - Digital Fan Models
Core models for AI Digital Twins of stadium visitors at FIFA World Cup 2026.
"""

import enum
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from ..database import Base


def _now() -> datetime:
    """Return timezone-aware current UTC time."""
    return datetime.now(timezone.utc)


def _uid() -> str:
    """Return a new UUID string for primary keys."""
    return str(uuid.uuid4())



# Enums for fan characteristics
class FanEmotion(str, enum.Enum):
    EXCITED = "excited"
    JOYFUL = "joyful"
    ANGRY = "angry"
    STRESSED = "stressed"
    CONFUSED = "confused"
    TIRED = "tired"
    FEARFUL = "fearful"
    NEUTRAL = "neutral"


class AccessibilityNeed(str, enum.Enum):
    WHEELCHAIR = "wheelchair"
    VISUAL_IMPAIRMENT = "visual_impairment"
    HEARING_IMPAIRMENT = "hearing_impairment"
    MOBILITY_AID = "mobility_aid"
    NONE = "none"


class TransportMode(str, enum.Enum):
    WALKING = "walking"
    METRO = "metro"
    BUS = "bus"
    TAXI = "taxi"
    CAR = "car"
    BIKE = "bike"


class PredictionType(str, enum.Enum):
    MOVEMENT = "movement"
    PURCHASE = "purchase"
    RESTROOM = "restroom"
    EXIT = "exit"
    EMERGENCY = "emergency"
    QUEUE = "queue"


class PersonalityTrait(str, enum.Enum):
    SOCIAL = "social"
    ADVENTUROUS = "adventurous"
    CAUTIOUS = "cautious"
    IMPATIENT = "impatient"
    PATIENT = "patient"
    CURIOUS = "curious"
    PRACTICAL = "practical"
    SPONTANEOUS = "spontaneous"
    LOYAL = "loyal"
    INDEPENDENT = "independent"
    FAMILY_ORIENTED = "family_oriented"
    BUDGET_CONSCIOUS = "budget_conscious"


class DigitalTwin(Base):
    """
    Enhanced Digital Twin for V2 - Living Brain Architecture
    Each fan has a persistent memory and unique personality
    """

    __tablename__ = "digital_twins"

    # Core Identity
    id = Column(String(36), primary_key=True, default=_uid)
    fan_id = Column(String(36), ForeignKey("digital_fans.id"), nullable=False)

    # Persistent Memory Storage
    memory_data = Column(JSON, default=dict)  # Complete memory storage
    personality_traits = Column(JSON, default=[])
    learning_history = Column(JSON, default=dict)  # AI learning patterns

    # Visit History
    total_visits = Column(Integer, default=1)
    first_visit = Column(DateTime(timezone=True), default=_now)
    last_visit = Column(DateTime(timezone=True), default=_now)

    # Behavioral Memory
    favorite_foods = Column(JSON, default=[])
    preferred_seats = Column(JSON, default=[])
    usual_companions = Column(JSON, default=[])
    spending_pattern = Column(JSON, default=dict)

    # Navigation Memory
    preferred_routes = Column(JSON, default=dict)
    avoided_areas = Column(JSON, default=[])
    navigation_speed_history = Column(JSON, default=[])

    # Interaction Memory
    volunteer_interactions = Column(JSON, default=dict)
    medical_history = Column(JSON, default=dict)
    complaints_feedback = Column(JSON, default=dict)

    # Prediction Memory
    prediction_accuracy_score = Column(Float, default=0.5)
    behavior_patterns = Column(JSON, default=dict)
    emotion_patterns = Column(JSON, default=dict)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=_now)
    updated_at = Column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )

    # Relationships
    fan = relationship("DigitalFan", back_populates="twin")
    memories = relationship(
        "TwinMemory", back_populates="twin", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<DigitalTwin(fan_id={self.fan_id}, visits={self.total_visits})>"

    def add_memory(self, category: str, data: Dict[str, Any], importance: float = 0.5):
        """Add a new memory to the twin's memory system"""
        if not self.memory_data:
            self.memory_data = {}

        if category not in self.memory_data:
            self.memory_data[category] = []

        memory_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
            "importance": importance,
            "recall_count": 0,
        }

        self.memory_data[category].append(memory_entry)

        # Keep only most important memories (max 50 per category)
        if len(self.memory_data[category]) > 50:
            self.memory_data[category].sort(key=lambda x: x["importance"], reverse=True)
            self.memory_data[category] = self.memory_data[category][:50]

    def recall_memories(self, category: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recall memories from a specific category"""
        if not self.memory_data or category not in self.memory_data:
            return []

        memories = self.memory_data[category]

        # Sort by importance and recency
        sorted_memories = sorted(
            memories, key=lambda x: (x["importance"], x["timestamp"]), reverse=True
        )

        # Update recall count for accessed memories
        for memory in sorted_memories[:limit]:
            memory["recall_count"] += 1

        return sorted_memories[:limit]

    def get_personality_description(self) -> str:
        """Generate natural language personality description"""
        if not self.personality_traits:
            return "Adaptable stadium visitor with standard preferences"

        trait_descriptions = {
            PersonalityTrait.SOCIAL: "enjoys interacting with other fans",
            PersonalityTrait.ADVENTUROUS: "likes exploring new areas of the stadium",
            PersonalityTrait.CAUTIOUS: "prefers familiar routes and seating",
            PersonalityTrait.IMPATIENT: "dislikes waiting in long queues",
            PersonalityTrait.PATIENT: "comfortable with waiting and delays",
            PersonalityTrait.CURIOUS: "interested in stadium features and amenities",
            PersonalityTrait.PRACTICAL: "focuses on essentials and efficiency",
            PersonalityTrait.SPONTANEOUS: "makes quick, impulse decisions",
            PersonalityTrait.LOYAL: "returns to same vendors and seats",
            PersonalityTrait.INDEPENDENT: "prefers navigating alone",
            PersonalityTrait.FAMILY_ORIENTED: "prioritizes group coordination",
            PersonalityTrait.BUDGET_CONSCIOUS: "carefully considers spending",
        }

        descriptions = [
            trait_descriptions.get(trait, trait.value)
            for trait in self.personality_traits[:3]
        ]
        return f"Fan who {', '.join(descriptions)}"

    def update_learning_patterns(
        self, prediction_accuracy: float, behavior_change: Dict[str, Any]
    ):
        """Update AI learning patterns based on prediction accuracy"""
        if not self.learning_history:
            self.learning_history = {"accuracy_history": [], "behavior_changes": []}

        self.learning_history["accuracy_history"].append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "accuracy": prediction_accuracy,
            }
        )

        self.learning_history["behavior_changes"].append(
            {"timestamp": datetime.utcnow().isoformat(), "change": behavior_change}
        )

        # Update overall prediction accuracy score
        accuracies = [
            entry["accuracy"]
            for entry in self.learning_history["accuracy_history"][-20:]
        ]
        self.prediction_accuracy_score = sum(accuracies) / len(accuracies)

    def to_memory_dict(self) -> Dict[str, Any]:
        """Convert twin memory to dictionary for AI processing"""
        return {
            "identity": {
                "fan_id": str(self.fan_id),
                "total_visits": self.total_visits,
                "personality": [trait.value for trait in self.personality_traits],
                "prediction_accuracy": self.prediction_accuracy_score,
            },
            "preferences": {
                "favorite_foods": self.favorite_foods,
                "preferred_seats": self.preferred_seats,
                "spending_pattern": self.spending_pattern,
                "usual_companions": self.usual_companions,
            },
            "navigation": {
                "preferred_routes": self.preferred_routes,
                "avoided_areas": self.avoided_areas,
                "avg_speed": sum(self.navigation_speed_history[-10:])
                / len(self.navigation_speed_history[-10:])
                if self.navigation_speed_history
                else 1.2,
            },
            "interactions": {
                "volunteer_history": self.volunteer_interactions,
                "medical_history": self.medical_history,
                "feedback_history": self.complaints_feedback,
            },
            "recent_memories": {
                category: self.recall_memories(category, 5)
                for category in [
                    "visits",
                    "purchases",
                    "interactions",
                    "navigation",
                    "emotions",
                ]
                if category in (self.memory_data or {})
            },
        }


class TwinMemory(Base):
    """
    Individual memory entries for Digital Twins
    Detailed storage of specific events and experiences
    """

    __tablename__ = "twin_memories"

    id = Column(String(36), primary_key=True, default=_uid)
    twin_id = Column(String(36), ForeignKey("digital_twins.id"), nullable=False)

    # Memory Classification
    category = Column(
        String(50), nullable=False
    )  # visits, purchases, interactions, navigation, emotions
    subcategory = Column(String(50))
    importance = Column(Float, default=0.5)  # 0.0 to 1.0

    # Memory Content
    title = Column(String(200), nullable=False)
    description = Column(Text)
    data = Column(JSON, default=dict)

    # Context
    location = Column(String)
    related_entities = Column(
        ARRAY(String), default=[]
    )  # volunteer IDs, facility IDs, etc.
    emotional_context = Column(String(50))

    # Memory Lifecycle
    created_at = Column(DateTime(timezone=True), default=_now)
    last_recalled = Column(DateTime(timezone=True))
    recall_count = Column(Integer, default=0)
    memory_strength = Column(Float, default=1.0)  # Decays over time

    # Relationships
    twin = relationship("DigitalTwin", back_populates="memories")

    def __repr__(self):
        return f"<TwinMemory(category={self.category}, title={self.title})>"

    def recall(self):
        """Record that this memory has been recalled"""
        self.last_recalled = _now
        self.recall_count += 1
        # Strengthen memory through recall
        self.memory_strength = min(1.0, self.memory_strength + 0.1)

    def decay(self, days_passed: int):
        """Apply memory decay based on time and importance"""
        if self.importance < 0.8:  # Important memories don't decay as much
            decay_rate = 0.01 * days_passed * (1 - self.importance)
            self.memory_strength = max(0.1, self.memory_strength - decay_rate)

    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary"""
        return {
            "id": str(self.id),
            "category": self.category,
            "subcategory": self.subcategory,
            "title": self.title,
            "description": self.description,
            "data": self.data,
            "importance": self.importance,
            "emotional_context": self.emotional_context,
            "location": [self.location.x, self.location.y] if self.location else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_recalled": self.last_recalled.isoformat()
            if self.last_recalled
            else None,
            "recall_count": self.recall_count,
            "memory_strength": self.memory_strength,
        }


class DigitalFan(Base):
    """
    Enhanced AI Digital Twin for each stadium visitor - V2 Living Brain
    Now with persistent memory, personality traits, and advanced behavioral modeling
    """

    __tablename__ = "digital_fans"

    # Primary identification
    id = Column(String(36), primary_key=True, default=_uid)
    fan_id = Column(
        String(20), unique=True, nullable=False, index=True
    )  # F001, F002, etc.
    name = Column(String(100), nullable=False)

    # Demographics and preferences
    country = Column(String(3), nullable=False)  # ISO country code
    language = Column(String(10), nullable=False, default="en")
    age = Column(Integer, nullable=False)
    accessibility_needs = Column(
        ENUM(AccessibilityNeed), default=AccessibilityNeed.NONE
    )
    favorite_team = Column(String(100))

    # V2 Enhancement: Personality Profile
    personality_traits = Column(JSON, default=[])
    persona_backstory = Column(Text)  # Generated unique backstory
    travel_group_size = Column(Integer, default=1)
    travel_companions = Column(JSON, default=[])

    # Current emotional and physical state
    current_emotion = Column(String(50), default=FanEmotion.NEUTRAL)
    stress_level = Column(Integer, default=50)  # 0-100
    excitement_level = Column(Integer, default=50)  # 0-100
    walking_speed = Column(Float, default=1.2)  # m/s
    hunger_level = Column(Integer, default=30)  # 0-100
    fatigue_level = Column(Integer, default=20)  # 0-100
    battery_level = Column(Integer, default=80)  # 0-100 for mobile device

    # V2 Enhancement: Emotion History
    emotion_history = Column(JSON, default=dict)  # Track emotion changes over time
    stress_triggers = Column(
        ARRAY(String), default=[]
    )  # What causes stress for this fan
    happiness_factors = Column(JSON, default=[])  # What makes this fan happy

    # Location and movement
    current_location = Column(String, nullable=False)
    destination = Column(String)
    transportation = Column(String(50), default=TransportMode.WALKING)

    # V2 Enhancement: Location Memory
    visited_zones = Column(JSON, default=[])
    favorite_locations = Column(JSON, default=dict)
    avoided_locations = Column(JSON, default=[])
    arrival_time = Column(DateTime(timezone=True))
    predicted_departure = Column(DateTime(timezone=True))

    # Behavioral patterns and tendencies
    purchase_intent = Column(Integer, default=30)  # 0-100 likelihood to purchase
    medical_risk_score = Column(Integer, default=10)  # 0-100 health risk
    lost_probability = Column(Float, default=0.05)  # 0.0-1.0 chance of getting lost
    queue_tolerance = Column(Integer, default=60)  # 0-100 patience for queues
    risk_score = Column(Integer, default=20)  # 0-100 overall safety risk

    # V2 Enhancement: Purchase and Interaction History
    purchase_history = Column(JSON, default=dict)
    food_preferences = Column(JSON, default=[])
    dietary_restrictions = Column(JSON, default=[])
    spending_budget = Column(Float, default=50.0)
    volunteer_interactions = Column(JSON, default=dict)

    # AI predictions and reasoning
    predicted_next_action = Column(Text)
    prediction_confidence = Column(Float)  # 0.0-1.0
    predicted_exit_time = Column(DateTime(timezone=True))
    prediction_reasoning = Column(Text)  # V2: Why AI made this prediction

    # V2 Enhancement: Future Branches
    future_branches = Column(JSON, default=dict)  # Best/Likely/Worst predictions
    last_prediction_accuracy = Column(Float, default=0.5)

    # Metadata and tracking
    created_at = Column(DateTime(timezone=True), default=_now)
    updated_at = Column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )
    is_active = Column(Boolean, default=True)

    # V2 Enhancement: Living Brain tracking
    last_ai_update = Column(DateTime(timezone=True), default=_now)
    ai_agent_notes = Column(JSON, default=dict)  # Notes from different AI agents
    collective_intelligence_score = Column(Float, default=0.5)

    # Relationships
    twin = relationship(
        "DigitalTwin", back_populates="fan", uselist=False, cascade="all, delete-orphan"
    )
    movements = relationship(
        "FanMovement", back_populates="fan", cascade="all, delete-orphan"
    )
    predictions = relationship(
        "FanPrediction", back_populates="fan", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<DigitalFan(id={self.fan_id}, name={self.name}, emotion={self.current_emotion})>"

    def get_personality_summary(self) -> str:
        """Generate a natural language personality summary"""
        if self.persona_backstory:
            return (
                self.persona_backstory[:200] + "..."
                if len(self.persona_backstory) > 200
                else self.persona_backstory
            )

        traits = (
            [trait.value for trait in self.personality_traits]
            if self.personality_traits
            else []
        )
        if not traits:
            return "Typical stadium visitor with adaptable preferences"

        return (
            f"A {traits[0]} fan who is {traits[1] if len(traits) > 1 else 'adaptable'}"
        )

    def update_emotion(
        self, new_emotion: FanEmotion, trigger: str = None, intensity: float = 1.0
    ):
        """Update fan emotion with history tracking"""
        old_emotion = self.current_emotion
        self.current_emotion = new_emotion

        # Update emotion history
        if not self.emotion_history:
            self.emotion_history = {"changes": [], "patterns": {}}

        change_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "from": old_emotion.value if old_emotion else "unknown",
            "to": new_emotion.value,
            "trigger": trigger,
            "intensity": intensity,
        }

        self.emotion_history["changes"].append(change_entry)

        # Keep only last 50 changes
        if len(self.emotion_history["changes"]) > 50:
            self.emotion_history["changes"] = self.emotion_history["changes"][-50:]

        # Update stress/excitement based on emotion
        emotion_effects = {
            FanEmotion.EXCITED: {"excitement": +20, "stress": -5},
            FanEmotion.JOYFUL: {"excitement": +15, "stress": -10},
            FanEmotion.ANGRY: {"stress": +25, "excitement": -10},
            FanEmotion.STRESSED: {"stress": +30, "excitement": -5},
            FanEmotion.FEARFUL: {"stress": +35, "excitement": -15},
            FanEmotion.TIRED: {"fatigue": +15, "excitement": -10},
            FanEmotion.CONFUSED: {"stress": +10, "lost_probability": +0.1},
        }

        if new_emotion in emotion_effects:
            effects = emotion_effects[new_emotion]
            for attribute, change in effects.items():
                if attribute in ["stress", "excitement", "fatigue"]:
                    current_value = getattr(self, f"{attribute}_level")
                    new_value = max(0, min(100, current_value + change))
                    setattr(self, f"{attribute}_level", new_value)
                elif attribute == "lost_probability":
                    self.lost_probability = max(
                        0.0, min(1.0, self.lost_probability + change)
                    )

    def add_memory_to_twin(
        self, category: str, title: str, data: Dict[str, Any], importance: float = 0.5
    ):
        """Add memory to associated digital twin"""
        if not self.twin:
            # Create twin if it doesn't exist
            from .fan import DigitalTwin

            self.twin = DigitalTwin(fan_id=self.id)

        self.twin.add_memory(category, {"title": title, **data}, importance)

    def generate_future_branches(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate best/likely/worst future scenarios"""
        base_time = datetime.utcnow()

        branches = {
            "best_case": {
                "description": "Optimal experience with minimal wait times",
                "stress_level": max(0, self.stress_level - 20),
                "satisfaction": 90,
                "exit_time": base_time.replace(hour=22, minute=30),
                "spending": self.spending_budget * 0.8,
                "key_events": ["Quick food service", "Great seat view", "Easy exit"],
            },
            "most_likely": {
                "description": "Expected experience based on current patterns",
                "stress_level": self.stress_level,
                "satisfaction": 70,
                "exit_time": base_time.replace(hour=23, minute=0),
                "spending": self.spending_budget,
                "key_events": [
                    "Normal queue times",
                    "Standard service",
                    "Typical exit",
                ],
            },
            "worst_case": {
                "description": "Challenging conditions with delays",
                "stress_level": min(100, self.stress_level + 30),
                "satisfaction": 40,
                "exit_time": base_time.replace(hour=23, minute=45),
                "spending": self.spending_budget * 1.2,
                "key_events": ["Long queues", "Service delays", "Crowded exits"],
            },
        }

        self.future_branches = branches
        return branches

    def to_dict(self) -> Dict[str, Any]:
        """Convert fan to dictionary for API responses with V2 enhancements"""
        return {
            "id": str(self.id),
            "fan_id": self.fan_id,
            "name": self.name,
            "country": self.country,
            "language": self.language,
            "age": self.age,
            "accessibility_needs": self.accessibility_needs.value
            if self.accessibility_needs
            else None,
            "favorite_team": self.favorite_team,
            # V2 Personality
            "personality_traits": [trait.value for trait in self.personality_traits]
            if self.personality_traits
            else [],
            "personality_summary": self.get_personality_summary(),
            "travel_group_size": self.travel_group_size,
            # Current state
            "current_emotion": self.current_emotion.value
            if self.current_emotion
            else None,
            "stress_level": self.stress_level,
            "excitement_level": self.excitement_level,
            "walking_speed": self.walking_speed,
            "hunger_level": self.hunger_level,
            "fatigue_level": self.fatigue_level,
            "battery_level": self.battery_level,
            # Location and preferences
            "current_coordinates": self.get_current_coordinates(),
            "destination_coordinates": self.get_destination_coordinates(),
            "transportation": self.transportation.value
            if self.transportation
            else None,
            "visited_zones": self.visited_zones,
            "food_preferences": self.food_preferences,
            # Behavioral patterns
            "purchase_intent": self.purchase_intent,
            "medical_risk_score": self.medical_risk_score,
            "lost_probability": self.lost_probability,
            "queue_tolerance": self.queue_tolerance,
            "risk_score": self.risk_score,
            # AI predictions with V2 reasoning
            "predicted_next_action": self.predicted_next_action,
            "prediction_confidence": self.prediction_confidence,
            "prediction_reasoning": self.prediction_reasoning,
            "predicted_exit_time": self.predicted_exit_time.isoformat()
            if self.predicted_exit_time
            else None,
            # V2 Future branches
            "future_branches": self.future_branches,
            "last_prediction_accuracy": self.last_prediction_accuracy,
            "collective_intelligence_score": self.collective_intelligence_score,
            # Metadata
            "is_active": self.is_active,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_ai_update": self.last_ai_update.isoformat()
            if self.last_ai_update
            else None,
        }

    def get_current_coordinates(self):
        """Get current location as [lng, lat] for frontend"""
        if self.current_location:
            # Note: PostGIS stores as (x, y) = (longitude, latitude)
            return [self.current_location.x, self.current_location.y]
        return None

    def get_destination_coordinates(self):
        """Get destination as [lng, lat] for frontend"""
        if self.destination:
            return [self.destination.x, self.destination.y]
        return None

    def update_emotion_based_on_event(self, event_type: str):
        """Update fan emotion based on stadium events"""
        emotion_mappings = {
            "goal_own_team": FanEmotion.EXCITED,
            "goal_opponent": FanEmotion.ANGRY,
            "rain_start": FanEmotion.STRESSED,
            "long_queue": FanEmotion.ANGRY,
            "medical_emergency": FanEmotion.FEARFUL,
            "lost_child": FanEmotion.STRESSED,
            "halftime": FanEmotion.TIRED,
        }

        new_emotion = emotion_mappings.get(event_type)
        if new_emotion:
            self.current_emotion = new_emotion

            # Update related metrics
            if new_emotion in [
                FanEmotion.STRESSED,
                FanEmotion.ANGRY,
                FanEmotion.FEARFUL,
            ]:
                self.stress_level = min(100, self.stress_level + 20)
                self.risk_score = min(100, self.risk_score + 10)
            elif new_emotion == FanEmotion.EXCITED:
                self.excitement_level = min(100, self.excitement_level + 30)
                self.stress_level = max(0, self.stress_level - 10)

    def calculate_movement_speed(self) -> float:
        """Calculate current movement speed based on various factors"""
        base_speed = self.walking_speed

        # Adjust for fatigue
        fatigue_factor = 1.0 - (self.fatigue_level / 200)

        # Adjust for stress (stressed people move faster or slower)
        if self.stress_level > 70:
            stress_factor = 1.2  # Move faster when stressed
        elif self.stress_level < 30:
            stress_factor = 0.9  # Move slower when relaxed
        else:
            stress_factor = 1.0

        # Adjust for accessibility needs
        accessibility_factor = (
            0.7 if self.accessibility_needs != AccessibilityNeed.NONE else 1.0
        )

        return base_speed * fatigue_factor * stress_factor * accessibility_factor


class FanMovement(Base):
    """
    Historical movement data for digital fans
    Tracks fan positions over time for analysis and learning
    """

    __tablename__ = "fan_movements"

    id = Column(String(36), primary_key=True, default=_uid)
    fan_id = Column(String(36), ForeignKey("digital_fans.id"), nullable=False)
    location = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=_now)
    speed = Column(Float)  # m/s
    direction = Column(Float)  # degrees from north
    zone_id = Column(String(36), ForeignKey("stadium_zones.id"))

    # Relationships
    fan = relationship("DigitalFan", back_populates="movements")
    zone = relationship("StadiumZone")

    def __repr__(self):
        return f"<FanMovement(fan_id={self.fan_id}, timestamp={self.timestamp})>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "fan_id": str(self.fan_id),
            "coordinates": [self.location.x, self.location.y]
            if self.location
            else None,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "speed": self.speed,
            "direction": self.direction,
            "zone_id": str(self.zone_id) if self.zone_id else None,
        }


class FanPrediction(Base):
    """
    AI-generated predictions for fan behavior
    Stores predictions with confidence scores for validation and learning
    """

    __tablename__ = "fan_predictions"

    id = Column(String(36), primary_key=True, default=_uid)
    fan_id = Column(String(36), ForeignKey("digital_fans.id"), nullable=False)
    prediction_type = Column(String(50), nullable=False)
    predicted_location = Column(String)
    predicted_time = Column(DateTime(timezone=True), nullable=False)
    confidence_score = Column(Float, nullable=False)  # 0.0-1.0
    prediction_data = Column(JSON)  # Flexible storage for prediction details
    actual_outcome = Column(JSON)  # For learning and validation
    created_at = Column(DateTime(timezone=True), default=_now)
    expires_at = Column(DateTime(timezone=True))
    is_accurate = Column(Boolean)  # Set after validation

    # Relationships
    fan = relationship("DigitalFan", back_populates="predictions")

    def __repr__(self):
        return f"<FanPrediction(fan_id={self.fan_id}, type={self.prediction_type}, confidence={self.confidence_score})>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "fan_id": str(self.fan_id),
            "prediction_type": self.prediction_type.value
            if self.prediction_type
            else None,
            "predicted_coordinates": [
                self.predicted_location.x,
                self.predicted_location.y,
            ]
            if self.predicted_location
            else None,
            "predicted_time": self.predicted_time.isoformat()
            if self.predicted_time
            else None,
            "confidence_score": self.confidence_score,
            "prediction_data": self.prediction_data,
            "actual_outcome": self.actual_outcome,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_accurate": self.is_accurate,
        }

    def validate_prediction(self, actual_data: dict) -> bool:
        """Validate prediction against actual outcome"""
        self.actual_outcome = actual_data

        # Simple validation logic - can be made more sophisticated
        if self.prediction_type == PredictionType.MOVEMENT:
            predicted_coords = [self.predicted_location.x, self.predicted_location.y]
            actual_coords = actual_data.get("coordinates", [])

            if predicted_coords and actual_coords:
                # Calculate distance between predicted and actual
                distance = (
                    (predicted_coords[0] - actual_coords[0]) ** 2
                    + (predicted_coords[1] - actual_coords[1]) ** 2
                ) ** 0.5

                # Consider accurate if within 50 meters (rough conversion)
                self.is_accurate = distance < 0.0005  # Approximate degrees
                return self.is_accurate

        return False

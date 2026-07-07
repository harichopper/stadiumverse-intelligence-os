"""
StadiumVerse AI - Digital Twin Engine
Core AI system that updates and manages digital twins of all fans
Updates every 5 seconds with predictive behavior modeling
"""

import asyncio
import logging
import random
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import AsyncSessionLocal
from ..models.fan import (
    DigitalFan,
    FanMovement,
    FanPrediction,
    FanEmotion,
    PredictionType,
)
from ..config import settings, STADIUM_ZONES
from ..ai.llm.openai_client import OpenAIClient
from ..ai.agents.navigation_agent import NavigationAgent

logger = logging.getLogger(__name__)


class DigitalTwinEngine:
    """
    Core engine for managing AI Digital Twins
    - Updates all fan states every 5 seconds
    - Predicts future behavior and movements
    - Simulates realistic fan interactions
    - Learns from historical patterns
    """

    def __init__(self):
        self.openai_client = OpenAIClient()
        self.navigation_agent = NavigationAgent()
        self.is_running = False
        self.update_count = 0
        self.performance_metrics = {
            "total_updates": 0,
            "average_update_time": 0,
            "prediction_accuracy": 0,
            "fans_processed": 0,
        }

        # Stadium layout for pathfinding
        self.stadium_layout = self._initialize_stadium_layout()

        # Behavioral patterns
        self.behavior_patterns = self._initialize_behavior_patterns()

        logger.info("Digital Twin Engine initialized")

    def _initialize_stadium_layout(self) -> Dict[str, Any]:
        """Initialize stadium layout data for movement calculations"""
        return {
            "center": settings.STADIUM_COORDINATES["center"],
            "bounds": settings.STADIUM_COORDINATES["bounds"],
            "zones": STADIUM_ZONES,
            "pathfinding_nodes": self._generate_pathfinding_nodes(),
            "crowd_flow_vectors": self._initialize_crowd_flow(),
        }

    def _generate_pathfinding_nodes(self) -> List[Dict[str, Any]]:
        """Generate pathfinding nodes for realistic movement"""
        nodes = []

        # Add major landmarks
        landmarks = [
            {"id": "main_entrance", "coords": [40.8135, -74.0745], "type": "entrance"},
            {"id": "north_plaza", "coords": [40.8145, -74.0745], "type": "food_court"},
            {"id": "south_plaza", "coords": [40.8125, -74.0745], "type": "food_court"},
            {"id": "medical_center", "coords": [40.8135, -74.0745], "type": "medical"},
            {
                "id": "security_office",
                "coords": [40.8140, -74.0750],
                "type": "security",
            },
        ]

        for landmark in landmarks:
            nodes.append(landmark)

        # Add gates
        for gate_id, gate_data in STADIUM_ZONES["gates"].items():
            nodes.append(
                {
                    "id": f"gate_{gate_id.lower()}",
                    "coords": gate_data["coordinates"],
                    "type": "gate",
                    "capacity": gate_data["capacity"],
                }
            )

        # Add restrooms
        for restroom_id, restroom_data in STADIUM_ZONES["restrooms"].items():
            nodes.append(
                {
                    "id": f"restroom_{restroom_id.lower()}",
                    "coords": restroom_data["coordinates"],
                    "type": "restroom",
                    "capacity": restroom_data["capacity"],
                }
            )

        return nodes

    def _initialize_crowd_flow(self) -> Dict[str, List[float]]:
        """Initialize crowd flow vectors for different areas"""
        return {
            "entrance_flow": [0.0, -0.5],  # Moving inward
            "exit_flow": [0.0, 0.5],  # Moving outward
            "concourse_flow": [0.3, 0.0],  # Lateral movement
            "emergency_flow": [0.0, 1.0],  # Moving toward exits
        }

    def _initialize_behavior_patterns(self) -> Dict[str, Any]:
        """Initialize behavioral patterns for different fan types"""
        return {
            "excited_fan": {
                "movement_speed_multiplier": 1.3,
                "queue_tolerance": 0.4,
                "purchase_probability": 0.7,
                "social_interaction_radius": 20,
                "decision_change_rate": 0.3,
            },
            "family_group": {
                "movement_speed_multiplier": 0.8,
                "queue_tolerance": 0.6,
                "purchase_probability": 0.8,
                "social_interaction_radius": 5,
                "decision_change_rate": 0.1,
            },
            "elderly_fan": {
                "movement_speed_multiplier": 0.6,
                "queue_tolerance": 0.3,
                "purchase_probability": 0.4,
                "social_interaction_radius": 10,
                "decision_change_rate": 0.1,
            },
            "young_adult": {
                "movement_speed_multiplier": 1.4,
                "queue_tolerance": 0.5,
                "purchase_probability": 0.9,
                "social_interaction_radius": 30,
                "decision_change_rate": 0.4,
            },
        }

    async def start_engine(self):
        """Start the digital twin engine"""
        self.is_running = True
        logger.info("Digital Twin Engine started")

        while self.is_running:
            try:
                start_time = datetime.utcnow()

                # Update all digital twins
                updated_fans = await self.update_all_fans()

                # Calculate performance metrics
                update_time = (datetime.utcnow() - start_time).total_seconds()
                self._update_performance_metrics(update_time, len(updated_fans))

                # Log progress
                if self.update_count % 10 == 0:  # Every 50 seconds
                    logger.info(
                        f"Digital Twin Engine: Updated {len(updated_fans)} fans in {update_time:.2f}s"
                    )

                self.update_count += 1

                # Wait for next update cycle
                await asyncio.sleep(settings.AI_UPDATE_INTERVAL)

            except Exception as e:
                logger.error(f"Digital Twin Engine error: {e}")
                await asyncio.sleep(5)  # Wait before retrying

    def stop_engine(self):
        """Stop the digital twin engine"""
        self.is_running = False
        logger.info("Digital Twin Engine stopped")

    async def update_all_fans(self) -> List[Dict[str, Any]]:
        """Update all active digital twins"""
        updated_fans = []

        async with AsyncSessionLocal() as session:
            # Get all active fans
            result = await session.execute(
                select(DigitalFan).where(DigitalFan.is_active)
            )
            fans = result.scalars().all()

            # Update each fan
            for fan in fans:
                try:
                    updated_fan = await self._update_single_fan(session, fan)
                    if updated_fan:
                        updated_fans.append(updated_fan)
                except Exception as e:
                    logger.error(f"Error updating fan {fan.fan_id}: {e}")

            await session.commit()

        return updated_fans

    async def _update_single_fan(
        self, session: AsyncSession, fan: DigitalFan
    ) -> Optional[Dict[str, Any]]:
        """Update a single digital twin with AI predictions"""

        # 1. Update fan's current state
        await self._update_fan_state(fan)

        # 2. Predict next movement
        next_location = await self._predict_fan_movement(fan)

        # 3. Update fan's location if they're moving
        if next_location:
            await self._move_fan(session, fan, next_location)

        # 4. Update behavioral patterns
        await self._update_fan_behavior(fan)

        # 5. Generate predictions
        await self._generate_fan_predictions(session, fan)

        # 6. Update emotion based on context
        await self._update_fan_emotion(fan)

        # 7. Save movement history
        await self._save_movement_history(session, fan)

        return fan.to_dict()

    async def _update_fan_state(self, fan: DigitalFan):
        """Update fan's physical and emotional state"""

        # Update fatigue based on time and activity
        time_factor = 0.1  # Fatigue increases over time
        fan.fatigue_level = min(100, fan.fatigue_level + time_factor)

        # Update hunger based on time since last meal
        hunger_increase = random.uniform(0.5, 1.5)
        fan.hunger_level = min(100, fan.hunger_level + hunger_increase)

        # Update battery level (phone/device)
        battery_drain = random.uniform(0.1, 0.3)
        fan.battery_level = max(0, fan.battery_level - battery_drain)

        # Adjust walking speed based on fatigue and age
        base_speed = 1.2
        age_factor = max(0.5, 1.0 - (fan.age - 25) * 0.01)  # Slower as age increases
        fatigue_factor = max(0.5, 1.0 - fan.fatigue_level * 0.005)

        fan.walking_speed = base_speed * age_factor * fatigue_factor

        # Update stress level based on various factors
        stress_factors = 0
        if fan.hunger_level > 70:
            stress_factors += 5
        if fan.fatigue_level > 60:
            stress_factors += 3
        if fan.battery_level < 20:
            stress_factors += 2

        fan.stress_level = min(100, max(0, fan.stress_level + stress_factors - 2))

    async def _predict_fan_movement(
        self, fan: DigitalFan
    ) -> Optional[Tuple[float, float]]:
        """Predict where the fan will move next"""

        current_coords = fan.get_current_coordinates()
        if not current_coords:
            return None

        # Decision-making factors
        decisions = []

        # 1. Hunger-based decisions
        if fan.hunger_level > 60:
            food_courts = self._get_nearest_facilities("food_court", current_coords)
            if food_courts:
                decisions.append(("food", food_courts[0], 0.7))

        # 2. Fatigue-based decisions
        if fan.fatigue_level > 70:
            restrooms = self._get_nearest_facilities("restroom", current_coords)
            if restrooms:
                decisions.append(("rest", restrooms[0], 0.6))

        # 3. Random exploration
        if random.random() < 0.3:  # 30% chance of random movement
            exploration_target = self._generate_exploration_target(current_coords)
            decisions.append(("explore", exploration_target, 0.4))

        # 4. Social following (follow other fans)
        social_target = await self._find_social_target(fan)
        if social_target:
            decisions.append(("social", social_target, 0.5))

        # Select decision based on weights and fan personality
        if decisions:
            # Weight decisions based on fan characteristics
            weighted_decisions = []
            for decision_type, target, base_weight in decisions:
                weight = base_weight * self._get_decision_weight(fan, decision_type)
                weighted_decisions.append((decision_type, target, weight))

            # Choose decision probabilistically
            total_weight = sum(w for _, _, w in weighted_decisions)
            if total_weight > 0:
                rand = random.uniform(0, total_weight)
                cumulative = 0

                for decision_type, target, weight in weighted_decisions:
                    cumulative += weight
                    if rand <= cumulative:
                        return self._calculate_next_position(
                            current_coords, target, fan
                        )

        return None

    def _get_nearest_facilities(
        self, facility_type: str, current_coords: List[float]
    ) -> List[Tuple[float, float]]:
        """Find nearest facilities of a given type"""
        facilities = []

        if facility_type == "food_court":
            for name, data in STADIUM_ZONES["food_courts"].items():
                distance = self._calculate_distance(current_coords, data["coordinates"])
                facilities.append((data["coordinates"], distance))
        elif facility_type == "restroom":
            for name, data in STADIUM_ZONES["restrooms"].items():
                distance = self._calculate_distance(current_coords, data["coordinates"])
                facilities.append((data["coordinates"], distance))

        # Sort by distance and return coordinates
        facilities.sort(key=lambda x: x[1])
        return [coords for coords, _ in facilities[:3]]  # Return top 3 nearest

    def _calculate_distance(self, coord1: List[float], coord2: List[float]) -> float:
        """Calculate distance between two coordinates"""
        dx = coord1[0] - coord2[0]
        dy = coord1[1] - coord2[1]
        return math.sqrt(dx * dx + dy * dy)

    def _generate_exploration_target(
        self, current_coords: List[float]
    ) -> Tuple[float, float]:
        """Generate a random exploration target near current position"""
        # Generate random movement within stadium bounds
        bounds = settings.STADIUM_COORDINATES["bounds"]

        # Move within a reasonable radius
        max_movement = 0.001  # Roughly 100 meters
        dx = random.uniform(-max_movement, max_movement)
        dy = random.uniform(-max_movement, max_movement)

        new_x = max(bounds["west"], min(bounds["east"], current_coords[0] + dx))
        new_y = max(bounds["south"], min(bounds["north"], current_coords[1] + dy))

        return (new_x, new_y)

    async def _find_social_target(
        self, fan: DigitalFan
    ) -> Optional[Tuple[float, float]]:
        """Find other fans to follow (social behavior)"""
        # For now, return None - can be enhanced with actual social graph
        return None

    def _get_decision_weight(self, fan: DigitalFan, decision_type: str) -> float:
        """Get weight multiplier for decision based on fan characteristics"""
        weights = {
            "food": 1.0 + (fan.hunger_level - 50) * 0.01,
            "rest": 1.0 + (fan.fatigue_level - 50) * 0.01,
            "explore": 1.0 if fan.age < 40 else 0.5,
            "social": 1.0 if fan.age < 35 else 0.7,
        }

        return max(0.1, weights.get(decision_type, 1.0))

    def _calculate_next_position(
        self, current: List[float], target: Tuple[float, float], fan: DigitalFan
    ) -> Tuple[float, float]:
        """Calculate next position moving toward target"""

        # Calculate direction vector
        dx = target[0] - current[0]
        dy = target[1] - current[1]
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 0.0001:  # Already at target
            return target

        # Normalize direction
        dx /= distance
        dy /= distance

        # Calculate movement step based on walking speed
        # Convert walking speed (m/s) to coordinate delta (rough approximation)
        speed_in_coords = fan.walking_speed * 0.00001 * settings.AI_UPDATE_INTERVAL

        # Apply some randomness for realistic movement
        noise_factor = 0.2
        dx += random.uniform(-noise_factor, noise_factor) * dx
        dy += random.uniform(-noise_factor, noise_factor) * dy

        # Calculate new position
        new_x = current[0] + dx * speed_in_coords
        new_y = current[1] + dy * speed_in_coords

        # Ensure we don't go outside stadium bounds
        bounds = settings.STADIUM_COORDINATES["bounds"]
        new_x = max(bounds["west"], min(bounds["east"], new_x))
        new_y = max(bounds["south"], min(bounds["north"], new_y))

        return (new_x, new_y)

    async def _move_fan(
        self, session: AsyncSession, fan: DigitalFan, new_location: Tuple[float, float]
    ):
        """Move fan to new location"""
        from geoalchemy2 import WKTElement

        # Update fan location
        fan.current_location = WKTElement(
            f"POINT({new_location[0]} {new_location[1]})", srid=4326
        )

        # Update destination if reached
        if fan.destination:
            dest_coords = fan.get_destination_coordinates()
            if dest_coords:
                distance_to_dest = self._calculate_distance(
                    [new_location[0], new_location[1]], dest_coords
                )
                if distance_to_dest < 0.0002:  # Reached destination
                    fan.destination = None
                    fan.predicted_next_action = "Reached destination"

    async def _update_fan_behavior(self, fan: DigitalFan):
        """Update fan behavioral patterns"""

        # Update purchase intent based on location and needs
        if fan.hunger_level > 60:
            fan.purchase_intent = min(100, fan.purchase_intent + 5)
        else:
            fan.purchase_intent = max(0, fan.purchase_intent - 2)

        # Update medical risk based on age, fatigue, and stress
        base_risk = 5
        age_risk = max(0, (fan.age - 60) * 0.5) if fan.age > 60 else 0
        fatigue_risk = fan.fatigue_level * 0.2
        stress_risk = fan.stress_level * 0.1

        fan.medical_risk_score = int(
            min(100, base_risk + age_risk + fatigue_risk + stress_risk)
        )

        # Update overall risk score
        risk_factors = [
            fan.medical_risk_score * 0.3,
            fan.stress_level * 0.2,
            (100 - fan.battery_level) * 0.1,
            fan.fatigue_level * 0.2,
            (fan.lost_probability * 100) * 0.2,
        ]

        fan.risk_score = int(min(100, sum(risk_factors)))

    async def _generate_fan_predictions(
        self, session: AsyncSession, fan: DigitalFan
    ) -> List[FanPrediction]:
        """Generate AI predictions for fan behavior"""
        predictions = []

        current_time = datetime.utcnow()

        # Movement prediction
        if random.random() < 0.8:  # Generate movement prediction 80% of the time
            predicted_time = current_time + timedelta(minutes=random.randint(5, 30))

            # Predict future location based on current trajectory and behavior
            future_location = await self._predict_future_location(fan, predicted_time)

            if future_location:
                from geoalchemy2 import WKTElement

                prediction = FanPrediction(
                    fan_id=fan.id,
                    prediction_type=PredictionType.MOVEMENT,
                    predicted_location=WKTElement(
                        f"POINT({future_location[0]} {future_location[1]})", srid=4326
                    ),
                    predicted_time=predicted_time,
                    confidence_score=random.uniform(0.6, 0.9),
                    prediction_data={
                        "current_speed": fan.walking_speed,
                        "predicted_reason": self._get_movement_reason(fan),
                        "factors": {
                            "hunger": fan.hunger_level,
                            "fatigue": fan.fatigue_level,
                            "stress": fan.stress_level,
                        },
                    },
                )
                predictions.append(prediction)

        # Purchase prediction
        if fan.purchase_intent > 40:
            predicted_time = current_time + timedelta(minutes=random.randint(5, 45))

            prediction = FanPrediction(
                fan_id=fan.id,
                prediction_type=PredictionType.PURCHASE,
                predicted_time=predicted_time,
                confidence_score=fan.purchase_intent / 100.0,
                prediction_data={
                    "purchase_type": "food" if fan.hunger_level > 60 else "merchandise",
                    "estimated_amount": random.randint(10, 50),
                    "hunger_level": fan.hunger_level,
                },
            )
            predictions.append(prediction)

        # Restroom prediction
        if fan.fatigue_level > 50 or random.random() < 0.1:
            predicted_time = current_time + timedelta(minutes=random.randint(10, 60))

            prediction = FanPrediction(
                fan_id=fan.id,
                prediction_type=PredictionType.RESTROOM,
                predicted_time=predicted_time,
                confidence_score=random.uniform(0.4, 0.7),
                prediction_data={
                    "urgency": "high" if fan.fatigue_level > 80 else "medium",
                    "fatigue_level": fan.fatigue_level,
                },
            )
            predictions.append(prediction)

        # Emergency prediction (rare but important)
        if fan.medical_risk_score > 70:
            predicted_time = current_time + timedelta(hours=random.randint(1, 4))

            prediction = FanPrediction(
                fan_id=fan.id,
                prediction_type=PredictionType.EMERGENCY,
                predicted_time=predicted_time,
                confidence_score=fan.medical_risk_score / 100.0,
                prediction_data={
                    "risk_type": "medical",
                    "risk_factors": {
                        "age": fan.age,
                        "medical_risk": fan.medical_risk_score,
                        "stress": fan.stress_level,
                        "fatigue": fan.fatigue_level,
                    },
                },
            )
            predictions.append(prediction)

        # Save predictions to database
        for prediction in predictions:
            session.add(prediction)

        return predictions

    async def _predict_future_location(
        self, fan: DigitalFan, target_time: datetime
    ) -> Optional[Tuple[float, float]]:
        """Predict fan location at future time"""

        current_coords = fan.get_current_coordinates()
        if not current_coords:
            return None

        # Simple prediction based on current trends
        (target_time - datetime.utcnow()).total_seconds() / 60

        # Predict movement based on fan's behavioral pattern
        if fan.hunger_level > 70:
            # Likely to move toward food court
            food_courts = self._get_nearest_facilities("food_court", current_coords)
            if food_courts:
                return food_courts[0]

        if fan.fatigue_level > 70:
            # Likely to move toward restroom or seating
            restrooms = self._get_nearest_facilities("restroom", current_coords)
            if restrooms:
                return restrooms[0]

        # Default: stay near current location with some drift
        drift_factor = 0.0005  # Small random movement
        new_x = current_coords[0] + random.uniform(-drift_factor, drift_factor)
        new_y = current_coords[1] + random.uniform(-drift_factor, drift_factor)

        return (new_x, new_y)

    def _get_movement_reason(self, fan: DigitalFan) -> str:
        """Get reason for predicted movement"""
        reasons = []

        if fan.hunger_level > 60:
            reasons.append("seeking food")
        if fan.fatigue_level > 60:
            reasons.append("seeking rest")
        if fan.stress_level > 70:
            reasons.append("avoiding crowds")
        if fan.excitement_level > 80:
            reasons.append("exploring stadium")

        return ", ".join(reasons) if reasons else "general movement"

    async def _update_fan_emotion(self, fan: DigitalFan):
        """Update fan emotion based on current context"""

        # Emotion transitions based on current state

        # Simple emotion logic
        if fan.stress_level > 70:
            if fan.current_emotion != FanEmotion.STRESSED:
                fan.current_emotion = FanEmotion.STRESSED
        elif fan.excitement_level > 80:
            if fan.current_emotion != FanEmotion.EXCITED:
                fan.current_emotion = FanEmotion.EXCITED
        elif fan.fatigue_level > 80:
            if fan.current_emotion != FanEmotion.TIRED:
                fan.current_emotion = FanEmotion.TIRED
        elif fan.hunger_level > 80:
            if fan.current_emotion != FanEmotion.ANGRY:
                fan.current_emotion = FanEmotion.ANGRY
        else:
            # Gradual return to neutral
            if fan.current_emotion not in [FanEmotion.NEUTRAL, FanEmotion.JOYFUL]:
                if random.random() < 0.3:  # 30% chance to return to neutral
                    fan.current_emotion = FanEmotion.NEUTRAL

    async def _save_movement_history(self, session: AsyncSession, fan: DigitalFan):
        """Save fan movement to history for analysis"""

        movement = FanMovement(
            fan_id=fan.id,
            location=fan.current_location,
            speed=fan.walking_speed,
            direction=random.uniform(0, 360),  # TODO: Calculate actual direction
            timestamp=datetime.utcnow(),
        )

        session.add(movement)

    def _update_performance_metrics(self, update_time: float, fans_processed: int):
        """Update engine performance metrics"""
        self.performance_metrics["total_updates"] += 1
        self.performance_metrics["fans_processed"] += fans_processed

        # Calculate moving average of update time
        current_avg = self.performance_metrics["average_update_time"]
        new_avg = (
            current_avg * (self.performance_metrics["total_updates"] - 1) + update_time
        ) / self.performance_metrics["total_updates"]
        self.performance_metrics["average_update_time"] = new_avg

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            **self.performance_metrics,
            "is_running": self.is_running,
            "update_count": self.update_count,
            "fans_per_second": self.performance_metrics["fans_processed"]
            / max(1, self.performance_metrics["average_update_time"]),
        }

    async def simulate_event_impact(
        self, event_type: str, event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Simulate the impact of an event on all fans"""

        impact_results = {
            "affected_fans": 0,
            "emotion_changes": {},
            "behavior_changes": {},
            "predicted_outcomes": [],
        }

        async with AsyncSessionLocal() as session:
            # Get all active fans
            result = await session.execute(
                select(DigitalFan).where(DigitalFan.is_active)
            )
            fans = result.scalars().all()

            for fan in fans:
                # Apply event impact to fan
                changes = await self._apply_event_impact(fan, event_type, event_data)

                if changes:
                    impact_results["affected_fans"] += 1

                    # Track emotion changes
                    old_emotion = changes.get("old_emotion")
                    new_emotion = changes.get("new_emotion")
                    if old_emotion != new_emotion:
                        emotion_key = f"{old_emotion} -> {new_emotion}"
                        impact_results["emotion_changes"][emotion_key] = (
                            impact_results["emotion_changes"].get(emotion_key, 0) + 1
                        )

            await session.commit()

        return impact_results

    async def _apply_event_impact(
        self, fan: DigitalFan, event_type: str, event_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Apply event impact to a specific fan"""

        old_emotion = fan.current_emotion
        changes = {"old_emotion": old_emotion}

        # Event-specific impacts
        if event_type == "goal_scored":
            team = event_data.get("team")
            if team == fan.favorite_team:
                fan.current_emotion = FanEmotion.EXCITED
                fan.excitement_level = min(100, fan.excitement_level + 30)
                fan.stress_level = max(0, fan.stress_level - 10)
            else:
                fan.current_emotion = FanEmotion.ANGRY
                fan.stress_level = min(100, fan.stress_level + 20)

        elif event_type == "weather_change":
            weather = event_data.get("weather")
            if weather == "rain":
                fan.stress_level = min(100, fan.stress_level + 15)
                fan.walking_speed *= 1.2  # People walk faster in rain
            elif weather == "hot":
                fan.fatigue_level = min(100, fan.fatigue_level + 10)
                fan.medical_risk_score = min(100, fan.medical_risk_score + 5)

        elif event_type == "emergency":
            fan.current_emotion = FanEmotion.FEARFUL
            fan.stress_level = min(100, fan.stress_level + 40)
            fan.walking_speed *= 1.5  # Emergency evacuation speed

        changes["new_emotion"] = fan.current_emotion

        return changes if changes["old_emotion"] != changes["new_emotion"] else None

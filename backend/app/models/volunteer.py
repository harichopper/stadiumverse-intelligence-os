"""
StadiumVerse AI - Volunteer Models
Models for volunteer management and task coordination
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
import uuid
import enum
from datetime import datetime

from ..database import Base

class VolunteerSkill(str, enum.Enum):
    FIRST_AID = "first_aid"
    MULTILINGUAL = "multilingual"
    CROWD_CONTROL = "crowd_control"
    TECHNICAL = "technical"
    ACCESSIBILITY = "accessibility"

class VolunteerStatus(str, enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    BREAK = "break"
    OFFLINE = "offline"

class TaskStatus(str, enum.Enum):
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(int, enum.Enum):
    LOW = 1
    MEDIUM = 2
    NORMAL = 3
    HIGH = 4
    CRITICAL = 5

class Volunteer(Base):
    """
    Volunteer model with skills, location, and availability tracking
    """
    __tablename__ = "volunteers"
    
    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    volunteer_id = Column(String(20), unique=True, nullable=False, index=True)  # V001, V002, etc.
    name = Column(String(100), nullable=False)
    
    # Skills and capabilities
    languages = Column(ARRAY(String), nullable=False, default=[])
    skills = Column(ARRAY(ENUM(VolunteerSkill)), default=[])
    medical_training = Column(Boolean, default=False)
    
    # Location and assignment
    current_location = Column(Geometry('POINT', srid=4326))
    availability_status = Column(ENUM(VolunteerStatus), default=VolunteerStatus.AVAILABLE)
    zone_assignment = Column(UUID(as_uuid=True), ForeignKey("stadium_zones.id"))
    
    # Schedule
    shift_start = Column(DateTime(timezone=True))
    shift_end = Column(DateTime(timezone=True))
    
    # Performance metrics
    tasks_completed_today = Column(Integer, default=0)
    average_response_time = Column(Integer)  # seconds
    satisfaction_rating = Column(Float)  # 1.0-5.0
    
    # Metadata
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    assigned_zone = relationship("StadiumZone")
    tasks = relationship("VolunteerTask", back_populates="volunteer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Volunteer(id={self.volunteer_id}, name={self.name}, status={self.availability_status})>"
    
    def to_dict(self):
        """Convert volunteer to dictionary for API responses"""
        return {
            "id": str(self.id),
            "volunteer_id": self.volunteer_id,
            "name": self.name,
            "languages": self.languages,
            "skills": [skill.value for skill in self.skills] if self.skills else [],
            "medical_training": self.medical_training,
            "current_coordinates": self.get_current_coordinates(),
            "availability_status": self.availability_status.value if self.availability_status else None,
            "zone_assignment": str(self.zone_assignment) if self.zone_assignment else None,
            "shift_start": self.shift_start.isoformat() if self.shift_start else None,
            "shift_end": self.shift_end.isoformat() if self.shift_end else None,
            "tasks_completed_today": self.tasks_completed_today,
            "average_response_time": self.average_response_time,
            "satisfaction_rating": self.satisfaction_rating,
            "is_active": self.is_active,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_current_coordinates(self):
        """Get current location as [lng, lat] for frontend"""
        if self.current_location:
            return [self.current_location.x, self.current_location.y]
        return None
    
    def is_available_for_task(self, required_skills: list = None, languages: list = None) -> bool:
        """Check if volunteer is available for a specific task"""
        if not self.is_active or self.availability_status != VolunteerStatus.AVAILABLE:
            return False
        
        # Check if volunteer has required skills
        if required_skills:
            volunteer_skills = [skill.value for skill in self.skills] if self.skills else []
            if not any(skill in volunteer_skills for skill in required_skills):
                return False
        
        # Check if volunteer speaks required languages
        if languages:
            if not any(lang in self.languages for lang in languages):
                return False
        
        return True
    
    def calculate_distance_to(self, target_location: tuple) -> float:
        """Calculate distance to target location in meters (approximate)"""
        if not self.current_location:
            return float('inf')
        
        # Simple distance calculation (for more accuracy, use geodesic)
        current = (self.current_location.x, self.current_location.y)
        dx = current[0] - target_location[0]
        dy = current[1] - target_location[1]
        
        # Rough conversion from degrees to meters (at NYC latitude)
        meters_per_degree_lat = 111000
        meters_per_degree_lng = 85000
        
        distance = ((dx * meters_per_degree_lng) ** 2 + (dy * meters_per_degree_lat) ** 2) ** 0.5
        return distance
    
    def assign_task(self, task_data: dict) -> "VolunteerTask":
        """Assign a new task to this volunteer"""
        from .volunteer import VolunteerTask
        
        task = VolunteerTask(
            volunteer_id=self.id,
            task_type=task_data.get("task_type"),
            title=task_data.get("title"),
            description=task_data.get("description"),
            priority=task_data.get("priority", TaskPriority.NORMAL),
            estimated_duration=task_data.get("estimated_duration"),
            status=TaskStatus.ASSIGNED
        )
        
        # Update volunteer status
        self.availability_status = VolunteerStatus.BUSY
        
        return task

class VolunteerTask(Base):
    """
    Individual tasks assigned to volunteers
    """
    __tablename__ = "volunteer_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    volunteer_id = Column(UUID(as_uuid=True), ForeignKey("volunteers.id"), nullable=False)
    
    # Task details
    task_type = Column(String(50), nullable=False)  # medical_assistance, crowd_control, information, etc.
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(Integer, default=3)  # 1-5 scale
    
    # Location and logistics
    location = Column(Geometry('POINT', srid=4326))
    estimated_duration = Column(Integer)  # minutes
    actual_duration = Column(Integer)  # minutes
    
    # Status tracking
    status = Column(ENUM(TaskStatus), default=TaskStatus.ASSIGNED)
    assigned_at = Column(DateTime(timezone=True), default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Assignment metadata
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assigned_by_ai = Column(Boolean, default=False)
    
    # Task outcome
    completion_notes = Column(Text)
    quality_rating = Column(Integer)  # 1-5 scale
    follow_up_required = Column(Boolean, default=False)
    
    # Relationships
    volunteer = relationship("Volunteer", back_populates="tasks")
    created_by_user = relationship("User")
    
    def __repr__(self):
        return f"<VolunteerTask(id={str(self.id)[:8]}, type={self.task_type}, status={self.status})>"
    
    def to_dict(self):
        """Convert task to dictionary for API responses"""
        return {
            "id": str(self.id),
            "volunteer_id": str(self.volunteer_id),
            "task_type": self.task_type,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "location_coordinates": self.get_location_coordinates(),
            "estimated_duration": self.estimated_duration,
            "actual_duration": self.actual_duration,
            "status": self.status.value if self.status else None,
            "assigned_at": self.assigned_at.isoformat() if self.assigned_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_by": str(self.created_by) if self.created_by else None,
            "assigned_by_ai": self.assigned_by_ai,
            "completion_notes": self.completion_notes,
            "quality_rating": self.quality_rating,
            "follow_up_required": self.follow_up_required
        }
    
    def get_location_coordinates(self):
        """Get task location as [lng, lat] for frontend"""
        if self.location:
            return [self.location.x, self.location.y]
        return None
    
    def start_task(self):
        """Mark task as started"""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = func.now()
        
        # Update volunteer status
        if self.volunteer:
            self.volunteer.availability_status = VolunteerStatus.BUSY
    
    def complete_task(self, completion_notes: str = None, quality_rating: int = None):
        """Mark task as completed"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = func.now()
        
        if completion_notes:
            self.completion_notes = completion_notes
        
        if quality_rating:
            self.quality_rating = quality_rating
        
        # Calculate actual duration
        if self.started_at:
            duration = (func.now() - self.started_at).total_seconds() / 60
            self.actual_duration = int(duration)
        
        # Update volunteer status and metrics
        if self.volunteer:
            self.volunteer.availability_status = VolunteerStatus.AVAILABLE
            self.volunteer.tasks_completed_today += 1
            
            # Update average response time
            if self.assigned_at and self.started_at:
                response_time = (self.started_at - self.assigned_at).total_seconds()
                if self.volunteer.average_response_time:
                    # Moving average
                    self.volunteer.average_response_time = int(
                        (self.volunteer.average_response_time + response_time) / 2
                    )
                else:
                    self.volunteer.average_response_time = int(response_time)
    
    def cancel_task(self, reason: str = None):
        """Cancel the task"""
        self.status = TaskStatus.CANCELLED
        
        if reason:
            self.completion_notes = f"Cancelled: {reason}"
        
        # Update volunteer status
        if self.volunteer:
            self.volunteer.availability_status = VolunteerStatus.AVAILABLE
    
    def get_urgency_score(self) -> float:
        """Calculate urgency score based on priority, duration, and assignment time"""
        priority_weight = self.priority / 5.0  # Normalize to 0-1
        
        # Time factor (older tasks become more urgent)
        time_since_assignment = (func.now() - self.assigned_at).total_seconds() / 3600  # hours
        time_weight = min(time_since_assignment / 2, 1.0)  # Cap at 2 hours
        
        # Combine factors
        urgency_score = (priority_weight * 0.6) + (time_weight * 0.4)
        
        return min(urgency_score, 1.0)

# Task type definitions for AI assignment
TASK_TYPE_REQUIREMENTS = {
    "medical_assistance": {
        "skills": [VolunteerSkill.FIRST_AID],
        "priority_range": (4, 5),
        "typical_duration": 15
    },
    "crowd_control": {
        "skills": [VolunteerSkill.CROWD_CONTROL],
        "priority_range": (3, 4),
        "typical_duration": 30
    },
    "information_assistance": {
        "skills": [VolunteerSkill.MULTILINGUAL],
        "priority_range": (2, 3),
        "typical_duration": 5
    },
    "accessibility_support": {
        "skills": [VolunteerSkill.ACCESSIBILITY],
        "priority_range": (3, 4),
        "typical_duration": 20
    },
    "technical_support": {
        "skills": [VolunteerSkill.TECHNICAL],
        "priority_range": (2, 4),
        "typical_duration": 25
    },
    "general_assistance": {
        "skills": [],
        "priority_range": (1, 3),
        "typical_duration": 10
    }
}
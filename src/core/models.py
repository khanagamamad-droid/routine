"""
Pydantic data models for task management system.
Includes models for tasks, users, scheduling, and related entities.
"""

from datetime import datetime, time
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator


# ============================================================================
# Enumerations
# ============================================================================

class RecurrenceType(str, Enum):
    """Enumeration for task recurrence patterns."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class NotificationType(str, Enum):
    """Enumeration for notification types."""
    REMINDER = "reminder"
    ALERT = "alert"
    INFO = "info"
    WARNING = "warning"


class ActivityCategory(str, Enum):
    """Enumeration for activity categories."""
    WORK = "work"
    HEALTH = "health"
    PERSONAL = "personal"
    LEARNING = "learning"
    EXERCISE = "exercise"
    MEDITATION = "meditation"
    LEISURE = "leisure"
    SOCIAL = "social"
    OTHER = "other"


class TaskStatus(str, Enum):
    """Enumeration for task status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


# ============================================================================
# Time-related Models
# ============================================================================

class TimeModel(BaseModel):
    """Model representing a time value."""
    hour: int = Field(..., ge=0, le=23, description="Hour of the day (0-23)")
    minute: int = Field(..., ge=0, le=59, description="Minute of the hour (0-59)")
    second: int = Field(default=0, ge=0, le=59, description="Second of the minute (0-59)")

    class Config:
        schema_extra = {
            "example": {
                "hour": 14,
                "minute": 30,
                "second": 0
            }
        }

    def to_time(self) -> time:
        """Convert to Python time object."""
        return time(hour=self.hour, minute=self.minute, second=self.second)

    def __str__(self) -> str:
        """String representation in HH:MM:SS format."""
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"


# ============================================================================
# Recurrence Model
# ============================================================================

class RecurrenceModel(BaseModel):
    """Model for task recurrence configuration."""
    type: RecurrenceType = Field(default=RecurrenceType.NONE, description="Type of recurrence")
    frequency: int = Field(default=1, ge=1, description="Frequency interval")
    days_of_week: Optional[List[int]] = Field(
        default=None,
        description="Days of week for weekly recurrence (0=Monday, 6=Sunday)"
    )
    days_of_month: Optional[List[int]] = Field(
        default=None,
        description="Days of month for monthly recurrence"
    )
    end_date: Optional[datetime] = Field(default=None, description="Recurrence end date")

    @validator('days_of_week')
    def validate_days_of_week(cls, v):
        """Validate days of week are within valid range."""
        if v is not None:
            if not all(0 <= day <= 6 for day in v):
                raise ValueError("Days of week must be between 0 and 6")
        return v

    @validator('days_of_month')
    def validate_days_of_month(cls, v):
        """Validate days of month are within valid range."""
        if v is not None:
            if not all(1 <= day <= 31 for day in v):
                raise ValueError("Days of month must be between 1 and 31")
        return v

    class Config:
        schema_extra = {
            "example": {
                "type": "weekly",
                "frequency": 1,
                "days_of_week": [0, 2, 4],
                "end_date": None
            }
        }


# ============================================================================
# Notification Model
# ============================================================================

class NotificationModel(BaseModel):
    """Model for task notifications/reminders."""
    id: Optional[str] = Field(default=None, description="Notification ID")
    type: NotificationType = Field(
        default=NotificationType.REMINDER,
        description="Type of notification"
    )
    time_before_minutes: int = Field(
        default=15,
        ge=0,
        description="Minutes before task to send notification"
    )
    enabled: bool = Field(default=True, description="Whether notification is enabled")
    message: Optional[str] = Field(default=None, description="Custom notification message")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "type": "reminder",
                "time_before_minutes": 15,
                "enabled": True,
                "message": "Time to start your task!"
            }
        }


# ============================================================================
# Activity Category Model
# ============================================================================

class ActivityCategoryModel(BaseModel):
    """Model for activity categories."""
    id: Optional[str] = Field(default=None, description="Category ID")
    name: ActivityCategory = Field(description="Category name")
    description: Optional[str] = Field(default=None, description="Category description")
    color: Optional[str] = Field(default=None, description="Hex color code for category")
    icon: Optional[str] = Field(default=None, description="Icon identifier")

    class Config:
        schema_extra = {
            "example": {
                "name": "work",
                "description": "Work-related tasks",
                "color": "#FF6B6B",
                "icon": "briefcase"
            }
        }


# ============================================================================
# Task Model
# ============================================================================

class TaskModel(BaseModel):
    """Model for tasks in the routine management system."""
    id: Optional[str] = Field(default=None, description="Task ID")
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(default=None, description="Task description")
    category: ActivityCategory = Field(
        default=ActivityCategory.PERSONAL,
        description="Activity category"
    )
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")
    priority: int = Field(default=0, ge=0, le=5, description="Priority level (0-5)")
    start_time: Optional[TimeModel] = Field(default=None, description="Task start time")
    end_time: Optional[TimeModel] = Field(default=None, description="Task end time")
    duration_minutes: Optional[int] = Field(
        default=None,
        ge=0,
        description="Estimated duration in minutes"
    )
    due_date: Optional[datetime] = Field(default=None, description="Task due date")
    recurrence: RecurrenceModel = Field(
        default_factory=RecurrenceModel,
        description="Recurrence configuration"
    )
    notifications: List[NotificationModel] = Field(
        default_factory=list,
        description="List of notifications"
    )
    tags: List[str] = Field(default_factory=list, description="Task tags")
    is_recurring: bool = Field(default=False, description="Whether task is recurring")
    is_completed: bool = Field(default=False, description="Whether task is completed")
    completion_date: Optional[datetime] = Field(default=None, description="Date when task was completed")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = Field(default=None, description="Associated user ID")

    @validator('end_time')
    def validate_end_time(cls, v, values):
        """Validate that end_time is after start_time."""
        if v is not None and 'start_time' in values and values['start_time'] is not None:
            if v.hour < values['start_time'].hour or \
               (v.hour == values['start_time'].hour and v.minute < values['start_time'].minute):
                raise ValueError("End time must be after start time")
        return v

    class Config:
        schema_extra = {
            "example": {
                "title": "Morning Meditation",
                "description": "15-minute meditation session",
                "category": "meditation",
                "status": "pending",
                "priority": 2,
                "start_time": {"hour": 7, "minute": 0, "second": 0},
                "end_time": {"hour": 7, "minute": 15, "second": 0},
                "duration_minutes": 15,
                "is_recurring": True,
                "tags": ["wellness", "morning"]
            }
        }


# ============================================================================
# User Profile Model
# ============================================================================

class UserProfileModel(BaseModel):
    """Model for user profile information."""
    id: Optional[str] = Field(default=None, description="User ID")
    username: str = Field(..., min_length=1, max_length=255, description="Username")
    email: str = Field(..., description="User email")
    first_name: Optional[str] = Field(default=None, description="User's first name")
    last_name: Optional[str] = Field(default=None, description="User's last name")
    bio: Optional[str] = Field(default=None, description="User biography")
    profile_picture_url: Optional[str] = Field(default=None, description="URL to profile picture")
    timezone: str = Field(default="UTC", description="User's timezone")
    language: str = Field(default="en", description="Preferred language")
    theme: str = Field(default="light", description="UI theme preference")
    notifications_enabled: bool = Field(default=True, description="Whether notifications are enabled")
    total_tasks: int = Field(default=0, ge=0, description="Total tasks created")
    completed_tasks: int = Field(default=0, ge=0, description="Total completed tasks")
    streak_days: int = Field(default=0, ge=0, description="Current completion streak in days")
    last_login: Optional[datetime] = Field(default=None, description="Last login timestamp")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    preferences: Dict[str, Any] = Field(default_factory=dict, description="Additional user preferences")

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "timezone": "America/New_York",
                "notifications_enabled": True,
                "streak_days": 5
            }
        }


# ============================================================================
# Daily Schedule Model
# ============================================================================

class DailyScheduleModel(BaseModel):
    """Model for a daily schedule with tasks."""
    id: Optional[str] = Field(default=None, description="Schedule ID")
    user_id: str = Field(..., description="Associated user ID")
    date: datetime = Field(..., description="Date of the schedule")
    tasks: List[TaskModel] = Field(default_factory=list, description="Tasks scheduled for the day")
    total_duration_minutes: int = Field(
        default=0,
        ge=0,
        description="Total duration of all tasks in minutes"
    )
    completed_tasks_count: int = Field(
        default=0,
        ge=0,
        description="Number of completed tasks"
    )
    pending_tasks_count: int = Field(
        default=0,
        ge=0,
        description="Number of pending tasks"
    )
    completion_percentage: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Percentage of tasks completed"
    )
    notes: Optional[str] = Field(default=None, description="Daily notes")
    mood: Optional[str] = Field(default=None, description="User's mood for the day")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "date": "2025-12-31T00:00:00Z",
                "tasks": [],
                "total_duration_minutes": 180,
                "completed_tasks_count": 3,
                "pending_tasks_count": 2,
                "completion_percentage": 60.0,
                "mood": "productive"
            }
        }


# ============================================================================
# Task Response Model
# ============================================================================

class TaskResponseModel(BaseModel):
    """Model for task API responses."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    data: Optional[TaskModel] = Field(default=None, description="Task data")
    errors: Optional[List[str]] = Field(default=None, description="List of errors if any")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Task created successfully",
                "data": {
                    "id": "task123",
                    "title": "Morning Run",
                    "category": "exercise",
                    "status": "pending"
                },
                "errors": None,
                "timestamp": "2025-12-31T21:29:02Z"
            }
        }


# ============================================================================
# Schedule Stats Model
# ============================================================================

class ScheduleStatsModel(BaseModel):
    """Model for schedule statistics and analytics."""
    id: Optional[str] = Field(default=None, description="Stats ID")
    user_id: str = Field(..., description="Associated user ID")
    period_start: datetime = Field(..., description="Start date of the statistics period")
    period_end: datetime = Field(..., description="End date of the statistics period")
    total_tasks: int = Field(default=0, ge=0, description="Total tasks in period")
    completed_tasks: int = Field(default=0, ge=0, description="Completed tasks in period")
    cancelled_tasks: int = Field(default=0, ge=0, description="Cancelled tasks in period")
    pending_tasks: int = Field(default=0, ge=0, description="Pending tasks in period")
    completion_rate: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Task completion rate percentage"
    )
    total_hours_logged: float = Field(default=0.0, ge=0.0, description="Total hours logged")
    average_daily_tasks: float = Field(
        default=0.0,
        ge=0.0,
        description="Average tasks per day"
    )
    tasks_by_category: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of tasks by category"
    )
    completion_by_category: Dict[str, float] = Field(
        default_factory=dict,
        description="Completion rate by category"
    )
    most_active_day: Optional[str] = Field(
        default=None,
        description="Day with most tasks completed"
    )
    longest_streak: int = Field(
        default=0,
        ge=0,
        description="Longest completion streak in days"
    )
    current_streak: int = Field(
        default=0,
        ge=0,
        description="Current completion streak in days"
    )
    weekly_breakdown: Dict[str, int] = Field(
        default_factory=dict,
        description="Tasks completed per week"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "period_start": "2025-12-01T00:00:00Z",
                "period_end": "2025-12-31T23:59:59Z",
                "total_tasks": 50,
                "completed_tasks": 42,
                "completion_rate": 84.0,
                "tasks_by_category": {
                    "work": 25,
                    "health": 15,
                    "personal": 10
                },
                "longest_streak": 7,
                "current_streak": 3
            }
        }

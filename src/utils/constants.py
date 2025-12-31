"""
Constants for the Daily Scheduler Application

This module contains all constants used throughout the daily scheduler application,
including configuration values, default settings, and application metadata.
"""

# ============================================================================
# APPLICATION METADATA
# ============================================================================
APP_NAME = "Daily Scheduler"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A daily task and schedule management application"

# ============================================================================
# TIME AND DATE CONSTANTS
# ============================================================================
# Default timezone for the application
DEFAULT_TIMEZONE = "UTC"

# Time format constants
TIME_FORMAT_24H = "%H:%M:%S"
TIME_FORMAT_12H = "%I:%M:%S %p"
DATE_FORMAT_ISO = "%Y-%m-%d"
DATETIME_FORMAT_ISO = "%Y-%m-%dT%H:%M:%S"
DATETIME_FORMAT_DISPLAY = "%Y-%m-%d %H:%M:%S"

# Schedule time boundaries (in 24-hour format)
SCHEDULER_START_HOUR = 0
SCHEDULER_END_HOUR = 23
SCHEDULER_START_MINUTE = 0
SCHEDULER_END_MINUTE = 59

# ============================================================================
# TASK CONSTANTS
# ============================================================================
# Task status values
TASK_STATUS_PENDING = "pending"
TASK_STATUS_IN_PROGRESS = "in_progress"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_CANCELLED = "cancelled"
TASK_STATUS_OVERDUE = "overdue"

VALID_TASK_STATUSES = [
    TASK_STATUS_PENDING,
    TASK_STATUS_IN_PROGRESS,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_CANCELLED,
    TASK_STATUS_OVERDUE,
]

# Task priority levels
TASK_PRIORITY_LOW = "low"
TASK_PRIORITY_MEDIUM = "medium"
TASK_PRIORITY_HIGH = "high"
TASK_PRIORITY_CRITICAL = "critical"

VALID_TASK_PRIORITIES = [
    TASK_PRIORITY_LOW,
    TASK_PRIORITY_MEDIUM,
    TASK_PRIORITY_HIGH,
    TASK_PRIORITY_CRITICAL,
]

# Priority numeric values for sorting
PRIORITY_WEIGHTS = {
    TASK_PRIORITY_LOW: 1,
    TASK_PRIORITY_MEDIUM: 2,
    TASK_PRIORITY_HIGH: 3,
    TASK_PRIORITY_CRITICAL: 4,
}

# Default task values
DEFAULT_TASK_PRIORITY = TASK_PRIORITY_MEDIUM
DEFAULT_TASK_STATUS = TASK_STATUS_PENDING

# Maximum task title length (characters)
MAX_TASK_TITLE_LENGTH = 255

# Maximum task description length (characters)
MAX_TASK_DESCRIPTION_LENGTH = 5000

# ============================================================================
# RECURRENCE CONSTANTS
# ============================================================================
# Recurrence types
RECURRENCE_NONE = "none"
RECURRENCE_DAILY = "daily"
RECURRENCE_WEEKLY = "weekly"
RECURRENCE_MONTHLY = "monthly"
RECURRENCE_YEARLY = "yearly"

VALID_RECURRENCE_TYPES = [
    RECURRENCE_NONE,
    RECURRENCE_DAILY,
    RECURRENCE_WEEKLY,
    RECURRENCE_MONTHLY,
    RECURRENCE_YEARLY,
]

# Weekday constants
WEEKDAY_MONDAY = "monday"
WEEKDAY_TUESDAY = "tuesday"
WEEKDAY_WEDNESDAY = "wednesday"
WEEKDAY_THURSDAY = "thursday"
WEEKDAY_FRIDAY = "friday"
WEEKDAY_SATURDAY = "saturday"
WEEKDAY_SUNDAY = "sunday"

VALID_WEEKDAYS = [
    WEEKDAY_MONDAY,
    WEEKDAY_TUESDAY,
    WEEKDAY_WEDNESDAY,
    WEEKDAY_THURSDAY,
    WEEKDAY_FRIDAY,
    WEEKDAY_SATURDAY,
    WEEKDAY_SUNDAY,
]

# Default recurrence
DEFAULT_RECURRENCE = RECURRENCE_NONE

# ============================================================================
# NOTIFICATION CONSTANTS
# ============================================================================
# Notification types
NOTIFICATION_TYPE_REMINDER = "reminder"
NOTIFICATION_TYPE_COMPLETION = "completion"
NOTIFICATION_TYPE_OVERDUE = "overdue"
NOTIFICATION_TYPE_UPCOMING = "upcoming"

VALID_NOTIFICATION_TYPES = [
    NOTIFICATION_TYPE_REMINDER,
    NOTIFICATION_TYPE_COMPLETION,
    NOTIFICATION_TYPE_OVERDUE,
    NOTIFICATION_TYPE_UPCOMING,
]

# Notification status
NOTIFICATION_STATUS_PENDING = "pending"
NOTIFICATION_STATUS_SENT = "sent"
NOTIFICATION_STATUS_FAILED = "failed"
NOTIFICATION_STATUS_DISMISSED = "dismissed"

VALID_NOTIFICATION_STATUSES = [
    NOTIFICATION_STATUS_PENDING,
    NOTIFICATION_STATUS_SENT,
    NOTIFICATION_STATUS_FAILED,
    NOTIFICATION_STATUS_DISMISSED,
]

# Default notification advance time (minutes before task)
DEFAULT_NOTIFICATION_MINUTES = 15

# ============================================================================
# DATABASE CONSTANTS
# ============================================================================
# Default database configuration
DEFAULT_DB_POOL_SIZE = 10
DEFAULT_DB_POOL_OVERFLOW = 20
DEFAULT_DB_POOL_TIMEOUT = 30

# Query limits
DEFAULT_QUERY_LIMIT = 100
MAX_QUERY_LIMIT = 1000

# ============================================================================
# VALIDATION CONSTANTS
# ============================================================================
# Username validation
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 50

# Password validation
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

# Email validation regex pattern
EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# ============================================================================
# ERROR MESSAGES
# ============================================================================
ERROR_TASK_NOT_FOUND = "Task not found"
ERROR_INVALID_TASK_STATUS = "Invalid task status"
ERROR_INVALID_TASK_PRIORITY = "Invalid task priority"
ERROR_INVALID_RECURRENCE_TYPE = "Invalid recurrence type"
ERROR_INVALID_TIME_FORMAT = "Invalid time format"
ERROR_TASK_TITLE_REQUIRED = "Task title is required"
ERROR_TASK_TITLE_TOO_LONG = f"Task title cannot exceed {MAX_TASK_TITLE_LENGTH} characters"
ERROR_TASK_DESCRIPTION_TOO_LONG = f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================
SUCCESS_TASK_CREATED = "Task created successfully"
SUCCESS_TASK_UPDATED = "Task updated successfully"
SUCCESS_TASK_DELETED = "Task deleted successfully"
SUCCESS_TASK_COMPLETED = "Task marked as completed"
SUCCESS_NOTIFICATION_SENT = "Notification sent successfully"

# ============================================================================
# PAGINATION CONSTANTS
# ============================================================================
DEFAULT_PAGE_SIZE = 20
MIN_PAGE_SIZE = 1
MAX_PAGE_SIZE = 100
DEFAULT_PAGE_NUMBER = 1

# ============================================================================
# CACHE CONSTANTS
# ============================================================================
# Cache time-to-live values (in seconds)
CACHE_TTL_SHORT = 60  # 1 minute
CACHE_TTL_MEDIUM = 300  # 5 minutes
CACHE_TTL_LONG = 3600  # 1 hour
CACHE_TTL_VERY_LONG = 86400  # 24 hours

# Cache key prefixes
CACHE_PREFIX_TASK = "task:"
CACHE_PREFIX_USER = "user:"
CACHE_PREFIX_SCHEDULE = "schedule:"

# ============================================================================
# LOGGING CONSTANTS
# ============================================================================
# Log levels
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"
LOG_LEVEL_CRITICAL = "CRITICAL"

# Default log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

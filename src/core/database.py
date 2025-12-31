"""
SQLite Database Schema and Table Definitions for Daily Scheduler Application

This module provides database initialization and management for the routine scheduler.
It includes tables for routines, tasks, reminders, and user preferences.
"""

import sqlite3
import os
from contextlib import contextmanager
from typing import Optional, List, Tuple, Any
from datetime import datetime


class RoutineDatabase:
    """SQLite database manager for the daily scheduler application."""
    
    def __init__(self, db_path: str = "routine.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.ensure_database_exists()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def ensure_database_exists(self) -> None:
        """Create database and initialize schema if it doesn't exist."""
        if not os.path.exists(self.db_path):
            self.create_schema()
        else:
            # Verify schema is complete
            self._verify_schema()
    
    def create_schema(self) -> None:
        """Create all database tables with proper schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Routines table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS routines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    start_time TIME,
                    end_time TIME,
                    color TEXT DEFAULT '#3498db',
                    icon TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # Tasks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    routine_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority TEXT DEFAULT 'medium',
                    status TEXT DEFAULT 'pending',
                    scheduled_date DATE,
                    scheduled_time TIME,
                    due_date DATE,
                    estimated_duration_minutes INTEGER,
                    completed_at TIMESTAMP,
                    order_index INTEGER DEFAULT 0,
                    is_recurring BOOLEAN DEFAULT 0,
                    recurrence_pattern TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (routine_id) REFERENCES routines(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # Reminders table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    reminder_time TIMESTAMP NOT NULL,
                    reminder_type TEXT DEFAULT 'notification',
                    message TEXT,
                    is_sent BOOLEAN DEFAULT 0,
                    sent_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # Routine history/logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS routine_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    routine_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    execution_date DATE NOT NULL,
                    completed_tasks INTEGER DEFAULT 0,
                    total_tasks INTEGER DEFAULT 0,
                    duration_minutes INTEGER,
                    notes TEXT,
                    completed_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (routine_id) REFERENCES routines(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # User preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    theme TEXT DEFAULT 'light',
                    notification_enabled BOOLEAN DEFAULT 1,
                    notification_time_minutes INTEGER DEFAULT 15,
                    date_format TEXT DEFAULT 'YYYY-MM-DD',
                    time_format TEXT DEFAULT '24h',
                    language TEXT DEFAULT 'en',
                    auto_sort_tasks BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # Task categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS task_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    color TEXT DEFAULT '#e74c3c',
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, name),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # Task-Category mapping table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS task_category_mapping (
                    task_id INTEGER NOT NULL,
                    category_id INTEGER NOT NULL,
                    PRIMARY KEY (task_id, category_id),
                    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
                    FOREIGN KEY (category_id) REFERENCES task_categories(id) ON DELETE CASCADE
                )
            ''')
            
            # Create indexes for better query performance
            self._create_indexes(cursor)
            
            conn.commit()
    
    def _create_indexes(self, cursor: sqlite3.Cursor) -> None:
        """Create database indexes for improved query performance."""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_routines_user_id ON routines(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_tasks_routine_id ON tasks(routine_id)",
            "CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)",
            "CREATE INDEX IF NOT EXISTS idx_tasks_scheduled_date ON tasks(scheduled_date)",
            "CREATE INDEX IF NOT EXISTS idx_reminders_task_id ON reminders(task_id)",
            "CREATE INDEX IF NOT EXISTS idx_reminders_user_id ON reminders(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_reminders_is_sent ON reminders(is_sent)",
            "CREATE INDEX IF NOT EXISTS idx_routine_logs_routine_id ON routine_logs(routine_id)",
            "CREATE INDEX IF NOT EXISTS idx_routine_logs_execution_date ON routine_logs(execution_date)",
            "CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_task_categories_user_id ON task_categories(user_id)",
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
    
    def _verify_schema(self) -> None:
        """Verify that all required tables exist in the database."""
        required_tables = {
            'users', 'routines', 'tasks', 'reminders', 'routine_logs',
            'user_preferences', 'task_categories', 'task_category_mapping'
        }
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            existing_tables = {row[0] for row in cursor.fetchall()}
            
            missing_tables = required_tables - existing_tables
            if missing_tables:
                # Recreate missing tables
                self.create_schema()
    
    def execute_query(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """
        Execute a SELECT query.
        
        Args:
            query: SQL SELECT query
            params: Query parameters
            
        Returns:
            List of rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_insert(self, query: str, params: Tuple = ()) -> int:
        """
        Execute an INSERT query.
        
        Args:
            query: SQL INSERT query
            params: Query parameters
            
        Returns:
            Last inserted row ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.lastrowid
    
    def execute_update(self, query: str, params: Tuple = ()) -> int:
        """
        Execute an UPDATE query.
        
        Args:
            query: SQL UPDATE query
            params: Query parameters
            
        Returns:
            Number of rows affected
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    
    def execute_delete(self, query: str, params: Tuple = ()) -> int:
        """
        Execute a DELETE query.
        
        Args:
            query: SQL DELETE query
            params: Query parameters
            
        Returns:
            Number of rows deleted
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    
    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Database initialization functions
def init_database(db_path: str = "routine.db") -> RoutineDatabase:
    """
    Initialize the routine database.
    
    Args:
        db_path: Path to SQLite database file
        
    Returns:
        RoutineDatabase instance
    """
    return RoutineDatabase(db_path)

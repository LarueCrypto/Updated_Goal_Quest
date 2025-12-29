"""
Goal Quest Database Models - Complete SQLAlchemy schema with all 14 tables
Exact replication of the Replit schema.ts
"""

import os
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, Float, DateTime, Date, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import enum

# Database URL - supports PostgreSQL for production, SQLite for local development
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./goal_quest.db")

# Handle PostgreSQL URL format from some providers
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============ ENUMS ============

class FrequencyType(str, enum.Enum):
    DAILY = "daily"
    WEEKDAYS = "weekdays"
    WEEKENDS = "weekends"
    SPECIFIC = "specific"
    CUSTOM = "custom"


class DifficultyLevel(int, enum.Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


class AvatarStyle(str, enum.Enum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    SAGE = "sage"


class NoteCategory(str, enum.Enum):
    PERSONAL = "personal"
    WORK = "work"
    HEALTH = "health"
    GOALS = "goals"
    IDEAS = "ideas"
    LEARNING = "learning"


class NoteColor(str, enum.Enum):
    DEFAULT = "default"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"


class AchievementCategory(str, enum.Enum):
    GENERAL = "general"
    STREAKS = "streaks"
    LEVELS = "levels"
    HABITS = "habits"
    GOALS = "goals"
    SPECIAL = "special"
    STATS = "stats"
    LEGENDARY = "legendary"


class AchievementTier(str, enum.Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    LEGENDARY = "legendary"


class HabitCategory(str, enum.Enum):
    HEALTH = "health"
    FITNESS = "fitness"
    LEARNING = "learning"
    MINDFULNESS = "mindfulness"
    PRODUCTIVITY = "productivity"
    SOCIAL = "social"
    CREATIVE = "creative"
    FINANCE = "finance"
    PERSONAL = "personal"
    WORK = "work"


class GoalCategory(str, enum.Enum):
    HEALTH = "health"
    FITNESS = "fitness"
    CAREER = "career"
    FINANCE = "finance"
    EDUCATION = "education"
    RELATIONSHIPS = "relationships"
    PERSONAL = "personal"
    CREATIVE = "creative"
    TRAVEL = "travel"
    OTHER = "other"


# ============ MODELS ============

class Habit(Base):
    """Habit tracking table - stores all user habits with scheduling"""
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    category = Column(String(50), default="personal")
    difficulty = Column(Integer, default=1)  # 1=easy, 2=medium, 3=hard
    xp_reward = Column(Integer, default=50)  # 50/100/300 based on difficulty
    difficulty_rationale = Column(Text, default="")  # AI explanation
    priority = Column(Boolean, default=False)
    color = Column(String(50), default="bg-primary")
    frequency = Column(String(20), default="daily")  # daily/weekdays/weekends/specific/custom
    frequency_days = Column(JSON, default=list)  # [0-6] for specific days
    custom_interval = Column(Integer, default=1)  # for custom frequency
    reminder_time = Column(String(10), default=None)  # HH:MM format
    reminder_enabled = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    completions = relationship("Completion", back_populates="habit", cascade="all, delete-orphan")


class Goal(Base):
    """Goal tracking table - stores user goals with progress and steps"""
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    category = Column(String(50), default="personal")
    deadline = Column(Date, default=None)
    progress = Column(Integer, default=0)  # 0-100
    difficulty = Column(Integer, default=1)  # 1=normal, 2=medium, 3=hard
    xp_reward = Column(Integer, default=1000)  # 1000/2000/3000 based on difficulty
    completed = Column(Boolean, default=False)
    priority = Column(Boolean, default=False)
    steps = Column(JSON, default=list)  # List of {id, title, completed, suggestedHabit}
    reminder_enabled = Column(Boolean, default=False)
    reminder_days_before = Column(Integer, default=7)
    parent_goal_id = Column(Integer, ForeignKey("goals.id"), default=None)
    created_at = Column(DateTime, default=datetime.utcnow)


class Completion(Base):
    """Completion tracking - records habit completions by date"""
    __tablename__ = "completions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    date = Column(String(10), nullable=False)  # YYYY-MM-DD format
    completed = Column(Boolean, default=True)
    
    # Relationships
    habit = relationship("Habit", back_populates="completions")


class UserStats(Base):
    """User statistics - XP, level, gold, and 6 stats"""
    __tablename__ = "user_stats"
    
    id = Column(Integer, primary_key=True, default=1)
    level = Column(Integer, default=1)
    current_xp = Column(Integer, default=0)
    total_xp = Column(Integer, default=0)
    last_level_up = Column(DateTime, default=None)
    
    # 6 Stats (Solo Leveling inspired)
    strength = Column(Integer, default=10)  # Fitness category
    intelligence = Column(Integer, default=10)  # Learning, work, creative
    vitality = Column(Integer, default=10)  # Health
    agility = Column(Integer, default=10)  # Productivity, social
    sense = Column(Integer, default=10)  # Mindfulness, finance
    willpower = Column(Integer, default=10)  # Personal
    
    # Currency
    current_gold = Column(Integer, default=0)
    lifetime_gold = Column(Integer, default=0)


class UserProfile(Base):
    """User profile - personalization settings"""
    __tablename__ = "user_profile"
    
    id = Column(Integer, primary_key=True, default=1)
    display_name = Column(String(100), default="Hunter")
    gender = Column(String(20), default="neutral")  # male/female/neutral
    avatar_style = Column(String(20), default="warrior")  # warrior/mage/rogue/sage
    timezone = Column(String(50), default="America/Chicago")
    onboarding_completed = Column(Boolean, default=False)
    notifications_enabled = Column(Boolean, default=True)
    daily_reminder_time = Column(String(10), default="09:00")
    weekly_report_enabled = Column(Boolean, default=True)
    philosophy_tradition = Column(String(50), default="esoteric")
    philosophy_traditions = Column(JSON, default=list)  # Multi-select traditions
    focus_areas = Column(JSON, default=list)  # Multi-select focus areas
    challenge_approaches = Column(JSON, default=list)  # Multi-select approaches
    created_at = Column(DateTime, default=datetime.utcnow)


class Note(Base):
    """Notes table - user notes with categories and AI summaries"""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, default="")
    category = Column(String(50), default="personal")
    tags = Column(JSON, default=list)
    ai_summary = Column(Text, default=None)
    pinned = Column(Boolean, default=False)
    color = Column(String(20), default="default")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Achievement(Base):
    """Achievements table - tracks unlocked achievements"""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False)  # Unique achievement key
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    icon = Column(String(50), default="Star")
    category = Column(String(50), default="general")
    tier = Column(String(20), default="bronze")  # bronze/silver/gold/platinum/legendary
    xp_reward = Column(Integer, default=100)
    gold_reward = Column(Integer, default=10)
    stat_bonus = Column(JSON, default=None)  # {stat: string, amount: number}
    special_power = Column(String(255), default=None)
    unlocked_at = Column(DateTime, default=None)


class Motivation(Base):
    """Daily motivations - wisdom quotes by date"""
    __tablename__ = "motivations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(10), unique=True, nullable=False)  # YYYY-MM-DD
    quote = Column(Text, nullable=False)
    philosophy = Column(Text, default="")  # Explanation
    tradition = Column(String(50), default="esoteric")
    habit_context = Column(Text, default="")  # Personalized context
    created_at = Column(DateTime, default=datetime.utcnow)


class InventoryItem(Base):
    """Inventory table - owned shop items"""
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(String(50), nullable=False)  # Shop item ID
    quantity = Column(Integer, default=1)
    purchased_at = Column(DateTime, default=datetime.utcnow)


class ActiveEffect(Base):
    """Active effects - temporary buffs from consumables"""
    __tablename__ = "active_effects"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    effect_type = Column(String(50), nullable=False)  # xp_multiplier, gold_multiplier, etc.
    value = Column(Float, default=1.0)  # Multiplier value
    expires_at = Column(DateTime, nullable=False)
    item_id = Column(String(50), default=None)  # Source item
    created_at = Column(DateTime, default=datetime.utcnow)


class PhilosophyDocument(Base):
    """Philosophy documents - uploaded wisdom documents"""
    __tablename__ = "philosophy_documents"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)  # pdf, jpg, png, etc.
    file_size = Column(Integer, default=0)
    object_path = Column(String(512), default="")  # Storage path
    category = Column(String(50), default="personal")
    extracted_text = Column(Text, default="")
    ai_summary = Column(Text, default="")
    key_themes = Column(JSON, default=list)
    is_processed = Column(Boolean, default=False)
    use_for_ai = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatSession(Base):
    """Chat sessions - AI coach conversations"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), default="New Chat")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    """Chat messages - individual messages in AI coach conversations"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user/assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")


# ============ DATABASE FUNCTIONS ============

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database and create all tables"""
    Base.metadata.create_all(bind=engine)
    
    # Initialize default records
    db = SessionLocal()
    try:
        # Create default user stats if not exists
        if not db.query(UserStats).first():
            db.add(UserStats(id=1))
            db.commit()
        
        # Create default user profile if not exists
        if not db.query(UserProfile).first():
            db.add(UserProfile(id=1))
            db.commit()
    finally:
        db.close()


def get_user_stats(db) -> UserStats:
    """Get or create user stats"""
    stats = db.query(UserStats).first()
    if not stats:
        stats = UserStats(id=1)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    return stats


def get_user_profile(db) -> UserProfile:
    """Get or create user profile"""
    profile = db.query(UserProfile).first()
    if not profile:
        profile = UserProfile(id=1)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


# Initialize on import
init_db()

"""
Goal Quest Gameplay Mechanics - XP, Ranks, Stats System
Exact replication of the Replit gameplay.ts
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


# ============ XP SYSTEM ============

BASE_XP = 1000  # XP required for level 1 -> 2
XP_GROWTH_RATE = 1.05  # 5% compound growth per level


def calculate_xp_for_level(level: int) -> int:
    """Calculate XP required to reach a specific level"""
    if level <= 1:
        return 0
    return int(BASE_XP * (XP_GROWTH_RATE ** (level - 1)))


def calculate_total_xp_for_level(level: int) -> int:
    """Calculate total XP needed from 0 to reach a level"""
    total = 0
    for lvl in range(2, level + 1):
        total += calculate_xp_for_level(lvl)
    return total


def calculate_level_from_xp(total_xp: int) -> Tuple[int, int, int]:
    """
    Calculate level and progress from total XP
    Returns: (level, current_xp_in_level, xp_needed_for_next_level)
    """
    level = 1
    remaining_xp = total_xp
    
    while True:
        xp_for_next = calculate_xp_for_level(level + 1)
        if remaining_xp < xp_for_next:
            return level, remaining_xp, xp_for_next
        remaining_xp -= xp_for_next
        level += 1
        if level > 100:  # Cap at level 100
            return 100, remaining_xp, xp_for_next


# ============ DIFFICULTY & XP REWARDS ============

HABIT_XP_REWARDS = {
    1: 50,   # Easy
    2: 100,  # Medium
    3: 300,  # Hard
}

GOAL_XP_REWARDS = {
    1: 1000,  # Normal
    2: 2000,  # Medium
    3: 3000,  # Hard
}

DIFFICULTY_NAMES = {
    1: "Easy",
    2: "Medium",
    3: "Hard",
}

DIFFICULTY_COLORS = {
    1: "#22c55e",  # Green
    2: "#eab308",  # Yellow
    3: "#ef4444",  # Red
}


def get_habit_xp(difficulty: int) -> int:
    """Get XP reward for habit based on difficulty"""
    return HABIT_XP_REWARDS.get(difficulty, 50)


def get_goal_xp(difficulty: int) -> int:
    """Get XP reward for goal based on difficulty"""
    return GOAL_XP_REWARDS.get(difficulty, 1000)


# ============ RANK SYSTEM ============

@dataclass
class Rank:
    title: str
    color: str
    min_level: int
    max_level: int


RANKS = [
    Rank("Beginner", "#9ca3af", 1, 10),       # Gray
    Rank("Novice Hunter", "#22c55e", 11, 25), # Green
    Rank("Skilled Hunter", "#3b82f6", 26, 40), # Blue
    Rank("Elite Hunter", "#a855f7", 41, 60),   # Purple
    Rank("Master Hunter", "#f97316", 61, 80),  # Orange
    Rank("S-Rank Hunter", "#ef4444", 81, 99),  # Red
    Rank("Shadow Monarch", "#eab308", 100, 999), # Gold/Yellow
]


def get_rank_for_level(level: int) -> Rank:
    """Get rank information for a given level"""
    for rank in RANKS:
        if rank.min_level <= level <= rank.max_level:
            return rank
    return RANKS[-1]  # Default to highest rank


# ============ STAT SYSTEM ============

@dataclass
class StatMetadata:
    label: str
    icon: str
    color: str
    bg_color: str
    categories: List[str]


STAT_METADATA: Dict[str, StatMetadata] = {
    "strength": StatMetadata(
        label="Strength",
        icon="sword",
        color="#ef4444",  # Red
        bg_color="bg-red-500",
        categories=["fitness"]
    ),
    "intelligence": StatMetadata(
        label="Intelligence",
        icon="brain",
        color="#3b82f6",  # Blue
        bg_color="bg-blue-500",
        categories=["learning", "work", "creative"]
    ),
    "vitality": StatMetadata(
        label="Vitality",
        icon="heart",
        color="#22c55e",  # Green
        bg_color="bg-green-500",
        categories=["health"]
    ),
    "agility": StatMetadata(
        label="Agility",
        icon="zap",
        color="#eab308",  # Yellow
        bg_color="bg-yellow-500",
        categories=["productivity", "social"]
    ),
    "sense": StatMetadata(
        label="Sense",
        icon="eye",
        color="#a855f7",  # Purple
        bg_color="bg-purple-500",
        categories=["mindfulness", "finance"]
    ),
    "willpower": StatMetadata(
        label="Willpower",
        icon="flame",
        color="#f97316",  # Orange
        bg_color="bg-orange-500",
        categories=["personal"]
    ),
}


def get_stat_for_category(category: str) -> Optional[str]:
    """Get which stat a category maps to"""
    category_lower = category.lower()
    for stat_name, metadata in STAT_METADATA.items():
        if category_lower in metadata.categories:
            return stat_name
    return "willpower"  # Default to willpower


def calculate_stat_increase(difficulty: int, base_amount: int = 1) -> int:
    """Calculate stat increase based on difficulty"""
    multipliers = {1: 1, 2: 2, 3: 3}
    return base_amount * multipliers.get(difficulty, 1)


# ============ GOLD SYSTEM ============

def calculate_gold_reward(difficulty: int, is_habit: bool = True) -> int:
    """Calculate gold reward for completing a habit or goal"""
    if is_habit:
        base = {1: 5, 2: 10, 3: 25}
    else:
        base = {1: 50, 2: 100, 3: 200}
    return base.get(difficulty, 5)


# ============ STREAK SYSTEM ============

def calculate_streak_bonus(streak: int) -> float:
    """Calculate XP multiplier bonus for streak"""
    if streak < 7:
        return 1.0
    elif streak < 14:
        return 1.1
    elif streak < 30:
        return 1.2
    elif streak < 60:
        return 1.3
    elif streak < 90:
        return 1.5
    else:
        return 2.0


# ============ FREQUENCY SYSTEM ============

FREQUENCY_TYPES = {
    "daily": "Every day",
    "weekdays": "Mon-Fri",
    "weekends": "Sat-Sun",
    "specific": "Specific days",
    "custom": "Custom interval",
}

WEEKDAYS = [1, 2, 3, 4, 5]  # Monday to Friday (Python weekday format)
WEEKENDS = [5, 6]  # Saturday, Sunday (using 5=Sat, 6=Sun for display)

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def should_show_habit_today(frequency: str, frequency_days: List[int], custom_interval: int, 
                            start_date: str, today_weekday: int) -> bool:
    """Check if a habit should be shown/tracked today"""
    if frequency == "daily":
        return True
    elif frequency == "weekdays":
        return today_weekday < 5  # 0-4 are Mon-Fri
    elif frequency == "weekends":
        return today_weekday >= 5  # 5-6 are Sat-Sun
    elif frequency == "specific":
        return today_weekday in frequency_days
    elif frequency == "custom":
        # Calculate days since start and check interval
        from datetime import datetime
        try:
            start = datetime.strptime(start_date[:10], "%Y-%m-%d")
            today = datetime.now()
            days_since = (today - start).days
            return days_since % custom_interval == 0
        except:
            return True
    return True


# ============ ACHIEVEMENT TIER COLORS ============

ACHIEVEMENT_TIER_COLORS = {
    "bronze": {
        "bg": "bg-amber-600",
        "text": "text-amber-100",
        "border": "border-amber-500",
        "gradient": "from-amber-600 to-amber-700",
    },
    "silver": {
        "bg": "bg-slate-400",
        "text": "text-slate-900",
        "border": "border-slate-300",
        "gradient": "from-slate-400 to-slate-500",
    },
    "gold": {
        "bg": "bg-yellow-500",
        "text": "text-yellow-900",
        "border": "border-yellow-400",
        "gradient": "from-yellow-400 to-yellow-600",
    },
    "platinum": {
        "bg": "bg-cyan-400",
        "text": "text-cyan-900",
        "border": "border-cyan-300",
        "gradient": "from-cyan-400 to-cyan-600",
    },
    "legendary": {
        "bg": "bg-purple-500",
        "text": "text-purple-100",
        "border": "border-purple-400",
        "gradient": "from-purple-500 to-pink-500",
        "glow": "shadow-purple-500/50",
    },
    "mythic": {
        "bg": "bg-rose-500",
        "text": "text-rose-100",
        "border": "border-rose-400",
        "gradient": "from-rose-500 to-orange-500",
        "glow": "shadow-rose-500/50",
    },
}


# ============ SHOP RARITY COLORS ============

RARITY_COLORS = {
    "common": {
        "bg": "#6b7280",  # Gray
        "text": "#ffffff",
        "border": "#9ca3af",
    },
    "uncommon": {
        "bg": "#22c55e",  # Green
        "text": "#ffffff",
        "border": "#4ade80",
    },
    "rare": {
        "bg": "#3b82f6",  # Blue
        "text": "#ffffff",
        "border": "#60a5fa",
    },
    "epic": {
        "bg": "#a855f7",  # Purple
        "text": "#ffffff",
        "border": "#c084fc",
    },
    "legendary": {
        "bg": "#f97316",  # Orange
        "text": "#ffffff",
        "border": "#fb923c",
    },
    "mythic": {
        "bg": "#ef4444",  # Red
        "text": "#ffffff",
        "border": "#f87171",
    },
    "divine": {
        "bg": "#eab308",  # Gold
        "text": "#000000",
        "border": "#fde047",
    },
}


# ============ CATEGORY COLORS ============

CATEGORY_COLORS = {
    "health": "#22c55e",      # Green
    "fitness": "#ef4444",     # Red
    "learning": "#3b82f6",    # Blue
    "mindfulness": "#a855f7", # Purple
    "productivity": "#eab308", # Yellow
    "social": "#ec4899",      # Pink
    "creative": "#f97316",    # Orange
    "finance": "#14b8a6",     # Teal
    "personal": "#6366f1",    # Indigo
    "work": "#64748b",        # Slate
}


# ============ PHILOSOPHY TRADITIONS ============

PHILOSOPHY_TRADITIONS = [
    {"id": "esoteric", "name": "Esoteric/Hermetic", "description": "Ancient mystery traditions"},
    {"id": "biblical", "name": "Biblical", "description": "Christian scripture wisdom"},
    {"id": "quranic", "name": "Quranic", "description": "Islamic spiritual guidance"},
    {"id": "metaphysical", "name": "Metaphysical", "description": "New Thought principles"},
    {"id": "philosophy", "name": "Ancient Philosophy", "description": "Greek and Roman wisdom"},
    {"id": "stoic", "name": "Stoic", "description": "Stoic philosophy"},
    {"id": "eastern", "name": "Eastern", "description": "Buddhist and Hindu teachings"},
    {"id": "kemetic", "name": "Kemetic", "description": "Ancient Egyptian wisdom"},
    {"id": "samurai", "name": "Samurai/Bushido", "description": "Way of the warrior"},
    {"id": "occult", "name": "Occult", "description": "Western mystical traditions"},
]


# ============ AVATAR STYLES ============

AVATAR_STYLES = [
    {"id": "warrior", "name": "Warrior", "icon": "⚔️", "description": "Strength and discipline"},
    {"id": "mage", "name": "Mage", "icon": "🪄", "description": "Knowledge and wisdom"},
    {"id": "rogue", "name": "Rogue", "icon": "👁️", "description": "Speed and adaptability"},
    {"id": "sage", "name": "Sage", "icon": "📚", "description": "Balance and insight"},
]


# ============ FOCUS AREAS ============

FOCUS_AREAS = [
    {"id": "health", "name": "Health & Fitness", "icon": "💪", "description": "Physical wellbeing"},
    {"id": "career", "name": "Career & Finance", "icon": "💼", "description": "Professional growth"},
    {"id": "relationships", "name": "Relationships", "icon": "❤️", "description": "Connections with others"},
    {"id": "creativity", "name": "Creativity", "icon": "🎨", "description": "Artistic expression"},
    {"id": "mindfulness", "name": "Mindfulness", "icon": "🧠", "description": "Mental clarity"},
    {"id": "learning", "name": "Learning", "icon": "📖", "description": "Knowledge acquisition"},
]


# ============ CHALLENGE APPROACHES ============

CHALLENGE_APPROACHES = [
    {"id": "discipline", "name": "Discipline", "icon": "⚔️", "description": "Consistent daily action"},
    {"id": "strategy", "name": "Strategy", "icon": "🧭", "description": "Careful planning"},
    {"id": "community", "name": "Community", "icon": "👥", "description": "Support from others"},
    {"id": "reflection", "name": "Reflection", "icon": "💡", "description": "Self-analysis"},
    {"id": "action", "name": "Bold Action", "icon": "⚡", "description": "Decisive moves"},
]


# ============ TIMEZONES ============

TIMEZONES = [
    {"value": "America/New_York", "label": "Eastern Time (ET)"},
    {"value": "America/Chicago", "label": "Central Time (CT)"},
    {"value": "America/Denver", "label": "Mountain Time (MT)"},
    {"value": "America/Los_Angeles", "label": "Pacific Time (PT)"},
    {"value": "America/Phoenix", "label": "Arizona Time"},
    {"value": "America/Anchorage", "label": "Alaska Time"},
    {"value": "Pacific/Honolulu", "label": "Hawaii Time"},
    {"value": "UTC", "label": "UTC"},
    {"value": "Europe/London", "label": "London (GMT/BST)"},
    {"value": "Europe/Paris", "label": "Paris (CET)"},
    {"value": "Asia/Tokyo", "label": "Tokyo (JST)"},
]

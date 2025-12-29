"""
Goal Quest UI Components - Streamlit components matching React UI
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, date, timedelta
import json

from gameplay import (
    STAT_METADATA, DIFFICULTY_NAMES, DIFFICULTY_COLORS, CATEGORY_COLORS,
    ACHIEVEMENT_TIER_COLORS, calculate_level_from_xp, get_rank_for_level
)


# ============ ICON MAPPING ============
# Map Lucide React icons to emoji equivalents
ICON_MAP = {
    # Stats
    "Sword": "⚔️",
    "Brain": "🧠",
    "Heart": "❤️",
    "Zap": "⚡",
    "Eye": "👁️",
    "Flame": "🔥",
    
    # Navigation
    "Home": "🏠",
    "Target": "🎯",
    "Trophy": "🏆",
    "Award": "🏅",
    "Medal": "🎖️",
    "Crown": "👑",
    "Star": "⭐",
    "Shield": "🛡️",
    
    # Actions
    "Check": "✅",
    "CheckCircle": "✅",
    "Plus": "➕",
    "Minus": "➖",
    "X": "❌",
    "Edit": "✏️",
    "Trash2": "🗑️",
    "Save": "💾",
    
    # Categories
    "Dumbbell": "💪",
    "BookOpen": "📖",
    "Briefcase": "💼",
    "Coins": "💰",
    "Calendar": "📅",
    "Clock": "🕐",
    "Bell": "🔔",
    "Settings": "⚙️",
    
    # Special
    "Sparkles": "✨",
    "Lightning": "⚡",
    "Sun": "☀️",
    "Moon": "🌙",
    "Globe": "🌍",
    "Compass": "🧭",
    "Map": "🗺️",
    "Rocket": "🚀",
    
    # Content
    "FileText": "📄",
    "PenTool": "✒️",
    "Quote": "💬",
    "MessageSquare": "💬",
    "Bot": "🤖",
    "User": "👤",
    "Users": "👥",
    "Upload": "📤",
    "Download": "📥",
    
    # Items
    "Flask": "🧪",
    "FlaskConical": "⚗️",
    "Wine": "🍷",
    "Diamond": "💎",
    "Gem": "💎",
    "Circle": "⭕",
    "Square": "⬜",
    "Triangle": "🔺",
    
    # Misc
    "RotateCcw": "🔄",
    "TrendingUp": "📈",
    "TrendingDown": "📉",
    "Activity": "📊",
    "BarChart": "📊",
    "PieChart": "🥧",
    "Layers": "📚",
    "Grid": "📱",
    "List": "📋",
    "Link": "🔗",
    "Lock": "🔒",
    "Unlock": "🔓",
    "Key": "🔑",
    "Search": "🔍",
    "Filter": "🔽",
    "Sort": "↕️",
    "ArrowUp": "⬆️",
    "ArrowDown": "⬇️",
    "ArrowLeft": "⬅️",
    "ArrowRight": "➡️",
    "ChevronUp": "🔼",
    "ChevronDown": "🔽",
    "ChevronLeft": "◀️",
    "ChevronRight": "▶️",
    "Sunrise": "🌅",
    "Sunset": "🌇",
    "Timer": "⏱️",
    "Hourglass": "⏳",
    "Mountain": "⛰️",
    "Scale": "⚖️",
    "Power": "🔌",
    "Palette": "🎨",
    "GraduationCap": "🎓",
    "ListChecks": "📋",
    "ListPlus": "📝",
    "Repeat": "🔁",
    "ArrowUpRight": "↗️",
    "ScrollText": "📜",
    "ShieldCheck": "🛡️",
    "ShieldHalf": "🛡️",
    "Swords": "⚔️",
    "Frame": "🖼️",
    "Library": "📚",
    "Scroll": "📜",
    "LogIn": "🚪",
    "UserCircle": "👤",
    "CalendarDays": "📆",
}


def get_icon(icon_name: str) -> str:
    """Get emoji icon for icon name"""
    return ICON_MAP.get(icon_name, "❓")


# ============ CARD COMPONENTS ============

def stat_card(stat_name: str, value: int, show_bar: bool = True, max_value: int = 100):
    """Render a stat card with icon, value, and optional progress bar"""
    meta = STAT_METADATA.get(stat_name)
    if not meta:
        return
    
    icon = get_icon(meta.icon.title())
    progress = min(value / max_value, 1.0) if show_bar else 0
    
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, {meta.color}15, transparent);
        border: 1px solid {meta.color}40;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    '>
        <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>{icon}</div>
        <div style='color: {meta.color}; font-size: 1.8rem; font-weight: 700;'>{value}</div>
        <div style='color: #9ca3af; font-size: 0.85rem; margin-bottom: 0.5rem;'>{meta.label}</div>
        {"<div style='background: rgba(0,0,0,0.3); border-radius: 8px; height: 6px; overflow: hidden;'><div style='background: " + meta.color + "; height: 100%; width: " + str(progress * 100) + "%; transition: width 0.5s ease;'></div></div>" if show_bar else ""}
    </div>
    """, unsafe_allow_html=True)


def player_card(stats, profile):
    """Render the player info card with level, rank, XP bar"""
    level, current_xp, xp_needed = calculate_level_from_xp(stats.total_xp)
    rank = get_rank_for_level(level)
    progress = (current_xp / xp_needed * 100) if xp_needed > 0 else 100
    
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.1), transparent);
        border: 2px solid rgba(251, 191, 36, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
    '>
        <div style='
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            border-radius: 50%;
            margin: 0 auto 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            box-shadow: 0 0 30px rgba(251, 191, 36, 0.4);
        '>👑</div>
        
        <h2 style='margin: 0; color: #fbbf24;'>{profile.display_name}</h2>
        
        <div style='
            display: inline-block;
            background: {rank.color}20;
            border: 1px solid {rank.color};
            color: {rank.color};
            padding: 4px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            margin: 0.5rem 0;
        '>{rank.title}</div>
        
        <div style='margin: 1rem 0;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                <span style='color: #fbbf24; font-weight: 600;'>Level {level}</span>
                <span style='color: #9ca3af; font-size: 0.9rem;'>{current_xp:,} / {xp_needed:,}</span>
            </div>
            <div style='background: rgba(0,0,0,0.4); border-radius: 10px; height: 12px; overflow: hidden;'>
                <div style='
                    background: linear-gradient(90deg, #fbbf24, #f59e0b);
                    height: 100%;
                    width: {progress}%;
                    border-radius: 10px;
                    transition: width 0.5s ease;
                    box-shadow: 0 0 10px rgba(251, 191, 36, 0.5);
                '></div>
            </div>
        </div>
        
        <div style='
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 1rem;
        '>
            <div style='text-align: center;'>
                <div style='color: #fbbf24; font-size: 1.2rem; font-weight: 600;'>💰 {stats.current_gold:,}</div>
                <div style='color: #9ca3af; font-size: 0.8rem;'>Gold</div>
            </div>
            <div style='text-align: center;'>
                <div style='color: #a855f7; font-size: 1.2rem; font-weight: 600;'>✨ {stats.total_xp:,}</div>
                <div style='color: #9ca3af; font-size: 0.8rem;'>Total XP</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def habit_card(habit, streak: int, completed_today: bool, on_complete: Callable = None):
    """Render a habit card with completion button"""
    difficulty_name = DIFFICULTY_NAMES.get(habit.difficulty, "Easy")
    difficulty_color = DIFFICULTY_COLORS.get(habit.difficulty, "#22c55e")
    category_color = CATEGORY_COLORS.get(habit.category, "#6366f1")
    xp_reward = {1: 50, 2: 100, 3: 300}.get(habit.difficulty, 50)
    
    bg_opacity = "0.15" if completed_today else "0.08"
    border_color = "#22c55e" if completed_today else f"{category_color}60"
    
    st.markdown(f"""
    <div style='
        background: rgba(30, 30, 50, {bg_opacity});
        border: 2px solid {border_color};
        border-radius: 16px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    '>
        <div style='display: flex; justify-content: space-between; align-items: start;'>
            <div style='flex: 1;'>
                <div style='display: flex; align-items: center; gap: 8px; flex-wrap: wrap;'>
                    {"⭐ " if habit.priority else ""}
                    <span style='font-weight: 600; font-size: 1.1rem;'>{habit.name}</span>
                    {"✅" if completed_today else ""}
                </div>
                
                {f"<p style='color: #9ca3af; font-size: 0.9rem; margin: 0.25rem 0;'>{habit.description}</p>" if habit.description else ""}
                
                <div style='display: flex; gap: 8px; flex-wrap: wrap; margin-top: 0.5rem;'>
                    <span style='
                        background: {category_color}25;
                        color: {category_color};
                        padding: 2px 10px;
                        border-radius: 12px;
                        font-size: 0.8rem;
                    '>{habit.category.title()}</span>
                    
                    <span style='
                        background: {difficulty_color}25;
                        color: {difficulty_color};
                        padding: 2px 10px;
                        border-radius: 12px;
                        font-size: 0.8rem;
                    '>{difficulty_name}</span>
                    
                    <span style='
                        background: rgba(251, 191, 36, 0.2);
                        color: #fbbf24;
                        padding: 2px 10px;
                        border-radius: 12px;
                        font-size: 0.8rem;
                    '>+{xp_reward} XP</span>
                </div>
            </div>
            
            <div style='text-align: right; margin-left: 1rem;'>
                <div style='
                    background: linear-gradient(135deg, #f97316, #ef4444);
                    color: white;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-weight: 600;
                    font-size: 0.9rem;
                '>🔥 {streak}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def goal_card(goal, days_remaining: Optional[int] = None):
    """Render a goal card with progress"""
    difficulty_name = DIFFICULTY_NAMES.get(goal.difficulty, "Normal")
    difficulty_color = DIFFICULTY_COLORS.get(goal.difficulty, "#22c55e")
    xp_reward = {1: 1000, 2: 2000, 3: 3000}.get(goal.difficulty, 1000)
    
    # Calculate days remaining color
    if days_remaining is not None:
        if days_remaining < 0:
            date_color = "#ef4444"
            date_text = f"Overdue by {abs(days_remaining)} days"
        elif days_remaining <= 7:
            date_color = "#eab308"
            date_text = f"{days_remaining} days left"
        else:
            date_color = "#22c55e"
            date_text = f"{days_remaining} days left"
    else:
        date_color = "#9ca3af"
        date_text = "No deadline"
    
    st.markdown(f"""
    <div style='
        background: rgba(30, 30, 50, 0.8);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 16px;
        padding: 1.25rem;
        margin: 0.5rem 0;
    '>
        <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;'>
            <div>
                <h3 style='margin: 0; font-size: 1.1rem;'>{"⭐ " if goal.priority else ""}🎯 {goal.title}</h3>
                {f"<p style='color: #9ca3af; font-size: 0.9rem; margin: 0.25rem 0;'>{goal.description}</p>" if goal.description else ""}
            </div>
            <div style='text-align: right;'>
                <span style='
                    background: {difficulty_color}25;
                    color: {difficulty_color};
                    padding: 2px 10px;
                    border-radius: 12px;
                    font-size: 0.8rem;
                '>{difficulty_name}</span>
            </div>
        </div>
        
        <div style='margin-bottom: 0.75rem;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                <span style='color: #9ca3af; font-size: 0.85rem;'>Progress</span>
                <span style='color: #fbbf24; font-weight: 600;'>{goal.progress}%</span>
            </div>
            <div style='background: rgba(0,0,0,0.4); border-radius: 8px; height: 10px; overflow: hidden;'>
                <div style='
                    background: linear-gradient(90deg, #fbbf24, #f59e0b);
                    height: 100%;
                    width: {goal.progress}%;
                    border-radius: 8px;
                '></div>
            </div>
        </div>
        
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='color: {date_color}; font-size: 0.85rem;'>📅 {date_text}</span>
            <span style='color: #fbbf24; font-size: 0.9rem; font-weight: 600;'>+{xp_reward} XP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def achievement_card(achievement, is_unlocked: bool = False):
    """Render an achievement card"""
    tier_colors = ACHIEVEMENT_TIER_COLORS.get(achievement.tier, ACHIEVEMENT_TIER_COLORS["bronze"])
    tier_color = {
        "bronze": "#d97706",
        "silver": "#9ca3af",
        "gold": "#fbbf24",
        "platinum": "#22d3ee",
        "legendary": "#a855f7",
        "mythic": "#ef4444"
    }.get(achievement.tier, "#fbbf24")
    
    icon = get_icon(achievement.icon) if is_unlocked else "🔒"
    opacity = "1" if is_unlocked else "0.5"
    
    st.markdown(f"""
    <div style='
        background: {"linear-gradient(135deg, " + tier_color + "15, transparent)" if is_unlocked else "rgba(30, 30, 50, 0.5)"};
        border: 2px solid {tier_color}{"" if is_unlocked else "40"};
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        opacity: {opacity};
        transition: all 0.3s ease;
    '>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{icon}</div>
        <div style='font-weight: 600; color: {tier_color}; margin-bottom: 0.25rem;'>{achievement.title}</div>
        <div style='font-size: 0.8rem; color: #9ca3af; margin-bottom: 0.5rem;'>{achievement.description}</div>
        <div style='font-size: 0.85rem;'>
            <span style='color: #fbbf24;'>+{achievement.xp_reward} XP</span>
            {f" • <span style='color: #eab308;'>+{achievement.gold_reward} 💰</span>" if achievement.gold_reward else ""}
        </div>
        <div style='
            background: {tier_color};
            color: {"#000" if achievement.tier in ["gold", "silver"] else "#fff"};
            padding: 2px 12px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            display: inline-block;
            margin-top: 0.5rem;
            text-transform: uppercase;
        '>{achievement.tier}</div>
    </div>
    """, unsafe_allow_html=True)


def shop_item_card(item, can_afford: bool, meets_level: bool, on_buy: Callable = None):
    """Render a shop item card"""
    from shop_items import RARITY_COLORS
    
    rarity_color = RARITY_COLORS.get(item.rarity, {}).get("bg", "#6b7280")
    opacity = "1" if can_afford and meets_level else "0.6"
    icon = get_icon(item.icon)
    
    st.markdown(f"""
    <div style='
        background: rgba(30, 30, 50, 0.8);
        border: 2px solid {rarity_color};
        border-radius: 16px;
        padding: 1rem;
        opacity: {opacity};
        transition: all 0.3s ease;
    '>
        <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;'>
            <span style='font-size: 1.5rem;'>{icon}</span>
            <span style='
                background: {rarity_color};
                color: white;
                padding: 2px 8px;
                border-radius: 8px;
                font-size: 0.7rem;
                font-weight: 600;
                text-transform: uppercase;
            '>{item.rarity}</span>
        </div>
        
        <div style='font-weight: 600; margin-bottom: 0.25rem;'>{item.name}</div>
        <div style='font-size: 0.8rem; color: #9ca3af; margin-bottom: 0.75rem; min-height: 40px;'>
            {item.description[:80]}{"..." if len(item.description) > 80 else ""}
        </div>
        
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <span style='color: #fbbf24; font-weight: 600;'>💰 {item.price.gold:,}</span>
                {f"<span style='color: #a855f7; margin-left: 8px;'>💎 {item.price.crystals}</span>" if item.price.crystals > 0 else ""}
            </div>
            {f"<span style='color: #9ca3af; font-size: 0.8rem;'>Lv.{item.level_required}</span>" if item.level_required else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)


def note_card(note):
    """Render a note card"""
    color_map = {
        "default": ("rgba(30, 30, 50, 0.8)", "#9ca3af"),
        "yellow": ("rgba(234, 179, 8, 0.15)", "#fbbf24"),
        "green": ("rgba(34, 197, 94, 0.15)", "#22c55e"),
        "blue": ("rgba(59, 130, 246, 0.15)", "#3b82f6"),
        "purple": ("rgba(168, 85, 247, 0.15)", "#a855f7"),
    }
    
    bg_color, accent_color = color_map.get(note.color, color_map["default"])
    
    category_icons = {
        "personal": "👤",
        "work": "💼",
        "health": "❤️",
        "goals": "🎯",
        "ideas": "💡",
        "learning": "📖",
    }
    
    icon = category_icons.get(note.category, "📝")
    
    st.markdown(f"""
    <div style='
        background: {bg_color};
        border: 1px solid {accent_color}40;
        border-radius: 16px;
        padding: 1rem;
        margin: 0.5rem 0;
    '>
        <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;'>
            <span style='font-weight: 600;'>{"📌 " if note.pinned else ""}{icon} {note.title}</span>
            <span style='
                background: {accent_color}25;
                color: {accent_color};
                padding: 2px 8px;
                border-radius: 8px;
                font-size: 0.75rem;
            '>{note.category}</span>
        </div>
        
        <p style='color: #9ca3af; font-size: 0.9rem; margin: 0.5rem 0;'>
            {(note.content or "")[:150]}{"..." if len(note.content or "") > 150 else ""}
        </p>
        
        {f"<div style='display: flex; gap: 4px; flex-wrap: wrap; margin: 0.5rem 0;'>" + "".join([f"<span style='background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 8px; font-size: 0.75rem;'>{tag}</span>" for tag in (note.tags or [])[:3]]) + "</div>" if note.tags else ""}
        
        <div style='color: #6b7280; font-size: 0.8rem; margin-top: 0.5rem;'>
            {note.created_at.strftime("%Y-%m-%d %H:%M") if note.created_at else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)


def wisdom_card(quote: str, philosophy: str, tradition: str):
    """Render a daily wisdom quote card"""
    tradition_icons = {
        "esoteric": "👁️",
        "biblical": "📖",
        "quranic": "📖",
        "metaphysical": "✨",
        "philosophy": "🏛️",
        "stoic": "🏛️",
        "eastern": "☯️",
        "kemetic": "𓂀",
        "samurai": "⚔️",
        "occult": "🔮",
    }
    
    icon = tradition_icons.get(tradition, "📜")
    
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.1), rgba(168, 85, 247, 0.05));
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
    '>
        <div style='font-size: 2rem; margin-bottom: 1rem;'>{icon}</div>
        
        <p style='
            font-size: 1.2rem;
            font-style: italic;
            color: #fbbf24;
            margin-bottom: 1rem;
            line-height: 1.6;
        '>"{quote}"</p>
        
        <p style='color: #9ca3af; font-size: 0.95rem; margin-bottom: 0.5rem;'>{philosophy}</p>
        
        <span style='
            background: rgba(251, 191, 36, 0.2);
            color: #fbbf24;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8rem;
        '>— {tradition.title()} Tradition</span>
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, icon: str = "📊", color: str = "#fbbf24"):
    """Render a metric card"""
    st.markdown(f"""
    <div style='
        background: rgba(30, 30, 50, 0.8);
        border: 1px solid {color}40;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
    '>
        <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>{icon}</div>
        <div style='font-size: 1.8rem; font-weight: 700; color: {color};'>{value}</div>
        <div style='color: #9ca3af; font-size: 0.85rem;'>{label}</div>
    </div>
    """, unsafe_allow_html=True)


def progress_ring(value: int, max_value: int, label: str, color: str = "#fbbf24"):
    """Render a circular progress indicator"""
    percentage = (value / max_value * 100) if max_value > 0 else 0
    
    st.markdown(f"""
    <div style='text-align: center;'>
        <div style='
            position: relative;
            width: 80px;
            height: 80px;
            margin: 0 auto;
        '>
            <svg viewBox="0 0 36 36" style="transform: rotate(-90deg);">
                <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="rgba(255,255,255,0.1)"
                    stroke-width="3"
                />
                <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="{color}"
                    stroke-width="3"
                    stroke-dasharray="{percentage}, 100"
                    stroke-linecap="round"
                />
            </svg>
            <div style='
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-weight: 700;
                font-size: 1rem;
                color: {color};
            '>{percentage:.0f}%</div>
        </div>
        <div style='color: #9ca3af; font-size: 0.85rem; margin-top: 0.5rem;'>{label}</div>
    </div>
    """, unsafe_allow_html=True)

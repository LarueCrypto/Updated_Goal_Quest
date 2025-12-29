"""
Goal Quest - Complete Demo Application
======================================
A demonstration of the character evolution system integrated
with a simple habit tracking interface.

Run with: streamlit run demo_app.py
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, List
import json

# Import character system
from character_system import (
    init_character_state,
    render_character_display,
    render_character_customization,
    render_shop_interface,
    render_equipment_manager,
    render_tier_overview,
    get_evolution_tier,
    EVOLUTION_TIERS
)

from integration_helpers import (
    setup_character_system,
    on_habit_complete,
    on_achievement_unlock,
    show_xp_notification,
    render_sidebar_character,
    get_current_tier_info,
    award_gold,
    award_gems,
    debug_panel
)


# =============================================================================
# SAMPLE HABIT DATA
# =============================================================================

SAMPLE_HABITS = [
    {
        "id": "habit_exercise",
        "name": "Exercise",
        "icon": "🏃",
        "description": "Complete at least 30 minutes of exercise",
        "xp_reward": 30,
        "gold_reward": 15,
        "streak": 0,
        "completed_today": False
    },
    {
        "id": "habit_reading",
        "name": "Read",
        "icon": "📚",
        "description": "Read for 20 minutes",
        "xp_reward": 20,
        "gold_reward": 10,
        "streak": 0,
        "completed_today": False
    },
    {
        "id": "habit_meditate",
        "name": "Meditate",
        "icon": "🧘",
        "description": "Meditate for 10 minutes",
        "xp_reward": 25,
        "gold_reward": 12,
        "streak": 0,
        "completed_today": False
    },
    {
        "id": "habit_water",
        "name": "Drink Water",
        "icon": "💧",
        "description": "Drink 8 glasses of water",
        "xp_reward": 15,
        "gold_reward": 8,
        "streak": 0,
        "completed_today": False
    },
    {
        "id": "habit_sleep",
        "name": "Sleep Well",
        "icon": "😴",
        "description": "Get 7-8 hours of sleep",
        "xp_reward": 35,
        "gold_reward": 20,
        "streak": 0,
        "completed_today": False
    },
    {
        "id": "habit_journal",
        "name": "Journal",
        "icon": "✍️",
        "description": "Write in your journal",
        "xp_reward": 25,
        "gold_reward": 15,
        "streak": 0,
        "completed_today": False
    }
]


SAMPLE_ACHIEVEMENTS = [
    {
        "id": "ach_first_habit",
        "name": "First Step",
        "icon": "🌟",
        "description": "Complete your first habit",
        "requirement": {"type": "habits_total", "count": 1},
        "gold_reward": 100,
        "gem_reward": 5,
        "xp_reward": 50,
        "unlocked": False
    },
    {
        "id": "ach_streak_3",
        "name": "On a Roll",
        "icon": "🔥",
        "description": "Reach a 3-day streak on any habit",
        "requirement": {"type": "streak", "count": 3},
        "gold_reward": 150,
        "gem_reward": 10,
        "xp_reward": 75,
        "unlocked": False
    },
    {
        "id": "ach_level_10",
        "name": "Rising Hero",
        "icon": "⚔️",
        "description": "Reach level 10",
        "requirement": {"type": "level", "count": 10},
        "gold_reward": 250,
        "gem_reward": 15,
        "xp_reward": 100,
        "unlocked": False
    },
    {
        "id": "ach_all_habits",
        "name": "Perfect Day",
        "icon": "👑",
        "description": "Complete all habits in one day",
        "requirement": {"type": "daily_all", "count": 1},
        "gold_reward": 200,
        "gem_reward": 20,
        "xp_reward": 100,
        "unlocked": False
    },
    {
        "id": "ach_shop_first",
        "name": "Fashion Forward",
        "icon": "🛍️",
        "description": "Purchase your first item from the shop",
        "requirement": {"type": "shop_purchase", "count": 1},
        "gold_reward": 50,
        "gem_reward": 5,
        "xp_reward": 30,
        "unlocked": False
    }
]


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def init_demo_state():
    """Initialize demo application state."""
    setup_character_system(
        initial_level=1,
        initial_gold=500,
        initial_gems=10,
        initial_xp=0
    )
    
    if "habits" not in st.session_state:
        st.session_state.habits = [dict(h) for h in SAMPLE_HABITS]
    
    if "achievements" not in st.session_state:
        st.session_state.achievements = [dict(a) for a in SAMPLE_ACHIEVEMENTS]
    
    if "total_habits_completed" not in st.session_state:
        st.session_state.total_habits_completed = 0
    
    if "last_check_date" not in st.session_state:
        st.session_state.last_check_date = str(date.today())
    
    # Reset daily habits if new day
    if st.session_state.last_check_date != str(date.today()):
        for habit in st.session_state.habits:
            if habit["completed_today"]:
                habit["streak"] += 1
            else:
                habit["streak"] = 0
            habit["completed_today"] = False
        st.session_state.last_check_date = str(date.today())


def check_achievements():
    """Check and unlock achievements."""
    for ach in st.session_state.achievements:
        if ach["unlocked"]:
            continue
        
        req = ach["requirement"]
        unlocked = False
        
        if req["type"] == "habits_total":
            unlocked = st.session_state.total_habits_completed >= req["count"]
        elif req["type"] == "streak":
            max_streak = max(h["streak"] for h in st.session_state.habits)
            unlocked = max_streak >= req["count"]
        elif req["type"] == "level":
            unlocked = st.session_state.player_level >= req["count"]
        elif req["type"] == "daily_all":
            unlocked = all(h["completed_today"] for h in st.session_state.habits)
        elif req["type"] == "shop_purchase":
            unlocked = len(st.session_state.inventory) >= req["count"]
        
        if unlocked:
            ach["unlocked"] = True
            result = on_achievement_unlock(
                ach["gold_reward"],
                ach["gem_reward"],
                ach["xp_reward"]
            )
            st.toast(f"🏆 Achievement Unlocked: {ach['name']}!")
            st.balloons()


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_habits_page():
    """Render the main habits tracking page."""
    st.title("📋 Daily Habits")
    
    completed_today = sum(1 for h in st.session_state.habits if h["completed_today"])
    total_habits = len(st.session_state.habits)
    
    # Progress bar
    st.progress(completed_today / total_habits, text=f"Today's Progress: {completed_today}/{total_habits}")
    
    st.markdown("---")
    
    # Habit grid
    cols = st.columns(2)
    
    for idx, habit in enumerate(st.session_state.habits):
        with cols[idx % 2]:
            with st.container():
                completed = habit["completed_today"]
                
                # Card styling
                bg_color = "rgba(34, 197, 94, 0.2)" if completed else "rgba(0, 0, 0, 0.2)"
                border_color = "#22C55E" if completed else "#374151"
                
                st.markdown(f"""
                <div style="
                    padding: 20px;
                    margin: 10px 0;
                    border-radius: 15px;
                    border: 2px solid {border_color};
                    background: {bg_color};
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 2rem;">{habit['icon']}</span>
                            <span style="font-size: 1.3rem; font-weight: bold; margin-left: 10px;">{habit['name']}</span>
                            {'<span style="color: #22C55E; margin-left: 10px;">✓</span>' if completed else ''}
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #F59E0B;">🔥 {habit['streak']} day streak</div>
                        </div>
                    </div>
                    <p style="color: #9CA3AF; margin: 10px 0;">{habit['description']}</p>
                    <div style="display: flex; gap: 15px;">
                        <span style="color: #A855F7;">⭐ {habit['xp_reward']} XP</span>
                        <span style="color: #F59E0B;">💰 {habit['gold_reward']} Gold</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if not completed:
                    if st.button(f"Complete {habit['icon']}", key=f"btn_{habit['id']}", use_container_width=True):
                        # Mark as completed
                        habit["completed_today"] = True
                        st.session_state.total_habits_completed += 1
                        
                        # Award rewards
                        result = on_habit_complete(habit["xp_reward"], habit["gold_reward"])
                        
                        # Show notification
                        show_xp_notification(result)
                        
                        # Check achievements
                        check_achievements()
                        
                        st.rerun()
                else:
                    st.success("Completed!")


def render_achievements_page():
    """Render the achievements page."""
    st.title("🏆 Achievements")
    
    unlocked = [a for a in st.session_state.achievements if a["unlocked"]]
    locked = [a for a in st.session_state.achievements if not a["unlocked"]]
    
    st.metric("Achievements", f"{len(unlocked)}/{len(st.session_state.achievements)}")
    
    st.markdown("---")
    
    if unlocked:
        st.markdown("### 🌟 Unlocked")
        for ach in unlocked:
            st.markdown(f"""
            <div style="
                padding: 15px;
                margin: 10px 0;
                border-radius: 10px;
                border: 2px solid #F59E0B;
                background: rgba(245, 158, 11, 0.1);
            ">
                <span style="font-size: 1.5rem;">{ach['icon']}</span>
                <span style="font-size: 1.2rem; font-weight: bold; color: #F59E0B; margin-left: 10px;">{ach['name']}</span>
                <p style="color: #9CA3AF; margin: 5px 0;">{ach['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    if locked:
        st.markdown("### 🔒 Locked")
        for ach in locked:
            st.markdown(f"""
            <div style="
                padding: 15px;
                margin: 10px 0;
                border-radius: 10px;
                border: 2px solid #374151;
                background: rgba(0, 0, 0, 0.2);
                opacity: 0.7;
            ">
                <span style="font-size: 1.5rem;">❓</span>
                <span style="font-size: 1.2rem; font-weight: bold; margin-left: 10px;">{ach['name']}</span>
                <p style="color: #9CA3AF; margin: 5px 0;">{ach['description']}</p>
                <div style="display: flex; gap: 15px; color: #6B7280;">
                    <span>💰 {ach['gold_reward']}</span>
                    <span>💎 {ach['gem_reward']}</span>
                    <span>⭐ {ach['xp_reward']} XP</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_stats_page():
    """Render statistics page."""
    st.title("📊 Statistics")
    
    tier_info = get_current_tier_info()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Level", st.session_state.player_level)
        st.metric("Total Habits", st.session_state.total_habits_completed)
    
    with col2:
        st.metric("Current Tier", f"{tier_info['tier_icon']} {tier_info['tier_name']}")
        unlocked_ach = sum(1 for a in st.session_state.achievements if a["unlocked"])
        st.metric("Achievements", f"{unlocked_ach}/{len(st.session_state.achievements)}")
    
    with col3:
        st.metric("Gold", st.session_state.player_gold)
        st.metric("Gems", st.session_state.player_gems)
    
    st.markdown("---")
    
    # Streak leaderboard
    st.markdown("### 🔥 Habit Streaks")
    
    sorted_habits = sorted(st.session_state.habits, key=lambda x: x["streak"], reverse=True)
    
    for habit in sorted_habits:
        streak_color = "#F59E0B" if habit["streak"] > 0 else "#6B7280"
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: space-between;
            padding: 10px;
            margin: 5px 0;
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.2);
        ">
            <span>{habit['icon']} {habit['name']}</span>
            <span style="color: {streak_color}; font-weight: bold;">🔥 {habit['streak']} days</span>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Goal Quest Demo",
        page_icon="⚔️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
        .stButton > button {
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stProgress > div > div {
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize
    init_demo_state()
    
    # Sidebar
    with st.sidebar:
        st.title("⚔️ Goal Quest")
        st.markdown("---")
        
        # Character display
        render_sidebar_character(show_currencies=True, avatar_size=120)
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["📋 Habits", "👤 Character", "🏪 Shop", "⚔️ Equipment", "🏆 Achievements", "📊 Stats", "🌟 Tiers"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Debug panel
        debug_panel()
    
    # Main content
    if page == "📋 Habits":
        render_habits_page()
    elif page == "👤 Character":
        st.title("👤 Your Character")
        
        tab1, tab2 = st.tabs(["View", "Customize"])
        
        with tab1:
            render_character_display(show_stats=True, size=250)
        
        with tab2:
            render_character_customization()
    
    elif page == "🏪 Shop":
        render_shop_interface()
        check_achievements()  # Check shop achievement
    
    elif page == "⚔️ Equipment":
        render_equipment_manager()
    
    elif page == "🏆 Achievements":
        render_achievements_page()
    
    elif page == "📊 Stats":
        render_stats_page()
    
    elif page == "🌟 Tiers":
        render_tier_overview()


if __name__ == "__main__":
    main()

"""
Goal Quest - Complete Streamlit Application
Exact replication of the Replit Goal Quest 2 app with all 11 pages
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import json
import os
from typing import List, Dict, Any, Optional
import random

# Import our custom modules
from database import (
    SessionLocal, init_db, 
    Habit, Goal, Completion, UserStats, UserProfile, 
    Note, Achievement, Motivation, InventoryItem, ActiveEffect,
    PhilosophyDocument, ChatSession, ChatMessage,
    get_user_stats, get_user_profile
)
from gameplay import (
    calculate_level_from_xp, calculate_xp_for_level, get_rank_for_level,
    get_habit_xp, get_goal_xp, calculate_gold_reward, calculate_streak_bonus,
    STAT_METADATA, DIFFICULTY_NAMES, DIFFICULTY_COLORS, CATEGORY_COLORS,
    PHILOSOPHY_TRADITIONS, AVATAR_STYLES, FOCUS_AREAS, CHALLENGE_APPROACHES, TIMEZONES,
    DAY_NAMES, should_show_habit_today, get_stat_for_category
)
from achievements import ALL_ACHIEVEMENTS, ACHIEVEMENTS_BY_KEY, ACHIEVEMENT_CATEGORIES, ACHIEVEMENT_TIERS
from shop_items import ALL_SHOP_ITEMS, SHOP_ITEMS_BY_ID, SHOP_CATEGORIES, RARITY_COLORS
from ai_integration import (
    get_wisdom_quote, generate_habit_suggestions as ai_generate_habits,
    generate_goal_plan as ai_generate_goal, generate_ai_summary, analyze_notes
)

# Page configuration
st.set_page_config(
    page_title="Goal Quest",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Custom CSS for Solo Leveling theme
def load_custom_css():
    st.markdown("""
    <style>
    /* Solo Leveling Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Gold accent colors */
    .gold-text { color: #fbbf24 !important; }
    .gold-bg { background: linear-gradient(135deg, #fbbf24, #f59e0b) !important; }
    
    /* Card styling */
    .quest-card {
        background: rgba(30, 30, 50, 0.8);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    
    .quest-card:hover {
        border-color: rgba(251, 191, 36, 0.6);
        box-shadow: 0 0 20px rgba(251, 191, 36, 0.2);
    }
    
    /* XP Bar */
    .xp-bar-container {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 3px;
        margin: 10px 0;
    }
    
    .xp-bar {
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
        border-radius: 8px;
        height: 20px;
        transition: width 0.5s ease;
    }
    
    /* Stat badges */
    .stat-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 12px;
        font-weight: 600;
        margin: 4px;
    }
    
    /* Tier colors */
    .tier-bronze { background: linear-gradient(135deg, #d97706, #b45309); }
    .tier-silver { background: linear-gradient(135deg, #9ca3af, #6b7280); }
    .tier-gold { background: linear-gradient(135deg, #fbbf24, #d97706); }
    .tier-platinum { background: linear-gradient(135deg, #22d3ee, #0891b2); }
    .tier-legendary { background: linear-gradient(135deg, #a855f7, #7c3aed); }
    
    /* Animation */
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(251, 191, 36, 0.5); }
        50% { box-shadow: 0 0 20px rgba(251, 191, 36, 0.8); }
    }
    
    .glow-effect { animation: glow 2s infinite; }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #1a1a2e; }
    ::-webkit-scrollbar-thumb { background: #fbbf24; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #f59e0b; }
    
    /* Metric cards */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #fbbf24;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        color: #000;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(251, 191, 36, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    if 'db' not in st.session_state:
        st.session_state.db = SessionLocal()
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if 'show_celebration' not in st.session_state:
        st.session_state.show_celebration = False


# ============ DATABASE HELPERS ============

def get_db():
    if 'db' not in st.session_state:
        st.session_state.db = SessionLocal()
    return st.session_state.db


def refresh_db():
    if 'db' in st.session_state:
        st.session_state.db.close()
    st.session_state.db = SessionLocal()
    return st.session_state.db


# ============ HELPER FUNCTIONS ============

def get_today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def calculate_streak(db, habit_id: int) -> int:
    """Calculate current streak for a habit"""
    completions = db.query(Completion).filter(
        Completion.habit_id == habit_id,
        Completion.completed == True
    ).order_by(Completion.date.desc()).all()
    
    if not completions:
        return 0
    
    streak = 0
    current_date = date.today()
    
    for completion in completions:
        comp_date = datetime.strptime(completion.date, "%Y-%m-%d").date()
        if comp_date == current_date or comp_date == current_date - timedelta(days=1):
            streak += 1
            current_date = comp_date - timedelta(days=1)
        else:
            break
    
    return streak


def get_daily_wisdom(db, tradition: str = "esoteric") -> Dict[str, str]:
    """Get or generate daily wisdom quote"""
    today = get_today_str()
    
    motivation = db.query(Motivation).filter(Motivation.date == today).first()
    
    if not motivation:
        # Use the AI integration module for wisdom quotes
        wisdom = get_wisdom_quote(tradition)
        
        motivation = Motivation(
            date=today,
            quote=wisdom["quote"],
            philosophy=wisdom["philosophy"],
            tradition=tradition,
            habit_context="Focus on your priority habits today."
        )
        db.add(motivation)
        db.commit()
    
    return {
        "quote": motivation.quote,
        "philosophy": motivation.philosophy,
        "tradition": motivation.tradition,
        "habit_context": motivation.habit_context
    }


def award_xp(db, amount: int, source: str = "habit"):
    """Award XP to user and handle level ups"""
    stats = get_user_stats(db)
    
    # Apply any active XP multipliers
    active_effects = db.query(ActiveEffect).filter(
        ActiveEffect.effect_type == "xp_multiplier",
        ActiveEffect.expires_at > datetime.now()
    ).all()
    
    multiplier = 1.0
    for effect in active_effects:
        multiplier *= effect.value
    
    final_xp = int(amount * multiplier)
    
    stats.current_xp += final_xp
    stats.total_xp += final_xp
    
    # Check for level up
    level, current_in_level, needed = calculate_level_from_xp(stats.total_xp)
    if level > stats.level:
        stats.level = level
        stats.current_xp = current_in_level
        stats.last_level_up = datetime.now()
        st.session_state.show_celebration = True
        st.balloons()
    
    db.commit()
    return final_xp


def award_gold(db, amount: int):
    """Award gold to user"""
    stats = get_user_stats(db)
    
    # Apply any active gold multipliers
    active_effects = db.query(ActiveEffect).filter(
        ActiveEffect.effect_type == "gold_multiplier",
        ActiveEffect.expires_at > datetime.now()
    ).all()
    
    multiplier = 1.0
    for effect in active_effects:
        multiplier *= effect.value
    
    final_gold = int(amount * multiplier)
    
    stats.current_gold += final_gold
    stats.lifetime_gold += final_gold
    db.commit()
    return final_gold


def update_stat(db, stat_name: str, amount: int = 1):
    """Update a specific stat"""
    stats = get_user_stats(db)
    current = getattr(stats, stat_name, 10)
    setattr(stats, stat_name, current + amount)
    db.commit()


# ============ PAGE COMPONENTS ============

def render_xp_bar(stats: UserStats):
    """Render the XP progress bar"""
    level, current_xp, xp_needed = calculate_level_from_xp(stats.total_xp)
    progress = (current_xp / xp_needed * 100) if xp_needed > 0 else 100
    rank = get_rank_for_level(level)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div style='background: rgba(0,0,0,0.3); border-radius: 12px; padding: 8px;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                <span style='color: #fbbf24; font-weight: bold;'>Level {level}</span>
                <span style='color: #9ca3af;'>{current_xp:,} / {xp_needed:,} XP</span>
            </div>
            <div style='background: rgba(0,0,0,0.5); border-radius: 8px; height: 24px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #fbbf24, #f59e0b); height: 100%; width: {progress}%; 
                     border-radius: 8px; transition: width 0.5s ease;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 8px; background: {rank.color}20; border-radius: 8px;'>
            <span style='color: {rank.color}; font-weight: bold; font-size: 0.9rem;'>{rank.title}</span>
        </div>
        """, unsafe_allow_html=True)


def render_stat_card(stat_name: str, value: int, icon: str):
    """Render a stat card"""
    meta = STAT_METADATA[stat_name]
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {meta.color}20, transparent); 
         border: 1px solid {meta.color}40; border-radius: 12px; padding: 12px; text-align: center;'>
        <div style='font-size: 1.5rem;'>{icon}</div>
        <div style='color: {meta.color}; font-size: 1.5rem; font-weight: bold;'>{value}</div>
        <div style='color: #9ca3af; font-size: 0.8rem;'>{meta.label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_habit_card(habit: Habit, db, completed_today: bool):
    """Render a habit card with completion button"""
    streak = calculate_streak(db, habit.id)
    difficulty_name = DIFFICULTY_NAMES.get(habit.difficulty, "Easy")
    xp_reward = get_habit_xp(habit.difficulty)
    
    with st.container():
        col1, col2, col3 = st.columns([4, 2, 1])
        
        with col1:
            st.markdown(f"**{habit.name}**")
            if habit.description:
                st.caption(habit.description)
            st.markdown(f"🔥 {streak} day streak • {difficulty_name} • +{xp_reward} XP")
        
        with col2:
            category_color = CATEGORY_COLORS.get(habit.category, "#6366f1")
            st.markdown(f"""
            <span style='background: {category_color}30; color: {category_color}; 
                  padding: 4px 12px; border-radius: 12px; font-size: 0.8rem;'>
                {habit.category.title()}
            </span>
            """, unsafe_allow_html=True)
        
        with col3:
            if completed_today:
                st.markdown("✅")
            else:
                if st.button("Complete", key=f"habit_{habit.id}"):
                    complete_habit(db, habit)
                    st.rerun()


def complete_habit(db, habit: Habit):
    """Complete a habit for today"""
    today = get_today_str()
    
    # Check if already completed
    existing = db.query(Completion).filter(
        Completion.habit_id == habit.id,
        Completion.date == today
    ).first()
    
    if not existing:
        completion = Completion(habit_id=habit.id, date=today, completed=True)
        db.add(completion)
        
        # Award XP
        xp = get_habit_xp(habit.difficulty)
        streak = calculate_streak(db, habit.id) + 1
        streak_bonus = calculate_streak_bonus(streak)
        final_xp = int(xp * streak_bonus)
        award_xp(db, final_xp, "habit")
        
        # Award gold
        gold = calculate_gold_reward(habit.difficulty, is_habit=True)
        award_gold(db, gold)
        
        # Update stat
        stat = get_stat_for_category(habit.category)
        update_stat(db, stat, 1)
        
        db.commit()
        st.success(f"🎉 +{final_xp} XP • +{gold} Gold!")


# ============ MAIN PAGES ============

def page_dashboard():
    """Dashboard page - Hero section with XP, daily wisdom, priority quests"""
    db = get_db()
    stats = get_user_stats(db)
    profile = get_user_profile(db)
    
    # Hero Section
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 2.5rem; margin: 0;'>Welcome back, <span style='color: #fbbf24;'>{profile.display_name}</span>!</h1>
        <p style='color: #9ca3af; margin-top: 8px;'>Continue your journey to greatness</p>
    </div>
    """, unsafe_allow_html=True)
    
    # XP Bar
    render_xp_bar(stats)
    
    # Stats Row
    st.markdown("### ⚔️ Your Stats")
    stat_cols = st.columns(6)
    stat_icons = {"strength": "⚔️", "intelligence": "🧠", "vitality": "❤️", 
                  "agility": "⚡", "sense": "👁️", "willpower": "🔥"}
    
    for i, (stat_name, icon) in enumerate(stat_icons.items()):
        with stat_cols[i]:
            value = getattr(stats, stat_name, 10)
            render_stat_card(stat_name, value, icon)
    
    st.markdown("---")
    
    # Two column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Daily Wisdom
        st.markdown("### 📜 Daily Wisdom")
        wisdom = get_daily_wisdom(db, profile.philosophy_tradition)
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(251, 191, 36, 0.1), transparent);
             border: 1px solid rgba(251, 191, 36, 0.3); border-radius: 16px; padding: 1.5rem;'>
            <p style='font-size: 1.2rem; font-style: italic; color: #fbbf24; margin-bottom: 1rem;'>
                "{wisdom['quote']}"
            </p>
            <p style='color: #9ca3af; font-size: 0.9rem;'>{wisdom['philosophy']}</p>
            <p style='color: #6b7280; font-size: 0.8rem; margin-top: 0.5rem;'>
                — {wisdom['tradition'].title()} Tradition
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Priority Quests
        st.markdown("### ⭐ Priority Quests")
        priority_habits = db.query(Habit).filter(
            Habit.active == True,
            Habit.priority == True
        ).limit(4).all()
        
        if priority_habits:
            today = get_today_str()
            for habit in priority_habits:
                completion = db.query(Completion).filter(
                    Completion.habit_id == habit.id,
                    Completion.date == today
                ).first()
                render_habit_card(habit, db, completion is not None)
        else:
            st.info("No priority habits set. Mark habits as priority in the Habits page!")
    
    with col2:
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        
        # Current streak
        today = get_today_str()
        completions_today = db.query(Completion).filter(
            Completion.date == today,
            Completion.completed == True
        ).count()
        
        total_habits = db.query(Habit).filter(Habit.active == True).count()
        
        st.metric("Completed Today", f"{completions_today}/{total_habits}")
        st.metric("Current Gold", f"💰 {stats.current_gold:,}")
        st.metric("Total XP", f"✨ {stats.total_xp:,}")
        
        # Level progress
        level, current_xp, xp_needed = calculate_level_from_xp(stats.total_xp)
        progress = current_xp / xp_needed if xp_needed > 0 else 1
        st.progress(progress, text=f"Level {level} Progress")


def page_habits():
    """Habits page - Habit management and tracking"""
    db = get_db()
    
    st.markdown("## ✅ Habits")
    st.markdown("Build your daily routines and track your progress")
    
    # Tabs for active and completed
    tab1, tab2 = st.tabs(["Active Habits", "Create New"])
    
    with tab1:
        habits = db.query(Habit).filter(Habit.active == True).all()
        
        if habits:
            today = get_today_str()
            
            for habit in habits:
                completion = db.query(Completion).filter(
                    Completion.habit_id == habit.id,
                    Completion.date == today
                ).first()
                
                with st.container():
                    render_habit_card(habit, db, completion is not None)
                    st.markdown("---")
        else:
            st.info("No habits yet! Create your first habit to begin your journey.")
    
    with tab2:
        st.markdown("### Create New Habit")
        
        with st.form("new_habit"):
            name = st.text_input("Habit Name", placeholder="e.g., Morning meditation")
            description = st.text_area("Description (optional)", placeholder="Why is this habit important?")
            
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("Category", [
                    "health", "fitness", "learning", "mindfulness",
                    "productivity", "social", "creative", "finance", "personal", "work"
                ])
            with col2:
                difficulty = st.selectbox("Difficulty", [
                    (1, "Easy - 50 XP"),
                    (2, "Medium - 100 XP"),
                    (3, "Hard - 300 XP")
                ], format_func=lambda x: x[1])
            
            col3, col4 = st.columns(2)
            with col3:
                frequency = st.selectbox("Frequency", [
                    "daily", "weekdays", "weekends", "specific", "custom"
                ])
            with col4:
                priority = st.checkbox("Mark as Priority")
            
            color = st.color_picker("Color", "#fbbf24")
            
            submitted = st.form_submit_button("Create Habit", use_container_width=True)
            
            if submitted and name:
                new_habit = Habit(
                    name=name,
                    description=description,
                    category=category,
                    difficulty=difficulty[0],
                    xp_reward=get_habit_xp(difficulty[0]),
                    priority=priority,
                    frequency=frequency,
                    color=color
                )
                db.add(new_habit)
                db.commit()
                st.success("🎉 Habit created successfully!")
                st.rerun()


def page_goals():
    """Goals page - Goal setting and tracking"""
    db = get_db()
    
    st.markdown("## 🎯 Goals")
    st.markdown("Set ambitious goals and track your progress")
    
    tab1, tab2, tab3 = st.tabs(["Active Goals", "Completed", "Create New"])
    
    with tab1:
        goals = db.query(Goal).filter(Goal.completed == False).all()
        
        if goals:
            for goal in goals:
                with st.expander(f"{'⭐ ' if goal.priority else ''}{goal.title}", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**{goal.description or 'No description'}**")
                        
                        # Progress bar
                        st.progress(goal.progress / 100, text=f"{goal.progress}% Complete")
                        
                        # Steps
                        if goal.steps:
                            st.markdown("**Steps:**")
                            steps = goal.steps if isinstance(goal.steps, list) else json.loads(goal.steps or "[]")
                            for i, step in enumerate(steps):
                                completed = step.get('completed', False)
                                st.checkbox(
                                    step.get('title', f'Step {i+1}'),
                                    value=completed,
                                    key=f"step_{goal.id}_{i}"
                                )
                    
                    with col2:
                        xp = get_goal_xp(goal.difficulty)
                        st.metric("XP Reward", f"+{xp}")
                        
                        if goal.deadline:
                            days_left = (goal.deadline - date.today()).days
                            if days_left < 0:
                                st.error(f"Overdue by {abs(days_left)} days")
                            elif days_left <= 7:
                                st.warning(f"{days_left} days left")
                            else:
                                st.info(f"{days_left} days left")
                        
                        # Update progress
                        new_progress = st.slider("Progress", 0, 100, goal.progress, key=f"prog_{goal.id}")
                        if new_progress != goal.progress:
                            goal.progress = new_progress
                            if new_progress == 100:
                                goal.completed = True
                                award_xp(db, xp, "goal")
                                award_gold(db, calculate_gold_reward(goal.difficulty, is_habit=False))
                            db.commit()
                            st.rerun()
        else:
            st.info("No active goals. Create a goal to start achieving!")
    
    with tab2:
        completed_goals = db.query(Goal).filter(Goal.completed == True).all()
        
        if completed_goals:
            for goal in completed_goals:
                st.markdown(f"✅ **{goal.title}** - +{get_goal_xp(goal.difficulty)} XP earned")
        else:
            st.info("No completed goals yet. Keep working on your active goals!")
    
    with tab3:
        st.markdown("### Create New Goal")
        
        with st.form("new_goal"):
            title = st.text_input("Goal Title", placeholder="e.g., Learn Spanish to B2 level")
            description = st.text_area("Description", placeholder="What does success look like?")
            
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("Category", [
                    "health", "fitness", "career", "finance", "education",
                    "relationships", "personal", "creative", "travel", "other"
                ])
            with col2:
                difficulty = st.selectbox("Difficulty", [
                    (1, "Normal - 1000 XP"),
                    (2, "Medium - 2000 XP"),
                    (3, "Hard - 3000 XP")
                ], format_func=lambda x: x[1])
            
            deadline = st.date_input("Deadline (optional)", value=None)
            priority = st.checkbox("Mark as Priority")
            
            submitted = st.form_submit_button("Create Goal", use_container_width=True)
            
            if submitted and title:
                new_goal = Goal(
                    title=title,
                    description=description,
                    category=category,
                    difficulty=difficulty[0],
                    xp_reward=get_goal_xp(difficulty[0]),
                    deadline=deadline,
                    priority=priority
                )
                db.add(new_goal)
                db.commit()
                st.success("🎯 Goal created successfully!")
                st.rerun()


def page_analytics():
    """Analytics page - Charts and progress tracking"""
    db = get_db()
    stats = get_user_stats(db)
    
    st.markdown("## 📊 Analytics")
    st.markdown("Track your progress and identify areas for improvement")
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Calculate weekly progress
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        weekly_completions = db.query(Completion).filter(
            Completion.date >= week_ago,
            Completion.completed == True
        ).count()
        total_possible = db.query(Habit).filter(Habit.active == True).count() * 7
        weekly_pct = (weekly_completions / total_possible * 100) if total_possible > 0 else 0
        st.metric("Weekly Progress", f"{weekly_pct:.0f}%")
    
    with col2:
        # Find best streak
        habits = db.query(Habit).filter(Habit.active == True).all()
        best_streak = max([calculate_streak(db, h.id) for h in habits], default=0)
        st.metric("Best Streak", f"🔥 {best_streak} days")
    
    with col3:
        total_completions = db.query(Completion).filter(Completion.completed == True).count()
        st.metric("Total Completions", f"✅ {total_completions}")
    
    with col4:
        st.metric("Total XP", f"✨ {stats.total_xp:,}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Completion Trend (Last 14 Days)")
        
        # Get completion data for last 14 days
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(13, -1, -1)]
        completion_counts = []
        
        for d in dates:
            count = db.query(Completion).filter(
                Completion.date == d,
                Completion.completed == True
            ).count()
            completion_counts.append(count)
        
        fig = px.line(
            x=dates, y=completion_counts,
            labels={"x": "Date", "y": "Completions"},
            markers=True
        )
        fig.update_traces(line_color="#fbbf24", marker_color="#f59e0b")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#ffffff"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Stats Distribution")
        
        stat_values = [
            stats.strength, stats.intelligence, stats.vitality,
            stats.agility, stats.sense, stats.willpower
        ]
        stat_names = ["Strength", "Intelligence", "Vitality", "Agility", "Sense", "Willpower"]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=stat_values,
            theta=stat_names,
            fill='toself',
            fillcolor='rgba(251, 191, 36, 0.3)',
            line_color='#fbbf24'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(stat_values) + 10]),
                bgcolor="rgba(0,0,0,0)"
            ),
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#ffffff"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Habit Performance
    st.markdown("### 📋 Habit Performance")
    habits = db.query(Habit).filter(Habit.active == True).all()
    
    if habits:
        habit_data = []
        for habit in habits:
            # Calculate completion rate for last 30 days
            month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            completions = db.query(Completion).filter(
                Completion.habit_id == habit.id,
                Completion.date >= month_ago,
                Completion.completed == True
            ).count()
            
            rate = (completions / 30) * 100
            habit_data.append({
                "Habit": habit.name,
                "Completion Rate": rate,
                "Category": habit.category.title(),
                "Streak": calculate_streak(db, habit.id)
            })
        
        df = pd.DataFrame(habit_data)
        
        fig = px.bar(
            df, x="Habit", y="Completion Rate",
            color="Category",
            text="Streak"
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#ffffff"
        )
        st.plotly_chart(fig, use_container_width=True)


def page_rewards():
    """Rewards/Achievements page"""
    db = get_db()
    
    st.markdown("## 🏆 Achievements")
    st.markdown("Track your accomplishments and unlock rewards")
    
    # Get unlocked achievements
    unlocked = db.query(Achievement).filter(Achievement.unlocked_at != None).all()
    unlocked_keys = {a.key for a in unlocked}
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Unlocked", f"{len(unlocked)}/{len(ALL_ACHIEVEMENTS)}")
    with col2:
        pct = (len(unlocked) / len(ALL_ACHIEVEMENTS)) * 100 if ALL_ACHIEVEMENTS else 0
        st.metric("Completion", f"{pct:.1f}%")
    with col3:
        total_xp = sum(a.xp_reward for a in unlocked)
        st.metric("XP Earned", f"✨ {total_xp:,}")
    
    st.markdown("---")
    
    # Category filter
    category_filter = st.selectbox(
        "Filter by Category",
        ["all"] + [c["id"] for c in ACHIEVEMENT_CATEGORIES if c["id"] != "all"],
        format_func=lambda x: x.title() if x != "all" else "All Categories"
    )
    
    tier_filter = st.selectbox(
        "Filter by Tier",
        ["all"] + [t["id"] for t in ACHIEVEMENT_TIERS if t["id"] != "all"],
        format_func=lambda x: x.title() if x != "all" else "All Tiers"
    )
    
    # Filter achievements
    filtered = ALL_ACHIEVEMENTS
    if category_filter != "all":
        filtered = [a for a in filtered if a.category == category_filter]
    if tier_filter != "all":
        filtered = [a for a in filtered if a.tier == tier_filter]
    
    # Display achievements
    cols = st.columns(4)
    for i, achievement in enumerate(filtered):
        is_unlocked = achievement.key in unlocked_keys
        
        with cols[i % 4]:
            tier_colors = {
                "bronze": "#d97706",
                "silver": "#9ca3af",
                "gold": "#fbbf24",
                "platinum": "#22d3ee",
                "legendary": "#a855f7"
            }
            tier_color = tier_colors.get(achievement.tier, "#fbbf24")
            
            opacity = "1" if is_unlocked else "0.5"
            
            st.markdown(f"""
            <div style='background: rgba(30, 30, 50, 0.8); border: 2px solid {tier_color}; 
                 border-radius: 12px; padding: 1rem; margin: 0.5rem 0; opacity: {opacity};
                 text-align: center;'>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>
                    {"🏆" if is_unlocked else "🔒"}
                </div>
                <div style='font-weight: bold; color: {tier_color};'>{achievement.title}</div>
                <div style='font-size: 0.8rem; color: #9ca3af; margin: 0.5rem 0;'>
                    {achievement.description}
                </div>
                <div style='font-size: 0.8rem;'>
                    <span style='color: #fbbf24;'>+{achievement.xp_reward} XP</span>
                    {f" • +{achievement.gold_reward} 💰" if achievement.gold_reward > 0 else ""}
                </div>
                <div style='font-size: 0.7rem; color: {tier_color}; margin-top: 0.5rem;'>
                    {achievement.tier.upper()}
                </div>
            </div>
            """, unsafe_allow_html=True)


def page_shop():
    """Shop page - Buy items with gold"""
    db = get_db()
    stats = get_user_stats(db)
    
    st.markdown("## 🛒 Hunter's Shop")
    st.markdown("Enhance your journey with powerful items")
    
    # Currency display
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        pass
    with col2:
        st.metric("Gold", f"💰 {stats.current_gold:,}")
    with col3:
        st.metric("Crystals", "💎 0")
    
    st.markdown("---")
    
    # Category tabs
    category = st.selectbox(
        "Category",
        [c["id"] for c in SHOP_CATEGORIES],
        format_func=lambda x: next((c["name"] for c in SHOP_CATEGORIES if c["id"] == x), x.title())
    )
    
    # Get items for category
    items = [item for item in ALL_SHOP_ITEMS if item.category == category]
    
    # Display items
    cols = st.columns(3)
    for i, item in enumerate(items):
        with cols[i % 3]:
            rarity_color = RARITY_COLORS.get(item.rarity, {}).get("bg", "#6b7280")
            can_afford = stats.current_gold >= item.price.gold
            
            level, _, _ = calculate_level_from_xp(stats.total_xp)
            meets_level = item.level_required is None or level >= item.level_required
            
            opacity = "1" if can_afford and meets_level else "0.6"
            
            st.markdown(f"""
            <div style='background: rgba(30, 30, 50, 0.8); border: 2px solid {rarity_color};
                 border-radius: 12px; padding: 1rem; margin: 0.5rem 0; opacity: {opacity};'>
                <div style='display: flex; justify-content: space-between; align-items: start;'>
                    <span style='font-weight: bold;'>{item.name}</span>
                    <span style='background: {rarity_color}; color: white; padding: 2px 8px;
                          border-radius: 8px; font-size: 0.7rem;'>{item.rarity.upper()}</span>
                </div>
                <p style='font-size: 0.8rem; color: #9ca3af; margin: 0.5rem 0;'>{item.description}</p>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;'>
                    <span style='color: #fbbf24; font-weight: bold;'>
                        💰 {item.price.gold:,}
                        {f" + 💎 {item.price.crystals}" if item.price.crystals > 0 else ""}
                    </span>
                    {f"<span style='color: #9ca3af; font-size: 0.8rem;'>Lv.{item.level_required}</span>" if item.level_required else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if can_afford and meets_level:
                if st.button(f"Buy {item.name}", key=f"buy_{item.id}"):
                    stats.current_gold -= item.price.gold
                    
                    # Add to inventory
                    inv_item = InventoryItem(item_id=item.id, quantity=1)
                    db.add(inv_item)
                    db.commit()
                    
                    st.success(f"Purchased {item.name}!")
                    st.rerun()


def page_notes():
    """Notes page - Personal notes with categories"""
    db = get_db()
    
    st.markdown("## 📝 Notes")
    st.markdown("Capture your ideas, plans, and reflections")
    
    tab1, tab2 = st.tabs(["My Notes", "Create New"])
    
    with tab1:
        # Filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("🔍 Search notes", placeholder="Search by title or content...")
        with col2:
            category_filter = st.selectbox("Category", [
                "all", "personal", "work", "health", "goals", "ideas", "learning"
            ])
        
        # Get notes
        query = db.query(Note)
        if category_filter != "all":
            query = query.filter(Note.category == category_filter)
        
        notes = query.order_by(Note.pinned.desc(), Note.created_at.desc()).all()
        
        if search:
            notes = [n for n in notes if search.lower() in n.title.lower() or search.lower() in (n.content or "").lower()]
        
        if notes:
            # Pinned notes
            pinned = [n for n in notes if n.pinned]
            if pinned:
                st.markdown("### 📌 Pinned")
                for note in pinned:
                    render_note_card(note, db)
            
            # Other notes
            other = [n for n in notes if not n.pinned]
            if other:
                if pinned:
                    st.markdown("### Other Notes")
                for note in other:
                    render_note_card(note, db)
        else:
            st.info("No notes yet. Create your first note!")
    
    with tab2:
        st.markdown("### Create New Note")
        
        with st.form("new_note"):
            title = st.text_input("Title", placeholder="Note title...")
            content = st.text_area("Content", placeholder="Write your thoughts...", height=200)
            
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("Category", [
                    "personal", "work", "health", "goals", "ideas", "learning"
                ])
            with col2:
                color = st.selectbox("Color", [
                    "default", "yellow", "green", "blue", "purple"
                ])
            
            pinned = st.checkbox("Pin this note")
            
            tags_input = st.text_input("Tags (comma-separated)", placeholder="productivity, goals, ideas")
            
            submitted = st.form_submit_button("Save Note", use_container_width=True)
            
            if submitted and title:
                tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else []
                
                new_note = Note(
                    title=title,
                    content=content,
                    category=category,
                    color=color,
                    pinned=pinned,
                    tags=tags
                )
                db.add(new_note)
                db.commit()
                st.success("📝 Note saved!")
                st.rerun()


def render_note_card(note: Note, db):
    """Render a note card"""
    color_classes = {
        "default": "rgba(30, 30, 50, 0.8)",
        "yellow": "rgba(234, 179, 8, 0.2)",
        "green": "rgba(34, 197, 94, 0.2)",
        "blue": "rgba(59, 130, 246, 0.2)",
        "purple": "rgba(168, 85, 247, 0.2)"
    }
    bg_color = color_classes.get(note.color, color_classes["default"])
    
    with st.container():
        st.markdown(f"""
        <div style='background: {bg_color}; border-radius: 12px; padding: 1rem; margin: 0.5rem 0;'>
            <div style='display: flex; justify-content: space-between; align-items: start;'>
                <span style='font-weight: bold;'>{"📌 " if note.pinned else ""}{note.title}</span>
                <span style='background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 8px;
                      font-size: 0.8rem;'>{note.category}</span>
            </div>
            <p style='color: #9ca3af; margin: 0.5rem 0; font-size: 0.9rem;'>
                {(note.content or "")[:150]}{"..." if len(note.content or "") > 150 else ""}
            </p>
            <div style='font-size: 0.8rem; color: #6b7280;'>
                {note.created_at.strftime("%Y-%m-%d %H:%M") if note.created_at else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Delete", key=f"del_note_{note.id}"):
                db.delete(note)
                db.commit()
                st.rerun()


def page_ai_coach():
    """AI Coach page - Get personalized suggestions"""
    db = get_db()
    
    st.markdown("## 🤖 AI Goal Coach")
    st.markdown("Get personalized habit and goal recommendations")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2));
         border-radius: 16px; padding: 2rem; text-align: center; margin-bottom: 2rem;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖</div>
        <h3 style='margin: 0;'>Share Your Mission</h3>
        <p style='color: #9ca3af;'>Describe what you want to achieve, and I'll suggest habits and goals to help you get there.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mode selection
    mode = st.radio("What would you like?", ["Quick Habits", "Full Goal Plan"], horizontal=True)
    
    context = st.text_area(
        "Describe your mission or goal",
        placeholder="e.g., I want to become fluent in Spanish and travel to Spain next year...",
        height=100
    )
    
    if st.button("✨ Generate Suggestions", use_container_width=True, disabled=not context):
        with st.spinner("Generating personalized suggestions..."):
            # Simulated AI response (in production, this would call an AI API)
            if mode == "Quick Habits":
                habits = generate_habit_suggestions(context)
                
                st.markdown("### 💡 Suggested Habits")
                for i, habit in enumerate(habits):
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**{habit['title']}**")
                            st.caption(habit['description'])
                            st.markdown(f"*{habit['reason']}*")
                        with col2:
                            if st.button("Add Habit", key=f"add_habit_{i}"):
                                new_habit = Habit(
                                    name=habit['title'],
                                    description=habit['description'],
                                    category="learning",
                                    difficulty=habit['difficulty']
                                )
                                db.add(new_habit)
                                db.commit()
                                st.success(f"Added: {habit['title']}")
                        st.markdown("---")
            else:
                goal = generate_goal_plan(context)
                
                st.markdown("### 🎯 Your Goal Plan")
                st.markdown(f"## {goal['title']}")
                st.markdown(goal['description'])
                
                st.markdown("**Steps to Success:**")
                for i, step in enumerate(goal['steps']):
                    st.markdown(f"{i+1}. {step}")
                
                if st.button("Add This Goal", use_container_width=True):
                    new_goal = Goal(
                        title=goal['title'],
                        description=goal['description'],
                        difficulty=2,
                        xp_reward=2000,
                        steps=goal['steps']
                    )
                    db.add(new_goal)
                    db.commit()
                    st.success("Goal added to your quest log!")


def generate_habit_suggestions(context: str) -> List[Dict]:
    """Generate habit suggestions based on context"""
    return ai_generate_habits(context, count=3)


def generate_goal_plan(context: str) -> Dict:
    """Generate a goal plan based on context"""
    return ai_generate_goal(context)


def page_philosophy():
    """Philosophy Library page - Upload and manage wisdom documents"""
    db = get_db()
    
    st.markdown("## 📚 Philosophy Library")
    st.markdown("Your personal collection of wisdom and guiding principles")
    
    # Stats
    docs = db.query(PhilosophyDocument).all()
    active_count = len([d for d in docs if d.use_for_ai])
    processed_count = len([d for d in docs if d.is_processed])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Documents", len(docs))
    with col2:
        st.metric("Active for AI", active_count)
    with col3:
        st.metric("Processed", processed_count)
    
    st.markdown("---")
    
    # Upload section
    with st.expander("📤 Upload New Document"):
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "txt", "md"],
            help="Upload PDF, TXT, or Markdown files"
        )
        
        if uploaded_file:
            doc_title = st.text_input("Document Title", value=uploaded_file.name)
            doc_category = st.selectbox("Category", [
                "personal", "business", "spiritual", "productivity", "health", "success", "mindfulness", "finance"
            ])
            
            if st.button("Upload Document"):
                # In production, this would handle file storage and processing
                new_doc = PhilosophyDocument(
                    title=doc_title,
                    file_name=uploaded_file.name,
                    file_type=uploaded_file.type.split("/")[-1] if uploaded_file.type else "txt",
                    file_size=uploaded_file.size,
                    category=doc_category,
                    is_processed=False,
                    use_for_ai=True
                )
                db.add(new_doc)
                db.commit()
                st.success("Document uploaded! It will be processed shortly.")
                st.rerun()
    
    # Document list
    if docs:
        for doc in docs:
            with st.container():
                col1, col2, col3 = st.columns([4, 1, 1])
                
                with col1:
                    icon = "📄" if doc.file_type == "pdf" else "📝"
                    st.markdown(f"{icon} **{doc.title}**")
                    st.caption(f"{doc.category.title()} • {doc.file_size // 1024}KB • {doc.file_type.upper()}")
                    
                    if doc.key_themes:
                        themes = doc.key_themes if isinstance(doc.key_themes, list) else []
                        st.markdown(" ".join([f"`{t}`" for t in themes[:3]]))
                
                with col2:
                    ai_status = "🟢 Active" if doc.use_for_ai else "⚪ Inactive"
                    if st.button(ai_status, key=f"toggle_{doc.id}"):
                        doc.use_for_ai = not doc.use_for_ai
                        db.commit()
                        st.rerun()
                
                with col3:
                    if st.button("🗑️", key=f"del_doc_{doc.id}"):
                        db.delete(doc)
                        db.commit()
                        st.rerun()
                
                st.markdown("---")
    else:
        st.info("No documents yet. Upload your first philosophy document!")


def page_settings():
    """Settings page - User preferences"""
    db = get_db()
    profile = get_user_profile(db)
    
    st.markdown("## ⚙️ Settings")
    st.markdown("Customize your experience")
    
    with st.form("settings"):
        st.markdown("### 👤 Profile")
        
        display_name = st.text_input("Display Name", value=profile.display_name or "Hunter")
        
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", ["male", "female", "neutral"],
                index=["male", "female", "neutral"].index(profile.gender or "neutral"))
        with col2:
            avatar = st.selectbox("Avatar Style", 
                [a["id"] for a in AVATAR_STYLES],
                format_func=lambda x: next((a["name"] for a in AVATAR_STYLES if a["id"] == x), x),
                index=[a["id"] for a in AVATAR_STYLES].index(profile.avatar_style or "warrior"))
        
        st.markdown("### 🔔 Notifications")
        
        notifications = st.checkbox("Enable Notifications", value=profile.notifications_enabled)
        
        col1, col2 = st.columns(2)
        with col1:
            reminder_time = st.time_input("Daily Reminder Time", 
                value=datetime.strptime(profile.daily_reminder_time or "09:00", "%H:%M").time())
        with col2:
            weekly_report = st.checkbox("Weekly Progress Report", value=profile.weekly_report_enabled)
        
        st.markdown("### 🌍 Region")
        
        timezone = st.selectbox("Timezone",
            [tz["value"] for tz in TIMEZONES],
            format_func=lambda x: next((tz["label"] for tz in TIMEZONES if tz["value"] == x), x),
            index=[tz["value"] for tz in TIMEZONES].index(profile.timezone or "America/Chicago"))
        
        st.markdown("### 📜 Philosophy")
        
        tradition = st.selectbox("Philosophy Tradition",
            [t["id"] for t in PHILOSOPHY_TRADITIONS],
            format_func=lambda x: next((t["name"] for t in PHILOSOPHY_TRADITIONS if t["id"] == x), x),
            index=[t["id"] for t in PHILOSOPHY_TRADITIONS].index(profile.philosophy_tradition or "esoteric"))
        
        submitted = st.form_submit_button("💾 Save Settings", use_container_width=True)
        
        if submitted:
            profile.display_name = display_name
            profile.gender = gender
            profile.avatar_style = avatar
            profile.notifications_enabled = notifications
            profile.daily_reminder_time = reminder_time.strftime("%H:%M")
            profile.weekly_report_enabled = weekly_report
            profile.timezone = timezone
            profile.philosophy_tradition = tradition
            db.commit()
            st.success("Settings saved!")


def page_onboarding():
    """Onboarding page - New user setup"""
    db = get_db()
    profile = get_user_profile(db)
    
    if profile.onboarding_completed:
        st.session_state.current_page = "Dashboard"
        st.rerun()
    
    st.markdown("""
    <div style='text-align: center; padding: 3rem;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>👑</div>
        <h1 style='font-size: 2.5rem;'>Welcome, <span style='color: #fbbf24;'>Warrior</span></h1>
        <p style='color: #9ca3af; font-size: 1.2rem;'>
            Every legend starts with a single step. You're about to embark on a journey 
            of transformation—one habit, one goal, one day at a time.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("onboarding"):
        st.markdown("### What should we call you?")
        name = st.text_input("Your Name", placeholder="Enter your name")
        
        st.markdown("### Choose your avatar style")
        avatar = st.selectbox("Avatar",
            [a["id"] for a in AVATAR_STYLES],
            format_func=lambda x: f"{next((a['icon'] for a in AVATAR_STYLES if a['id'] == x), '⚔️')} {next((a['name'] for a in AVATAR_STYLES if a['id'] == x), x)} - {next((a['description'] for a in AVATAR_STYLES if a['id'] == x), '')}")
        
        st.markdown("### Select your philosophy tradition")
        tradition = st.selectbox("Tradition",
            [t["id"] for t in PHILOSOPHY_TRADITIONS],
            format_func=lambda x: f"{next((t['name'] for t in PHILOSOPHY_TRADITIONS if t['id'] == x), x)} - {next((t['description'] for t in PHILOSOPHY_TRADITIONS if t['id'] == x), '')}")
        
        st.markdown("### What are your focus areas?")
        focus_areas = st.multiselect("Focus Areas",
            [f["id"] for f in FOCUS_AREAS],
            format_func=lambda x: f"{next((f['icon'] for f in FOCUS_AREAS if f['id'] == x), '📌')} {next((f['name'] for f in FOCUS_AREAS if f['id'] == x), x)}")
        
        submitted = st.form_submit_button("🚀 Start My Journey", use_container_width=True)
        
        if submitted and name:
            profile.display_name = name
            profile.avatar_style = avatar
            profile.philosophy_tradition = tradition
            profile.focus_areas = focus_areas
            profile.onboarding_completed = True
            db.commit()
            st.success("Welcome aboard! Let's begin your journey!")
            st.session_state.current_page = "Dashboard"
            st.rerun()


# ============ MAIN APP ============

def main():
    """Main application entry point"""
    load_custom_css()
    init_session_state()
    
    db = get_db()
    profile = get_user_profile(db)
    
    # Check if onboarding needed
    if not profile.onboarding_completed:
        page_onboarding()
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 2rem;'>⚔️</div>
            <h2 style='margin: 0; color: #fbbf24;'>Goal Quest</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation buttons
        pages = [
            ("🏠 Dashboard", "Dashboard"),
            ("✅ Habits", "Habits"),
            ("🎯 Goals", "Goals"),
            ("📊 Analytics", "Analytics"),
            ("🏆 Rewards", "Rewards"),
            ("🛒 Shop", "Shop"),
            ("📝 Notes", "Notes"),
            ("🤖 AI Coach", "AI Coach"),
            ("📚 Philosophy", "Philosophy"),
            ("⚙️ Settings", "Settings"),
        ]
        
        for label, page in pages:
            if st.button(label, key=page, use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats in sidebar
        stats = get_user_stats(db)
        level, _, _ = calculate_level_from_xp(stats.total_xp)
        rank = get_rank_for_level(level)
        
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: rgba(0,0,0,0.2); border-radius: 12px;'>
            <div style='font-size: 1.5rem; font-weight: bold; color: #fbbf24;'>Lv. {level}</div>
            <div style='color: {rank.color}; font-size: 0.9rem;'>{rank.title}</div>
            <div style='margin-top: 0.5rem; color: #9ca3af;'>💰 {stats.current_gold:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    current_page = st.session_state.current_page
    
    if current_page == "Dashboard":
        page_dashboard()
    elif current_page == "Habits":
        page_habits()
    elif current_page == "Goals":
        page_goals()
    elif current_page == "Analytics":
        page_analytics()
    elif current_page == "Rewards":
        page_rewards()
    elif current_page == "Shop":
        page_shop()
    elif current_page == "Notes":
        page_notes()
    elif current_page == "AI Coach":
        page_ai_coach()
    elif current_page == "Philosophy":
        page_philosophy()
    elif current_page == "Settings":
        page_settings()


if __name__ == "__main__":
    main()

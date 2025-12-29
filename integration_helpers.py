"""
Goal Quest - Character System Integration Helper
=================================================
Easy integration utilities for connecting the character system
to existing Goal Quest applications.
"""

import streamlit as st
from typing import Dict, Any, Optional, Callable
from character_system import (
    init_character_state,
    render_character_display,
    render_character_customization,
    render_shop_interface,
    render_equipment_manager,
    render_tier_overview,
    award_xp_with_bonus,
    get_character_data_for_profile,
    load_character_data_from_profile,
    get_evolution_tier,
    calculate_tier_progress,
    get_equipped_items,
    calculate_total_xp_bonus,
    EVOLUTION_TIERS,
    SHOP_ITEMS,
    RARITY_CONFIG,
    Rarity
)


# =============================================================================
# QUICK SETUP
# =============================================================================

def setup_character_system(
    initial_level: int = 1,
    initial_gold: int = 500,
    initial_gems: int = 10,
    initial_xp: int = 0
):
    """
    Quick setup for the character system with custom initial values.
    Call this at the start of your app.
    
    Args:
        initial_level: Starting level (default: 1)
        initial_gold: Starting gold (default: 500)
        initial_gems: Starting gems (default: 10)
        initial_xp: Starting XP (default: 0)
    """
    init_character_state()
    
    # Only set initial values if not already set
    if st.session_state.get("_character_initialized") is None:
        st.session_state.player_level = initial_level
        st.session_state.player_gold = initial_gold
        st.session_state.player_gems = initial_gems
        st.session_state.player_xp = initial_xp
        st.session_state._character_initialized = True


def sync_from_profile(profile_data: Dict[str, Any]):
    """
    Sync character system from existing user profile data.
    
    Args:
        profile_data: Dictionary containing user profile with character data
    """
    init_character_state()
    
    # Load character-specific data
    if "character" in profile_data:
        load_character_data_from_profile(profile_data["character"])
    
    # Sync player stats from profile
    if "level" in profile_data:
        st.session_state.player_level = profile_data["level"]
    if "xp" in profile_data:
        st.session_state.player_xp = profile_data["xp"]
    if "xp_for_next_level" in profile_data:
        st.session_state.xp_for_next_level = profile_data["xp_for_next_level"]
    if "gold" in profile_data:
        st.session_state.player_gold = profile_data["gold"]
    if "gems" in profile_data:
        st.session_state.player_gems = profile_data["gems"]


def sync_to_profile(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sync character system data back to user profile.
    
    Args:
        profile_data: Existing profile data to update
        
    Returns:
        Updated profile data dictionary
    """
    profile_data["character"] = get_character_data_for_profile()
    profile_data["level"] = st.session_state.player_level
    profile_data["xp"] = st.session_state.player_xp
    profile_data["xp_for_next_level"] = st.session_state.xp_for_next_level
    profile_data["gold"] = st.session_state.player_gold
    profile_data["gems"] = st.session_state.player_gems
    
    return profile_data


# =============================================================================
# XP AND LEVELING INTEGRATION
# =============================================================================

def on_habit_complete(base_xp: int, gold_reward: int = 0) -> Dict[str, Any]:
    """
    Call when a habit is completed. Handles XP, gold, and level-ups.
    
    Args:
        base_xp: Base XP reward for the habit
        gold_reward: Gold to award (default: 0)
        
    Returns:
        Dictionary with results:
        - xp_earned: Total XP with bonuses
        - leveled_up: Whether player leveled up
        - new_level: Current level
        - tier_evolved: Whether tier changed
        - new_tier: Current tier name
    """
    old_level = st.session_state.player_level
    old_tier = get_evolution_tier(old_level)
    
    # Award XP with equipment bonuses
    xp_earned = award_xp_with_bonus(base_xp)
    
    # Award gold
    if gold_reward > 0:
        st.session_state.player_gold += gold_reward
    
    new_level = st.session_state.player_level
    new_tier = get_evolution_tier(new_level)
    
    return {
        "xp_earned": xp_earned,
        "xp_bonus": xp_earned - base_xp,
        "gold_earned": gold_reward,
        "leveled_up": new_level > old_level,
        "levels_gained": new_level - old_level,
        "new_level": new_level,
        "tier_evolved": new_tier > old_tier,
        "new_tier": EVOLUTION_TIERS[new_tier]["name"] if new_tier > old_tier else None,
        "tier_icon": EVOLUTION_TIERS[new_tier]["icon"]
    }


def on_achievement_unlock(gold_reward: int = 100, gem_reward: int = 5, xp_reward: int = 50):
    """
    Call when an achievement is unlocked.
    
    Args:
        gold_reward: Gold to award
        gem_reward: Gems to award
        xp_reward: XP to award
        
    Returns:
        Dictionary with results
    """
    st.session_state.player_gold += gold_reward
    st.session_state.player_gems += gem_reward
    
    result = on_habit_complete(xp_reward, 0)
    result["gold_earned"] = gold_reward
    result["gems_earned"] = gem_reward
    
    return result


def on_quest_complete(xp_reward: int, gold_reward: int, gem_reward: int = 0):
    """
    Call when a quest is completed.
    """
    st.session_state.player_gold += gold_reward
    st.session_state.player_gems += gem_reward
    
    return on_habit_complete(xp_reward, 0)


# =============================================================================
# SIDEBAR COMPONENTS
# =============================================================================

def render_sidebar_character(show_currencies: bool = True, avatar_size: int = 120):
    """
    Render a compact character display suitable for sidebars.
    
    Args:
        show_currencies: Whether to show gold/gems
        avatar_size: Size of the avatar
    """
    init_character_state()
    
    with st.container():
        render_character_display(show_stats=False, size=avatar_size)
        
        tier = get_evolution_tier(st.session_state.player_level)
        tier_config = EVOLUTION_TIERS[tier]
        
        # Compact stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Level", st.session_state.player_level)
        with col2:
            st.metric("Tier", tier_config["icon"])
        
        # XP progress
        progress = calculate_tier_progress(
            st.session_state.player_level,
            st.session_state.player_xp,
            st.session_state.xp_for_next_level
        )
        st.progress(
            progress["level_progress"] / 100,
            text=f"{st.session_state.player_xp}/{st.session_state.xp_for_next_level} XP"
        )
        
        # Currencies
        if show_currencies:
            curr_col1, curr_col2 = st.columns(2)
            with curr_col1:
                st.metric("💰", st.session_state.player_gold)
            with curr_col2:
                st.metric("💎", st.session_state.player_gems)
        
        # XP bonus indicator
        equipped = get_equipped_items()
        xp_bonus = calculate_total_xp_bonus(equipped)
        if xp_bonus > 0:
            st.success(f"+{xp_bonus}% XP Bonus")


def render_mini_character(size: int = 80):
    """
    Render a minimal character display for very compact spaces.
    """
    init_character_state()
    
    from character_system import generate_avatar_url
    
    appearance = st.session_state.character_appearance
    equipped = get_equipped_items()
    avatar_url = generate_avatar_url(appearance, equipped, size)
    
    tier = get_evolution_tier(st.session_state.player_level)
    tier_config = EVOLUTION_TIERS[tier]
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px;">
        <img src="{avatar_url}" width="{size}" style="border-radius: 50%; border: 2px solid {tier_config['border_color']};" />
        <div>
            <div style="font-weight: bold;">Lv. {st.session_state.player_level}</div>
            <div style="color: {tier_config['title_color']};">{tier_config['icon']} {tier_config['name']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# NOTIFICATION HELPERS
# =============================================================================

def show_xp_notification(result: Dict[str, Any]):
    """
    Display XP gain notification with all relevant info.
    
    Args:
        result: Result dictionary from on_habit_complete or similar
    """
    # XP earned
    bonus_text = f" (+{result['xp_bonus']} bonus)" if result['xp_bonus'] > 0 else ""
    st.success(f"⭐ +{result['xp_earned']} XP{bonus_text}")
    
    # Level up
    if result['leveled_up']:
        st.balloons()
        if result['levels_gained'] > 1:
            st.success(f"🎉 LEVEL UP x{result['levels_gained']}! You are now level {result['new_level']}!")
        else:
            st.success(f"🎉 LEVEL UP! You are now level {result['new_level']}!")
    
    # Tier evolution
    if result['tier_evolved']:
        st.success(f"✨ EVOLUTION! You've become a {result['tier_icon']} {result['new_tier']}!")
    
    # Gold earned
    if result.get('gold_earned', 0) > 0:
        st.info(f"💰 +{result['gold_earned']} Gold")
    
    # Gems earned
    if result.get('gems_earned', 0) > 0:
        st.info(f"💎 +{result['gems_earned']} Gems")


def show_purchase_notification(item_name: str, cost_gold: int, cost_gems: int = 0):
    """
    Display purchase notification.
    """
    cost_text = f"💰 {cost_gold}"
    if cost_gems > 0:
        cost_text += f" + 💎 {cost_gems}"
    
    st.success(f"🛒 Purchased {item_name} for {cost_text}!")


# =============================================================================
# QUICK ACTIONS
# =============================================================================

def award_gold(amount: int, source: str = ""):
    """Quick helper to award gold."""
    st.session_state.player_gold += amount
    if source:
        st.toast(f"💰 +{amount} Gold from {source}")


def award_gems(amount: int, source: str = ""):
    """Quick helper to award gems."""
    st.session_state.player_gems += amount
    if source:
        st.toast(f"💎 +{amount} Gems from {source}")


def spend_gold(amount: int) -> bool:
    """Try to spend gold. Returns True if successful."""
    if st.session_state.player_gold >= amount:
        st.session_state.player_gold -= amount
        return True
    return False


def spend_gems(amount: int) -> bool:
    """Try to spend gems. Returns True if successful."""
    if st.session_state.player_gems >= amount:
        st.session_state.player_gems -= amount
        return True
    return False


def can_afford(gold: int, gems: int = 0) -> bool:
    """Check if player can afford a purchase."""
    return (st.session_state.player_gold >= gold and 
            st.session_state.player_gems >= gems)


# =============================================================================
# EQUIPMENT HELPERS
# =============================================================================

def get_equipped_xp_bonus() -> int:
    """Get total XP bonus from equipped items."""
    return calculate_total_xp_bonus(get_equipped_items())


def get_equipped_item_names() -> list:
    """Get list of equipped item names."""
    return [item.name for item in get_equipped_items()]


def has_item(item_id: str) -> bool:
    """Check if player owns an item."""
    return item_id in st.session_state.inventory


def is_equipped(item_id: str) -> bool:
    """Check if an item is currently equipped."""
    return item_id in st.session_state.equipped_items.values()


# =============================================================================
# TIER HELPERS
# =============================================================================

def get_current_tier_info() -> Dict[str, Any]:
    """Get information about the current tier."""
    tier = get_evolution_tier(st.session_state.player_level)
    config = EVOLUTION_TIERS[tier]
    progress = calculate_tier_progress(
        st.session_state.player_level,
        st.session_state.player_xp,
        st.session_state.xp_for_next_level
    )
    
    return {
        "tier_number": tier,
        "tier_name": config["name"],
        "tier_icon": config["icon"],
        "progress_percent": progress["tier_progress"],
        "levels_to_next": progress["levels_until_next_tier"],
        "next_tier_name": progress["next_tier_name"]
    }


def is_max_tier() -> bool:
    """Check if player is at maximum tier."""
    return get_evolution_tier(st.session_state.player_level) >= 6


# =============================================================================
# PAGE RENDERING HELPERS
# =============================================================================

def render_character_page():
    """
    Render a complete character page with tabs.
    Useful for creating a dedicated character section.
    """
    init_character_state()
    
    st.title("👤 Character")
    
    tabs = st.tabs(["Overview", "Customize", "Equipment", "Shop", "Tiers"])
    
    with tabs[0]:
        render_character_display(show_stats=True, size=250)
    
    with tabs[1]:
        render_character_customization()
    
    with tabs[2]:
        render_equipment_manager()
    
    with tabs[3]:
        render_shop_interface()
    
    with tabs[4]:
        render_tier_overview()


# =============================================================================
# DEBUG UTILITIES
# =============================================================================

def debug_panel():
    """Render a debug panel for testing."""
    with st.expander("🔧 Debug Panel"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**XP Controls**")
            if st.button("Add 100 XP"):
                show_xp_notification(on_habit_complete(100))
            if st.button("Add 500 XP"):
                show_xp_notification(on_habit_complete(500))
        
        with col2:
            st.markdown("**Currency Controls**")
            if st.button("Add 1000 Gold"):
                award_gold(1000, "Debug")
            if st.button("Add 50 Gems"):
                award_gems(50, "Debug")
        
        with col3:
            st.markdown("**Level Controls**")
            if st.button("Set Level 50"):
                st.session_state.player_level = 50
                st.rerun()
            if st.button("Reset All"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        st.markdown("**Current State**")
        st.json({
            "level": st.session_state.player_level,
            "xp": st.session_state.player_xp,
            "gold": st.session_state.player_gold,
            "gems": st.session_state.player_gems,
            "tier": get_current_tier_info(),
            "equipped_count": len(get_equipped_items()),
            "inventory_count": len(st.session_state.inventory)
        })

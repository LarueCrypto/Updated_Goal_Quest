"""
Goal Quest Avatar System
========================
Full-body character avatars that evolve based on level/rank.
Uses SVG converted to base64 for 100% reliable Streamlit rendering.
"""

import base64
from typing import Dict, Optional


# ============ AVATAR CONFIGURATION ============

GENDER_CONFIG = {
    "male": {
        "head": "M50 25 C65 25 75 40 75 55 C75 75 65 85 50 85 C35 85 25 75 25 55 C25 40 35 25 50 25",
        "body_width": 40,
        "hair": "M30 45 Q35 20 50 15 Q65 20 70 45 Q65 35 50 32 Q35 35 30 45",
        "shoulders": 45,
    },
    "female": {
        "head": "M50 28 C63 28 72 42 72 55 C72 73 63 82 50 82 C37 82 28 73 28 55 C28 42 37 28 50 28",
        "body_width": 35,
        "hair": "M25 55 Q28 20 50 12 Q72 20 75 55 Q70 45 70 60 L68 90 Q50 85 32 90 L30 60 Q30 45 25 55",
        "shoulders": 40,
    },
    "neutral": {
        "head": "M50 26 C64 26 74 41 74 55 C74 74 64 84 50 84 C36 84 26 74 26 55 C26 41 36 26 50 26",
        "body_width": 38,
        "hair": "M32 48 Q36 22 50 16 Q64 22 68 48 Q62 38 50 35 Q38 38 32 48",
        "shoulders": 42,
    }
}

CLASS_CONFIG = {
    "warrior": {
        "primary": "#ef4444",      # Red
        "secondary": "#991b1b",
        "accent": "#fca5a5",
        "armor_style": "heavy",
        "weapon": "sword",
        "aura_color": "#ef4444",
    },
    "mage": {
        "primary": "#8b5cf6",      # Purple
        "secondary": "#5b21b6",
        "accent": "#c4b5fd",
        "armor_style": "robes",
        "weapon": "staff",
        "aura_color": "#8b5cf6",
    },
    "rogue": {
        "primary": "#22c55e",      # Green
        "secondary": "#15803d",
        "accent": "#86efac",
        "armor_style": "light",
        "weapon": "daggers",
        "aura_color": "#22c55e",
    },
    "sage": {
        "primary": "#3b82f6",      # Blue
        "secondary": "#1d4ed8",
        "accent": "#93c5fd",
        "armor_style": "robes",
        "weapon": "tome",
        "aura_color": "#3b82f6",
    }
}

# Evolution stages based on rank
EVOLUTION_CONFIG = {
    "E": {  # Level 1-9
        "armor_tier": 1,
        "aura": False,
        "glow": False,
        "cape": False,
        "wings": False,
        "title": "Novice",
    },
    "D": {  # Level 10-19
        "armor_tier": 2,
        "aura": False,
        "glow": False,
        "cape": False,
        "wings": False,
        "title": "Apprentice",
    },
    "C": {  # Level 20-39
        "armor_tier": 3,
        "aura": True,
        "glow": False,
        "cape": False,
        "wings": False,
        "title": "Adept",
    },
    "B": {  # Level 40-59
        "armor_tier": 4,
        "aura": True,
        "glow": True,
        "cape": True,
        "wings": False,
        "title": "Expert",
    },
    "A": {  # Level 60-79
        "armor_tier": 5,
        "aura": True,
        "glow": True,
        "cape": True,
        "wings": False,
        "title": "Master",
    },
    "S": {  # Level 80-99
        "armor_tier": 6,
        "aura": True,
        "glow": True,
        "cape": True,
        "wings": True,
        "title": "Champion",
    },
    "SS": {  # Level 100+
        "armor_tier": 7,
        "aura": True,
        "glow": True,
        "cape": True,
        "wings": True,
        "title": "Shadow Monarch",
    }
}


def get_rank_from_level(level: int) -> str:
    """Get rank letter from level"""
    if level < 10:
        return "E"
    elif level < 20:
        return "D"
    elif level < 40:
        return "C"
    elif level < 60:
        return "B"
    elif level < 80:
        return "A"
    elif level < 100:
        return "S"
    else:
        return "SS"


def generate_avatar_svg(
    gender: str = "neutral",
    avatar_class: str = "warrior",
    level: int = 1,
    skin_tone: str = "#e8beac",
    hair_color: str = "#2d2d2d",
    width: int = 200,
    height: int = 300
) -> str:
    """
    Generate a full-body avatar SVG that evolves based on level.
    
    Args:
        gender: "male", "female", or "neutral"
        avatar_class: "warrior", "mage", "rogue", or "sage"
        level: Player level (determines evolution stage)
        skin_tone: Hex color for skin
        hair_color: Hex color for hair
        width: SVG width
        height: SVG height
    
    Returns:
        SVG string
    """
    rank = get_rank_from_level(level)
    gender_data = GENDER_CONFIG.get(gender, GENDER_CONFIG["neutral"])
    class_data = CLASS_CONFIG.get(avatar_class, CLASS_CONFIG["warrior"])
    evolution = EVOLUTION_CONFIG.get(rank, EVOLUTION_CONFIG["E"])
    
    # Calculate armor opacity based on tier
    armor_tier = evolution["armor_tier"]
    armor_opacity = 0.3 + (armor_tier * 0.1)  # 0.4 to 1.0
    
    # Build SVG parts
    svg_parts = []
    
    # Background glow for higher ranks
    if evolution["glow"]:
        svg_parts.append(f'''
        <defs>
            <radialGradient id="auraGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:{class_data['aura_color']};stop-opacity:0.4"/>
                <stop offset="100%" style="stop-color:{class_data['aura_color']};stop-opacity:0"/>
            </radialGradient>
        </defs>
        <ellipse cx="100" cy="200" rx="80" ry="120" fill="url(#auraGlow)"/>
        ''')
    
    # Wings for S-rank and above
    if evolution["wings"]:
        svg_parts.append(f'''
        <!-- Wings -->
        <path d="M30 140 Q-20 100 10 60 Q30 90 50 120 Z" fill="{class_data['accent']}" opacity="0.7"/>
        <path d="M170 140 Q220 100 190 60 Q170 90 150 120 Z" fill="{class_data['accent']}" opacity="0.7"/>
        <path d="M35 150 Q-10 120 20 80 Q35 105 50 130 Z" fill="{class_data['primary']}" opacity="0.5"/>
        <path d="M165 150 Q210 120 180 80 Q165 105 150 130 Z" fill="{class_data['primary']}" opacity="0.5"/>
        ''')
    
    # Cape for B-rank and above
    if evolution["cape"]:
        svg_parts.append(f'''
        <!-- Cape -->
        <path d="M60 120 Q50 180 45 260 L100 280 L155 260 Q150 180 140 120 Z" 
              fill="{class_data['secondary']}" opacity="0.9"/>
        <path d="M65 125 Q55 180 52 250 L100 268 L148 250 Q145 180 135 125 Z" 
              fill="{class_data['primary']}" opacity="0.8"/>
        ''')
    
    # Legs
    svg_parts.append(f'''
    <!-- Legs -->
    <rect x="70" y="210" width="25" height="70" rx="8" fill="{class_data['secondary']}"/>
    <rect x="105" y="210" width="25" height="70" rx="8" fill="{class_data['secondary']}"/>
    <!-- Boots -->
    <path d="M65 270 L95 270 L98 290 L62 290 Z" fill="#1a1a1a"/>
    <path d="M105 270 L135 290 L138 290 L102 290 Z" fill="#1a1a1a"/>
    ''')
    
    # Body/Torso
    body_width = gender_data["body_width"]
    svg_parts.append(f'''
    <!-- Body -->
    <path d="M{100-body_width} 110 
             Q{100-body_width-5} 160 {100-body_width+5} 220 
             L{100+body_width-5} 220 
             Q{100+body_width+5} 160 {100+body_width} 110 Z" 
          fill="{class_data['primary']}" opacity="{armor_opacity}"/>
    ''')
    
    # Armor details based on tier
    if armor_tier >= 2:
        svg_parts.append(f'''
        <!-- Chest plate -->
        <path d="M75 115 L100 130 L125 115 L125 160 L100 175 L75 160 Z" 
              fill="{class_data['secondary']}" opacity="0.8"/>
        ''')
    
    if armor_tier >= 3:
        svg_parts.append(f'''
        <!-- Shoulder guards -->
        <ellipse cx="60" cy="115" rx="18" ry="12" fill="{class_data['primary']}"/>
        <ellipse cx="140" cy="115" rx="18" ry="12" fill="{class_data['primary']}"/>
        ''')
    
    if armor_tier >= 4:
        svg_parts.append(f'''
        <!-- Belt -->
        <rect x="70" y="195" width="60" height="12" rx="3" fill="#d4af37"/>
        <circle cx="100" cy="201" r="6" fill="#ffd700"/>
        ''')
    
    if armor_tier >= 5:
        svg_parts.append(f'''
        <!-- Ornate chest symbol -->
        <circle cx="100" cy="145" r="12" fill="{class_data['accent']}" opacity="0.9"/>
        <circle cx="100" cy="145" r="8" fill="{class_data['aura_color']}" opacity="0.7"/>
        ''')
    
    if armor_tier >= 6:
        svg_parts.append(f'''
        <!-- Crown/helm detail -->
        <path d="M70 55 L80 45 L90 55 L100 40 L110 55 L120 45 L130 55" 
              stroke="#d4af37" stroke-width="3" fill="none"/>
        ''')
    
    # Arms
    svg_parts.append(f'''
    <!-- Arms -->
    <path d="M55 115 Q40 150 35 190 Q38 195 45 190 Q55 155 65 125 Z" fill="{skin_tone}"/>
    <path d="M145 115 Q160 150 165 190 Q162 195 155 190 Q145 155 135 125 Z" fill="{skin_tone}"/>
    <!-- Arm armor -->
    <path d="M55 118 Q45 145 42 170 L52 170 Q58 145 62 122 Z" 
          fill="{class_data['primary']}" opacity="{armor_opacity}"/>
    <path d="M145 118 Q155 145 158 170 L148 170 Q142 145 138 122 Z" 
          fill="{class_data['primary']}" opacity="{armor_opacity}"/>
    ''')
    
    # Hands
    svg_parts.append(f'''
    <!-- Hands -->
    <circle cx="38" cy="195" r="8" fill="{skin_tone}"/>
    <circle cx="162" cy="195" r="8" fill="{skin_tone}"/>
    ''')
    
    # Weapon based on class
    if class_data["weapon"] == "sword":
        svg_parts.append(f'''
        <!-- Sword -->
        <rect x="165" y="120" width="6" height="80" rx="2" fill="#9ca3af"/>
        <rect x="160" y="115" width="16" height="8" rx="2" fill="#d4af37"/>
        <polygon points="168,120 168,100 171,90 174,100 174,120" fill="#e5e7eb"/>
        ''')
    elif class_data["weapon"] == "staff":
        svg_parts.append(f'''
        <!-- Staff -->
        <rect x="167" y="80" width="5" height="130" rx="2" fill="#8b4513"/>
        <circle cx="170" cy="75" r="15" fill="{class_data['accent']}" opacity="0.8"/>
        <circle cx="170" cy="75" r="8" fill="{class_data['aura_color']}"/>
        ''')
    elif class_data["weapon"] == "daggers":
        svg_parts.append(f'''
        <!-- Daggers -->
        <polygon points="25,180 20,195 30,195" fill="#9ca3af"/>
        <rect x="23" y="195" width="4" height="15" fill="#d4af37"/>
        <polygon points="175,180 170,195 180,195" fill="#9ca3af"/>
        <rect x="173" y="195" width="4" height="15" fill="#d4af37"/>
        ''')
    elif class_data["weapon"] == "tome":
        svg_parts.append(f'''
        <!-- Tome -->
        <rect x="20" y="175" width="25" height="35" rx="3" fill="#8b4513"/>
        <rect x="23" y="178" width="19" height="29" rx="2" fill="{class_data['accent']}"/>
        <circle cx="32" cy="192" r="6" fill="{class_data['aura_color']}"/>
        ''')
    
    # Neck
    svg_parts.append(f'''
    <!-- Neck -->
    <rect x="90" y="85" width="20" height="30" rx="5" fill="{skin_tone}"/>
    ''')
    
    # Head
    svg_parts.append(f'''
    <!-- Head -->
    <ellipse cx="100" cy="55" rx="28" ry="32" fill="{skin_tone}"/>
    ''')
    
    # Hair
    svg_parts.append(f'''
    <!-- Hair -->
    <path d="{gender_data['hair'].replace('50', '100').replace('M25', 'M75').replace('M30', 'M80').replace('M32', 'M82').replace('Q35', 'Q85').replace('Q36', 'Q86').replace('Q65', 'Q115').replace('Q64', 'Q114').replace('Q70', 'Q120').replace('Q72', 'Q122').replace('L68', 'L118').replace('L70', 'L120').replace('L30', 'L80').replace('L32', 'L82')}" 
          fill="{hair_color}" transform="translate(0, 15)"/>
    ''')
    
    # Face
    svg_parts.append(f'''
    <!-- Eyes -->
    <ellipse cx="88" cy="55" rx="5" ry="4" fill="#1a1a1a"/>
    <ellipse cx="112" cy="55" rx="5" ry="4" fill="#1a1a1a"/>
    <circle cx="89" cy="54" r="1.5" fill="white"/>
    <circle cx="113" cy="54" r="1.5" fill="white"/>
    <!-- Mouth -->
    <path d="M95 68 Q100 72 105 68" stroke="#1a1a1a" stroke-width="1.5" fill="none"/>
    ''')
    
    # Aura effect for C-rank and above
    if evolution["aura"]:
        svg_parts.append(f'''
        <!-- Aura particles -->
        <circle cx="50" cy="100" r="3" fill="{class_data['aura_color']}" opacity="0.6">
            <animate attributeName="cy" values="100;80;100" dur="2s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.6;0.2;0.6" dur="2s" repeatCount="indefinite"/>
        </circle>
        <circle cx="150" cy="120" r="2" fill="{class_data['aura_color']}" opacity="0.5">
            <animate attributeName="cy" values="120;95;120" dur="2.5s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.5;0.1;0.5" dur="2.5s" repeatCount="indefinite"/>
        </circle>
        <circle cx="70" cy="180" r="2.5" fill="{class_data['aura_color']}" opacity="0.4">
            <animate attributeName="cy" values="180;160;180" dur="3s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.4;0.1;0.4" dur="3s" repeatCount="indefinite"/>
        </circle>
        <circle cx="130" cy="200" r="2" fill="{class_data['aura_color']}" opacity="0.5">
            <animate attributeName="cy" values="200;175;200" dur="2.8s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.5;0.2;0.5" dur="2.8s" repeatCount="indefinite"/>
        </circle>
        ''')
    
    # Assemble SVG
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300" width="{width}" height="{height}">
    <rect width="200" height="300" fill="transparent"/>
    {''.join(svg_parts)}
</svg>'''
    
    return svg


def svg_to_base64(svg_string: str) -> str:
    """Convert SVG string to base64 data URI"""
    svg_bytes = svg_string.encode('utf-8')
    b64 = base64.b64encode(svg_bytes).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64}"


def get_avatar_image(
    gender: str = "neutral",
    avatar_class: str = "warrior", 
    level: int = 1,
    skin_tone: str = "#e8beac",
    hair_color: str = "#2d2d2d",
    width: int = 200,
    height: int = 300
) -> str:
    """
    Get avatar as a base64 image URI for use in st.image()
    
    Usage in Streamlit:
        from avatar_system import get_avatar_image
        avatar_uri = get_avatar_image(gender="male", avatar_class="warrior", level=50)
        st.image(avatar_uri, width=200)
    """
    svg = generate_avatar_svg(
        gender=gender,
        avatar_class=avatar_class,
        level=level,
        skin_tone=skin_tone,
        hair_color=hair_color,
        width=width,
        height=height
    )
    return svg_to_base64(svg)


# ============ STREAMLIT INTEGRATION ============

def render_avatar_streamlit(profile, stats, show_info: bool = True):
    """
    Render the full avatar card in Streamlit.
    
    Usage:
        from avatar_system import render_avatar_streamlit
        render_avatar_streamlit(profile, stats)
    """
    import streamlit as st
    
    gender = profile.gender or "neutral"
    avatar_class = profile.avatar_style or "warrior"
    level = stats.level or 1
    display_name = profile.display_name or "Hunter"
    current_gold = stats.current_gold or 0
    
    # Get evolution info
    rank = get_rank_from_level(level)
    evolution = EVOLUTION_CONFIG.get(rank, EVOLUTION_CONFIG["E"])
    class_data = CLASS_CONFIG.get(avatar_class, CLASS_CONFIG["warrior"])
    
    # Generate avatar
    avatar_uri = get_avatar_image(
        gender=gender,
        avatar_class=avatar_class,
        level=level,
        width=200,
        height=300
    )
    
    # Display avatar
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(avatar_uri, use_container_width=True)
    
    if show_info:
        # Character info below
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, #1a1a2e, #0f0f1a); border: 2px solid #d4af37; border-radius: 15px; margin-top: 10px;">
            <h2 style="color: #d4af37; margin: 0 0 5px 0;">{display_name}</h2>
            <p style="color: {class_data['primary']}; font-weight: bold; margin: 5px 0;">
                {avatar_class.title()} • Level {level}
            </p>
            <span style="display: inline-block; background: #6b728033; border: 2px solid #6b7280; color: #9ca3af; padding: 3px 12px; border-radius: 15px; font-size: 14px; margin: 5px 0;">
                {rank}-Rank {evolution['title']}
            </span>
            <div style="margin-top: 10px; padding: 8px; background: #1a1a1a; border: 1px solid #d4af37; border-radius: 8px;">
                <span style="color: #ffd700;">💰 {current_gold:,} Gold</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_stats_streamlit(stats):
    """
    Render stats panel using native Streamlit components.
    
    Usage:
        from avatar_system import render_stats_streamlit
        render_stats_streamlit(stats)
    """
    import streamlit as st
    
    stat_config = [
        ("Strength", "strength", "💪"),
        ("Intelligence", "intelligence", "🧠"),
        ("Vitality", "vitality", "❤️"),
        ("Agility", "agility", "⚡"),
        ("Sense", "sense", "👁️"),
        ("Willpower", "willpower", "🔥"),
    ]
    
    st.markdown("### 📊 Combat Stats")
    
    for label, key, icon in stat_config:
        value = getattr(stats, key, 0) or 0
        col1, col2 = st.columns([4, 1])
        with col1:
            st.caption(f"{icon} {label}")
            st.progress(min(value / 100, 1.0))
        with col2:
            st.markdown(f"**{value}**")


# ============ PREVIEW/TESTING ============

if __name__ == "__main__":
    # Test generating avatars at different levels
    import os
    
    test_cases = [
        ("E-Rank", 5),
        ("D-Rank", 15),
        ("C-Rank", 30),
        ("B-Rank", 50),
        ("A-Rank", 70),
        ("S-Rank", 90),
        ("SS-Rank", 100),
    ]
    
    for rank_name, level in test_cases:
        svg = generate_avatar_svg(
            gender="male",
            avatar_class="warrior",
            level=level
        )
        print(f"Generated {rank_name} avatar (Level {level})")

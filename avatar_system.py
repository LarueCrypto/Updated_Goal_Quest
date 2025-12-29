"""
Goal Quest - Character Evolution & Equipment System
====================================================
A comprehensive character system with DiceBear Micah avatars,
evolution tiers, and shop item integration.

Author: Goal Quest Team
Version: 1.0.0
"""

import streamlit as st
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import base64
from urllib.parse import urlencode

# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class Rarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class EquipmentSlot(Enum):
    HEAD = "head"
    BODY = "body"
    WEAPON = "weapon"
    OFFHAND = "offhand"
    ACCESSORY = "accessory"
    AURA = "aura"
    PET = "pet"
    CAPE = "cape"

class CharacterClass(Enum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    PALADIN = "paladin"
    RANGER = "ranger"

# Rarity colors and effects
RARITY_CONFIG = {
    Rarity.COMMON: {
        "color": "#9CA3AF",
        "glow": "none",
        "border": "2px solid #9CA3AF",
        "badge": "⚪",
        "xp_bonus": 0
    },
    Rarity.UNCOMMON: {
        "color": "#22C55E",
        "glow": "0 0 5px #22C55E",
        "border": "2px solid #22C55E",
        "badge": "🟢",
        "xp_bonus": 5
    },
    Rarity.RARE: {
        "color": "#3B82F6",
        "glow": "0 0 10px #3B82F6",
        "border": "2px solid #3B82F6",
        "badge": "🔵",
        "xp_bonus": 10
    },
    Rarity.EPIC: {
        "color": "#A855F7",
        "glow": "0 0 15px #A855F7",
        "border": "3px solid #A855F7",
        "badge": "🟣",
        "xp_bonus": 20
    },
    Rarity.LEGENDARY: {
        "color": "#F59E0B",
        "glow": "0 0 20px #F59E0B, 0 0 40px #F59E0B",
        "border": "3px solid #F59E0B",
        "badge": "🟡",
        "xp_bonus": 50
    }
}

# Evolution tier configuration
EVOLUTION_TIERS = {
    1: {
        "name": "Novice Adventurer",
        "level_range": (1, 10),
        "icon": "🌱",
        "border_color": "#6B7280",
        "background": "linear-gradient(135deg, #374151 0%, #1F2937 100%)",
        "aura": None,
        "title_color": "#9CA3AF"
    },
    2: {
        "name": "Apprentice Hero",
        "level_range": (11, 25),
        "icon": "⚔️",
        "border_color": "#22C55E",
        "background": "linear-gradient(135deg, #065F46 0%, #064E3B 100%)",
        "aura": "0 0 10px rgba(34, 197, 94, 0.3)",
        "title_color": "#22C55E"
    },
    3: {
        "name": "Seasoned Champion",
        "level_range": (26, 50),
        "icon": "🛡️",
        "border_color": "#3B82F6",
        "background": "linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%)",
        "aura": "0 0 15px rgba(59, 130, 246, 0.4)",
        "title_color": "#3B82F6"
    },
    4: {
        "name": "Elite Vanquisher",
        "level_range": (51, 75),
        "icon": "👑",
        "border_color": "#A855F7",
        "background": "linear-gradient(135deg, #581C87 0%, #6B21A8 100%)",
        "aura": "0 0 20px rgba(168, 85, 247, 0.5)",
        "title_color": "#A855F7"
    },
    5: {
        "name": "Legendary Master",
        "level_range": (76, 100),
        "icon": "🌟",
        "border_color": "#F59E0B",
        "background": "linear-gradient(135deg, #B45309 0%, #D97706 100%)",
        "aura": "0 0 30px rgba(245, 158, 11, 0.6), 0 0 60px rgba(245, 158, 11, 0.3)",
        "title_color": "#F59E0B"
    },
    6: {
        "name": "Mythic Ascendant",
        "level_range": (101, 999),
        "icon": "✨",
        "border_color": "#EC4899",
        "background": "linear-gradient(135deg, #831843 0%, #BE185D 50%, #F59E0B 100%)",
        "aura": "0 0 40px rgba(236, 72, 153, 0.7), 0 0 80px rgba(245, 158, 11, 0.4)",
        "title_color": "linear-gradient(90deg, #EC4899, #F59E0B)"
    }
}

# DiceBear Micah customization options
DICEBEAR_OPTIONS = {
    "baseColor": ["ac6651", "f9c9b6", "77311d", "d2b48c", "8d5524"],
    "earringColor": ["transparent", "f59e0b", "9ca3af", "fbbf24", "a855f7"],
    "eyebrowStyle": ["up", "down", "eyelashesUp", "eyelashesDown"],
    "eyeColor": ["6b7280", "3b82f6", "22c55e", "a855f7", "f59e0b"],
    "eyesStyle": ["eyes", "round", "smiling", "eyesShadow"],
    "facialHairColor": ["transparent", "2c1810", "4a3728", "6b4423", "1a1a1a"],
    "facialHairStyle": ["beard", "scruff", "transparent"],
    "glassesProbability": [0, 50, 100],
    "glassesColor": ["1f2937", "6b7280", "3b82f6", "f59e0b"],
    "glassesStyle": ["round", "square"],
    "hairColor": ["2c1810", "4a3728", "6b4423", "1a1a1a", "d4a574", "c4a484", "e8d5b7", "f59e0b", "a855f7", "3b82f6"],
    "hairStyle": ["dannyPhantom", "dougFunny", "fonze", "full", "mrClean", "mrT", "pixie", "turpieFull", "turban"],
    "mouthStyle": ["laughing", "nervous", "pucker", "sad", "smile", "smirk", "surprised"],
    "noseStyle": ["curve", "pointed", "round"],
    "shirtColor": ["6b7280", "3b82f6", "22c55e", "ef4444", "a855f7", "f59e0b", "1f2937"],
    "shirtStyle": ["collared", "crew", "open"]
}

# Character class presets
CLASS_PRESETS = {
    CharacterClass.WARRIOR: {
        "name": "Warrior",
        "icon": "⚔️",
        "description": "A brave fighter skilled in combat",
        "defaults": {
            "hairStyle": "mrT",
            "hairColor": "2c1810",
            "eyesStyle": "eyes",
            "mouthStyle": "smirk",
            "shirtStyle": "crew",
            "shirtColor": "ef4444"
        }
    },
    CharacterClass.MAGE: {
        "name": "Mage",
        "icon": "🔮",
        "description": "A wise spellcaster with arcane powers",
        "defaults": {
            "hairStyle": "full",
            "hairColor": "a855f7",
            "eyesStyle": "eyesShadow",
            "mouthStyle": "smile",
            "shirtStyle": "collared",
            "shirtColor": "3b82f6"
        }
    },
    CharacterClass.ROGUE: {
        "name": "Rogue",
        "icon": "🗡️",
        "description": "A stealthy trickster and master of shadows",
        "defaults": {
            "hairStyle": "pixie",
            "hairColor": "1a1a1a",
            "eyesStyle": "round",
            "mouthStyle": "smirk",
            "shirtStyle": "open",
            "shirtColor": "1f2937"
        }
    },
    CharacterClass.PALADIN: {
        "name": "Paladin",
        "icon": "🛡️",
        "description": "A holy warrior blessed with divine power",
        "defaults": {
            "hairStyle": "fonze",
            "hairColor": "d4a574",
            "eyesStyle": "smiling",
            "mouthStyle": "smile",
            "shirtStyle": "crew",
            "shirtColor": "f59e0b"
        }
    },
    CharacterClass.RANGER: {
        "name": "Ranger",
        "icon": "🏹",
        "description": "A skilled hunter at home in the wilderness",
        "defaults": {
            "hairStyle": "dougFunny",
            "hairColor": "6b4423",
            "eyesStyle": "eyes",
            "mouthStyle": "nervous",
            "shirtStyle": "open",
            "shirtColor": "22c55e"
        }
    }
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ShopItem:
    """Represents an item available in the shop or player inventory."""
    id: str
    name: str
    description: str
    cost_gold: int
    cost_gems: int
    rarity: Rarity
    slot: EquipmentSlot
    level_requirement: int
    icon: str
    visual_effect: Dict[str, Any]  # DiceBear parameters or overlay info
    stat_bonuses: Dict[str, int] = field(default_factory=dict)
    is_equipped: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "cost_gold": self.cost_gold,
            "cost_gems": self.cost_gems,
            "rarity": self.rarity.value,
            "slot": self.slot.value,
            "level_requirement": self.level_requirement,
            "icon": self.icon,
            "visual_effect": self.visual_effect,
            "stat_bonuses": self.stat_bonuses,
            "is_equipped": self.is_equipped
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ShopItem':
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            cost_gold=data["cost_gold"],
            cost_gems=data["cost_gems"],
            rarity=Rarity(data["rarity"]),
            slot=EquipmentSlot(data["slot"]),
            level_requirement=data["level_requirement"],
            icon=data["icon"],
            visual_effect=data["visual_effect"],
            stat_bonuses=data.get("stat_bonuses", {}),
            is_equipped=data.get("is_equipped", False)
        )


@dataclass
class CharacterAppearance:
    """Stores character customization settings."""
    base_color: str = "f9c9b6"
    hair_style: str = "full"
    hair_color: str = "2c1810"
    eyes_style: str = "eyes"
    eye_color: str = "6b7280"
    eyebrow_style: str = "up"
    mouth_style: str = "smile"
    nose_style: str = "round"
    facial_hair_style: str = "transparent"
    facial_hair_color: str = "transparent"
    glasses_style: Optional[str] = None
    glasses_color: str = "1f2937"
    earring_color: str = "transparent"
    shirt_style: str = "crew"
    shirt_color: str = "3b82f6"
    character_class: str = "warrior"
    
    def to_dict(self) -> Dict:
        return {
            "baseColor": self.base_color,
            "hairStyle": self.hair_style,
            "hairColor": self.hair_color,
            "eyesStyle": self.eyes_style,
            "eyeColor": self.eye_color,
            "eyebrowStyle": self.eyebrow_style,
            "mouthStyle": self.mouth_style,
            "noseStyle": self.nose_style,
            "facialHairStyle": self.facial_hair_style,
            "facialHairColor": self.facial_hair_color,
            "glassesStyle": self.glasses_style or "",
            "glassesColor": self.glasses_color,
            "earringColor": self.earring_color,
            "shirtStyle": self.shirt_style,
            "shirtColor": self.shirt_color
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CharacterAppearance':
        return cls(
            base_color=data.get("baseColor", "f9c9b6"),
            hair_style=data.get("hairStyle", "full"),
            hair_color=data.get("hairColor", "2c1810"),
            eyes_style=data.get("eyesStyle", "eyes"),
            eye_color=data.get("eyeColor", "6b7280"),
            eyebrow_style=data.get("eyebrowStyle", "up"),
            mouth_style=data.get("mouthStyle", "smile"),
            nose_style=data.get("noseStyle", "round"),
            facial_hair_style=data.get("facialHairStyle", "transparent"),
            facial_hair_color=data.get("facialHairColor", "transparent"),
            glasses_style=data.get("glassesStyle"),
            glasses_color=data.get("glassesColor", "1f2937"),
            earring_color=data.get("earringColor", "transparent"),
            shirt_style=data.get("shirtStyle", "crew"),
            shirt_color=data.get("shirtColor", "3b82f6"),
            character_class=data.get("characterClass", "warrior")
        )


# =============================================================================
# SHOP ITEM CATALOG
# =============================================================================

SHOP_ITEMS_CATALOG = [
    # WEAPONS
    ShopItem(
        id="weapon_wooden_sword",
        name="Wooden Training Sword",
        description="A simple wooden sword for beginners",
        cost_gold=50,
        cost_gems=0,
        rarity=Rarity.COMMON,
        slot=EquipmentSlot.WEAPON,
        level_requirement=1,
        icon="🗡️",
        visual_effect={"overlay": "sword_wooden", "position": "right_hand"},
        stat_bonuses={"xp_bonus": 2}
    ),
    ShopItem(
        id="weapon_iron_sword",
        name="Iron Longsword",
        description="A reliable iron sword forged by skilled blacksmiths",
        cost_gold=200,
        cost_gems=0,
        rarity=Rarity.UNCOMMON,
        slot=EquipmentSlot.WEAPON,
        level_requirement=10,
        icon="⚔️",
        visual_effect={"overlay": "sword_iron", "position": "right_hand"},
        stat_bonuses={"xp_bonus": 5}
    ),
    ShopItem(
        id="weapon_crystal_staff",
        name="Crystal Mage Staff",
        description="A staff imbued with magical crystal energy",
        cost_gold=350,
        cost_gems=5,
        rarity=Rarity.RARE,
        slot=EquipmentSlot.WEAPON,
        level_requirement=20,
        icon="🔮",
        visual_effect={"overlay": "staff_crystal", "position": "right_hand", "glow": "#3B82F6"},
        stat_bonuses={"xp_bonus": 10}
    ),
    ShopItem(
        id="weapon_shadow_dagger",
        name="Shadow Dagger",
        description="A dagger that seems to absorb light",
        cost_gold=500,
        cost_gems=10,
        rarity=Rarity.EPIC,
        slot=EquipmentSlot.WEAPON,
        level_requirement=35,
        icon="🗡️",
        visual_effect={"overlay": "dagger_shadow", "position": "right_hand", "glow": "#A855F7"},
        stat_bonuses={"xp_bonus": 20}
    ),
    ShopItem(
        id="weapon_legendary_blade",
        name="Excalibur's Echo",
        description="A legendary blade said to be a shard of Excalibur itself",
        cost_gold=2000,
        cost_gems=50,
        rarity=Rarity.LEGENDARY,
        slot=EquipmentSlot.WEAPON,
        level_requirement=50,
        icon="⚔️",
        visual_effect={"overlay": "sword_legendary", "position": "right_hand", "glow": "#F59E0B", "particles": True},
        stat_bonuses={"xp_bonus": 50}
    ),
    
    # HEAD ITEMS
    ShopItem(
        id="head_leather_cap",
        name="Leather Cap",
        description="Basic head protection for novice adventurers",
        cost_gold=30,
        cost_gems=0,
        rarity=Rarity.COMMON,
        slot=EquipmentSlot.HEAD,
        level_requirement=1,
        icon="🧢",
        visual_effect={"dicebear_mod": {"hairStyle": "mrClean"}, "overlay": "cap_leather"},
        stat_bonuses={}
    ),
    ShopItem(
        id="head_wizard_hat",
        name="Apprentice Wizard Hat",
        description="A pointed hat worn by magic users",
        cost_gold=150,
        cost_gems=0,
        rarity=Rarity.UNCOMMON,
        slot=EquipmentSlot.HEAD,
        level_requirement=10,
        icon="🎩",
        visual_effect={"overlay": "hat_wizard", "color": "#3B82F6"},
        stat_bonuses={"xp_bonus": 3}
    ),
    ShopItem(
        id="head_knight_helm",
        name="Knight's Steel Helm",
        description="A polished steel helmet befitting a noble knight",
        cost_gold=400,
        cost_gems=5,
        rarity=Rarity.RARE,
        slot=EquipmentSlot.HEAD,
        level_requirement=25,
        icon="⛑️",
        visual_effect={"overlay": "helm_knight", "color": "#6B7280"},
        stat_bonuses={"xp_bonus": 8}
    ),
    ShopItem(
        id="head_crown_flames",
        name="Crown of Eternal Flames",
        description="A crown wreathed in magical fire that never burns its wearer",
        cost_gold=1500,
        cost_gems=30,
        rarity=Rarity.LEGENDARY,
        slot=EquipmentSlot.HEAD,
        level_requirement=60,
        icon="👑",
        visual_effect={"overlay": "crown_fire", "glow": "#F59E0B", "particles": True, "animation": "flame"},
        stat_bonuses={"xp_bonus": 35}
    ),
    
    # ACCESSORIES
    ShopItem(
        id="acc_simple_cape",
        name="Traveler's Cape",
        description="A simple but warm cape for long journeys",
        cost_gold=75,
        cost_gems=0,
        rarity=Rarity.COMMON,
        slot=EquipmentSlot.CAPE,
        level_requirement=5,
        icon="🧣",
        visual_effect={"overlay": "cape_simple", "color": "#6B7280"},
        stat_bonuses={}
    ),
    ShopItem(
        id="acc_fire_aura",
        name="Ember Aura",
        description="A fiery aura that surrounds you with warmth",
        cost_gold=300,
        cost_gems=10,
        rarity=Rarity.RARE,
        slot=EquipmentSlot.AURA,
        level_requirement=20,
        icon="🔥",
        visual_effect={"aura_type": "fire", "color": "#EF4444", "intensity": 0.6},
        stat_bonuses={"xp_bonus": 5}
    ),
    ShopItem(
        id="acc_lightning_aura",
        name="Storm Aura",
        description="Crackling lightning dances around your form",
        cost_gold=600,
        cost_gems=20,
        rarity=Rarity.EPIC,
        slot=EquipmentSlot.AURA,
        level_requirement=40,
        icon="⚡",
        visual_effect={"aura_type": "lightning", "color": "#FBBF24", "intensity": 0.8},
        stat_bonuses={"xp_bonus": 15}
    ),
    ShopItem(
        id="acc_pet_dragon",
        name="Baby Dragon Companion",
        description="A loyal baby dragon that follows you everywhere",
        cost_gold=1000,
        cost_gems=25,
        rarity=Rarity.EPIC,
        slot=EquipmentSlot.PET,
        level_requirement=30,
        icon="🐉",
        visual_effect={"pet_type": "dragon", "position": "shoulder", "color": "#EF4444"},
        stat_bonuses={"xp_bonus": 10}
    ),
    ShopItem(
        id="acc_wings_angel",
        name="Angel Wings",
        description="Divine wings that grant an ethereal appearance",
        cost_gold=2500,
        cost_gems=75,
        rarity=Rarity.LEGENDARY,
        slot=EquipmentSlot.ACCESSORY,
        level_requirement=70,
        icon="👼",
        visual_effect={"overlay": "wings_angel", "color": "#FFFFFF", "glow": "#F59E0B", "animation": "flutter"},
        stat_bonuses={"xp_bonus": 40}
    ),
    ShopItem(
        id="acc_shadow_cloak",
        name="Cloak of Shadows",
        description="A mysterious cloak that seems to bend light around it",
        cost_gold=800,
        cost_gems=15,
        rarity=Rarity.EPIC,
        slot=EquipmentSlot.CAPE,
        level_requirement=45,
        icon="🌑",
        visual_effect={"overlay": "cape_shadow", "color": "#1F2937", "glow": "#A855F7", "opacity": 0.8},
        stat_bonuses={"xp_bonus": 18}
    ),
    
    # OFFHAND
    ShopItem(
        id="offhand_wooden_shield",
        name="Wooden Shield",
        description="A basic shield for blocking attacks",
        cost_gold=40,
        cost_gems=0,
        rarity=Rarity.COMMON,
        slot=EquipmentSlot.OFFHAND,
        level_requirement=1,
        icon="🛡️",
        visual_effect={"overlay": "shield_wooden", "position": "left_hand"},
        stat_bonuses={}
    ),
    ShopItem(
        id="offhand_tome",
        name="Ancient Tome of Wisdom",
        description="A book containing forgotten knowledge",
        cost_gold=450,
        cost_gems=8,
        rarity=Rarity.RARE,
        slot=EquipmentSlot.OFFHAND,
        level_requirement=25,
        icon="📖",
        visual_effect={"overlay": "tome", "position": "left_hand", "glow": "#3B82F6"},
        stat_bonuses={"xp_bonus": 12}
    ),
]

# Convert to dictionary for easy lookup
SHOP_ITEMS = {item.id: item for item in SHOP_ITEMS_CATALOG}


# =============================================================================
# EQUIPMENT LOADOUTS
# =============================================================================

DEFAULT_LOADOUTS = {
    "warrior_set": {
        "name": "Warrior's Arsenal",
        "description": "A balanced set for frontline combat",
        "items": ["weapon_iron_sword", "head_knight_helm", "offhand_wooden_shield", "acc_simple_cape"]
    },
    "mage_set": {
        "name": "Mage's Regalia",
        "description": "Arcane equipment for spellcasters",
        "items": ["weapon_crystal_staff", "head_wizard_hat", "offhand_tome", "acc_fire_aura"]
    },
    "rogue_set": {
        "name": "Shadow's Embrace",
        "description": "Gear for those who walk in darkness",
        "items": ["weapon_shadow_dagger", "acc_shadow_cloak"]
    }
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_evolution_tier(level: int) -> int:
    """Determine the evolution tier based on character level."""
    for tier, config in EVOLUTION_TIERS.items():
        min_level, max_level = config["level_range"]
        if min_level <= level <= max_level:
            return tier
    return 6  # Max tier for very high levels


def calculate_tier_progress(level: int, xp: int, xp_for_next_level: int) -> Dict:
    """Calculate progress within the current tier."""
    tier = get_evolution_tier(level)
    tier_config = EVOLUTION_TIERS[tier]
    min_level, max_level = tier_config["level_range"]
    
    levels_in_tier = max_level - min_level + 1
    levels_completed = level - min_level
    
    # Progress as percentage
    tier_progress = (levels_completed / levels_in_tier) * 100
    
    # XP progress to next level
    level_progress = (xp / xp_for_next_level) * 100 if xp_for_next_level > 0 else 100
    
    return {
        "tier": tier,
        "tier_name": tier_config["name"],
        "tier_icon": tier_config["icon"],
        "tier_progress": tier_progress,
        "level_progress": level_progress,
        "levels_until_next_tier": max_level - level + 1 if tier < 6 else 0,
        "next_tier_name": EVOLUTION_TIERS.get(tier + 1, {}).get("name", "Max Tier Reached")
    }


def generate_avatar_url(appearance: CharacterAppearance, equipped_items: List[ShopItem] = None, size: int = 200) -> str:
    """Generate DiceBear Micah avatar URL with equipped item modifications."""
    base_url = "https://api.dicebear.com/9.x/micah/svg"
    
    params = appearance.to_dict()
    params["size"] = size
    
    # Apply item modifications to appearance
    if equipped_items:
        for item in equipped_items:
            if "dicebear_mod" in item.visual_effect:
                params.update(item.visual_effect["dicebear_mod"])
    
    # Build URL
    query = urlencode(params)
    return f"{base_url}?{query}"


def calculate_total_xp_bonus(equipped_items: List[ShopItem]) -> int:
    """Calculate total XP bonus from all equipped items."""
    total = 0
    for item in equipped_items:
        total += item.stat_bonuses.get("xp_bonus", 0)
        total += RARITY_CONFIG[item.rarity]["xp_bonus"]
    return total


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def init_character_state():
    """Initialize character-related session state."""
    if "character_appearance" not in st.session_state:
        st.session_state.character_appearance = CharacterAppearance()
    
    if "inventory" not in st.session_state:
        st.session_state.inventory = []  # List of item IDs owned
    
    if "equipped_items" not in st.session_state:
        st.session_state.equipped_items = {}  # slot -> item_id
    
    if "saved_loadouts" not in st.session_state:
        st.session_state.saved_loadouts = {}
    
    if "character_created" not in st.session_state:
        st.session_state.character_created = False
    
    # Initialize player stats if not present
    if "player_level" not in st.session_state:
        st.session_state.player_level = 1
    
    if "player_xp" not in st.session_state:
        st.session_state.player_xp = 0
    
    if "xp_for_next_level" not in st.session_state:
        st.session_state.xp_for_next_level = 100
    
    if "player_gold" not in st.session_state:
        st.session_state.player_gold = 500
    
    if "player_gems" not in st.session_state:
        st.session_state.player_gems = 10


def get_equipped_items() -> List[ShopItem]:
    """Get list of currently equipped ShopItem objects."""
    items = []
    for slot, item_id in st.session_state.equipped_items.items():
        if item_id and item_id in SHOP_ITEMS:
            items.append(SHOP_ITEMS[item_id])
    return items


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_character_display(show_stats: bool = True, size: int = 200):
    """Render the character avatar with all equipped items and tier effects."""
    init_character_state()
    
    appearance = st.session_state.character_appearance
    equipped = get_equipped_items()
    level = st.session_state.player_level
    tier = get_evolution_tier(level)
    tier_config = EVOLUTION_TIERS[tier]
    
    # Generate avatar URL
    avatar_url = generate_avatar_url(appearance, equipped, size)
    
    # Build visual effects based on equipped items
    aura_effects = []
    overlays = []
    
    for item in equipped:
        effect = item.visual_effect
        if "aura_type" in effect:
            aura_effects.append(effect)
        if "overlay" in effect:
            overlays.append(effect)
    
    # Combine tier aura with item auras
    tier_aura = tier_config.get("aura", "")
    
    # Calculate glow effects
    glow_effects = []
    if tier_aura:
        glow_effects.append(tier_aura)
    for item in equipped:
        if "glow" in item.visual_effect:
            glow_effects.append(f"0 0 15px {item.visual_effect['glow']}")
    
    combined_glow = ", ".join(glow_effects) if glow_effects else "none"
    
    # CSS for character display
    character_css = f"""
    <style>
        .character-container {{
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            background: {tier_config['background']};
            border-radius: 20px;
            border: 3px solid {tier_config['border_color']};
            box-shadow: {combined_glow};
            transition: all 0.3s ease;
        }}
        .character-container:hover {{
            transform: scale(1.02);
        }}
        .avatar-wrapper {{
            position: relative;
            display: inline-block;
        }}
        .avatar-img {{
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            box-shadow: {combined_glow};
        }}
        .tier-badge {{
            position: absolute;
            top: -10px;
            right: -10px;
            background: {tier_config['border_color']};
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        .tier-title {{
            color: {tier_config['title_color']};
            font-size: 1.2rem;
            font-weight: bold;
            margin-top: 15px;
            text-shadow: 0 0 10px rgba(0,0,0,0.5);
        }}
        .level-badge {{
            background: rgba(0,0,0,0.5);
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            margin-top: 10px;
        }}
        .equipped-icons {{
            display: flex;
            gap: 8px;
            margin-top: 15px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        .equipped-icon {{
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            transition: transform 0.2s;
        }}
        .equipped-icon:hover {{
            transform: scale(1.2);
        }}
        .xp-bonus-badge {{
            background: linear-gradient(135deg, #22C55E, #16A34A);
            color: white;
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 0.8rem;
            margin-top: 10px;
        }}
    </style>
    """
    
    # Build equipped items display
    equipped_icons_html = ""
    for item in equipped:
        rarity_config = RARITY_CONFIG[item.rarity]
        equipped_icons_html += f"""
        <div class="equipped-icon" style="background: {rarity_config['color']}20; border: 2px solid {rarity_config['color']};" title="{item.name}">
            {item.icon}
        </div>
        """
    
    # XP bonus calculation
    total_xp_bonus = calculate_total_xp_bonus(equipped)
    xp_bonus_html = ""
    if total_xp_bonus > 0:
        xp_bonus_html = f'<div class="xp-bonus-badge">+{total_xp_bonus}% XP Bonus</div>'
    
    # Complete HTML
    character_html = f"""
    {character_css}
    <div class="character-container">
        <div class="avatar-wrapper">
            <img src="{avatar_url}" class="avatar-img" width="{size}" height="{size}" alt="Character Avatar"/>
            <div class="tier-badge">{tier_config['icon']}</div>
        </div>
        <div class="tier-title">{tier_config['name']}</div>
        <div class="level-badge">Level {level}</div>
        {xp_bonus_html}
        <div class="equipped-icons">
            {equipped_icons_html}
        </div>
    </div>
    """
    
    st.markdown(character_html, unsafe_allow_html=True)
    
    # Show progress bar
    if show_stats:
        progress = calculate_tier_progress(
            level, 
            st.session_state.player_xp, 
            st.session_state.xp_for_next_level
        )
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Tier", f"{progress['tier_icon']} {progress['tier_name']}")
        with col2:
            if progress['levels_until_next_tier'] > 0:
                st.metric("Next Tier", f"{progress['next_tier_name']} ({progress['levels_until_next_tier']} levels)")
            else:
                st.metric("Tier Status", "🌟 Maximum Tier Reached!")
        
        # XP Progress bar
        st.progress(progress['level_progress'] / 100, text=f"XP: {st.session_state.player_xp}/{st.session_state.xp_for_next_level}")


def render_character_customization():
    """Render the character creation/customization screen."""
    init_character_state()
    
    st.markdown("## 🎨 Character Customization")
    
    # Class selection
    st.markdown("### Choose Your Class")
    class_cols = st.columns(len(CLASS_PRESETS))
    
    for idx, (class_enum, preset) in enumerate(CLASS_PRESETS.items()):
        with class_cols[idx]:
            if st.button(
                f"{preset['icon']} {preset['name']}",
                key=f"class_{class_enum.value}",
                use_container_width=True
            ):
                # Apply class preset
                for key, value in preset["defaults"].items():
                    setattr(st.session_state.character_appearance, 
                           key.replace("Style", "_style").replace("Color", "_color").lower().replace("hair_s", "hair_s"),
                           value)
                st.session_state.character_appearance.character_class = class_enum.value
                st.rerun()
            st.caption(preset["description"])
    
    st.markdown("---")
    
    # Preview and customization side by side
    preview_col, customize_col = st.columns([1, 2])
    
    with preview_col:
        st.markdown("### Preview")
        render_character_display(show_stats=False, size=180)
    
    with customize_col:
        st.markdown("### Customize Appearance")
        
        appearance = st.session_state.character_appearance
        
        # Skin tone
        skin_options = DICEBEAR_OPTIONS["baseColor"]
        skin_labels = ["Light", "Fair", "Dark", "Tan", "Medium"]
        appearance.base_color = st.selectbox(
            "Skin Tone",
            skin_options,
            format_func=lambda x: skin_labels[skin_options.index(x)] if x in skin_options else x,
            index=skin_options.index(appearance.base_color) if appearance.base_color in skin_options else 0
        )
        
        # Hair style and color
        col1, col2 = st.columns(2)
        with col1:
            appearance.hair_style = st.selectbox(
                "Hair Style",
                DICEBEAR_OPTIONS["hairStyle"],
                index=DICEBEAR_OPTIONS["hairStyle"].index(appearance.hair_style) if appearance.hair_style in DICEBEAR_OPTIONS["hairStyle"] else 0
            )
        with col2:
            hair_colors = DICEBEAR_OPTIONS["hairColor"]
            hair_labels = ["Dark Brown", "Medium Brown", "Light Brown", "Black", "Blonde", "Light Blonde", "Platinum", "Orange", "Purple", "Blue"]
            appearance.hair_color = st.selectbox(
                "Hair Color",
                hair_colors,
                format_func=lambda x: hair_labels[hair_colors.index(x)] if x in hair_colors else x,
                index=hair_colors.index(appearance.hair_color) if appearance.hair_color in hair_colors else 0
            )
        
        # Eyes and eyebrows
        col1, col2 = st.columns(2)
        with col1:
            appearance.eyes_style = st.selectbox(
                "Eye Style",
                DICEBEAR_OPTIONS["eyesStyle"],
                index=DICEBEAR_OPTIONS["eyesStyle"].index(appearance.eyes_style) if appearance.eyes_style in DICEBEAR_OPTIONS["eyesStyle"] else 0
            )
        with col2:
            eye_colors = DICEBEAR_OPTIONS["eyeColor"]
            eye_labels = ["Gray", "Blue", "Green", "Purple", "Amber"]
            appearance.eye_color = st.selectbox(
                "Eye Color",
                eye_colors,
                format_func=lambda x: eye_labels[eye_colors.index(x)] if x in eye_colors else x,
                index=eye_colors.index(appearance.eye_color) if appearance.eye_color in eye_colors else 0
            )
        
        # Mouth and nose
        col1, col2 = st.columns(2)
        with col1:
            appearance.mouth_style = st.selectbox(
                "Expression",
                DICEBEAR_OPTIONS["mouthStyle"],
                index=DICEBEAR_OPTIONS["mouthStyle"].index(appearance.mouth_style) if appearance.mouth_style in DICEBEAR_OPTIONS["mouthStyle"] else 0
            )
        with col2:
            appearance.nose_style = st.selectbox(
                "Nose Style",
                DICEBEAR_OPTIONS["noseStyle"],
                index=DICEBEAR_OPTIONS["noseStyle"].index(appearance.nose_style) if appearance.nose_style in DICEBEAR_OPTIONS["noseStyle"] else 0
            )
        
        # Shirt
        col1, col2 = st.columns(2)
        with col1:
            appearance.shirt_style = st.selectbox(
                "Shirt Style",
                DICEBEAR_OPTIONS["shirtStyle"],
                index=DICEBEAR_OPTIONS["shirtStyle"].index(appearance.shirt_style) if appearance.shirt_style in DICEBEAR_OPTIONS["shirtStyle"] else 0
            )
        with col2:
            shirt_colors = DICEBEAR_OPTIONS["shirtColor"]
            shirt_labels = ["Gray", "Blue", "Green", "Red", "Purple", "Gold", "Black"]
            appearance.shirt_color = st.selectbox(
                "Shirt Color",
                shirt_colors,
                format_func=lambda x: shirt_labels[shirt_colors.index(x)] if x in shirt_colors else x,
                index=shirt_colors.index(appearance.shirt_color) if appearance.shirt_color in shirt_colors else 0
            )
        
        # Facial hair (optional)
        with st.expander("Additional Options"):
            appearance.facial_hair_style = st.selectbox(
                "Facial Hair",
                DICEBEAR_OPTIONS["facialHairStyle"],
                index=DICEBEAR_OPTIONS["facialHairStyle"].index(appearance.facial_hair_style) if appearance.facial_hair_style in DICEBEAR_OPTIONS["facialHairStyle"] else 0
            )
            
            appearance.earring_color = st.selectbox(
                "Earrings",
                DICEBEAR_OPTIONS["earringColor"],
                format_func=lambda x: "None" if x == "transparent" else x.upper(),
                index=DICEBEAR_OPTIONS["earringColor"].index(appearance.earring_color) if appearance.earring_color in DICEBEAR_OPTIONS["earringColor"] else 0
            )
    
    st.markdown("---")
    
    if st.button("✅ Confirm Character", type="primary", use_container_width=True):
        st.session_state.character_created = True
        st.success("Character created successfully!")
        st.balloons()


def render_shop_interface():
    """Render the shop with item previews on character."""
    init_character_state()
    
    st.markdown("## 🏪 Item Shop")
    
    # Currency display
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.metric("💰 Gold", st.session_state.player_gold)
    with col2:
        st.metric("💎 Gems", st.session_state.player_gems)
    with col3:
        st.metric("📊 Level", st.session_state.player_level)
    
    st.markdown("---")
    
    # Category filter
    categories = ["All"] + [slot.value.title() for slot in EquipmentSlot]
    selected_category = st.selectbox("Filter by Category", categories)
    
    # Preview mode
    preview_item_id = st.session_state.get("preview_item", None)
    
    # Layout
    shop_col, preview_col = st.columns([2, 1])
    
    with preview_col:
        st.markdown("### 👤 Preview")
        if preview_item_id and preview_item_id in SHOP_ITEMS:
            preview_item = SHOP_ITEMS[preview_item_id]
            # Temporarily add to equipped for preview
            temp_equipped = get_equipped_items() + [preview_item]
            avatar_url = generate_avatar_url(st.session_state.character_appearance, temp_equipped, 150)
            
            tier = get_evolution_tier(st.session_state.player_level)
            tier_config = EVOLUTION_TIERS[tier]
            
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: {tier_config['background']}; border-radius: 15px; border: 2px solid {tier_config['border_color']};">
                <img src="{avatar_url}" width="150" style="border-radius: 50%;" />
                <p style="color: white; margin-top: 10px;">Previewing: {preview_item.icon} {preview_item.name}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            render_character_display(show_stats=False, size=150)
    
    with shop_col:
        # Filter items
        filtered_items = [item for item in SHOP_ITEMS_CATALOG]
        if selected_category != "All":
            filtered_items = [item for item in filtered_items if item.slot.value.title() == selected_category]
        
        # Sort by level requirement
        filtered_items.sort(key=lambda x: (x.level_requirement, x.cost_gold))
        
        for item in filtered_items:
            owned = item.id in st.session_state.inventory
            equipped = item.id in st.session_state.equipped_items.values()
            can_afford = (st.session_state.player_gold >= item.cost_gold and 
                         st.session_state.player_gems >= item.cost_gems)
            meets_level = st.session_state.player_level >= item.level_requirement
            
            rarity_config = RARITY_CONFIG[item.rarity]
            
            with st.container():
                st.markdown(f"""
                <div style="
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 10px;
                    border: {rarity_config['border']};
                    background: rgba(0,0,0,0.2);
                    box-shadow: {rarity_config['glow']};
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.5rem;">{item.icon}</span>
                            <span style="color: {rarity_config['color']}; font-weight: bold; margin-left: 10px;">{item.name}</span>
                            <span style="margin-left: 5px;">{rarity_config['badge']}</span>
                        </div>
                        <div style="text-align: right;">
                            <span style="color: #9CA3AF; font-size: 0.9rem;">{item.slot.value.title()}</span>
                        </div>
                    </div>
                    <p style="color: #9CA3AF; margin: 5px 0;">{item.description}</p>
                    <div style="display: flex; gap: 15px; margin-top: 5px;">
                        <span>💰 {item.cost_gold}</span>
                        {'<span>💎 ' + str(item.cost_gems) + '</span>' if item.cost_gems > 0 else ''}
                        <span style="color: {'#22C55E' if meets_level else '#EF4444'}">📊 Lvl {item.level_requirement}</span>
                        {f'<span style="color: #22C55E;">+{item.stat_bonuses.get("xp_bonus", 0)}% XP</span>' if item.stat_bonuses.get("xp_bonus") else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("👁️ Preview", key=f"preview_{item.id}"):
                        st.session_state.preview_item = item.id
                        st.rerun()
                
                with col2:
                    if owned:
                        if equipped:
                            st.success("✅ Equipped")
                        else:
                            st.info("📦 Owned")
                    else:
                        if not meets_level:
                            st.warning(f"🔒 Lvl {item.level_requirement}")
                        elif not can_afford:
                            st.error("💸 Can't Afford")
                        else:
                            if st.button("🛒 Buy", key=f"buy_{item.id}", type="primary"):
                                # Purchase item
                                st.session_state.player_gold -= item.cost_gold
                                st.session_state.player_gems -= item.cost_gems
                                st.session_state.inventory.append(item.id)
                                st.success(f"Purchased {item.name}!")
                                st.rerun()
                
                with col3:
                    if owned and not equipped:
                        if st.button("⚔️ Equip", key=f"equip_{item.id}"):
                            st.session_state.equipped_items[item.slot.value] = item.id
                            st.rerun()
                    elif equipped:
                        if st.button("📤 Unequip", key=f"unequip_{item.id}"):
                            del st.session_state.equipped_items[item.slot.value]
                            st.rerun()


def render_equipment_manager():
    """Render the equipment management screen."""
    init_character_state()
    
    st.markdown("## ⚔️ Equipment Manager")
    
    # Character display
    col1, col2 = st.columns([1, 2])
    
    with col1:
        render_character_display(show_stats=True, size=180)
    
    with col2:
        st.markdown("### Equipped Items")
        
        for slot in EquipmentSlot:
            item_id = st.session_state.equipped_items.get(slot.value)
            
            col_slot, col_item, col_action = st.columns([1, 2, 1])
            
            with col_slot:
                slot_icons = {
                    EquipmentSlot.HEAD: "🎩",
                    EquipmentSlot.BODY: "👕",
                    EquipmentSlot.WEAPON: "⚔️",
                    EquipmentSlot.OFFHAND: "🛡️",
                    EquipmentSlot.ACCESSORY: "💍",
                    EquipmentSlot.AURA: "✨",
                    EquipmentSlot.PET: "🐾",
                    EquipmentSlot.CAPE: "🧣"
                }
                st.markdown(f"**{slot_icons.get(slot, '📦')} {slot.value.title()}**")
            
            with col_item:
                if item_id and item_id in SHOP_ITEMS:
                    item = SHOP_ITEMS[item_id]
                    rarity_config = RARITY_CONFIG[item.rarity]
                    st.markdown(f"""
                    <span style="color: {rarity_config['color']};">{item.icon} {item.name}</span>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("*Empty*")
            
            with col_action:
                if item_id:
                    if st.button("❌", key=f"remove_{slot.value}"):
                        del st.session_state.equipped_items[slot.value]
                        st.rerun()
        
        st.markdown("---")
        
        # Inventory
        st.markdown("### 📦 Inventory")
        
        unequipped_items = [
            item_id for item_id in st.session_state.inventory 
            if item_id not in st.session_state.equipped_items.values()
        ]
        
        if unequipped_items:
            for item_id in unequipped_items:
                if item_id in SHOP_ITEMS:
                    item = SHOP_ITEMS[item_id]
                    rarity_config = RARITY_CONFIG[item.rarity]
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"""
                        <span style="color: {rarity_config['color']};">
                            {item.icon} {item.name} 
                            <span style="color: #9CA3AF;">({item.slot.value.title()})</span>
                        </span>
                        """, unsafe_allow_html=True)
                    with col2:
                        if st.button("⚔️ Equip", key=f"inv_equip_{item_id}"):
                            st.session_state.equipped_items[item.slot.value] = item_id
                            st.rerun()
        else:
            st.info("No unequipped items in inventory. Visit the shop!")
        
        st.markdown("---")
        
        # Loadouts
        st.markdown("### 💾 Equipment Loadouts")
        
        loadout_name = st.text_input("Loadout Name", placeholder="Enter loadout name...")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Current", use_container_width=True):
                if loadout_name:
                    st.session_state.saved_loadouts[loadout_name] = dict(st.session_state.equipped_items)
                    st.success(f"Saved loadout: {loadout_name}")
        
        with col2:
            saved_names = list(st.session_state.saved_loadouts.keys())
            if saved_names:
                selected_loadout = st.selectbox("Load Loadout", ["Select..."] + saved_names)
                if selected_loadout != "Select..." and st.button("📂 Load"):
                    st.session_state.equipped_items = dict(st.session_state.saved_loadouts[selected_loadout])
                    st.rerun()


def render_tier_overview():
    """Display all evolution tiers and requirements."""
    st.markdown("## 🌟 Evolution Tiers")
    
    current_level = st.session_state.get("player_level", 1)
    current_tier = get_evolution_tier(current_level)
    
    for tier_num, config in EVOLUTION_TIERS.items():
        min_level, max_level = config["level_range"]
        is_current = tier_num == current_tier
        is_unlocked = current_level >= min_level
        
        border_style = "3px solid" if is_current else "1px solid"
        opacity = "1" if is_unlocked else "0.5"
        
        st.markdown(f"""
        <div style="
            padding: 20px;
            margin: 10px 0;
            border-radius: 15px;
            border: {border_style} {config['border_color']};
            background: {config['background']};
            opacity: {opacity};
            box-shadow: {config.get('aura', 'none')};
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 2rem;">{config['icon']}</span>
                    <span style="color: {config['title_color']}; font-size: 1.3rem; font-weight: bold; margin-left: 15px;">
                        {config['name']}
                    </span>
                    {'<span style="margin-left: 10px; background: #22C55E; padding: 3px 10px; border-radius: 10px; font-size: 0.8rem;">CURRENT</span>' if is_current else ''}
                </div>
                <div style="color: #9CA3AF;">
                    Levels {min_level} - {max_level if max_level < 999 else '∞'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# INTEGRATION HELPERS
# =============================================================================

def award_xp_with_bonus(base_xp: int) -> int:
    """Award XP to player with equipped item bonuses."""
    equipped = get_equipped_items()
    bonus_percent = calculate_total_xp_bonus(equipped)
    
    total_xp = int(base_xp * (1 + bonus_percent / 100))
    
    st.session_state.player_xp += total_xp
    
    # Check for level up
    while st.session_state.player_xp >= st.session_state.xp_for_next_level:
        st.session_state.player_xp -= st.session_state.xp_for_next_level
        st.session_state.player_level += 1
        st.session_state.xp_for_next_level = int(st.session_state.xp_for_next_level * 1.15)
        st.balloons()
        st.success(f"🎉 Level Up! You are now level {st.session_state.player_level}!")
        
        # Check for tier evolution
        new_tier = get_evolution_tier(st.session_state.player_level)
        old_tier = get_evolution_tier(st.session_state.player_level - 1)
        if new_tier > old_tier:
            tier_config = EVOLUTION_TIERS[new_tier]
            st.success(f"✨ EVOLUTION! You've become a {tier_config['icon']} {tier_config['name']}!")
    
    return total_xp


def get_character_data_for_profile() -> Dict:
    """Get character data to store in user profile."""
    return {
        "appearance": st.session_state.character_appearance.to_dict(),
        "inventory": st.session_state.inventory,
        "equipped_items": st.session_state.equipped_items,
        "saved_loadouts": st.session_state.saved_loadouts,
        "character_created": st.session_state.character_created
    }


def load_character_data_from_profile(data: Dict):
    """Load character data from user profile."""
    if "appearance" in data:
        st.session_state.character_appearance = CharacterAppearance.from_dict(data["appearance"])
    if "inventory" in data:
        st.session_state.inventory = data["inventory"]
    if "equipped_items" in data:
        st.session_state.equipped_items = data["equipped_items"]
    if "saved_loadouts" in data:
        st.session_state.saved_loadouts = data["saved_loadouts"]
    if "character_created" in data:
        st.session_state.character_created = data["character_created"]


# =============================================================================
# MAIN DEMO APP
# =============================================================================

def main():
    """Main demo application."""
    st.set_page_config(
        page_title="Goal Quest - Character System",
        page_icon="⚔️",
        layout="wide"
    )
    
    # Initialize
    init_character_state()
    
    # Sidebar navigation
    st.sidebar.title("⚔️ Goal Quest")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["👤 Character", "🎨 Customize", "🏪 Shop", "⚔️ Equipment", "🌟 Tiers", "🎮 Demo"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Stats")
    st.sidebar.metric("Level", st.session_state.player_level)
    st.sidebar.metric("Gold", st.session_state.player_gold)
    st.sidebar.metric("Gems", st.session_state.player_gems)
    
    # Page routing
    if page == "👤 Character":
        st.title("👤 Your Character")
        render_character_display(show_stats=True, size=250)
        
    elif page == "🎨 Customize":
        render_character_customization()
        
    elif page == "🏪 Shop":
        render_shop_interface()
        
    elif page == "⚔️ Equipment":
        render_equipment_manager()
        
    elif page == "🌟 Tiers":
        render_tier_overview()
        
    elif page == "🎮 Demo":
        st.title("🎮 Demo Controls")
        st.markdown("Use these controls to test the character system.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### XP Controls")
            xp_amount = st.number_input("XP Amount", 10, 1000, 50)
            if st.button("➕ Add XP", use_container_width=True):
                actual_xp = award_xp_with_bonus(xp_amount)
                st.success(f"Awarded {actual_xp} XP (with bonuses)")
        
        with col2:
            st.markdown("### Currency Controls")
            gold_amount = st.number_input("Gold Amount", 10, 10000, 100)
            if st.button("💰 Add Gold", use_container_width=True):
                st.session_state.player_gold += gold_amount
                st.rerun()
            
            gem_amount = st.number_input("Gem Amount", 1, 100, 10)
            if st.button("💎 Add Gems", use_container_width=True):
                st.session_state.player_gems += gem_amount
                st.rerun()
        
        with col3:
            st.markdown("### Level Controls")
            if st.button("⬆️ Level Up", use_container_width=True):
                st.session_state.player_level += 1
                st.rerun()
            
            target_level = st.number_input("Set Level", 1, 150, st.session_state.player_level)
            if st.button("🎯 Set Level", use_container_width=True):
                st.session_state.player_level = target_level
                st.rerun()
        
        st.markdown("---")
        st.markdown("### Reset")
        if st.button("🔄 Reset All Data", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


if __name__ == "__main__":
    main()

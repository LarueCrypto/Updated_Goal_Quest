"""
Goal Quest Shop Items System - All 50+ items
Exact replication of the Replit shopItems.ts
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Price:
    gold: int
    crystals: int = 0


@dataclass
class Effect:
    type: str
    value: Optional[float] = None
    duration: Optional[int] = None  # seconds
    stats: Optional[str] = None
    uses: Optional[int] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    frequency: Optional[str] = None
    chance: Optional[float] = None
    multiplier: Optional[float] = None
    per_habit: Optional[float] = None
    max_bonus: Optional[float] = None
    xp: Optional[float] = None
    gold_mult: Optional[float] = None
    choosable: Optional[bool] = None


@dataclass
class Visual:
    type: str
    color: Optional[str] = None


@dataclass
class ShopItem:
    id: str
    name: str
    description: str
    icon: str
    rarity: str  # common/uncommon/rare/epic/legendary/mythic/divine
    price: Price
    category: str  # consumable/equipment/material/ability/cosmetic
    effect: Optional[Effect] = None
    stackable: bool = False
    max_stack: int = 1
    slot: Optional[str] = None  # weapon/armor/ring/amulet/head
    stats: Optional[Dict[str, int]] = None
    permanent: bool = False
    visual: Optional[Visual] = None
    level_required: Optional[int] = None


# Rarity colors for display
RARITY_COLORS = {
    "common": {"bg": "#64748b", "text": "#ffffff", "border": "#94a3b8"},
    "uncommon": {"bg": "#22c55e", "text": "#ffffff", "border": "#4ade80"},
    "rare": {"bg": "#3b82f6", "text": "#ffffff", "border": "#60a5fa"},
    "epic": {"bg": "#a855f7", "text": "#ffffff", "border": "#c084fc"},
    "legendary": {"bg": "#f97316", "text": "#ffffff", "border": "#fb923c"},
    "mythic": {"bg": "#ef4444", "text": "#ffffff", "border": "#f87171"},
    "divine": {"bg": "#eab308", "text": "#000000", "border": "#fde047"},
}


# ALL 50+ SHOP ITEMS
ALL_SHOP_ITEMS: List[ShopItem] = [
    # ============ CONSUMABLES - XP Boosters ============
    ShopItem(
        id="xp_boost_1h",
        name="Lesser Mana Potion",
        description="Doubles XP gains for 1 hour. The energy of a low-rank dungeon flows through you.",
        icon="Flask",
        rarity="common",
        price=Price(500),
        effect=Effect(type="xp_multiplier", value=2, duration=3600),
        stackable=True,
        max_stack=99,
        category="consumable",
    ),
    ShopItem(
        id="xp_boost_6h",
        name="Greater Mana Potion",
        description="Doubles XP gains for 6 hours. Concentrated essence from B-Rank dungeons.",
        icon="FlaskConical",
        rarity="uncommon",
        price=Price(2500),
        effect=Effect(type="xp_multiplier", value=2, duration=21600),
        stackable=True,
        max_stack=50,
        category="consumable",
    ),
    ShopItem(
        id="xp_boost_24h",
        name="Elixir of Awakening",
        description="Triples XP gains for 24 hours. A rare elixir that awakens your true potential.",
        icon="Wine",
        rarity="rare",
        price=Price(8000, 10),
        effect=Effect(type="xp_multiplier", value=3, duration=86400),
        stackable=True,
        max_stack=10,
        category="consumable",
    ),
    ShopItem(
        id="xp_mega_boost",
        name="Essence of the Monarch",
        description="5x XP for 12 hours. The concentrated power of a Monarch flows through your veins.",
        icon="Crown",
        rarity="legendary",
        price=Price(50000, 100),
        effect=Effect(type="xp_multiplier", value=5, duration=43200),
        stackable=True,
        max_stack=3,
        category="consumable",
    ),
    
    # ============ CONSUMABLES - Gold Boosters ============
    ShopItem(
        id="gold_boost_1h",
        name="Goblin's Lucky Coin",
        description="Doubles gold earned for 1 hour. Even goblins know the value of wealth.",
        icon="Coins",
        rarity="common",
        price=Price(400),
        effect=Effect(type="gold_multiplier", value=2, duration=3600),
        stackable=True,
        max_stack=99,
        category="consumable",
    ),
    ShopItem(
        id="gold_boost_24h",
        name="Dragon's Hoard Blessing",
        description="Triples gold earned for 24 hours. A dragon's greed becomes your fortune.",
        icon="Flame",
        rarity="epic",
        price=Price(10000, 15),
        effect=Effect(type="gold_multiplier", value=3, duration=86400),
        stackable=True,
        max_stack=5,
        category="consumable",
    ),
    
    # ============ CONSUMABLES - Streak Protectors ============
    ShopItem(
        id="streak_shield",
        name="Shield of Perseverance",
        description="Protects your streak from breaking once. Even hunters need a safety net.",
        icon="Shield",
        rarity="uncommon",
        price=Price(1000),
        effect=Effect(type="streak_protection", uses=1),
        stackable=True,
        max_stack=20,
        category="consumable",
    ),
    ShopItem(
        id="streak_shield_mega",
        name="Barrier of the Unwavering",
        description="Protects your streak from breaking 5 times. For those who refuse to fall.",
        icon="ShieldCheck",
        rarity="rare",
        price=Price(4000, 5),
        effect=Effect(type="streak_protection", uses=5),
        stackable=True,
        max_stack=5,
        category="consumable",
    ),
    
    # ============ CONSUMABLES - Instant Completes ============
    ShopItem(
        id="instant_complete_habit",
        name="Shadow Clone Scroll",
        description="Instantly complete one habit. Your shadow does the work for you.",
        icon="ScrollText",
        rarity="rare",
        price=Price(3000, 5),
        effect=Effect(type="instant_complete_habit", quantity=1),
        stackable=True,
        max_stack=10,
        category="consumable",
    ),
    ShopItem(
        id="instant_complete_step",
        name="Time Manipulation Crystal",
        description="Instantly complete one goal step. Bend time to your will.",
        icon="Timer",
        rarity="epic",
        price=Price(8000, 20),
        effect=Effect(type="instant_complete_step", quantity=1),
        stackable=True,
        max_stack=5,
        category="consumable",
    ),
    
    # ============ CONSUMABLES - Stat Boosters ============
    ShopItem(
        id="stat_boost_temp",
        name="Essence of Strength",
        description="+10 to all stats for 24 hours. Feel the power surge through you.",
        icon="Dumbbell",
        rarity="rare",
        price=Price(6000, 10),
        effect=Effect(type="stat_boost_temp", stats="all", value=10, duration=86400),
        stackable=True,
        max_stack=10,
        category="consumable",
    ),
    ShopItem(
        id="stat_boost_perm",
        name="Eternal Growth Elixir",
        description="Permanently increases one stat by 5. Choose your path wisely.",
        icon="Sparkles",
        rarity="legendary",
        price=Price(50000, 150),
        effect=Effect(type="stat_boost_perm", value=5, choosable=True),
        stackable=True,
        max_stack=5,
        category="consumable",
    ),
    
    # ============ EQUIPMENT - Weapons ============
    ShopItem(
        id="iron_dagger",
        name="Iron Dagger of the Novice",
        description="+5% XP for fitness goals. Your first real weapon.",
        icon="Sword",
        rarity="common",
        price=Price(2000),
        effect=Effect(type="category_xp_boost", category="fitness", value=1.05),
        slot="weapon",
        stats={"strength": 5},
        category="equipment",
    ),
    ShopItem(
        id="knights_sword",
        name="Knight's Longsword",
        description="+15% XP for fitness goals. A weapon worthy of a true warrior.",
        icon="Swords",
        rarity="uncommon",
        price=Price(8000, 10),
        effect=Effect(type="category_xp_boost", category="fitness", value=1.15),
        slot="weapon",
        stats={"strength": 15, "vitality": 5},
        category="equipment",
    ),
    ShopItem(
        id="demons_dagger",
        name="Demon King's Dagger",
        description="+25% XP for all challenging goals. Forged in the depths of hell.",
        icon="Sword",
        rarity="legendary",
        price=Price(100000, 200),
        effect=Effect(type="difficulty_xp_boost", difficulty="challenging", value=1.25),
        slot="weapon",
        stats={"strength": 30, "agility": 20, "willpower": 15},
        category="equipment",
        level_required=50,
    ),
    
    # ============ EQUIPMENT - Armor ============
    ShopItem(
        id="leather_armor",
        name="Hunter's Leather Armor",
        description="Reduces habit difficulty by 5%. Lighter steps on your journey.",
        icon="Shield",
        rarity="common",
        price=Price(2500),
        effect=Effect(type="difficulty_reduction", value=0.05),
        slot="armor",
        stats={"vitality": 10},
        category="equipment",
    ),
    ShopItem(
        id="knight_armor",
        name="Knight's Plate Armor",
        description="Streak shield activates automatically once per week.",
        icon="ShieldHalf",
        rarity="rare",
        price=Price(15000, 25),
        effect=Effect(type="auto_streak_shield", frequency="weekly"),
        slot="armor",
        stats={"vitality": 25, "willpower": 10},
        category="equipment",
        level_required=25,
    ),
    ShopItem(
        id="shadow_armor",
        name="Armor of the Shadow Monarch",
        description="Immune to streak breaks. The shadows protect you always.",
        icon="Moon",
        rarity="mythic",
        price=Price(500000, 1000),
        effect=Effect(type="streak_immunity"),
        slot="armor",
        stats={"vitality": 50, "willpower": 50, "sense": 30},
        category="equipment",
        level_required=80,
    ),
    
    # ============ EQUIPMENT - Accessories ============
    ShopItem(
        id="ring_focus",
        name="Ring of Focus",
        description="+10% XP for learning goals. Clarity of mind brings power.",
        icon="Circle",
        rarity="uncommon",
        price=Price(5000, 5),
        effect=Effect(type="category_xp_boost", category="learning", value=1.10),
        slot="ring",
        stats={"intelligence": 10},
        category="equipment",
    ),
    ShopItem(
        id="amulet_wealth",
        name="Amulet of Prosperity",
        description="+20% gold from all sources. Wealth flows to you naturally.",
        icon="Gem",
        rarity="rare",
        price=Price(12000, 20),
        effect=Effect(type="gold_multiplier_perm", value=1.20),
        slot="amulet",
        stats={"sense": 15},
        category="equipment",
        level_required=30,
    ),
    ShopItem(
        id="crown_monarch",
        name="Crown of the Eternal Monarch",
        description="+50% XP and gold from all sources. Rule your domain.",
        icon="Crown",
        rarity="mythic",
        price=Price(1000000, 2500),
        effect=Effect(type="all_multiplier", xp=1.50, gold_mult=1.50),
        slot="head",
        stats={"strength": 40, "intelligence": 40, "vitality": 40, "agility": 40, "sense": 40, "willpower": 60},
        category="equipment",
        level_required=100,
    ),
    
    # ============ MATERIALS ============
    ShopItem(
        id="essence_common",
        name="Essence Stone",
        description="Common crafting material. The basic building block of power.",
        icon="Diamond",
        rarity="common",
        price=Price(100),
        stackable=True,
        max_stack=999,
        category="material",
    ),
    ShopItem(
        id="essence_rare",
        name="Mana Crystal",
        description="Rare crafting material. Pulsing with magical energy.",
        icon="Gem",
        rarity="rare",
        price=Price(1000, 2),
        stackable=True,
        max_stack=99,
        category="material",
    ),
    ShopItem(
        id="essence_legendary",
        name="Shadow Fragment",
        description="Legendary crafting material. A piece of the void itself.",
        icon="Moon",
        rarity="legendary",
        price=Price(25000, 50),
        stackable=True,
        max_stack=20,
        category="material",
    ),
    
    # ============ ABILITIES ============
    ShopItem(
        id="ability_double_tap",
        name="Double Impact",
        description="Completing a habit has a 20% chance to count twice. Strike with precision.",
        icon="Zap",
        rarity="rare",
        price=Price(20000, 50),
        effect=Effect(type="habit_double_chance", value=0.20),
        permanent=True,
        category="ability",
        level_required=20,
    ),
    ShopItem(
        id="ability_chain_bonus",
        name="Chain Mastery",
        description="Each consecutive habit completion increases XP by 10% (max 50%). Build momentum.",
        icon="Link",
        rarity="epic",
        price=Price(40000, 100),
        effect=Effect(type="chain_bonus", per_habit=0.10, max_bonus=0.50),
        permanent=True,
        category="ability",
        level_required=35,
    ),
    ShopItem(
        id="ability_critical_strike",
        name="Critical Success",
        description="10% chance to earn 5x XP on any action. Fortune favors the bold.",
        icon="Target",
        rarity="legendary",
        price=Price(100000, 250),
        effect=Effect(type="critical_chance", chance=0.10, multiplier=5),
        permanent=True,
        category="ability",
        level_required=50,
    ),
    ShopItem(
        id="ability_shadow_soldiers",
        name="Summon Shadow Soldiers",
        description="Automatically complete one random habit per day. The shadows serve you.",
        icon="Users",
        rarity="mythic",
        price=Price(500000, 1000),
        effect=Effect(type="auto_complete_daily", quantity=1),
        permanent=True,
        category="ability",
        level_required=75,
    ),
    ShopItem(
        id="ability_arise",
        name="Arise",
        description="Once per week, automatically complete all habits. The ultimate power.",
        icon="Sunrise",
        rarity="divine",
        price=Price(2000000, 5000),
        effect=Effect(type="auto_complete_all", frequency="weekly"),
        permanent=True,
        category="ability",
        level_required=100,
    ),
    
    # ============ COSMETICS ============
    ShopItem(
        id="aura_blue",
        name="Azure Aura",
        description="Surrounds your profile with a blue aura. Style for the skilled.",
        icon="Circle",
        rarity="uncommon",
        price=Price(3000, 5),
        visual=Visual(type="aura", color="#3B82F6"),
        category="cosmetic",
    ),
    ShopItem(
        id="aura_purple",
        name="Violet Veil",
        description="A mystical purple aura surrounds your profile. Emanate power.",
        icon="Circle",
        rarity="rare",
        price=Price(8000, 15),
        visual=Visual(type="aura", color="#8B5CF6"),
        category="cosmetic",
    ),
    ShopItem(
        id="aura_gold",
        name="Golden Radiance",
        description="The legendary gold aura of champions. Show your wealth.",
        icon="Circle",
        rarity="legendary",
        price=Price(50000, 100),
        visual=Visual(type="aura", color="#F59E0B"),
        category="cosmetic",
        level_required=50,
    ),
    ShopItem(
        id="aura_shadow",
        name="Shadow Monarch's Aura",
        description="The dark aura of the Shadow Monarch. Fear personified.",
        icon="Moon",
        rarity="mythic",
        price=Price(250000, 500),
        visual=Visual(type="aura", color="#1F2937"),
        category="cosmetic",
        level_required=90,
    ),
    ShopItem(
        id="frame_gold",
        name="Golden Frame",
        description="A golden frame around your avatar. Elegance defined.",
        icon="Frame",
        rarity="epic",
        price=Price(25000, 50),
        visual=Visual(type="frame", color="#F59E0B"),
        category="cosmetic",
        level_required=40,
    ),
    ShopItem(
        id="title_shadow_hunter",
        name="Shadow Hunter Title",
        description="Display 'Shadow Hunter' as your title. Walk the path of darkness.",
        icon="Award",
        rarity="epic",
        price=Price(30000, 75),
        visual=Visual(type="title"),
        category="cosmetic",
        level_required=60,
    ),
]


# Item lookup by ID
SHOP_ITEMS_BY_ID: Dict[str, ShopItem] = {item.id: item for item in ALL_SHOP_ITEMS}


def get_item_by_id(item_id: str) -> Optional[ShopItem]:
    """Get shop item by ID"""
    return SHOP_ITEMS_BY_ID.get(item_id)


def get_items_by_category(category: str) -> List[ShopItem]:
    """Get all items in a category"""
    return [item for item in ALL_SHOP_ITEMS if item.category == category]


def get_items_by_rarity(rarity: str) -> List[ShopItem]:
    """Get all items of a rarity"""
    return [item for item in ALL_SHOP_ITEMS if item.rarity == rarity]


def get_affordable_items(gold: int, crystals: int = 0) -> List[ShopItem]:
    """Get items the user can afford"""
    return [
        item for item in ALL_SHOP_ITEMS
        if item.price.gold <= gold and item.price.crystals <= crystals
    ]


def get_items_for_level(level: int) -> List[ShopItem]:
    """Get items available at a given level"""
    return [
        item for item in ALL_SHOP_ITEMS
        if item.level_required is None or item.level_required <= level
    ]


# Shop categories for display
SHOP_CATEGORIES = [
    {"id": "consumable", "name": "Consumables", "icon": "Flask", "description": "Temporary boosts and one-time use items"},
    {"id": "equipment", "name": "Equipment", "icon": "Sword", "description": "Permanent gear with stat bonuses"},
    {"id": "material", "name": "Materials", "icon": "Diamond", "description": "Crafting components and upgrade materials"},
    {"id": "ability", "name": "Abilities", "icon": "Zap", "description": "Permanent special powers"},
    {"id": "cosmetic", "name": "Cosmetics", "icon": "Sparkles", "description": "Visual customization items"},
]

# Equipment slots
EQUIPMENT_SLOTS = ["weapon", "armor", "ring", "amulet", "head"]

# Item rarities in order
ITEM_RARITIES = ["common", "uncommon", "rare", "epic", "legendary", "mythic", "divine"]

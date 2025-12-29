# Goal Quest - Character Evolution & Equipment System

## 📚 Documentation

### Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Integration Guide](#integration-guide)
4. [Component Reference](#component-reference)
5. [Customization Guide](#customization-guide)
6. [Adding New Items](#adding-new-items)
7. [Modifying Evolution Tiers](#modifying-evolution-tiers)
8. [DiceBear Parameters](#dicebear-parameters)
9. [API Reference](#api-reference)

---

## Overview

The Character Evolution & Equipment System provides a comprehensive character management solution for Goal Quest, featuring:

- **DiceBear Micah Avatars**: Full character customization using the DiceBear API
- **Evolution Tiers**: Visual character progression based on level (6 tiers)
- **Shop Integration**: Purchase and equip items that appear on your character
- **Equipment System**: Manage equipped items with visual feedback
- **XP Bonus System**: Equipped items provide XP bonuses
- **Loadout System**: Save and load equipment configurations

---

## Installation

### Requirements
```
streamlit>=1.28.0
```

### Quick Start
```bash
# Clone or copy the character_system.py file to your project
# Run the demo
streamlit run character_system.py
```

### GitHub Deployment
1. Create a `requirements.txt` file:
```
streamlit>=1.28.0
```

2. Configure Streamlit Cloud:
   - Connect your GitHub repository
   - Set the main file path to your app entry point
   - Deploy!

---

## Integration Guide

### Basic Integration

```python
from character_system import (
    init_character_state,
    render_character_display,
    render_shop_interface,
    award_xp_with_bonus,
    get_character_data_for_profile,
    load_character_data_from_profile
)

# Initialize the character system
init_character_state()

# Render the character avatar
render_character_display(show_stats=True, size=200)

# Award XP (with equipment bonuses)
actual_xp = award_xp_with_bonus(50)  # Returns XP with bonuses applied
```

### Profile Integration

Save character data to your existing user profile:

```python
# When saving user profile
def save_user_profile(profile):
    character_data = get_character_data_for_profile()
    profile['character'] = character_data
    # Save profile to your storage...

# When loading user profile
def load_user_profile(profile):
    if 'character' in profile:
        load_character_data_from_profile(profile['character'])
```

### Connecting to Existing XP System

```python
from character_system import award_xp_with_bonus, get_evolution_tier

# When user completes a habit
def complete_habit(habit_xp):
    # This automatically applies equipment bonuses
    total_xp = award_xp_with_bonus(habit_xp)
    
    # Check for tier evolution
    new_tier = get_evolution_tier(st.session_state.player_level)
    
    return total_xp
```

---

## Component Reference

### UI Components

| Function | Description | Parameters |
|----------|-------------|------------|
| `render_character_display()` | Shows character avatar with effects | `show_stats: bool`, `size: int` |
| `render_character_customization()` | Character creation/edit screen | None |
| `render_shop_interface()` | Full shop with preview | None |
| `render_equipment_manager()` | Equipment slots & inventory | None |
| `render_tier_overview()` | Shows all evolution tiers | None |

### Helper Functions

| Function | Description | Returns |
|----------|-------------|---------|
| `get_evolution_tier(level)` | Get tier number for level | `int` (1-6) |
| `calculate_tier_progress(level, xp, xp_next)` | Get detailed progress info | `Dict` |
| `generate_avatar_url(appearance, equipped, size)` | Generate DiceBear URL | `str` |
| `calculate_total_xp_bonus(equipped_items)` | Sum all XP bonuses | `int` |
| `award_xp_with_bonus(base_xp)` | Award XP with bonuses | `int` |
| `get_equipped_items()` | Get list of equipped items | `List[ShopItem]` |

---

## Customization Guide

### Adding New Character Classes

```python
# In character_system.py, add to CLASS_PRESETS:

CharacterClass.NECROMANCER: {
    "name": "Necromancer",
    "icon": "💀",
    "description": "A dark mage who commands the undead",
    "defaults": {
        "hairStyle": "full",
        "hairColor": "1a1a1a",
        "eyesStyle": "eyesShadow",
        "mouthStyle": "smirk",
        "shirtStyle": "collared",
        "shirtColor": "1f2937"
    }
}
```

### Customizing Visual Effects

The visual effect system supports:

```python
visual_effect = {
    # DiceBear parameter modifications
    "dicebear_mod": {"hairStyle": "mrClean"},
    
    # Overlay images (for custom rendering)
    "overlay": "sword_iron",
    "position": "right_hand",
    
    # Glow effects
    "glow": "#3B82F6",
    
    # Aura effects
    "aura_type": "fire",
    "color": "#EF4444",
    "intensity": 0.6,
    
    # Special effects
    "particles": True,
    "animation": "flutter"
}
```

---

## Adding New Items

### Item Structure

```python
ShopItem(
    id="unique_item_id",           # Unique identifier
    name="Display Name",            # Shown in UI
    description="Item description", # Tooltip text
    cost_gold=100,                  # Gold cost
    cost_gems=0,                    # Gem cost
    rarity=Rarity.RARE,            # COMMON/UNCOMMON/RARE/EPIC/LEGENDARY
    slot=EquipmentSlot.WEAPON,     # Equipment slot
    level_requirement=10,           # Minimum level to purchase
    icon="⚔️",                      # Emoji icon
    visual_effect={...},           # Visual modifications
    stat_bonuses={"xp_bonus": 5}   # Stat bonuses
)
```

### Adding Items to Catalog

```python
# Add to SHOP_ITEMS_CATALOG list:

SHOP_ITEMS_CATALOG.append(
    ShopItem(
        id="weapon_mystic_bow",
        name="Mystic Longbow",
        description="A bow enchanted with moonlight",
        cost_gold=600,
        cost_gems=15,
        rarity=Rarity.EPIC,
        slot=EquipmentSlot.WEAPON,
        level_requirement=35,
        icon="🏹",
        visual_effect={
            "overlay": "bow_mystic",
            "position": "right_hand",
            "glow": "#A855F7"
        },
        stat_bonuses={"xp_bonus": 22}
    )
)

# Rebuild the lookup dictionary
SHOP_ITEMS = {item.id: item for item in SHOP_ITEMS_CATALOG}
```

### Equipment Slots

| Slot | Description | Example Items |
|------|-------------|---------------|
| `HEAD` | Helmets, hats, crowns | Wizard Hat, Knight Helm |
| `BODY` | Armor, robes | Plate Armor, Mage Robes |
| `WEAPON` | Main hand weapons | Swords, Staffs, Bows |
| `OFFHAND` | Secondary items | Shields, Tomes |
| `ACCESSORY` | Special items | Wings, Badges |
| `AURA` | Surrounding effects | Fire Aura, Lightning |
| `PET` | Companion creatures | Dragon, Phoenix |
| `CAPE` | Back items | Cloaks, Capes |

---

## Modifying Evolution Tiers

### Tier Configuration

```python
EVOLUTION_TIERS = {
    1: {
        "name": "Novice Adventurer",    # Display name
        "level_range": (1, 10),          # Min/max levels
        "icon": "🌱",                    # Tier icon
        "border_color": "#6B7280",       # Border color
        "background": "linear-gradient(...)",  # CSS gradient
        "aura": None,                    # Box shadow for glow
        "title_color": "#9CA3AF"         # Title text color
    },
    # ... more tiers
}
```

### Adding a New Tier

```python
# Add tier 7 for levels 151+
EVOLUTION_TIERS[7] = {
    "name": "Cosmic Entity",
    "level_range": (151, 9999),
    "icon": "🌌",
    "border_color": "#8B5CF6",
    "background": "linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%)",
    "aura": "0 0 50px rgba(139, 92, 246, 0.8), 0 0 100px rgba(79, 70, 229, 0.4)",
    "title_color": "#A78BFA"
}
```

---

## DiceBear Parameters

### Available Options

The Micah avatar style supports these customization options:

| Parameter | Options |
|-----------|---------|
| `baseColor` | Skin tones: `ac6651`, `f9c9b6`, `77311d`, `d2b48c`, `8d5524` |
| `hairStyle` | `dannyPhantom`, `dougFunny`, `fonze`, `full`, `mrClean`, `mrT`, `pixie`, `turpieFull`, `turban` |
| `hairColor` | Hex colors (without #) |
| `eyesStyle` | `eyes`, `round`, `smiling`, `eyesShadow` |
| `eyeColor` | Hex colors (without #) |
| `mouthStyle` | `laughing`, `nervous`, `pucker`, `sad`, `smile`, `smirk`, `surprised` |
| `noseStyle` | `curve`, `pointed`, `round` |
| `shirtStyle` | `collared`, `crew`, `open` |
| `shirtColor` | Hex colors (without #) |
| `facialHairStyle` | `beard`, `scruff`, `transparent` |
| `earringColor` | `transparent` or hex colors |
| `glassesStyle` | `round`, `square` |

### URL Generation

```python
from urllib.parse import urlencode

def generate_custom_avatar(options: dict, size: int = 200) -> str:
    base_url = "https://api.dicebear.com/9.x/micah/svg"
    params = {**options, "size": size}
    return f"{base_url}?{urlencode(params)}"
```

---

## API Reference

### Session State Variables

| Variable | Type | Description |
|----------|------|-------------|
| `character_appearance` | `CharacterAppearance` | Current appearance settings |
| `inventory` | `List[str]` | List of owned item IDs |
| `equipped_items` | `Dict[str, str]` | Slot -> item_id mapping |
| `saved_loadouts` | `Dict[str, Dict]` | Named loadout configurations |
| `character_created` | `bool` | Whether character was created |
| `player_level` | `int` | Current player level |
| `player_xp` | `int` | Current XP |
| `xp_for_next_level` | `int` | XP needed for next level |
| `player_gold` | `int` | Gold currency |
| `player_gems` | `int` | Premium currency |

### Data Classes

#### CharacterAppearance
```python
@dataclass
class CharacterAppearance:
    base_color: str        # Skin tone
    hair_style: str        # Hair style
    hair_color: str        # Hair color
    eyes_style: str        # Eye style
    eye_color: str         # Eye color
    eyebrow_style: str     # Eyebrow style
    mouth_style: str       # Mouth/expression
    nose_style: str        # Nose style
    facial_hair_style: str # Facial hair
    facial_hair_color: str # Facial hair color
    glasses_style: str     # Glasses (optional)
    glasses_color: str     # Glasses color
    earring_color: str     # Earring color
    shirt_style: str       # Shirt style
    shirt_color: str       # Shirt color
    character_class: str   # Class type
```

#### ShopItem
```python
@dataclass
class ShopItem:
    id: str                      # Unique identifier
    name: str                    # Display name
    description: str             # Description text
    cost_gold: int               # Gold cost
    cost_gems: int               # Gem cost
    rarity: Rarity               # Rarity tier
    slot: EquipmentSlot          # Equipment slot
    level_requirement: int       # Min level to buy
    icon: str                    # Emoji icon
    visual_effect: Dict          # Visual modifications
    stat_bonuses: Dict[str, int] # Stat bonuses
    is_equipped: bool            # Equipped status
```

---

## Examples

### Complete Integration Example

```python
import streamlit as st
from character_system import *

def main():
    st.set_page_config(page_title="Goal Quest", layout="wide")
    
    # Initialize character system
    init_character_state()
    
    # Sidebar with character
    with st.sidebar:
        render_character_display(show_stats=True, size=150)
        
        st.metric("Gold", st.session_state.player_gold)
        st.metric("Gems", st.session_state.player_gems)
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["Habits", "Shop", "Equipment"])
    
    with tab1:
        # Your habit tracking code
        if st.button("Complete Habit (+25 XP)"):
            xp = award_xp_with_bonus(25)
            st.success(f"Earned {xp} XP!")
    
    with tab2:
        render_shop_interface()
    
    with tab3:
        render_equipment_manager()

if __name__ == "__main__":
    main()
```

### Custom Item Preview

```python
def preview_item_on_character(item_id: str):
    """Show how an item would look on the character."""
    item = SHOP_ITEMS[item_id]
    current_equipped = get_equipped_items()
    preview_equipped = current_equipped + [item]
    
    avatar_url = generate_avatar_url(
        st.session_state.character_appearance,
        preview_equipped,
        200
    )
    
    st.image(avatar_url)
```

---

## Troubleshooting

### Common Issues

1. **Avatar not loading**: Check internet connection; DiceBear API requires online access
2. **Items not appearing**: Ensure item is in `SHOP_ITEMS` dictionary
3. **XP not updating**: Verify `init_character_state()` is called before any operations
4. **Tier not changing**: Check `EVOLUTION_TIERS` level ranges for gaps

### Debug Mode

```python
def debug_character_state():
    st.json({
        "level": st.session_state.player_level,
        "tier": get_evolution_tier(st.session_state.player_level),
        "inventory": st.session_state.inventory,
        "equipped": st.session_state.equipped_items,
        "appearance": st.session_state.character_appearance.to_dict()
    })
```

---

## License

This character system is part of the Goal Quest project. Feel free to modify and extend for your own gamification projects!

# ⚔️ Goal Quest - Gamified Habit & Goal Tracker

A complete gamified habit tracking and goal management application inspired by Solo Leveling. Transform your daily habits into epic quests and level up your real life!

![Goal Quest Banner](https://img.shields.io/badge/Goal%20Quest-Level%20Up%20Your%20Life-gold?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Im0xMiAyIDEuNyA1LjJoNS41bC00LjUgMy4zIDEuNyA1LjItNC40LTMuMi00LjQgMy4yIDEuNy01LjItNC41LTMuM2g1LjV6Ii8+PC9zdmc+)

## ✨ Features

### 🎮 Gamification System
- **XP & Leveling**: 5% compound XP growth with 100 levels
- **6 Core Stats**: Strength, Intelligence, Vitality, Agility, Sense, Willpower
- **Rank System**: Progress from Beginner to Shadow Monarch
- **200 Achievements**: Unlock rewards across 8 categories
- **Gold Currency**: Earn and spend gold in the Hunter's Shop

### 📋 Habit Tracking
- Create habits with multiple frequency options (daily, weekdays, specific days, custom)
- Difficulty levels: Easy (50 XP), Medium (100 XP), Hard (300 XP)
- Streak tracking with XP multiplier bonuses
- Category-based stat improvements
- Priority habits for daily focus

### 🎯 Goal Management
- Long-term goal setting with deadlines
- Step-by-step progress tracking
- AI-generated goal plans
- Difficulty tiers with XP rewards (1000/2000/3000)

### 🛒 Hunter's Shop
- **50+ Items** across 5 categories:
  - Consumables (XP/Gold boosters, streak shields)
  - Equipment (weapons, armor, accessories)
  - Materials (crafting components)
  - Abilities (permanent special powers)
  - Cosmetics (auras, frames, titles)
- Rarity system: Common → Divine

### 📊 Analytics
- Completion trend charts
- Stats radar visualization
- Habit performance tracking
- Weekly/monthly progress reports

### 📝 Notes System
- Categories: Personal, Work, Health, Goals, Ideas, Learning
- Color-coded notes
- Tag system
- Pin important notes
- AI-powered summaries

### 🤖 AI Coach
- Generate personalized habit suggestions
- Create full goal plans with actionable steps
- Philosophy-based daily wisdom quotes

### 📚 Philosophy Library
- Upload personal philosophy documents
- Multiple wisdom traditions:
  - Esoteric/Hermetic
  - Biblical
  - Quranic
  - Metaphysical
  - Ancient Philosophy
  - Stoic, Eastern, Kemetic, Samurai, Occult

## 🚀 Quick Start

### Deploy to Streamlit Cloud

1. Fork this repository
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Click "New app"
4. Select your forked repository
5. Set main file path: `app.py`
6. Click "Deploy"

### Run Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/goal-quest.git
cd goal-quest

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📁 Project Structure

```
goal-quest/
├── app.py                 # Main Streamlit application (11 pages)
├── database.py            # SQLAlchemy models (14 tables)
├── gameplay.py            # Game mechanics (XP, stats, ranks)
├── achievements.py        # 200 achievement definitions
├── shop_items.py          # 50+ shop items
├── components.py          # Reusable UI components
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
└── README.md
```

## 🎨 Theme

The app features a **Solo Leveling** inspired dark theme with:
- Deep blue/purple gradient background
- Gold (#fbbf24) accent colors
- Glowing effects and smooth animations
- Custom progress bars and stat displays

## 📱 Pages

| Page | Description |
|------|-------------|
| 🏠 Dashboard | XP bar, daily wisdom, priority quests, stats overview |
| ✅ Habits | Create, track, and complete daily habits |
| 🎯 Goals | Set and track long-term goals with steps |
| 📊 Analytics | Charts, trends, and performance metrics |
| 🏆 Rewards | 200 achievements with tier badges |
| 🛒 Shop | Buy items with gold and crystals |
| 📝 Notes | Personal journal with categories and AI summaries |
| 🤖 AI Coach | Generate habits and goal plans |
| 📚 Philosophy | Upload and manage wisdom documents |
| ⚙️ Settings | Profile, notifications, timezone, philosophy tradition |

## 🏆 Achievement Categories

- **Streaks** (25): Maintain consecutive days
- **Levels** (25): Reach level milestones
- **Habits** (40): Complete habits
- **Goals** (40): Achieve goals
- **Special** (30): Unique accomplishments
- **Stats** (30): Reach stat milestones
- **Legendary** (10): Ultimate achievements

## 💎 Item Rarities

| Rarity | Color | Description |
|--------|-------|-------------|
| Common | Gray | Basic items |
| Uncommon | Green | Useful enhancements |
| Rare | Blue | Significant boosts |
| Epic | Purple | Powerful effects |
| Legendary | Orange | Game-changing items |
| Mythic | Red | Extremely rare |
| Divine | Gold | Ultimate power |

## 🔧 Environment Variables (Optional)

For AI features, set these in Streamlit Cloud secrets:

```toml
OPENAI_API_KEY = "your-openai-api-key"
ANTHROPIC_API_KEY = "your-anthropic-api-key"
```

## 📄 License

MIT License - feel free to use, modify, and distribute!

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests.

## 📞 Support

If you encounter issues, please open a GitHub issue.

---

**⚔️ Arise, Hunter! Your journey awaits.**

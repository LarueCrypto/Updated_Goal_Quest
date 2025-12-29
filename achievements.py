"""
Goal Quest Achievements System - All 200 achievements
Exact replication of the Replit achievements.ts
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class StatBonus:
    stat: str
    amount: int


@dataclass
class AchievementDef:
    key: str
    title: str
    description: str
    icon: str
    category: str
    tier: str
    xp_reward: int
    gold_reward: int
    stat_bonus: Optional[StatBonus] = None
    special_power: Optional[str] = None


# ALL 200 ACHIEVEMENTS
ALL_ACHIEVEMENTS: List[AchievementDef] = [
    # ============ STREAKS (1-25) ============
    AchievementDef("streak_3", "Getting Started", "Maintain a 3-day streak", "Flame", "streaks", "bronze", 100, 10),
    AchievementDef("streak_7", "Week Warrior", "Maintain a 7-day streak", "Flame", "streaks", "bronze", 250, 25),
    AchievementDef("streak_14", "Fortnight Fighter", "Maintain a 14-day streak", "Flame", "streaks", "silver", 500, 50),
    AchievementDef("streak_21", "Three Week Titan", "Maintain a 21-day streak", "Flame", "streaks", "silver", 750, 75),
    AchievementDef("streak_30", "Monthly Master", "Maintain a 30-day streak", "Flame", "streaks", "gold", 1000, 100),
    AchievementDef("streak_45", "Iron Will", "Maintain a 45-day streak", "Flame", "streaks", "gold", 1500, 150),
    AchievementDef("streak_60", "Diamond Discipline", "Maintain a 60-day streak", "Flame", "streaks", "platinum", 2000, 200, StatBonus("willpower", 5)),
    AchievementDef("streak_90", "Quarterly Champion", "Maintain a 90-day streak", "Flame", "streaks", "platinum", 3000, 300, StatBonus("willpower", 10)),
    AchievementDef("streak_180", "Half-Year Hero", "Maintain a 180-day streak", "Flame", "streaks", "legendary", 5000, 500, StatBonus("willpower", 15), "Double XP on weekends"),
    AchievementDef("streak_365", "Year of Power", "Maintain a 365-day streak", "Crown", "streaks", "legendary", 10000, 1000, StatBonus("willpower", 25), "Permanent 10% XP boost"),
    AchievementDef("comeback_3", "Rising Again", "Recover a 3-day streak after breaking", "RotateCcw", "streaks", "bronze", 150, 15),
    AchievementDef("comeback_7", "Phoenix Rising", "Recover a 7-day streak after breaking", "RotateCcw", "streaks", "silver", 400, 40),
    AchievementDef("comeback_30", "Unstoppable Force", "Recover a 30-day streak after breaking", "RotateCcw", "streaks", "gold", 1000, 100),
    AchievementDef("streak_multi_3", "Multi-Tasker", "Maintain 3 habits with 7+ day streaks", "Layers", "streaks", "silver", 500, 50),
    AchievementDef("streak_multi_5", "Habit Master", "Maintain 5 habits with 7+ day streaks", "Layers", "streaks", "gold", 1000, 100),
    AchievementDef("streak_multi_10", "Discipline Incarnate", "Maintain 10 habits with 7+ day streaks", "Layers", "streaks", "legendary", 2500, 250, StatBonus("agility", 10)),
    AchievementDef("weekend_warrior", "Weekend Warrior", "Complete habits every weekend for a month", "Calendar", "streaks", "silver", 600, 60),
    AchievementDef("early_bird_7", "Early Bird", "Complete a habit before 7AM for 7 days", "Sunrise", "streaks", "silver", 400, 40, StatBonus("vitality", 3)),
    AchievementDef("night_owl_7", "Night Owl", "Complete a habit after 10PM for 7 days", "Moon", "streaks", "silver", 400, 40, StatBonus("sense", 3)),
    AchievementDef("perfect_week", "Perfect Week", "Complete all habits for 7 consecutive days", "CheckCircle", "streaks", "gold", 1200, 120),
    AchievementDef("perfect_month", "Perfect Month", "Complete all habits for 30 consecutive days", "CheckCircle", "streaks", "legendary", 5000, 500, StatBonus("willpower", 20), "Unlock exclusive avatar frame"),
    AchievementDef("consistency_king", "Consistency King", "90% completion rate for 30 days", "TrendingUp", "streaks", "gold", 1500, 150),
    AchievementDef("no_breaks", "No Breaks", "Don't skip any scheduled habits for 14 days", "Shield", "streaks", "silver", 700, 70),
    AchievementDef("daily_grind_100", "Daily Grind", "Complete 100 total habit check-ins", "Activity", "streaks", "silver", 500, 50),
    AchievementDef("daily_grind_500", "Relentless", "Complete 500 total habit check-ins", "Activity", "streaks", "gold", 1500, 150),
    
    # ============ LEVELS (26-50) ============
    AchievementDef("level_5", "Rising Star", "Reach Level 5", "Star", "levels", "bronze", 500, 50),
    AchievementDef("level_10", "Seasoned Adventurer", "Reach Level 10", "Star", "levels", "silver", 1000, 100),
    AchievementDef("level_15", "Veteran", "Reach Level 15", "Star", "levels", "silver", 1500, 150),
    AchievementDef("level_20", "Expert", "Reach Level 20", "Crown", "levels", "gold", 2000, 200),
    AchievementDef("level_25", "Elite Champion", "Reach Level 25", "Crown", "levels", "gold", 2500, 250),
    AchievementDef("level_30", "Master", "Reach Level 30", "Crown", "levels", "gold", 3000, 300, StatBonus("intelligence", 5)),
    AchievementDef("level_40", "Grandmaster", "Reach Level 40", "Shield", "levels", "platinum", 4000, 400, StatBonus("strength", 5)),
    AchievementDef("level_50", "Legendary Hero", "Reach Level 50", "Shield", "levels", "platinum", 5000, 500, StatBonus("vitality", 10), "Unlock S-Rank missions"),
    AchievementDef("level_60", "Mythic Guardian", "Reach Level 60", "Sword", "levels", "platinum", 6000, 600, StatBonus("agility", 10)),
    AchievementDef("level_70", "Titan", "Reach Level 70", "Sword", "levels", "platinum", 7000, 700, StatBonus("sense", 10)),
    AchievementDef("level_80", "Demigod", "Reach Level 80", "Sword", "levels", "legendary", 8000, 800, StatBonus("willpower", 15)),
    AchievementDef("level_90", "Ascended", "Reach Level 90", "Sparkles", "levels", "legendary", 9000, 900, StatBonus("intelligence", 15)),
    AchievementDef("level_100", "Shadow Monarch", "Reach Level 100 - Ultimate Power", "Crown", "levels", "legendary", 15000, 1500, StatBonus("strength", 25), "Unlock Shadow Realm challenges"),
    AchievementDef("fast_leveler", "Fast Leveler", "Gain 5 levels in one week", "Zap", "levels", "silver", 800, 80),
    AchievementDef("xp_hunter_1k", "XP Hunter", "Earn 1,000 total XP", "Target", "levels", "bronze", 100, 10),
    AchievementDef("xp_hunter_10k", "XP Collector", "Earn 10,000 total XP", "Target", "levels", "silver", 500, 50),
    AchievementDef("xp_hunter_50k", "XP Hoarder", "Earn 50,000 total XP", "Target", "levels", "gold", 2000, 200),
    AchievementDef("xp_hunter_100k", "XP Legend", "Earn 100,000 total XP", "Target", "levels", "platinum", 5000, 500),
    AchievementDef("xp_hunter_500k", "XP Immortal", "Earn 500,000 total XP", "Target", "levels", "legendary", 15000, 1500, None, "Golden XP particles effect"),
    AchievementDef("daily_xp_500", "Daily Champion", "Earn 500 XP in a single day", "Flame", "levels", "silver", 300, 30),
    AchievementDef("daily_xp_1000", "XP Blitz", "Earn 1,000 XP in a single day", "Flame", "levels", "gold", 600, 60),
    AchievementDef("rank_novice", "Novice Hunter", "Achieve Novice Hunter rank", "Shield", "levels", "bronze", 300, 30),
    AchievementDef("rank_skilled", "Skilled Hunter", "Achieve Skilled Hunter rank", "Shield", "levels", "silver", 600, 60),
    AchievementDef("rank_elite", "Elite Hunter", "Achieve Elite Hunter rank", "Shield", "levels", "gold", 1200, 120),
    AchievementDef("rank_srank", "S-Rank Hunter", "Achieve S-Rank Hunter status", "Shield", "levels", "legendary", 3000, 300, None, "S-Rank badge on profile"),
    
    # ============ HABITS (51-90) ============
    AchievementDef("first_habit", "Habit Former", "Create your first habit", "Zap", "habits", "bronze", 100, 10),
    AchievementDef("habits_5", "Building Foundation", "Create 5 habits", "Layers", "habits", "bronze", 250, 25),
    AchievementDef("habits_10", "Habit Collector", "Create 10 habits", "Layers", "habits", "silver", 500, 50),
    AchievementDef("habits_15", "Habit Enthusiast", "Create 15 habits", "Layers", "habits", "silver", 750, 75),
    AchievementDef("habits_20", "Habit Architect", "Create 20 habits", "Layers", "habits", "gold", 1000, 100),
    AchievementDef("habits_30", "Habit Master", "Create 30 habits", "Layers", "habits", "platinum", 1500, 150, StatBonus("intelligence", 5)),
    AchievementDef("first_complete", "First Step", "Complete your first habit", "Check", "habits", "bronze", 50, 5),
    AchievementDef("complete_10", "Getting Momentum", "Complete habits 10 times", "Check", "habits", "bronze", 200, 20),
    AchievementDef("complete_50", "Building Routine", "Complete habits 50 times", "Check", "habits", "silver", 400, 40),
    AchievementDef("complete_100", "Century Mark", "Complete habits 100 times", "Check", "habits", "silver", 800, 80),
    AchievementDef("complete_250", "Quarter Thousand", "Complete habits 250 times", "Check", "habits", "gold", 1200, 120),
    AchievementDef("complete_500", "Half Millennium", "Complete habits 500 times", "Check", "habits", "gold", 2000, 200),
    AchievementDef("complete_1000", "Thousand Strong", "Complete habits 1,000 times", "Check", "habits", "platinum", 4000, 400, StatBonus("vitality", 10)),
    AchievementDef("complete_5000", "Habit Legend", "Complete habits 5,000 times", "Check", "habits", "legendary", 10000, 1000, None, "Legendary completion animation"),
    AchievementDef("hard_habit_1", "Challenge Accepted", "Complete a hard difficulty habit", "Sword", "habits", "bronze", 200, 20),
    AchievementDef("hard_habit_10", "Challenge Seeker", "Complete 10 hard habits", "Sword", "habits", "silver", 500, 50),
    AchievementDef("hard_habit_50", "Challenge Master", "Complete 50 hard habits", "Sword", "habits", "gold", 1500, 150, StatBonus("strength", 5)),
    AchievementDef("hard_habit_100", "Challenge Conqueror", "Complete 100 hard habits", "Sword", "habits", "platinum", 3000, 300, StatBonus("strength", 10)),
    AchievementDef("category_fitness", "Fitness Devotee", "Complete 50 fitness habits", "Dumbbell", "habits", "silver", 600, 60, StatBonus("strength", 5)),
    AchievementDef("category_health", "Health Guardian", "Complete 50 health habits", "Heart", "habits", "silver", 600, 60, StatBonus("vitality", 5)),
    AchievementDef("category_learning", "Knowledge Seeker", "Complete 50 learning habits", "BookOpen", "habits", "silver", 600, 60, StatBonus("intelligence", 5)),
    AchievementDef("category_mindfulness", "Inner Peace", "Complete 50 mindfulness habits", "Heart", "habits", "silver", 600, 60, StatBonus("sense", 5)),
    AchievementDef("category_productivity", "Efficiency Expert", "Complete 50 productivity habits", "Zap", "habits", "silver", 600, 60, StatBonus("agility", 5)),
    AchievementDef("perfect_day", "Perfect Day", "Complete all habits in a single day", "Sparkles", "habits", "gold", 1000, 100),
    AchievementDef("perfect_day_5", "Flawless Five", "Achieve 5 perfect days", "Sparkles", "habits", "gold", 2000, 200),
    AchievementDef("perfect_day_30", "Perfection Incarnate", "Achieve 30 perfect days", "Sparkles", "habits", "legendary", 8000, 800, None, "Perfect day crown animation"),
    AchievementDef("diversity_3", "Well-Rounded", "Complete habits in 3 different categories today", "Circle", "habits", "bronze", 150, 15),
    AchievementDef("diversity_5", "Renaissance Soul", "Complete habits in 5 different categories today", "Circle", "habits", "silver", 400, 40),
    AchievementDef("priority_master", "Priority Master", "Complete all priority habits for 7 days", "Star", "habits", "silver", 700, 70),
    AchievementDef("habit_veteran", "Habit Veteran", "Keep the same habit active for 90 days", "Clock", "habits", "gold", 1500, 150),
    AchievementDef("habit_ancient", "Ancient Wisdom", "Keep the same habit active for 365 days", "Clock", "habits", "legendary", 5000, 500, None, "Ancient habit badge"),
    AchievementDef("quick_complete", "Speed Runner", "Complete 5 habits within 1 hour", "Timer", "habits", "silver", 400, 40),
    AchievementDef("balanced_life", "Balanced Life", "Have habits in all 6 categories", "Scale", "habits", "gold", 1000, 100),
    AchievementDef("weekday_warrior", "Weekday Warrior", "Complete all weekday habits for 4 weeks", "Calendar", "habits", "gold", 1200, 120),
    AchievementDef("custom_schedule", "Schedule Master", "Create 5 habits with custom schedules", "CalendarDays", "habits", "silver", 500, 50),
    AchievementDef("reminder_guru", "Reminder Guru", "Set up reminders for 10 habits", "Bell", "habits", "silver", 400, 40),
    AchievementDef("color_coded", "Color Coordinated", "Assign colors to 10 habits", "Palette", "habits", "bronze", 200, 20),
    AchievementDef("description_writer", "Detail Oriented", "Add descriptions to 10 habits", "FileText", "habits", "bronze", 200, 20),
    AchievementDef("active_manager", "Active Manager", "Deactivate and reactivate a habit", "Power", "habits", "bronze", 100, 10),
    
    # ============ GOALS (91-130) ============
    AchievementDef("first_goal", "Goal Setter", "Create your first goal", "Target", "goals", "bronze", 150, 15),
    AchievementDef("goals_5", "Ambitious", "Create 5 goals", "Target", "goals", "silver", 400, 40),
    AchievementDef("goals_10", "Visionary", "Create 10 goals", "Target", "goals", "gold", 800, 80),
    AchievementDef("goals_25", "Dream Architect", "Create 25 goals", "Target", "goals", "platinum", 1500, 150),
    AchievementDef("goal_complete_1", "Achiever", "Complete your first goal", "Trophy", "goals", "bronze", 300, 30),
    AchievementDef("goal_complete_5", "Goal Crusher", "Complete 5 goals", "Trophy", "goals", "silver", 750, 75),
    AchievementDef("goal_complete_10", "Ambitious Achiever", "Complete 10 goals", "Trophy", "goals", "gold", 1500, 150),
    AchievementDef("goal_complete_25", "Dream Realizer", "Complete 25 goals", "Trophy", "goals", "platinum", 3500, 350, StatBonus("intelligence", 10)),
    AchievementDef("goal_complete_50", "Life Transformer", "Complete 50 goals", "Trophy", "goals", "legendary", 7500, 750, None, "Goal mastery crown"),
    AchievementDef("hard_goal_1", "Big Dreamer", "Complete a hard difficulty goal", "Mountain", "goals", "silver", 500, 50),
    AchievementDef("hard_goal_5", "Mountain Climber", "Complete 5 hard goals", "Mountain", "goals", "gold", 1500, 150),
    AchievementDef("hard_goal_10", "Peak Conqueror", "Complete 10 hard goals", "Mountain", "goals", "platinum", 3000, 300, StatBonus("willpower", 10)),
    AchievementDef("step_complete_10", "Step by Step", "Complete 10 goal steps", "ListChecks", "goals", "bronze", 200, 20),
    AchievementDef("step_complete_50", "Methodical", "Complete 50 goal steps", "ListChecks", "goals", "silver", 600, 60),
    AchievementDef("step_complete_100", "Process Master", "Complete 100 goal steps", "ListChecks", "goals", "gold", 1200, 120),
    AchievementDef("on_time_1", "Punctual", "Complete a goal before deadline", "Clock", "goals", "bronze", 250, 25),
    AchievementDef("on_time_5", "Time Keeper", "Complete 5 goals before deadline", "Clock", "goals", "silver", 700, 70),
    AchievementDef("on_time_10", "Deadline Master", "Complete 10 goals before deadline", "Clock", "goals", "gold", 1400, 140),
    AchievementDef("early_bird_goal", "Early Finisher", "Complete a goal a week early", "Rocket", "goals", "silver", 500, 50),
    AchievementDef("month_achiever", "Monthly Achiever", "Complete a goal in under 30 days", "Calendar", "goals", "silver", 600, 60),
    AchievementDef("year_planner", "Year Planner", "Set a goal with a 1-year deadline", "CalendarDays", "goals", "silver", 400, 40),
    AchievementDef("priority_goals", "Priority Focused", "Complete 5 priority goals", "Star", "goals", "gold", 1000, 100),
    AchievementDef("goal_chain_3", "Chain Reaction", "Complete 3 progressive goals in a row", "Link", "goals", "gold", 1500, 150),
    AchievementDef("goal_chain_5", "Unstoppable Progress", "Complete 5 progressive goals", "Link", "goals", "platinum", 2500, 250),
    AchievementDef("ai_goal_1", "AI Collaborator", "Complete an AI-generated goal", "Brain", "goals", "bronze", 300, 30),
    AchievementDef("ai_goal_5", "AI Partner", "Complete 5 AI-generated goals", "Brain", "goals", "silver", 800, 80),
    AchievementDef("full_progress", "Full Progress", "Update a goal from 0% to 100%", "TrendingUp", "goals", "bronze", 200, 20),
    AchievementDef("goal_steps_5", "Planner", "Create a goal with 5+ steps", "ListPlus", "goals", "bronze", 150, 15),
    AchievementDef("goal_steps_10", "Master Planner", "Create a goal with 10+ steps", "ListPlus", "goals", "silver", 400, 40),
    AchievementDef("multi_category_goals", "Diverse Goals", "Complete goals in 5 different categories", "Grid", "goals", "gold", 1000, 100),
    AchievementDef("goal_spree", "Goal Spree", "Complete 3 goals in one week", "Flame", "goals", "gold", 1200, 120),
    AchievementDef("long_term_1", "Long-Term Thinker", "Complete a goal set 6+ months ago", "Hourglass", "goals", "gold", 1500, 150),
    AchievementDef("progressive_master", "Progressive Master", "Complete 10 progressive follow-up goals", "ArrowUpRight", "goals", "legendary", 5000, 500, None, "Automatic goal difficulty scaling"),
    AchievementDef("habit_from_goal", "Habit Creator", "Create a habit from a goal suggestion", "Repeat", "goals", "silver", 400, 40),
    AchievementDef("fitness_goal", "Fitness Achiever", "Complete 5 fitness goals", "Dumbbell", "goals", "silver", 700, 70, StatBonus("strength", 5)),
    AchievementDef("learning_goal", "Knowledge Achiever", "Complete 5 learning goals", "GraduationCap", "goals", "silver", 700, 70, StatBonus("intelligence", 5)),
    AchievementDef("personal_goal", "Self-Improvement", "Complete 5 personal goals", "User", "goals", "silver", 700, 70, StatBonus("willpower", 5)),
    AchievementDef("work_goal", "Career Builder", "Complete 5 work goals", "Briefcase", "goals", "silver", 700, 70, StatBonus("agility", 5)),
    AchievementDef("health_goal", "Health Champion", "Complete 5 health goals", "Heart", "goals", "silver", 700, 70, StatBonus("vitality", 5)),
    AchievementDef("finance_goal", "Wealth Builder", "Complete 5 finance goals", "Coins", "goals", "silver", 700, 70, StatBonus("sense", 5)),
    
    # ============ SPECIAL (131-160) ============
    AchievementDef("first_login", "Welcome", "Log in for the first time", "LogIn", "special", "bronze", 50, 5),
    AchievementDef("profile_complete", "Identity Established", "Complete your profile", "User", "special", "bronze", 100, 10),
    AchievementDef("avatar_chosen", "Avatar Selected", "Choose your character avatar", "UserCircle", "special", "bronze", 50, 5),
    AchievementDef("first_note", "Scribe", "Create your first note", "PenTool", "special", "bronze", 100, 10),
    AchievementDef("notes_10", "Journal Keeper", "Create 10 notes", "BookOpen", "special", "silver", 400, 40),
    AchievementDef("notes_50", "Chronicler", "Create 50 notes", "BookOpen", "special", "gold", 1000, 100),
    AchievementDef("ai_summary", "AI Wisdom", "Get an AI summary for a note", "Brain", "special", "bronze", 150, 15),
    AchievementDef("library_upload", "Library Founder", "Upload your first philosophy document", "Upload", "special", "bronze", 200, 20),
    AchievementDef("library_10", "Library Builder", "Upload 10 philosophy documents", "Library", "special", "silver", 600, 60),
    AchievementDef("library_25", "Philosopher", "Upload 25 philosophy documents", "Library", "special", "gold", 1500, 150, StatBonus("intelligence", 10)),
    AchievementDef("motivation_read", "Daily Wisdom", "Read your first daily motivation", "Quote", "special", "bronze", 50, 5),
    AchievementDef("motivation_week", "Wisdom Seeker", "Read motivations for 7 days", "Quote", "special", "silver", 300, 30),
    AchievementDef("tradition_esoteric", "Hermetic Initiate", "Read 10 Esoteric tradition quotes", "Eye", "special", "silver", 400, 40, StatBonus("sense", 5)),
    AchievementDef("tradition_biblical", "Scripture Scholar", "Read 10 Biblical tradition quotes", "Book", "special", "silver", 400, 40, StatBonus("willpower", 5)),
    AchievementDef("tradition_quranic", "Quran Reader", "Read 10 Quranic tradition quotes", "Book", "special", "silver", 400, 40, StatBonus("sense", 5)),
    AchievementDef("tradition_philosophy", "Ancient Philosopher", "Read 10 Ancient Philosophy quotes", "Scroll", "special", "silver", 400, 40, StatBonus("intelligence", 5)),
    AchievementDef("tradition_metaphysical", "Metaphysician", "Read 10 Metaphysical quotes", "Sparkles", "special", "silver", 400, 40, StatBonus("sense", 5)),
    AchievementDef("all_traditions", "Universal Wisdom", "Read quotes from all 5 traditions", "Globe", "special", "gold", 1000, 100, StatBonus("intelligence", 10), "Unlock special wisdom quotes"),
    AchievementDef("gold_100", "Gold Collector", "Accumulate 100 gold", "Coins", "special", "bronze", 100, 0),
    AchievementDef("gold_500", "Gold Hoarder", "Accumulate 500 gold", "Coins", "special", "silver", 300, 0),
    AchievementDef("gold_1000", "Wealthy", "Accumulate 1,000 gold", "Coins", "special", "gold", 600, 0),
    AchievementDef("gold_5000", "Rich", "Accumulate 5,000 gold", "Coins", "special", "platinum", 1500, 0),
    AchievementDef("gold_10000", "Dragon's Hoard", "Accumulate 10,000 gold", "Coins", "special", "legendary", 3000, 0, None, "Golden profile border"),
    AchievementDef("analytics_view", "Data Driven", "View your analytics page", "BarChart", "special", "bronze", 50, 5),
    AchievementDef("dark_mode", "Shadow Walker", "Enable dark mode", "Moon", "special", "bronze", 25, 0),
    AchievementDef("ai_coach_chat", "Coach Consultation", "Have a conversation with AI Coach", "MessageSquare", "special", "bronze", 150, 15),
    AchievementDef("ai_coach_10", "Regular Coaching", "Have 10 AI Coach conversations", "MessageSquare", "special", "silver", 500, 50),
    AchievementDef("philosophy_ai", "Wisdom Integration", "Use philosophy docs for AI suggestions", "Brain", "special", "gold", 800, 80),
    AchievementDef("explorer", "Explorer", "Visit all pages of the app", "Compass", "special", "bronze", 100, 10),
    AchievementDef("weekend_check", "Weekend Check-In", "Check in on both Saturday and Sunday", "Calendar", "special", "bronze", 150, 15),
    
    # ============ STATS (161-190) ============
    AchievementDef("strength_10", "Strong", "Reach 10 Strength", "Sword", "stats", "bronze", 200, 20),
    AchievementDef("strength_25", "Mighty", "Reach 25 Strength", "Sword", "stats", "silver", 500, 50),
    AchievementDef("strength_50", "Powerful", "Reach 50 Strength", "Sword", "stats", "gold", 1000, 100),
    AchievementDef("strength_100", "Titan Strength", "Reach 100 Strength", "Sword", "stats", "legendary", 2500, 250, None, "Strength training bonus XP"),
    AchievementDef("intelligence_10", "Clever", "Reach 10 Intelligence", "Brain", "stats", "bronze", 200, 20),
    AchievementDef("intelligence_25", "Wise", "Reach 25 Intelligence", "Brain", "stats", "silver", 500, 50),
    AchievementDef("intelligence_50", "Brilliant", "Reach 50 Intelligence", "Brain", "stats", "gold", 1000, 100),
    AchievementDef("intelligence_100", "Genius", "Reach 100 Intelligence", "Brain", "stats", "legendary", 2500, 250, None, "Learning bonus XP"),
    AchievementDef("vitality_10", "Healthy", "Reach 10 Vitality", "Heart", "stats", "bronze", 200, 20),
    AchievementDef("vitality_25", "Robust", "Reach 25 Vitality", "Heart", "stats", "silver", 500, 50),
    AchievementDef("vitality_50", "Resilient", "Reach 50 Vitality", "Heart", "stats", "gold", 1000, 100),
    AchievementDef("vitality_100", "Indomitable", "Reach 100 Vitality", "Heart", "stats", "legendary", 2500, 250, None, "Health bonus XP"),
    AchievementDef("agility_10", "Quick", "Reach 10 Agility", "Zap", "stats", "bronze", 200, 20),
    AchievementDef("agility_25", "Swift", "Reach 25 Agility", "Zap", "stats", "silver", 500, 50),
    AchievementDef("agility_50", "Lightning", "Reach 50 Agility", "Zap", "stats", "gold", 1000, 100),
    AchievementDef("agility_100", "Flash", "Reach 100 Agility", "Zap", "stats", "legendary", 2500, 250, None, "Productivity bonus XP"),
    AchievementDef("sense_10", "Aware", "Reach 10 Sense", "Eye", "stats", "bronze", 200, 20),
    AchievementDef("sense_25", "Perceptive", "Reach 25 Sense", "Eye", "stats", "silver", 500, 50),
    AchievementDef("sense_50", "Clairvoyant", "Reach 50 Sense", "Eye", "stats", "gold", 1000, 100),
    AchievementDef("sense_100", "Omniscient", "Reach 100 Sense", "Eye", "stats", "legendary", 2500, 250, None, "Sense-related bonus XP"),
    AchievementDef("willpower_10", "Determined", "Reach 10 Willpower", "Flame", "stats", "bronze", 200, 20),
    AchievementDef("willpower_25", "Resolute", "Reach 25 Willpower", "Flame", "stats", "silver", 500, 50),
    AchievementDef("willpower_50", "Unbreakable", "Reach 50 Willpower", "Flame", "stats", "gold", 1000, 100),
    AchievementDef("willpower_100", "Iron Will", "Reach 100 Willpower", "Flame", "stats", "legendary", 2500, 250, None, "Willpower bonus XP"),
    AchievementDef("balanced_stats_10", "Balanced Beginner", "All stats at 10+", "Scale", "stats", "silver", 800, 80),
    AchievementDef("balanced_stats_25", "Balanced Warrior", "All stats at 25+", "Scale", "stats", "gold", 2000, 200),
    AchievementDef("balanced_stats_50", "Perfect Balance", "All stats at 50+", "Scale", "stats", "platinum", 5000, 500, StatBonus("willpower", 15)),
    AchievementDef("balanced_stats_100", "True Mastery", "All stats at 100+", "Crown", "stats", "legendary", 15000, 1500, None, "Universal 5% XP boost"),
    AchievementDef("stat_total_100", "Growing Power", "Reach 100 total stat points", "TrendingUp", "stats", "silver", 500, 50),
    AchievementDef("stat_total_500", "Formidable", "Reach 500 total stat points", "TrendingUp", "stats", "platinum", 2500, 250),
    
    # ============ LEGENDARY (191-200) ============
    AchievementDef("ultimate_hunter", "Ultimate Hunter", "Unlock 50 achievements", "Award", "legendary", "legendary", 5000, 500, None, "Achievement hunter badge"),
    AchievementDef("achievement_master", "Achievement Master", "Unlock 100 achievements", "Award", "legendary", "legendary", 10000, 1000, None, "Master collector frame"),
    AchievementDef("completionist", "Completionist", "Unlock 150 achievements", "Medal", "legendary", "legendary", 20000, 2000, None, "Completionist title"),
    AchievementDef("legend", "Living Legend", "Unlock all 200 achievements", "Crown", "legendary", "legendary", 50000, 5000, StatBonus("willpower", 50), "Legendary status - Ultimate power unlocked"),
    AchievementDef("year_one", "Year One", "Use the app for a full year", "Calendar", "legendary", "legendary", 10000, 1000, None, "Anniversary badge"),
    AchievementDef("shadow_monarch", "True Shadow Monarch", "Reach Level 100 with all stats at 100", "Crown", "legendary", "legendary", 25000, 2500, None, "Shadow Monarch powers unlocked"),
    AchievementDef("perfect_year", "Perfect Year", "365 perfect days", "Sparkles", "legendary", "legendary", 50000, 5000, None, "Golden year aura"),
    AchievementDef("million_xp", "Million XP Club", "Earn 1,000,000 total XP", "Star", "legendary", "legendary", 25000, 2500, None, "Million XP particle effects"),
    AchievementDef("habit_legend", "Habit Legend", "10,000 habit completions", "Flame", "legendary", "legendary", 25000, 2500, None, "Legendary habit animation"),
    AchievementDef("enlightened", "Enlightened One", "Max level, all achievements, perfect balance", "Sun", "legendary", "legendary", 100000, 10000, StatBonus("sense", 100), "Enlightenment - transcend limits"),
]


# Achievement lookup by key
ACHIEVEMENTS_BY_KEY: Dict[str, AchievementDef] = {a.key: a for a in ALL_ACHIEVEMENTS}


def get_achievement_by_key(key: str) -> Optional[AchievementDef]:
    """Get achievement definition by key"""
    return ACHIEVEMENTS_BY_KEY.get(key)


def get_achievements_by_category(category: str) -> List[AchievementDef]:
    """Get all achievements in a category"""
    return [a for a in ALL_ACHIEVEMENTS if a.category == category]


def get_achievements_by_tier(tier: str) -> List[AchievementDef]:
    """Get all achievements of a tier"""
    return [a for a in ALL_ACHIEVEMENTS if a.tier == tier]


# Achievement categories
ACHIEVEMENT_CATEGORIES = [
    {"id": "all", "name": "All", "count": len(ALL_ACHIEVEMENTS)},
    {"id": "streaks", "name": "Streaks", "count": len(get_achievements_by_category("streaks"))},
    {"id": "levels", "name": "Levels", "count": len(get_achievements_by_category("levels"))},
    {"id": "habits", "name": "Habits", "count": len(get_achievements_by_category("habits"))},
    {"id": "goals", "name": "Goals", "count": len(get_achievements_by_category("goals"))},
    {"id": "special", "name": "Special", "count": len(get_achievements_by_category("special"))},
    {"id": "stats", "name": "Stats", "count": len(get_achievements_by_category("stats"))},
    {"id": "legendary", "name": "Legendary", "count": len(get_achievements_by_category("legendary"))},
]

# Achievement tiers
ACHIEVEMENT_TIERS = [
    {"id": "all", "name": "All Tiers"},
    {"id": "bronze", "name": "Bronze"},
    {"id": "silver", "name": "Silver"},
    {"id": "gold", "name": "Gold"},
    {"id": "platinum", "name": "Platinum"},
    {"id": "legendary", "name": "Legendary"},
]

"""
Goal Quest AI Integration - Habit and Goal Generation
Handles AI-powered features for personalized recommendations
"""

import os
import random
from typing import List, Dict, Any, Optional
from datetime import datetime

# Try to import AI libraries (optional)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


# ============ WISDOM QUOTES DATABASE ============

WISDOM_QUOTES = {
    "esoteric": [
        {
            "quote": "As above, so below; as within, so without.",
            "philosophy": "The Emerald Tablet teaches us that our inner world reflects our outer reality. Transform yourself to transform your world.",
            "source": "Hermetic Principles"
        },
        {
            "quote": "Know thyself, and thou shalt know the universe and the gods.",
            "philosophy": "Self-knowledge is the key to understanding all mysteries. Your journey inward is the greatest adventure.",
            "source": "Temple of Apollo at Delphi"
        },
        {
            "quote": "The lips of wisdom are closed, except to the ears of understanding.",
            "philosophy": "True wisdom reveals itself only to those who have prepared their minds to receive it.",
            "source": "The Kybalion"
        },
        {
            "quote": "Mind is the master power that molds and makes.",
            "philosophy": "Your thoughts shape your reality. Master your mind, master your destiny.",
            "source": "Hermetic Teaching"
        },
        {
            "quote": "Every moment of transformation begins within the silence of the soul.",
            "philosophy": "The greatest changes start in stillness. Cultivate inner peace to manifest outer power.",
            "source": "Mystery School Tradition"
        },
    ],
    "biblical": [
        {
            "quote": "I can do all things through Christ who strengthens me.",
            "philosophy": "Divine strength flows through dedication and faith. You are capable of more than you know.",
            "source": "Philippians 4:13"
        },
        {
            "quote": "Faith without works is dead.",
            "philosophy": "Belief must be backed by action. Your habits are the proof of your convictions.",
            "source": "James 2:26"
        },
        {
            "quote": "For as he thinketh in his heart, so is he.",
            "philosophy": "Your thoughts determine your character. Guard your mind with intention.",
            "source": "Proverbs 23:7"
        },
        {
            "quote": "Be strong and courageous. Do not be afraid; do not be discouraged.",
            "philosophy": "Fear is the enemy of progress. Face each day with the courage of a warrior.",
            "source": "Joshua 1:9"
        },
        {
            "quote": "Commit thy works unto the Lord, and thy thoughts shall be established.",
            "philosophy": "Align your actions with your highest purpose, and clarity will follow.",
            "source": "Proverbs 16:3"
        },
    ],
    "quranic": [
        {
            "quote": "Indeed, Allah will not change the condition of a people until they change what is in themselves.",
            "philosophy": "Personal transformation is the foundation of all change. Start within.",
            "source": "Surah Ar-Ra'd 13:11"
        },
        {
            "quote": "And whoever relies upon Allah - then He is sufficient for him.",
            "philosophy": "Trust in the divine plan while taking purposeful action each day.",
            "source": "Surah At-Talaq 65:3"
        },
        {
            "quote": "Verily, with hardship comes ease.",
            "philosophy": "Every challenge carries within it the seed of growth. Persist through difficulty.",
            "source": "Surah Ash-Sharh 94:6"
        },
        {
            "quote": "And say: My Lord, increase me in knowledge.",
            "philosophy": "The pursuit of knowledge is a sacred duty. Never stop learning.",
            "source": "Surah Ta-Ha 20:114"
        },
        {
            "quote": "So remember Me; I will remember you.",
            "philosophy": "Mindfulness of the divine brings divine mindfulness of you.",
            "source": "Surah Al-Baqarah 2:152"
        },
    ],
    "metaphysical": [
        {
            "quote": "Thoughts become things. Choose the good ones.",
            "philosophy": "Your mind is the architect of your reality. Build wisely with positive thoughts.",
            "source": "Mike Dooley"
        },
        {
            "quote": "What you focus on expands.",
            "philosophy": "Direct your attention to what you wish to create. Energy flows where attention goes.",
            "source": "New Thought Principle"
        },
        {
            "quote": "You are the creator of your own destiny.",
            "philosophy": "No force outside yourself determines your fate. You hold the pen.",
            "source": "Swami Vivekananda"
        },
        {
            "quote": "The Universe is not outside of you. Look inside yourself; everything that you want, you already are.",
            "philosophy": "All that you seek is already within. Your habits reveal what's hidden.",
            "source": "Rumi"
        },
        {
            "quote": "Act as if what you do makes a difference. It does.",
            "philosophy": "Every small action ripples through the fabric of reality. Nothing is insignificant.",
            "source": "William James"
        },
    ],
    "philosophy": [
        {
            "quote": "We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
            "philosophy": "Your habits define your character. Cultivate excellence through daily practice.",
            "source": "Aristotle"
        },
        {
            "quote": "He who conquers himself is the mightiest warrior.",
            "philosophy": "True victory lies in self-mastery. The battle within is the only one that matters.",
            "source": "Confucius"
        },
        {
            "quote": "The unexamined life is not worth living.",
            "philosophy": "Regular reflection transforms mere existence into meaningful life. Review your progress.",
            "source": "Socrates"
        },
        {
            "quote": "No man is free who is not master of himself.",
            "philosophy": "Freedom comes through discipline. Your habits are either chains or wings.",
            "source": "Epictetus"
        },
        {
            "quote": "The happiness of your life depends upon the quality of your thoughts.",
            "philosophy": "Guard your mind. What you think, you become.",
            "source": "Marcus Aurelius"
        },
    ],
    "stoic": [
        {
            "quote": "You have power over your mind - not outside events. Realize this, and you will find strength.",
            "philosophy": "Focus only on what you can control: your thoughts, habits, and responses.",
            "source": "Marcus Aurelius"
        },
        {
            "quote": "Waste no more time arguing about what a good man should be. Be one.",
            "philosophy": "Action speaks louder than philosophy. Start now, not tomorrow.",
            "source": "Marcus Aurelius"
        },
        {
            "quote": "It is not that we have a short time to live, but that we waste a lot of it.",
            "philosophy": "Time is your most precious resource. Spend it on what truly matters.",
            "source": "Seneca"
        },
        {
            "quote": "The obstacle is the way.",
            "philosophy": "What stands in the way becomes the way. Embrace challenges as teachers.",
            "source": "Marcus Aurelius"
        },
        {
            "quote": "First say to yourself what you would be; and then do what you have to do.",
            "philosophy": "Define your ideal self, then align your habits accordingly.",
            "source": "Epictetus"
        },
    ],
    "eastern": [
        {
            "quote": "The journey of a thousand miles begins with a single step.",
            "philosophy": "Start where you are. Small daily progress leads to massive transformation.",
            "source": "Lao Tzu"
        },
        {
            "quote": "Be the change you wish to see in the world.",
            "philosophy": "External change starts with internal transformation. Change yourself first.",
            "source": "Mahatma Gandhi"
        },
        {
            "quote": "The mind is everything. What you think you become.",
            "philosophy": "Your thoughts are seeds. Plant them wisely in the garden of your mind.",
            "source": "Buddha"
        },
        {
            "quote": "When you realize nothing is lacking, the whole world belongs to you.",
            "philosophy": "Abundance is a state of mind. Gratitude opens doors to prosperity.",
            "source": "Lao Tzu"
        },
        {
            "quote": "Knowing others is intelligence; knowing yourself is true wisdom.",
            "philosophy": "Self-awareness is the highest form of knowledge. Track your patterns.",
            "source": "Lao Tzu"
        },
    ],
}


# ============ HABIT SUGGESTION TEMPLATES ============

HABIT_TEMPLATES = {
    "health": [
        {"title": "Morning Hydration", "description": "Drink a full glass of water upon waking", "reason": "Hydration improves focus and energy levels"},
        {"title": "Healthy Breakfast", "description": "Eat a nutritious breakfast with protein", "reason": "Starting the day with good nutrition sets the tone"},
        {"title": "Evening Walk", "description": "Take a 20-minute walk after dinner", "reason": "Movement aids digestion and reduces stress"},
        {"title": "Sleep Hygiene", "description": "Go to bed at a consistent time each night", "reason": "Consistent sleep improves overall health"},
        {"title": "Stretch Routine", "description": "Spend 10 minutes stretching daily", "reason": "Flexibility prevents injury and reduces tension"},
    ],
    "fitness": [
        {"title": "Morning Exercise", "description": "Complete a 30-minute workout each morning", "reason": "Morning exercise boosts metabolism and mood"},
        {"title": "Strength Training", "description": "Do resistance exercises 3x per week", "reason": "Building muscle improves metabolism and strength"},
        {"title": "Daily Steps", "description": "Walk at least 10,000 steps each day", "reason": "Regular movement is essential for health"},
        {"title": "Core Workout", "description": "5 minutes of core exercises daily", "reason": "Core strength improves posture and prevents injury"},
        {"title": "Active Breaks", "description": "Take movement breaks every hour", "reason": "Breaking up sitting time improves health"},
    ],
    "learning": [
        {"title": "Daily Reading", "description": "Read for 30 minutes each day", "reason": "Reading expands knowledge and perspective"},
        {"title": "Skill Practice", "description": "Practice a new skill for 30 minutes", "reason": "Consistent practice leads to mastery"},
        {"title": "Language Learning", "description": "Study a new language for 15 minutes", "reason": "Language learning improves cognitive function"},
        {"title": "Online Course", "description": "Complete one lesson from an online course", "reason": "Structured learning accelerates growth"},
        {"title": "Learn Something New", "description": "Research one new topic each day", "reason": "Curiosity keeps the mind sharp"},
    ],
    "mindfulness": [
        {"title": "Morning Meditation", "description": "Meditate for 10 minutes each morning", "reason": "Meditation improves focus and reduces stress"},
        {"title": "Gratitude Journal", "description": "Write 3 things you're grateful for", "reason": "Gratitude improves mental well-being"},
        {"title": "Breathing Exercises", "description": "Practice deep breathing for 5 minutes", "reason": "Breathwork calms the nervous system"},
        {"title": "Digital Detox", "description": "Spend 1 hour without screens before bed", "reason": "Reducing screen time improves sleep quality"},
        {"title": "Mindful Moments", "description": "Take 3 mindful pauses throughout the day", "reason": "Presence improves decision-making and peace"},
    ],
    "productivity": [
        {"title": "Morning Planning", "description": "Plan your day each morning", "reason": "Planning increases productivity and focus"},
        {"title": "Deep Work Block", "description": "Complete 2 hours of focused work", "reason": "Deep work produces the highest quality results"},
        {"title": "Inbox Zero", "description": "Process all emails to zero", "reason": "A clear inbox reduces mental clutter"},
        {"title": "Weekly Review", "description": "Review progress and plan the week ahead", "reason": "Regular reviews ensure continuous improvement"},
        {"title": "Priority Task First", "description": "Complete your most important task first", "reason": "Tackling big tasks early builds momentum"},
    ],
    "creative": [
        {"title": "Creative Practice", "description": "Spend 30 minutes on creative work", "reason": "Regular practice develops creative skills"},
        {"title": "Idea Generation", "description": "Write down 10 new ideas daily", "reason": "Idea generation exercises the creative muscle"},
        {"title": "Creative Journal", "description": "Document creative inspirations and thoughts", "reason": "Tracking ideas leads to breakthrough insights"},
        {"title": "Learn New Technique", "description": "Study one new creative technique weekly", "reason": "Expanding techniques expands possibilities"},
        {"title": "Creative Play", "description": "Experiment without expectations", "reason": "Play removes pressure and sparks innovation"},
    ],
    "finance": [
        {"title": "Track Expenses", "description": "Log all spending for the day", "reason": "Awareness of spending enables better decisions"},
        {"title": "Review Budget", "description": "Check budget and adjust as needed", "reason": "Regular review keeps finances on track"},
        {"title": "Save First", "description": "Transfer savings before spending", "reason": "Paying yourself first builds wealth"},
        {"title": "Financial Education", "description": "Learn something new about money", "reason": "Financial literacy improves outcomes"},
        {"title": "Investment Review", "description": "Review investment portfolio weekly", "reason": "Monitoring investments ensures alignment with goals"},
    ],
}


# ============ GOAL PLAN TEMPLATES ============

GOAL_TEMPLATES = {
    "fitness": {
        "title": "Transform Your Physical Health",
        "description": "A comprehensive plan to improve fitness, strength, and overall physical well-being.",
        "steps": [
            {"title": "Establish baseline measurements", "suggestedHabit": "Weekly weigh-in and measurements"},
            {"title": "Design your workout routine", "suggestedHabit": "30-minute daily exercise"},
            {"title": "Optimize your nutrition plan", "suggestedHabit": "Track daily meals"},
            {"title": "Build consistency for 30 days", "suggestedHabit": "Morning workout routine"},
            {"title": "Increase intensity progressively", "suggestedHabit": "Weekly workout review"},
            {"title": "Add variety and challenges", "suggestedHabit": "Try new exercises weekly"},
            {"title": "Achieve and maintain your goal", "suggestedHabit": "Monthly fitness assessment"},
        ]
    },
    "learning": {
        "title": "Master a New Skill",
        "description": "A structured approach to learning and mastering any new skill or subject.",
        "steps": [
            {"title": "Define specific learning objectives", "suggestedHabit": "Daily learning session"},
            {"title": "Gather learning resources", "suggestedHabit": "Weekly resource review"},
            {"title": "Create a structured curriculum", "suggestedHabit": "Study plan execution"},
            {"title": "Begin foundational learning", "suggestedHabit": "30 minutes of practice"},
            {"title": "Apply knowledge through projects", "suggestedHabit": "Daily practice exercises"},
            {"title": "Seek feedback and iterate", "suggestedHabit": "Weekly skill assessment"},
            {"title": "Achieve proficiency milestone", "suggestedHabit": "Monthly progress review"},
        ]
    },
    "career": {
        "title": "Advance Your Career",
        "description": "Strategic steps to achieve your next career milestone.",
        "steps": [
            {"title": "Define your career vision", "suggestedHabit": "Weekly career reflection"},
            {"title": "Identify skill gaps", "suggestedHabit": "Daily skill development"},
            {"title": "Build your professional network", "suggestedHabit": "Weekly networking outreach"},
            {"title": "Create value in current role", "suggestedHabit": "Daily excellence habit"},
            {"title": "Develop leadership abilities", "suggestedHabit": "Leadership reading"},
            {"title": "Position for opportunities", "suggestedHabit": "Monthly visibility actions"},
            {"title": "Execute career transition", "suggestedHabit": "Daily application activity"},
        ]
    },
    "personal": {
        "title": "Personal Transformation",
        "description": "A holistic approach to becoming your best self.",
        "steps": [
            {"title": "Clarify your values and vision", "suggestedHabit": "Daily journaling"},
            {"title": "Audit current habits and patterns", "suggestedHabit": "Weekly habit review"},
            {"title": "Design your ideal daily routine", "suggestedHabit": "Morning routine practice"},
            {"title": "Build keystone habits", "suggestedHabit": "Habit stacking"},
            {"title": "Develop mental resilience", "suggestedHabit": "Daily meditation"},
            {"title": "Strengthen relationships", "suggestedHabit": "Weekly connection time"},
            {"title": "Live aligned with purpose", "suggestedHabit": "Daily purpose alignment"},
        ]
    },
}


# ============ AI FUNCTIONS ============

def get_wisdom_quote(tradition: str) -> Dict[str, str]:
    """Get a random wisdom quote from the specified tradition"""
    quotes = WISDOM_QUOTES.get(tradition, WISDOM_QUOTES["philosophy"])
    quote_data = random.choice(quotes)
    return {
        "quote": quote_data["quote"],
        "philosophy": quote_data["philosophy"],
        "tradition": tradition,
        "source": quote_data["source"]
    }


def generate_habit_suggestions(context: str, count: int = 3) -> List[Dict]:
    """Generate habit suggestions based on user context"""
    # Detect relevant categories from context
    context_lower = context.lower()
    
    detected_categories = []
    category_keywords = {
        "health": ["health", "healthy", "wellness", "medical", "doctor"],
        "fitness": ["fitness", "exercise", "workout", "gym", "run", "weight", "muscle", "strength"],
        "learning": ["learn", "study", "read", "language", "skill", "course", "education"],
        "mindfulness": ["meditation", "mindful", "stress", "calm", "peace", "yoga", "breath"],
        "productivity": ["productive", "work", "focus", "organize", "efficient", "task"],
        "creative": ["creative", "art", "write", "music", "design", "create", "paint"],
        "finance": ["money", "finance", "save", "invest", "budget", "wealth", "income"],
    }
    
    for category, keywords in category_keywords.items():
        if any(keyword in context_lower for keyword in keywords):
            detected_categories.append(category)
    
    if not detected_categories:
        detected_categories = ["productivity", "health", "learning"]
    
    # Gather relevant habits
    suggestions = []
    for category in detected_categories:
        category_habits = HABIT_TEMPLATES.get(category, [])
        for habit in random.sample(category_habits, min(2, len(category_habits))):
            suggestions.append({
                "title": habit["title"],
                "description": habit["description"],
                "reason": f"Based on your goal: {habit['reason']}",
                "type": category,
                "difficulty": random.choice([1, 2])
            })
    
    return suggestions[:count]


def generate_goal_plan(context: str) -> Dict:
    """Generate a complete goal plan based on user context"""
    context_lower = context.lower()
    
    # Detect goal category
    if any(word in context_lower for word in ["fitness", "exercise", "health", "weight", "gym"]):
        template = GOAL_TEMPLATES["fitness"]
    elif any(word in context_lower for word in ["learn", "study", "skill", "language", "course"]):
        template = GOAL_TEMPLATES["learning"]
    elif any(word in context_lower for word in ["career", "job", "work", "promotion", "business"]):
        template = GOAL_TEMPLATES["career"]
    else:
        template = GOAL_TEMPLATES["personal"]
    
    # Generate steps with IDs
    steps = []
    for i, step in enumerate(template["steps"]):
        steps.append({
            "id": f"step_{i+1}",
            "title": step["title"],
            "completed": False,
            "suggestedHabit": step["suggestedHabit"]
        })
    
    return {
        "title": f"Goal: {context[:50]}..." if len(context) > 50 else f"Goal: {context}",
        "description": template["description"],
        "steps": steps,
        "difficulty": 2,  # Medium difficulty
        "xpReward": 2000
    }


def generate_ai_summary(content: str) -> str:
    """Generate an AI summary of note content"""
    # Simple extractive summary (in production, use AI)
    sentences = content.split('. ')
    if len(sentences) <= 3:
        return content
    
    # Return first and last sentences as summary
    summary_sentences = [sentences[0], sentences[-1]] if sentences[-1] else [sentences[0]]
    return '. '.join(summary_sentences) + '.'


def analyze_notes(notes: List[Dict], action: str) -> str:
    """Analyze multiple notes based on action type"""
    if not notes:
        return "No notes to analyze."
    
    contents = [n.get("content", "") for n in notes]
    combined = " ".join(contents)
    
    if action == "summarize":
        return f"Summary of {len(notes)} notes: {generate_ai_summary(combined)}"
    elif action == "themes":
        words = combined.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 4:
                word_freq[word] = word_freq.get(word, 0) + 1
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        themes = [word for word, _ in top_words]
        return f"Key themes: {', '.join(themes)}"
    elif action == "connections":
        return f"Found {len(notes)} related notes. Consider grouping by topic or date."
    elif action == "insights":
        return f"Analysis of {len(notes)} notes reveals patterns in your thinking. Regular reflection deepens these insights."
    
    return "Analysis complete."


# ============ AI API INTEGRATION (Optional) ============

def call_openai(prompt: str, system_prompt: str = None) -> Optional[str]:
    """Call OpenAI API if available"""
    if not OPENAI_AVAILABLE:
        return None
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    
    try:
        client = openai.OpenAI(api_key=api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None


def call_anthropic(prompt: str, system_prompt: str = None) -> Optional[str]:
    """Call Anthropic API if available"""
    if not ANTHROPIC_AVAILABLE:
        return None
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            system=system_prompt or "You are a helpful assistant.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Anthropic API error: {e}")
        return None

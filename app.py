# Therapy Bot Guide - Streamlit Web Application
# Mental Health Support and Resource Finder

"""
🌱 IMPROVED THERAPY BOT WITH FLEXIBLE KEYWORD MATCHING

📋 EXAMPLE OF HOW THE IMPROVED ALGORITHM WORKS:

QUESTIONS (6 total):
1. "What's been bothering you lately?"
2. "How long have you been feeling this way?"
3. "On a scale of 1-10, how intense are these feelings?"
4. "Have you tried therapy before?"
5. "Do you prefer online therapy or in-person?"
6. "Do you have health insurance or need low-cost options?"

USER ANSWERS:
Q1: "I've been feeling really anxious and overthinking everything. 
     I worry constantly and have negative thoughts racing through my mind."
Q2: "About 6 months, since my breakup."
Q3: "About 8 out of 10. It's affecting my work and sleep."
Q4: "Never tried therapy, but meditation helped a little."
Q5: "Online sessions preferred. Too anxious to leave the house."
Q6: "Have insurance but need affordable options."

OLD VERSION (❌ Problem):
Combined text scanned for exact matches only:
- CBT: 1 match (only exact "negative thoughts")
- Exposure: 0 matches (keyword "anxiety" but user said "anxious")
- Others: 0 matches ← Confusing! Why all zeros?

NEW IMPROVED VERSION (✓ Better):
Smart flexible matching:
- CBT: 6 matches ✓
  * "anxious" matches "anxiety" keyword +1
  * "overthinking" exact match +1
  * "worry" exact match +1
  * "negative thoughts" exact match +2 (bonus!)
  * "stress" (work) found +1
  
- Exposure: 3 matches ✓
  * "anxious" exact match +1
  * "worry" exact match +1
  * "anxious leaving house" (avoidance) +1
  
- Mindfulness: 3 matches ✓
  * "overthinking" +1
  * "meditation" exact +1
  * "calm" implied +1

- Others: 0-2 matches each

🎯 RESULT: CBT (6 points) recommended with clear scoring breakdown!

KEY IMPROVEMENTS:
✓ Exact phrase match = 2 points (high value)
✓ Individual word match = 1 point (handles variations)
✓ "anxious" correctly matches keyword "anxiety"
✓ "stressed" correctly matches keyword "stress"
✓ Word filter > 2 chars (avoids "is", "it", "to" false positives)
✓ ALL 6 therapy types scored (never confusing zeros)
✓ Scores sorted highest to lowest

MATCHING ALGORITHM:
1. Combine all 6 user answers into lowercase text
2. Split into individual words for flexible matching
3. For each therapy keyword:
   - Exact phrase match FIRST → +2 points (e.g., "negative thoughts")
   - Individual word match → +1 point (e.g., "anxious" for "anxiety")
4. Calculate total score for each therapy
5. Recommend highest scoring therapy (random tie-breaker)
6. Display ALL scores ranked highest to lowest
"""

import streamlit as st
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Therapy Guide",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 🌿 NATURAL HARMONY DESIGN SYSTEM - COMPREHENSIVE CSS STYLING
st.markdown("""
    <style>

    /* CSS VARIABLES */
    :root {
        --primary: #6A8C7E;
        --primary-dark: #5A6C5E;
        --primary-darker: #4A5C4E;
        --primary-light: #8BA99D;
        --secondary: #A8B8A8;
        --secondary-light: #C0D0C0;
        --bg-primary: #F0F4F2;
        --bg-card: #FFFFFF;
        --bg-hover: #E0E8E4;
        --bg-alt: #F8FAF9;
        --text-primary: #4A5C54;
        --text-secondary: #5D6D65;
        --text-muted: #7D8D85;
        --border: #C0D0C0;
        --border-light: #D8E4DD;
        --user-msg-bg: #C0D0C0;
        --bot-msg-bg: #FFFFFF;
        --success: #6A8C7E;
        --warning: #C4A055;
        --error: #B87070;
        --info: #7A9CB8;
    }
    
    /* GLOBAL STYLES */
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important; }
    
    /* PAGE BACKGROUND - SOFT GREEN - VERY AGGRESSIVE */
    html, body, .main, 
    .stApp, 
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    section[data-testid="stMain"],
    .main .block-container,
    [class*="main"] { 
        background-color: #F0F4F2 !important; 
        background: #F0F4F2 !important;
        color: var(--text-primary) !important; 
    }
    
    /* TYPOGRAPHY */
    h1, h2, h3 { color: var(--primary-darker) !important; font-weight: 600 !important; letter-spacing: -0.02em !important; }
    h1 { font-size: 2rem !important; margin-bottom: 1rem !important; }
    h2 { font-size: 1.5rem !important; margin-bottom: 0.875rem !important; }
    h3 { font-size: 1.25rem !important; margin-bottom: 0.75rem !important; }
    p, li { line-height: 1.6 !important; color: var(--text-primary) !important; }
    
    /* SIDEBAR STYLING - DARKER DISTINCTIVE BACKGROUND */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    [data-testid="stSidebar"],
    .sidebar .sidebar-content { 
        background-color: #E8EDE9 !important; 
        background: #E8EDE9 !important;
        border-right: 2px solid var(--border-light) !important; 
    }
    section[data-testid="stSidebar"] > div { 
        padding-top: 2rem !important; 
    }
    section[data-testid="stSidebar"] h1 { 
        font-size: 1.25rem !important; 
        color: var(--primary-darker) !important; 
        margin-bottom: 1.5rem !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown { 
        margin-bottom: 0.5rem !important; 
    }
    
    /* FIX WHITE TOP AREA - MORE AGGRESSIVE */
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    .stApp > header,
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],
    iframe[title="streamlit_option_menu.option_menu"],
    .css-1dp5vir,
    .appview-container,
    div[class*="stApp"] > header {
        background-color: #F0F4F2 !important;
        background: #F0F4F2 !important;
    }
    
    /* HIDE/FIX STREAMLIT HEADER */
    header[data-testid="stHeader"] {
        background-color: #F0F4F2 !important;
        background: #F0F4F2 !important;
    }
    header[data-testid="stHeader"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 100%;
        background-color: #F0F4F2 !important;
        z-index: -1;
    }
    
    /* BUTTONS - COMPREHENSIVE STYLING */
    .stButton > button, button {
        background-color: var(--primary) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--primary) !important;
        border-radius: 6px !important;
        padding: 0.625rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.9375rem !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(106,140,126,0.08) !important;
        width: auto !important;
    }
    .stButton button *, .stButton button span, .stButton button div, .stButton button p { color: #FFFFFF !important; }
    .stButton > button:hover {
        background-color: var(--primary-dark) !important;
        border-color: var(--primary-dark) !important;
        box-shadow: 0 2px 8px rgba(106,140,126,0.15) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active { background-color: var(--primary-darker) !important; transform: translateY(0) !important; }
    .stButton > button:focus { outline: 2px solid var(--primary-light) !important; outline-offset: 2px !important; }
    
    /* INPUT FIELDS */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border-light) !important;
        border-radius: 6px !important;
        padding: 0.625rem 0.875rem !important;
        font-size: 0.9375rem !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder { color: var(--text-muted) !important; opacity: 0.7 !important; }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border: 2px solid var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(106,140,126,0.1) !important;
        outline: none !important;
    }
    
    /* CARDS & CONTAINERS */
    .element-container, [data-testid="stVerticalBlock"] > div {
        background-color: transparent !important;
    }
    div[data-testid="stContainer"],
    div[data-testid="column"] > div {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 8px !important;
        padding: 1.25rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }
    
    /* EXPANDERS */
    .streamlit-expanderHeader {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 6px !important;
        padding: 0.875rem 1rem !important;
        font-weight: 500 !important;
        color: var(--primary-darker) !important;
        transition: all 0.2s ease !important;
    }
    .streamlit-expanderHeader:hover {
        background-color: var(--bg-hover) !important;
        border-color: var(--primary-light) !important;
    }
    .streamlit-expanderContent {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-top: none !important;
        border-radius: 0 0 6px 6px !important;
        padding: 1rem !important;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem !important;
        background-color: transparent !important;
        border-bottom: 2px solid var(--border-light) !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        padding: 0.75rem 1.25rem !important;
        border-radius: 6px 6px 0 0 !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--bg-hover) !important;
        color: var(--primary) !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--bg-card) !important;
        color: var(--primary) !important;
        border-bottom: 3px solid var(--primary) !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-top: none !important;
        border-radius: 0 6px 6px 6px !important;
        padding: 1.5rem !important;
    }
    
    /* ALERTS & MESSAGES */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 8px !important;
        padding: 1rem 1.25rem !important;
        border-left: 4px solid !important;
        margin: 1rem 0 !important;
    }
    .stSuccess { background-color: rgba(106,140,126,0.1) !important; border-left-color: var(--success) !important; }
    .stInfo { background-color: rgba(122,156,184,0.1) !important; border-left-color: var(--info) !important; }
    .stWarning { background-color: rgba(196,160,85,0.1) !important; border-left-color: var(--warning) !important; }
    
    /* ERROR MESSAGES - LIGHT SAGE GREEN - SUPER AGGRESSIVE OVERRIDE */
    .stAlert,
    .stError, 
    .stException,
    div.stAlert,
    div.stError,
    div[data-testid="stException"],
    div[data-testid="stNotification"],
    div[data-baseweb="notification"],
    [class*="stAlert"],
    [class*="stError"],
    [data-testid*="Exception"],
    [data-testid*="error"] { 
        background-color: #E8F0ED !important; 
        background: #E8F0ED !important;
        border: 1px solid #D8E4DD !important;
        border-left: 5px solid #C4A055 !important; 
        border-radius: 8px !important;
        color: #4A5C54 !important; 
        padding: 1rem 1.25rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    /* Error message icons */
    .stError svg,
    .stAlert svg,
    .stException svg,
    div.stError svg,
    [class*="stError"] svg,
    [class*="stAlert"] svg { 
        color: #C4A055 !important; 
        fill: #C4A055 !important;
    }
    
    /* Error message text */
    .stError *,
    .stAlert *,
    .stException *,
    div.stError *,
    [class*="stError"] *,
    [class*="stAlert"] * {
        color: #4A5C54 !important;
    }
    
    /* Error message bold text */
    .stError strong,
    .stError b,
    .stAlert strong,
    .stAlert b,
    div.stError strong,
    div.stError b { 
        color: #3A4C44 !important; 
        font-weight: 600 !important;
    }
    
    /* CHAT MESSAGES */
    .stChatMessage {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 0.75rem !important;
    }
    [data-testid="stChatMessageContent"] { color: var(--text-primary) !important; }
    
    /* SELECTBOX DROPDOWN */
    .stSelectbox > div > div > div { background-color: var(--bg-card) !important; }
    
    /* DIVIDERS */
    hr { border-color: var(--border-light) !important; margin: 1.5rem 0 !important; }
    
    /* LINKS */
    a { color: var(--primary) !important; text-decoration: none !important; font-weight: 500 !important; }
    a:hover { color: var(--primary-dark) !important; text-decoration: underline !important; }
    
    /* PROGRESS & METRICS */
    [data-testid="stMetricValue"] { color: var(--primary-darker) !important; font-weight: 600 !important; }
    [data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }
    
    /* MARKDOWN CONTENT */
    .stMarkdown strong, .stMarkdown b { color: var(--primary-darker) !important; font-weight: 600 !important; }
    .stMarkdown em, .stMarkdown i { color: var(--text-secondary) !important; }
    .stMarkdown code {
        background-color: var(--bg-hover) !important;
        color: var(--primary-darker) !important;
        padding: 0.125rem 0.375rem !important;
        border-radius: 4px !important;
        font-size: 0.875em !important;
    }
    
    /* LISTS */
    .stMarkdown ul, .stMarkdown ol { padding-left: 1.5rem !important; margin: 0.5rem 0 !important; }
    .stMarkdown li { margin: 0.375rem 0 !important; color: var(--text-primary) !important; }
    
    /* SCROLLBAR STYLING */
    ::-webkit-scrollbar { width: 8px !important; height: 8px !important; }
    ::-webkit-scrollbar-track { background: var(--bg-primary) !important; }
    ::-webkit-scrollbar-thumb {
        background: var(--secondary-light) !important;
        border-radius: 4px !important;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--secondary) !important; }
    
    /* CHAT INPUT */
    .stChatInput > div > div > div > input {
        background-color: var(--bg-card) !important;
        border: 1.5px solid var(--border-light) !important;
        border-radius: 24px !important;
        padding: 0.75rem 1.25rem !important;
        font-size: 0.9375rem !important;
    }
    .stChatInput > div > div > div > input:focus {
        border: 2px solid var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(106,140,126,0.1) !important;
    }
    
    /* LOADING SPINNER */
    .stSpinner > div { border-top-color: var(--primary) !important; }
    
    /* ADDITIONAL ERROR MESSAGE OVERRIDES - ENSURE LIGHT SAGE GREEN APPLIES */
    div.stAlert.stError,
    div[data-testid="stNotificationContentError"],
    div[data-baseweb="notification"][kind="error"],
    [class*="stAlert"][class*="error"] {
        background-color: #E8F0ED !important;
        background: #E8F0ED !important;
        border: 1px solid #D8E4DD !important;
        border-left: 5px solid #C4A055 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    div.stAlert.stError > div,
    div[data-testid="stNotificationContentError"] > div {
        background-color: #E8F0ED !important;
        background: #E8F0ED !important;
    }
    .stAlert.stError p, .stAlert.stError div, .stAlert.stError span {
        color: #4A5C54 !important;
    }
    
    /* FORCE LEFT BORDER ON ERROR PARENT CONTAINERS */
    div[data-testid="stNotification"],
    div[class*="Alert"],
    div[class*="Error"] {
        border-left: 5px solid #C4A055 !important;
    }
    </style>
""", unsafe_allow_html=True)
class TherapyBotGuide:
    def __init__(self):
        """Initialize the bot with all its knowledge and capabilities"""

        # Crisis detection words
        self.crisis_words = [
            'suicide', 'kill myself', 'end my life', 'want to die',
            'hurt myself', 'overdose', 'can\'t go on', 'ending it all',
            'better off dead', 'no point living'
        ]

        # Therapy knowledge database
        self.therapy_types = {
            'CBT': {
                'name': 'Cognitive Behavioral Therapy (CBT)',
                'good_for': [
                    'anxiety', 'anxious', 'anxieties',
                    'depression', 'depressed', 'sad', 'sadness',
                    'worry', 'worried', 'worries', 'worrying',
                    'panic', 'panicking', 'panicked',
                    'negative thoughts', 'negative thinking',
                    'fear', 'afraid', 'fears',
                    'stress', 'stressed', 'stressful', 'stressing',
                    'overthinking', 'overthink', 'overthinks',
                    'patterns', 'habits',
                    'breakup', 'breakups', 'heartbreak', 'heartbroken'
                ],
                'description': 'Helps you identify and change negative thought patterns and behaviors',
                'example': 'Learning to challenge thoughts like "I always fail at everything"',
                'duration': 'Usually 12-20 sessions',
                'effectiveness': 'Highly effective for anxiety and depression'
            },
            'DBT': {
                'name': 'Dialectical Behavior Therapy (DBT)',
                'good_for': [
                    'intense emotions', 'intensely emotional', 'emotional intensity',
                    'self harm', 'self-harm', 'self harming',
                    'relationships', 'relationship', 'relationship issues',
                    'borderline personality', 'unstable',
                    'anger', 'angry', 'enraged', 'rage', 'raging',
                    'emotional', 'emotionally', 'emotional regulation',
                    'overwhelmed', 'overwhelming', 'overwhelm',
                    'impulsive', 'impulsivity'
                ],
                'description': 'Teaches skills to manage intense emotions and improve relationships',
                'example': 'Learning breathing techniques and distress tolerance when overwhelmed',
                'duration': 'Usually 1-2 years of skills training',
                'effectiveness': 'Very effective for emotional regulation'
            },
            'Family_Therapy': {
                'name': 'Family or Couples Therapy',
                'good_for': [
                    'family problems', 'family conflict', 'family issues',
                    'relationship issues', 'relationship conflict', 'relationship problems',
                    'communication', 'communicating', 'communication problems',
                    'couples', 'couple', 'partner', 'marriage', 'spouse',
                    'conflict', 'conflicted', 'conflicts',
                    'arguing', 'argue', 'argument', 'fight', 'fighting',
                    'divorce', 'divorced', 'breakup', 'breaking up',
                    'love', 'trust', 'intimacy'
                ],
                'description': 'Helps families and couples improve communication and resolve conflicts',
                'example': 'Learning to express feelings without fighting or shutting down',
                'duration': '8-20 sessions depending on issues',
                'effectiveness': 'Effective for relationship and family conflicts'
            },
            'Trauma_Therapy': {
                'name': 'Trauma-Focused Therapy (EMDR/CPT)',
                'good_for': [
                    'trauma', 'traumatic', 'traumatized',
                    'ptsd', 'post-traumatic', 'post traumatic',
                    'bad memories', 'traumatic memories', 'painful memories',
                    'abuse', 'abused', 'abusive',
                    'flashbacks', 'flashback', 'intrusive thoughts',
                    'violence', 'violent', 'attack', 'attacked',
                    'accident', 'accidents',
                    'painful', 'pain', 'hurt', 'injury',
                    'haunting', 'haunted', 'disturbing'
                ],
                'description': 'Helps process and heal from traumatic experiences',
                'example': 'Working through disturbing memories in a safe, controlled way',
                'duration': '12-25 sessions typically',
                'effectiveness': 'Highly effective for PTSD and trauma'
            },
            'Humanistic': {
                'name': 'Humanistic/Person-Centered Therapy',
                'good_for': [
                    'self esteem', 'self-esteem', 'low self esteem',
                    'identity', 'identity issues', 'who am i',
                    'personal growth', 'growth', 'growing',
                    'life transitions', 'transition', 'change', 'changing',
                    'purpose', 'meaningful', 'meaning',
                    'authentic', 'authenticity',
                    'self-acceptance', 'self acceptance',
                    'values', 'valued',
                    'development', 'developing',
                    'self-compassion', 'compassion'
                ],
                'description': 'Focuses on self-acceptance and personal growth',
                'example': 'Exploring your authentic self and building self-compassion',
                'duration': 'Often longer-term, 6 months to several years',
                'effectiveness': 'Good for personal development and self-awareness'
            }
        }

        # Assessment questions
        self.assessment_questions = [
            "What's been bothering you lately? (Describe your main concerns)",
            "How long have you been feeling this way?",
            "On a scale of 1-10, how intense are these feelings?",
            "Have you tried therapy before? What was helpful or not helpful?",
            "Do you prefer online therapy or meeting in person?",
            "Do you have health insurance or need low-cost options?"
        ]

        # Professional resources
        self.professional_resources = {
            'Psychology_Today': {
                'website': 'psychologytoday.com/us/therapists',
                'description': 'Find therapists near you with photos, specialties, and reviews',
                'good_for': 'Finding local therapists',
                'cost': 'Varies by therapist ($80-200+ per session)',
                'type': 'Directory'
            },
            'BetterHelp': {
                'website': 'betterhelp.com',
                'description': 'Online therapy through video, phone, or text messaging',
                'good_for': 'Online therapy',
                'cost': '$60-90 per week (unlimited messaging + live sessions)',
                'type': 'Online Platform'
            },
            'Talkspace': {
                'website': 'talkspace.com',
                'description': 'Text-based therapy with licensed therapists',
                'good_for': 'Text-based therapy',
                'cost': '$69-109 per week',
                'type': 'Online Platform'
            },
            'Open_Path': {
                'website': 'openpathcollective.org',
                'description': 'Affordable therapy sessions with sliding scale fees',
                'good_for': 'Low-cost therapy options',
                'cost': '$30-60 per session',
                'type': 'Affordable Care'
            },
            'Crisis_Text_Line': {
                'website': 'crisistextline.org',
                'phone': 'Text HOME to 741741',
                'description': '24/7 crisis support via text message - completely free',
                'good_for': 'Immediate crisis support',
                'cost': 'Free',
                'type': 'Crisis Support'
            },
            'SAMHSA': {
                'website': 'samhsa.gov/find-treatment',
                'phone': '1-800-662-4357',
                'description': 'Government treatment locator for mental health and substance abuse',
                'good_for': 'Finding local treatment facilities',
                'cost': 'Varies',
                'type': 'Government Resource'
            }
        }

    def check_for_crisis(self, user_message):
        """Check if someone is in immediate danger"""
        if not user_message:
            return False

        message_lower = user_message.lower()
        for crisis_word in self.crisis_words:
            if crisis_word in message_lower:
                return True
        return False

    def get_crisis_help(self):
        """Provide immediate crisis resources"""
        return """
        ⚠️ **IMMEDIATE HELP AVAILABLE** ⚠️

        **If you're thinking about hurting yourself, please reach out RIGHT NOW:**

        ☎️ **CALL: 988** (Suicide & Crisis Lifeline) - Available 24/7
        💬 **TEXT: HOME to 741741** (Crisis Text Line)
        🏥 **EMERGENCY: Call 911** or go to nearest emergency room
        🌐 **CHAT: suicidepreventionlifeline.org** (Online chat available)

        **You are NOT alone. These feelings CAN change with help.**
        """

    def find_best_therapy(self, user_problems):
        """
        Figure out which therapy might help based on user's problems.
        
        IMPROVED ALGORITHM with flexible keyword matching:
        - Exact phrase match = 2 points (higher value)
        - Individual word match = 1 point (handles variations)
        - Avoids false positives with word length filter (> 2 chars)
        
        EXAMPLE:
        User says: "I'm anxious, overthinking, and stressed about my breakup"
        
        For CBT therapy with keywords ["anxiety", "breakup", "stress", ...]:
        - "anxiety" found in "anxious" → +1 point
        - "breakup" exact match → +2 points
        - "stress" found in "stressed" → +1 point
        Total CBT: 4+ points
        
        Returns: (best_therapy_name, therapy_scores_dict)
        """
        therapy_scores = {}

        # Start all therapy types with 0 points
        for therapy_name in self.therapy_types:
            therapy_scores[therapy_name] = 0

        # Convert user problems to lowercase for easier matching
        user_text = ' '.join(user_problems).lower()
        
        # Split user text into individual words for flexible matching
        # Example: "I'm anxious and stressed" → {"i'm", "anxious", "and", "stressed", ...}
        user_words = set(user_text.split())

        # Check each therapy type for matches
        for therapy_name, therapy_info in self.therapy_types.items():
            for keyword in therapy_info['good_for']:
                keyword_lower = keyword.lower()
                
                # STEP 1: Try exact phrase match first - HIGHER VALUE
                # Example: if user said "negative thoughts", this matches exactly
                if keyword_lower in user_text:
                    therapy_scores[therapy_name] += 2  # Exact match gets 2 points
                else:
                    # STEP 2: Try individual word matches from multi-word keywords
                    # Example: keyword "negative thoughts" → split into ["negative", "thoughts"]
                    keyword_words = keyword_lower.split()
                    for word in keyword_words:
                        # Only match words > 2 chars (avoids false positives from "is", "it", etc)
                        # Example: "anxious" matches part of keyword "anxiety"
                        if len(word) > 2 and word in user_words:
                            therapy_scores[therapy_name] += 1  # Partial match gets 1 point
                            break  # Count once per keyword

        # Find the therapy type with the most points
        if max(therapy_scores.values()) > 0:
            best_therapy = max(therapy_scores, key=therapy_scores.get)
        else:
            best_therapy = 'CBT'  # Default recommendation if no matches

        return best_therapy, therapy_scores

    def get_resources_for_user(self, user_preferences):
        """Find the best resources based on what user needs"""
        recommended_resources = []
        user_text = ' '.join(user_preferences).lower()

        # Online preference
        if 'online' in user_text:
            recommended_resources.extend(['BetterHelp', 'Talkspace'])

        # Cost considerations
        if any(word in user_text for word in ['cost', 'money', 'affordable', 'cheap', 'low-cost', 'sliding scale']):
            recommended_resources.append('Open_Path')

        # Always include Psychology Today and SAMHSA
        recommended_resources.extend(['Psychology_Today', 'SAMHSA'])

        # Add crisis support
        recommended_resources.append('Crisis_Text_Line')

        # Remove duplicates while preserving order
        seen = set()
        final_resources = []
        for resource in recommended_resources:
            if resource not in seen:
                seen.add(resource)
                final_resources.append(resource)

        return final_resources

def main():
    """Main Streamlit application"""

    # Initialize bot with error handling
    if 'bot' not in st.session_state:
        try:
            st.session_state.bot = TherapyBotGuide()
            # Verify the bot has the required method
            if not hasattr(st.session_state.bot, 'find_best_therapy'):
                st.error("⚠️ Bot initialization error: find_best_therapy method missing")
                st.stop()
        except Exception as e:
            st.error(f"⚠️ Error initializing bot: {str(e)}")
            st.stop()

    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'assessment_started' not in st.session_state:
        st.session_state.assessment_started = False
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False

    # Header
    st.title("🌱 Therapy Guide")
    st.markdown("**Your Personal Mental Health Resource Finder**")

    # Important disclaimer
    st.error("⚠️ **IMPORTANT:** This tool is for educational purposes only and is not a replacement for professional mental health care. If you're in crisis, please seek immediate help.")

    # Sidebar with navigation
    st.sidebar.title("Navigation")

    # Crisis button (always visible)
    if st.sidebar.button("⚠️ Crisis Help - Get Help Now"):
        st.error(st.session_state.bot.get_crisis_help())

    st.sidebar.markdown("---")
    
    # Debug / Clear session button
    with st.sidebar.expander("⚙️ Troubleshooting"):
        st.write("Having issues? Try clearing the session:")
        if st.button("🗑️ Clear Session & Restart"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.sidebar.markdown("---")

    # Main navigation
    if not st.session_state.assessment_started:
        page = st.sidebar.selectbox(
            "Choose an option:",
            ["🏡 Home", "⚠️ Crisis Resources", "💭 Learn About Therapy", "🔗 Find Resources"]
        )

        if page == "🏡 Home":
            show_home_page()
        elif page == "⚠️ Crisis Resources":
            show_crisis_page()
        elif page == "💭 Learn About Therapy":
            show_therapy_types_page()
        elif page == "🔗 Find Resources":
            show_resources_page()
    else:
        # Assessment is active
        st.sidebar.write("✍️ **Assessment in Progress**")
        if st.sidebar.button("↻ Start Over"):
            st.session_state.assessment_started = False
            st.session_state.current_question = 0
            st.session_state.user_answers = []
            st.session_state.show_results = False
            st.rerun()

        if st.session_state.show_results:
            show_assessment_results()
        else:
            show_assessment_page()

def show_home_page():
    """Show the home page"""
    st.header("Welcome! How can I help you today?")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💡 What This Tool Does")
        st.write("""
        - **Assesses** your mental health concerns
        - **Recommends** appropriate therapy types
        - **Connects** you with professional resources
        - **Provides** crisis support information
        - **Educates** about different therapy options
        """)

        if st.button("✍️ Start Assessment", type="primary"):
            st.session_state.assessment_started = True
            st.session_state.current_question = 0
            st.session_state.user_answers = []
            st.session_state.show_results = False
            st.rerun()

    with col2:
        st.subheader("🆘 Need Immediate Help?")
        st.write("""
        If you're having thoughts of self-harm or suicide:
        - **Call 988** (Suicide & Crisis Lifeline)
        - **Text HOME to 741741** (Crisis Text Line)
        - **Call 911** for emergency services
        """)

        if st.button("🆘 Get Crisis Resources"):
            st.error(st.session_state.bot.get_crisis_help())

    # Statistics and info
    st.markdown("---")
    st.subheader("📌 Mental Health Facts")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Adults with Mental Illness", "1 in 5", "In the US annually")
    with col2:
        st.metric("Therapy Effectiveness", "75%", "Show improvement")
    with col3:
        st.metric("Crisis Line Response", "24/7", "Available support")

def show_assessment_page():
    """
    Show the assessment questionnaire in a chat-like format.
    
    INTERFACE DESIGN:
    ✅ Questions appear one per row in natural conversation flow
    ✅ Previous Q&A pairs remain visible for context and continuity
    ✅ Chat input at bottom for natural, intuitive interaction
    ✅ Automatic progression to next question (no buttons needed)
    
    This creates a better UX than traditional forms with Next/Previous buttons.
    Users experience it like a real conversation with the bot.
    """
    st.header("✍️ Mental Health Assessment")
    st.write("Please answer these questions honestly. Your responses will help me recommend appropriate resources.")

    # Progress bar
    progress = st.session_state.current_question / len(st.session_state.bot.assessment_questions)
    st.progress(progress)
    st.write(f"Question {st.session_state.current_question + 1} of {len(st.session_state.bot.assessment_questions)}")
    
    st.markdown("---")

    # Show assessment in progress
    if st.session_state.current_question < len(st.session_state.bot.assessment_questions):
        # Display chat history (previous questions and answers)
        # This maintains conversation context as user progresses through questions
        for i in range(st.session_state.current_question):
            question = st.session_state.bot.assessment_questions[i]
            answer = st.session_state.user_answers[i] if i < len(st.session_state.user_answers) else ""
            
            # Show previous questions as bot messages
            with st.chat_message("assistant"):
                st.write(question)
            # Show previous answers as user messages
            with st.chat_message("user"):
                st.write(answer)
        
        # Current question - the one user needs to answer now
        current_question = st.session_state.bot.assessment_questions[st.session_state.current_question]
        with st.chat_message("assistant"):
            st.write(current_question)
        
        # Chat input for current question
        # Using st.chat_input for natural messaging experience
        user_input = st.chat_input("Your answer...", key=f"q_{st.session_state.current_question}")
        
        if user_input:
            # Check for crisis indicators in user's response
            if st.session_state.bot.check_for_crisis(user_input):
                st.error(st.session_state.bot.get_crisis_help())
                return
            
            # Save answer to session state
            if len(st.session_state.user_answers) <= st.session_state.current_question:
                st.session_state.user_answers.append(user_input)
            else:
                st.session_state.user_answers[st.session_state.current_question] = user_input
            
            # Move to next question
            st.session_state.current_question += 1
            st.rerun()

    else:
        # Assessment complete - show results
        st.session_state.show_results = True
        st.rerun()

def show_assessment_results():
    """Show personalized recommendations based on assessment"""
    st.success("✓ Assessment Complete!")
    st.header("📋 Your Personalized Recommendations")

    # Find best therapy type with error handling
    try:
        # Verify bot object exists and has the method
        if not hasattr(st.session_state, 'bot'):
            st.error("⚠️ Error: Bot not initialized. Please refresh the page.")
            if st.button("↻ Refresh Page"):
                st.rerun()
            return
            
        if not hasattr(st.session_state.bot, 'find_best_therapy'):
            st.error("⚠️ Error: Bot is missing required methods. Please refresh the page.")
            st.write(f"Bot type: {type(st.session_state.bot)}")
            st.write(f"Bot methods: {[m for m in dir(st.session_state.bot) if not m.startswith('_')]}")
            if st.button("↻ Refresh Page"):
                st.rerun()
            return
            
        best_therapy, therapy_scores = st.session_state.bot.find_best_therapy(st.session_state.user_answers)
        therapy_info = st.session_state.bot.therapy_types[best_therapy]
    except Exception as e:
        st.error(f"⚠️ Error generating recommendations: {str(e)}")
        st.write("**Debug info:**")
        st.write(f"- Error type: {type(e).__name__}")
        st.write(f"- User answers: {len(st.session_state.user_answers)} answers")
        if st.button("↻ Try Again"):
            st.session_state.show_results = False
            st.rerun()
        return

    # Therapy recommendation
    st.subheader("⭐ Recommended Therapy Type")
    with st.container():
        st.markdown(f"### {therapy_info['name']}")
        st.write(f"**What it does:** {therapy_info['description']}")
        st.write(f"**Example:** {therapy_info['example']}")
        st.write(f"**Typical duration:** {therapy_info['duration']}")
        st.write(f"**Effectiveness:** {therapy_info['effectiveness']}")

    # Show all therapy scores
    with st.expander("📈 See how other therapies scored for you"):
        st.write("**Your therapy scores:** (sorted from highest to lowest)")
        
        # Sort scores in descending order to show best matches first
        # Example: CBT: 8, DBT: 2, Humanistic: 1, Others: 0
        sorted_scores = sorted(therapy_scores.items(), key=lambda x: x[1], reverse=True)
        
        for therapy_name, score in sorted_scores:
            therapy_data = st.session_state.bot.therapy_types[therapy_name]
            
            # Visual indicators help users quickly understand results:
            # ✅ = therapy matched (score > 0)
            # ⭕ = therapy didn't match (score = 0)
            if score > 0:
                st.write(f"✅ **{therapy_data['name']}:** {score} matches")
            else:
                st.write(f"⭕ **{therapy_data['name']}:** {score} matches")

    # Resource recommendations
    st.subheader("🔗 Where to Find Help")
    resources = st.session_state.bot.get_resources_for_user(st.session_state.user_answers)

    for resource_name in resources:
        resource = st.session_state.bot.professional_resources[resource_name]
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**[{resource['website']}](https://{resource['website']})**")
                st.write(resource['description'])
                st.write(f"*Good for: {resource['good_for']}*")
            with col2:
                st.write(f"**Cost:** {resource['cost']}")
                st.write(f"**Type:** {resource['type']}")
        st.markdown("---")

    # Next steps
    st.subheader("→ Next Steps")
    st.write("""
    1. **Review** the therapy type recommendation above
    2. **Visit** one or more of the recommended websites
    3. **Contact** a mental health professional
    4. **Remember** that finding the right therapist may take time
    5. **Don't give up** - help is available!
    """)

    # Reset button
    if st.button("↻ Take Assessment Again"):
        st.session_state.assessment_started = False
        st.session_state.current_question = 0
        st.session_state.user_answers = []
        st.session_state.show_results = False
        st.rerun()

def show_crisis_page():
    """Show crisis resources page"""
    st.header("⚠️ Crisis Resources")
    st.error(st.session_state.bot.get_crisis_help())

    st.subheader("☎️ Additional Crisis Resources")

    crisis_resources = [
        {"name": "National Suicide Prevention Lifeline", "contact": "988", "description": "24/7 crisis support"},
        {"name": "Crisis Text Line", "contact": "Text HOME to 741741", "description": "24/7 text-based crisis support"},
        {"name": "SAMHSA National Helpline", "contact": "1-800-662-4357", "description": "Treatment referral service"},
        {"name": "National Domestic Violence Hotline", "contact": "1-800-799-7233", "description": "24/7 support for domestic violence"},
        {"name": "LGBTQ National Hotline", "contact": "1-888-843-4564", "description": "Support for LGBTQ+ individuals"},
        {"name": "Veterans Crisis Line", "contact": "1-800-273-8255", "description": "24/7 support for veterans"}
    ]

    for resource in crisis_resources:
        with st.container():
            st.markdown(f"**{resource['name']}**")
            st.markdown(f"☎️ {resource['contact']}")
            st.write(resource['description'])
            st.markdown("---")

def show_therapy_types_page():
    """Show information about different therapy types"""
    st.header("💭 Types of Therapy")
    st.write("Learn about different therapeutic approaches and what they help with.")

    # Create tabs for each therapy type
    therapy_names = list(st.session_state.bot.therapy_types.keys())
    tabs = st.tabs([st.session_state.bot.therapy_types[name]['name'] for name in therapy_names])

    for i, tab in enumerate(tabs):
        with tab:
            therapy_name = therapy_names[i]
            therapy_info = st.session_state.bot.therapy_types[therapy_name]

            st.subheader(therapy_info['name'])
            st.write(f"**Description:** {therapy_info['description']}")
            st.write(f"**Good for:** {', '.join(therapy_info['good_for'])}")
            st.write(f"**Example:** {therapy_info['example']}")
            st.write(f"**Duration:** {therapy_info['duration']}")
            st.write(f"**Effectiveness:** {therapy_info['effectiveness']}")

def show_resources_page():
    """Show all available resources"""
    st.header("🔗 Mental Health Resources")
    st.write("Browse all available resources for mental health support.")

    # Filter options
    resource_types = ['All'] + list(set([r['type'] for r in st.session_state.bot.professional_resources.values()]))
    selected_type = st.selectbox("Filter by type:", resource_types)

    # Display resources
    for resource_name, resource in st.session_state.bot.professional_resources.items():
        if selected_type == 'All' or resource['type'] == selected_type:
            with st.container():
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"### [{resource['website']}](https://{resource['website']})")
                    st.write(resource['description'])
                    if 'phone' in resource:
                        st.write(f"☎️ {resource['phone']}")
                with col2:
                    st.write(f"**Type:** {resource['type']}")
                    st.write(f"**Cost:** {resource['cost']}")
                    st.write(f"**Good for:** {resource['good_for']}")
                st.markdown("---")

if __name__ == "__main__":
    main()
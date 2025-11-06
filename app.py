import streamlit as st
from datetime import datetime
import re
from streamlit_option_menu import option_menu

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
    
    /* PAGE BACKGROUND */
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
    
    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    [data-testid="stSidebar"],
    .sidebar .sidebar-content { 
        background-color: #E8EDE9 !important; 
        background: #E8EDE9 !important;
        border-right: 2px solid var(--border-light) !important; 
    }
    section[data-testid="stSidebar"] > div { padding-top: 2rem !important; }
    section[data-testid="stSidebar"] h1 { 
        font-size: 1.25rem !important; 
        color: var(--primary-darker) !important; 
        margin-bottom: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    /* BUTTONS */
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
    .stButton button * { color: #FFFFFF !important; }
    .stButton > button:hover {
        background-color: var(--primary-dark) !important;
        border-color: var(--primary-dark) !important;
        box-shadow: 0 2px 8px rgba(106,140,126,0.15) !important;
        transform: translateY(-1px) !important;
    }
    
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
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border: 2px solid var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(106,140,126,0.1) !important;
        outline: none !important;
    }
    
    /* ALERTS & MESSAGES - FIXED TO PREVENT MULTIPLE BORDERS */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 8px !important;
        padding: 1rem 1.25rem !important;
        border-left: 4px solid !important;
        margin: 1rem 0 !important;
    }
    .stSuccess { background-color: rgba(106,140,126,0.1) !important; border-left-color: var(--success) !important; }
    .stInfo { background-color: rgba(122,156,184,0.1) !important; border-left-color: var(--info) !important; }
    .stWarning { background-color: rgba(196,160,85,0.1) !important; border-left-color: var(--warning) !important; }
    
    /* ERROR MESSAGES - SINGLE BORDER ONLY */
    /* Reset parent containers */
    .stAlert,
    .stError, 
    div.stAlert,
    div.stError,
    div[data-testid="stNotification"] { 
        border: none !important;
        border-left: none !important;
        background-color: transparent !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Apply styling ONLY to innermost child */
    .stAlert > div:first-child,
    .stError > div:first-child,
    div.stAlert > div:first-child,
    div.stError > div:first-child,
    div[data-testid="stNotification"] > div:first-child { 
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
    
    /* Error message text */
    .stError *, .stAlert * { color: #4A5C54 !important; }
    .stError svg, .stAlert svg { color: #C4A055 !important; fill: #C4A055 !important; }
    .stError strong, .stError b { color: #3A4C44 !important; font-weight: 600 !important; }
    
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
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--bg-card) !important;
        color: var(--primary) !important;
        border-bottom: 3px solid var(--primary) !important;
    }
    
    /* CHAT MESSAGES */
    .stChatMessage {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    /* LINKS */
    a { color: var(--primary) !important; text-decoration: none !important; font-weight: 500 !important; }
    a:hover { color: var(--primary-dark) !important; text-decoration: underline !important; }
    
    /* OPTION MENU STYLING */
    .nav-link {
        text-align: left !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
        margin-bottom: 0.5rem !important;
        transition: all 0.2s ease !important;
    }
    .nav-link.active {
        background-color: var(--primary) !important;
        color: white !important;
        font-weight: 500 !important;
    }
    .nav-link:hover {
        background-color: var(--bg-hover) !important;
        color: var(--primary-dark) !important;
    }
    </style>
""", unsafe_allow_html=True)

class TherapyBotGuide:
    def __init__(self):
        """Initialize the bot with all its knowledge and capabilities"""
        self.crisis_words = [
            'suicide', 'kill myself', 'end my life', 'want to die',
            'hurt myself', 'overdose', 'can\'t go on', 'ending it all',
            'better off dead', 'no point living'
        ]

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

        self.assessment_questions = [
            "What's been bothering you lately? (Describe your main concerns)",
            "How long have you been feeling this way?",
            "On a scale of 1-10, how intense are these feelings?",
            "Have you tried therapy before? What was helpful or not helpful?",
            "Do you prefer online therapy or meeting in person?",
            "Do you have health insurance or need low-cost options?"
        ]

        self.professional_resources = {
            'Psychology_Today': {
                'website': 'psychologytoday.com/us/therapists',
                'description': 'Find therapists near you with photos, specialties, and reviews',
                'good_for': 'Finding local therapists',
                'cost': 'Varies by therapist ($80-200+ per session)',
                'type': 'Directory'
            },
            'Psychology_Today_Canada': {
                'website': 'psychologytoday.com/ca/therapists',
                'description': 'Find Canadian therapists with photos, specialties, and reviews',
                'good_for': 'Finding Canadian therapists',
                'cost': 'Varies by therapist (CAD $100-250+ per session)',
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
            'Inkblot_Therapy': {
                'website': 'inkblottherapy.com',
                'description': 'Canadian online therapy platform with video counselling',
                'good_for': 'Online therapy in Canada',
                'cost': 'CAD $100-140 per session or covered by insurance',
                'type': 'Online Platform'
            },
            'Open_Path': {
                'website': 'openpathcollective.org',
                'description': 'Affordable therapy sessions with sliding scale fees',
                'good_for': 'Low-cost therapy options',
                'cost': '$30-60 per session',
                'type': 'Affordable Care'
            },
            'Wellness_Together_Canada': {
                'website': 'wellnesstogether.ca',
                'description': 'Free mental health and substance use support for Canadians',
                'good_for': 'Free Canadian mental health support',
                'cost': 'Free',
                'type': 'Government Resource'
            },
            'Crisis_Text_Line': {
                'website': 'crisistextline.org',
                'phone': 'Text HOME to 741741 (US) or CONNECT to 686868 (Canada)',
                'description': '24/7 crisis support via text message - completely free',
                'good_for': 'Immediate crisis support',
                'cost': 'Free',
                'type': 'Crisis Support'
            },
            'SAMHSA': {
                'website': 'samhsa.gov/find-treatment',
                'phone': '1-800-662-4357',
                'description': 'US Government treatment locator for mental health and substance abuse',
                'good_for': 'Finding US treatment facilities',
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

        **🇺🇸 United States:**
        - ☎️ **CALL/TEXT: 988** (Suicide & Crisis Lifeline) - 24/7
        - 💬 **TEXT: HOME to 741741** (Crisis Text Line)
        - 🌐 **CHAT: suicidepreventionlifeline.org**

        **🇨🇦 Canada:**
        - ☎️ **CALL/TEXT: 9-8-8** (Suicide Crisis Helpline) - 24/7
        - 📱 **Kids Help Phone (ages 5-29): 1-800-668-6868 or Text CONNECT to 686868**
        - 🌐 **Indigenous Hope for Wellness: 1-855-242-3310** (English, French, Cree, Ojibway, Inuktitut)

        **🏥 EMERGENCY: Call 911 or go to nearest emergency room**

        **You are NOT alone. These feelings CAN change with help.**
        """

    def find_best_therapy(self, user_problems):
        """Find the best therapy type based on user's problems"""
        therapy_scores = {}
        for therapy_name in self.therapy_types:
            therapy_scores[therapy_name] = 0

        user_text = ' '.join(user_problems).lower()
        user_words = set(user_text.split())

        for therapy_name, therapy_info in self.therapy_types.items():
            for keyword in therapy_info['good_for']:
                keyword_lower = keyword.lower()
                if keyword_lower in user_text:
                    therapy_scores[therapy_name] += 2
                else:
                    keyword_words = keyword_lower.split()
                    for word in keyword_words:
                        if len(word) > 2 and word in user_words:
                            therapy_scores[therapy_name] += 1
                            break

        if max(therapy_scores.values()) > 0:
            best_therapy = max(therapy_scores, key=therapy_scores.get)
        else:
            best_therapy = 'CBT'

        return best_therapy, therapy_scores

    def get_resources_for_user(self, user_preferences):
        """Find the best resources based on what user needs"""
        recommended_resources = []
        user_text = ' '.join(user_preferences).lower()

        # Check for Canadian location indicators
        is_canada = any(word in user_text for word in ['canada', 'canadian', 'cad', 'ontario', 'quebec', 'british columbia', 'alberta'])

        if 'online' in user_text:
            recommended_resources.extend(['BetterHelp', 'Talkspace'])
            if is_canada:
                recommended_resources.append('Inkblot_Therapy')

        if any(word in user_text for word in ['cost', 'money', 'affordable', 'cheap', 'low-cost', 'sliding scale']):
            recommended_resources.append('Open_Path')
            if is_canada:
                recommended_resources.append('Wellness_Together_Canada')

        # Add appropriate directories based on location
        if is_canada:
            recommended_resources.extend(['Psychology_Today_Canada', 'Wellness_Together_Canada'])
        else:
            recommended_resources.extend(['Psychology_Today', 'SAMHSA'])
        
        recommended_resources.append('Crisis_Text_Line')

        seen = set()
        final_resources = []
        for resource in recommended_resources:
            if resource not in seen:
                seen.add(resource)
                final_resources.append(resource)

        return final_resources

def main():
    """Main Streamlit application"""
    if 'bot' not in st.session_state:
        try:
            st.session_state.bot = TherapyBotGuide()
            if not hasattr(st.session_state.bot, 'find_best_therapy'):
                st.error("⚠️ Bot initialization error: find_best_therapy method missing")
                st.stop()
        except Exception as e:
            st.error(f"⚠️ Error initializing bot: {str(e)}")
            st.stop()

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'assessment_started' not in st.session_state:
        st.session_state.assessment_started = False
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False

    st.title("🌱 Therapy Guide")
    st.markdown("**Your Personal Mental Health Resource Finder**")
    st.error("⚠️ **IMPORTANT:** This tool is for educational purposes only and is not a replacement for professional mental health care. If you're in crisis, please seek immediate help.")

    st.sidebar.title("Navigation")
    if st.sidebar.button("⚠️ Crisis Help - Get Help Now"):
        st.error(st.session_state.bot.get_crisis_help())

    st.sidebar.markdown("---")
    
    with st.sidebar.expander("⚙️ Troubleshooting"):
        st.write("Having issues? Try clearing the session:")
        if st.button("🗑️ Clear Session & Restart"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if not st.session_state.assessment_started:
        with st.sidebar:
            selected = option_menu(
                menu_title=None,
                options=["Home", "Crisis Resources", "Learn About Therapy", "Find Resources"],
                icons=["house", "exclamation-triangle", "book", "link"],
                default_index=0,
                styles={
                    "container": {"padding": "0!important"},
                    "icon": {"font-size": "1rem", "margin-right": "8px"},
                    "nav-link": {
                        "font-size": "0.9375rem",
                        "text-align": "left",
                        "margin": "0px",
                        "padding": "0.625rem 1.25rem",
                        "--hover-color": "#E0E8E4"
                    },
                    "nav-link-selected": {
                        "background-color": "#6A8C7E",
                        "font-weight": "500"
                    }
                }
            )
        
        if selected == "Home":
            show_home_page()
        elif selected == "Crisis Resources":
            show_crisis_page()
        elif selected == "Learn About Therapy":
            show_therapy_types_page()
        elif selected == "Find Resources":
            show_resources_page()
    else:
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
        **If you're having thoughts of self-harm or suicide:**
        
        🇺🇸 **US:** Call/Text **988**
        
        🇨🇦 **Canada:** Call/Text **9-8-8**
        
        📱 **Canada Youth (5-29):** **1-800-668-6868**
        
        🏥 **Emergency:** Call **911**
        """)
        if st.button("🆘 Get Crisis Resources"):
            st.error(st.session_state.bot.get_crisis_help())

    st.markdown("---")
    st.subheader("📌 Mental Health Facts")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("People with Mental Illness", "1 in 5", "Globally each year")
    with col2:
        st.metric("Therapy Effectiveness", "75%", "Show improvement")
    with col3:
        st.metric("Crisis Support", "24/7", "Available worldwide")

def show_assessment_page():
    """Show the assessment questionnaire"""
    st.header("✍️ Mental Health Assessment")
    st.write("Please answer these questions honestly. Your responses will help me recommend appropriate resources.")

    progress = st.session_state.current_question / len(st.session_state.bot.assessment_questions)
    st.progress(progress)
    st.write(f"Question {st.session_state.current_question + 1} of {len(st.session_state.bot.assessment_questions)}")
    st.markdown("---")

    if st.session_state.current_question < len(st.session_state.bot.assessment_questions):
        for i in range(st.session_state.current_question):
            question = st.session_state.bot.assessment_questions[i]
            answer = st.session_state.user_answers[i] if i < len(st.session_state.user_answers) else ""
            with st.chat_message("assistant"):
                st.write(question)
            with st.chat_message("user"):
                st.write(answer)
        
        current_question = st.session_state.bot.assessment_questions[st.session_state.current_question]
        with st.chat_message("assistant"):
            st.write(current_question)
        
        user_input = st.chat_input("Your answer...", key=f"q_{st.session_state.current_question}")
        
        if user_input:
            if st.session_state.bot.check_for_crisis(user_input):
                st.error(st.session_state.bot.get_crisis_help())
                return
            
            if len(st.session_state.user_answers) <= st.session_state.current_question:
                st.session_state.user_answers.append(user_input)
            else:
                st.session_state.user_answers[st.session_state.current_question] = user_input
            
            st.session_state.current_question += 1
            st.rerun()
    else:
        st.session_state.show_results = True
        st.rerun()

def show_assessment_results():
    """Show personalized recommendations based on assessment"""
    st.success("✓ Assessment Complete!")
    st.header("📋 Your Personalized Recommendations")

    try:
        if not hasattr(st.session_state, 'bot'):
            st.error("⚠️ Error: Bot not initialized. Please refresh the page.")
            if st.button("↻ Refresh Page"):
                st.rerun()
            return
            
        if not hasattr(st.session_state.bot, 'find_best_therapy'):
            st.error("⚠️ Error: Bot is missing required methods. Please refresh the page.")
            if st.button("↻ Refresh Page"):
                st.rerun()
            return
            
        best_therapy, therapy_scores = st.session_state.bot.find_best_therapy(st.session_state.user_answers)
        therapy_info = st.session_state.bot.therapy_types[best_therapy]
    except Exception as e:
        st.error(f"⚠️ Error generating recommendations: {str(e)}")
        if st.button("↻ Try Again"):
            st.session_state.show_results = False
            st.rerun()
        return

    st.subheader("⭐ Recommended Therapy Type")
    with st.container():
        st.markdown(f"### {therapy_info['name']}")
        st.write(f"**What it does:** {therapy_info['description']}")
        st.write(f"**Example:** {therapy_info['example']}")
        st.write(f"**Typical duration:** {therapy_info['duration']}")
        st.write(f"**Effectiveness:** {therapy_info['effectiveness']}")

    with st.expander("📈 See how other therapies scored for you"):
        st.write("**Your therapy scores:** (sorted from highest to lowest)")
        sorted_scores = sorted(therapy_scores.items(), key=lambda x: x[1], reverse=True)
        for therapy_name, score in sorted_scores:
            therapy_data = st.session_state.bot.therapy_types[therapy_name]
            if score > 0:
                st.write(f"✅ **{therapy_data['name']}:** {score} matches")
            else:
                st.write(f"⭕ **{therapy_data['name']}:** {score} matches")

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

    st.subheader("→ Next Steps")
    st.write("""
    1. **Review** the therapy type recommendation above
    2. **Visit** one or more of the recommended websites
    3. **Contact** a mental health professional
    4. **Remember** that finding the right therapist may take time
    5. **Don't give up** - help is available!
    """)

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

    st.subheader("🇺🇸 United States Crisis Resources")
    us_crisis_resources = [
        {"name": "National Suicide Prevention Lifeline", "contact": "Call or Text 988", "description": "24/7 crisis support"},
        {"name": "Crisis Text Line", "contact": "Text HOME to 741741", "description": "24/7 text-based crisis support"},
        {"name": "SAMHSA National Helpline", "contact": "1-800-662-4357", "description": "Treatment referral service"},
        {"name": "National Domestic Violence Hotline", "contact": "1-800-799-7233", "description": "24/7 support for domestic violence"},
        {"name": "LGBTQ National Hotline", "contact": "1-888-843-4564", "description": "Support for LGBTQ+ individuals"},
        {"name": "Veterans Crisis Line", "contact": "1-800-273-8255", "description": "24/7 support for veterans"}
    ]

    for resource in us_crisis_resources:
        with st.container():
            st.markdown(f"**{resource['name']}**")
            st.markdown(f"☎️ {resource['contact']}")
            st.write(resource['description'])
            st.markdown("---")

    st.subheader("🇨🇦 Canadian Crisis Resources")
    canada_crisis_resources = [
        {"name": "9-8-8: Suicide Crisis Helpline", "contact": "Call or Text 9-8-8", "description": "24/7 for anyone thinking about suicide or worried about someone they know"},
        {"name": "Kids Help Phone", "contact": "1-800-668-6868 or Text CONNECT to 686868", "description": "24/7 support for youth aged 5-29"},
        {"name": "Hope for Wellness Help Line", "contact": "1-855-242-3310 or online chat", "description": "24/7 support for Indigenous peoples (English, French, Cree, Ojibway, Inuktitut)"},
        {"name": "Talk Suicide Canada", "contact": "1-833-456-4566 or text 45645", "description": "24/7 suicide prevention and support"},
        {"name": "Wellness Together Canada", "contact": "Visit wellnesstogether.ca", "description": "Free mental health and substance use support"}
    ]

    for resource in canada_crisis_resources:
        with st.container():
            st.markdown(f"**{resource['name']}**")
            st.markdown(f"☎️ {resource['contact']}")
            st.write(resource['description'])
            st.markdown("---")

def show_therapy_types_page():
    """Show information about different therapy types"""
    st.header("💭 Types of Therapy")
    st.write("Learn about different therapeutic approaches and what they help with.")

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

    resource_types = ['All'] + list(set([r['type'] for r in st.session_state.bot.professional_resources.values()]))
    selected_type = st.selectbox("Filter by type:", resource_types)

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

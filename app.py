import streamlit as st
import time
import re

# --- 1. FULL, CORRECTED CSS BLOCK (Includes fix for overlapping elements) ---
# This CSS implements the "Natural Harmony Design System" aesthetic and corrects 
# the sidebar overlap issue reported on the deployed app.
CSS_STYLE = """
<style>

/* CSS VARIABLES */
:root {
    --primary: #6A8C7E; /* Sage Green */
    --primary-dark: #5A6C5E;
    --primary-darker: #4A5C4E;
    --primary-light: #8BA99D;
    --secondary: #A8B8A8;
    --secondary-light: #C0D0C0;
    --bg-primary: #F0F4F2; /* Very Light Green-Gray */
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

/* FIX FOR OVERLAPPING BUTTONS/TEXT */
div[data-testid="stVerticalBlock"] {
    overflow-x: hidden !important; /* Prevents content from overflowing horizontally in containers, fixing sidebar button issues. */
}
    
/* PAGE BACKGROUND - SOFT GREEN - VERY AGGRESSIVE */
html, body, .main, 
.stApp, 
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section[data-testid="stMain"],
.main .block-container,
[class*="main"] { 
    background-color: var(--bg-primary) !important; 
    background: var(--bg-primary) !important;
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
    
/* FIX WHITE TOP AREA */
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
    background-color: var(--bg-primary) !important;
    background: var(--bg-primary) !important;
}
    
/* HIDE/FIX STREAMLIT HEADER */
header[data-testid="stHeader"] {
    background-color: var(--bg-primary) !important;
    background: var(--bg-primary) !important;
}
header[data-testid="stHeader"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 100%;
    background-color: var(--bg-primary) !important;
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
    
/* FORCE LEFT BORDER ON ERROR PARENT CONTAINERS */
div[data-testid="stNotification"],
div[class*="Alert"],
div[class*="Error"] {
    border-left: 5px solid #C4A055 !important;
}
</style>
"""

# --- 2. CONFIGURATION AND DATA ---

# Therapy types with their core focus keywords for scoring
THERAPY_DATA = {
    "CBT (Cognitive Behavioral Therapy)": {
        "description": "Focuses on identifying and changing negative thought patterns and behaviors to solve current problems.",
        "keywords": ["thoughts", "patterns", "challenge thoughts", "cognitive distortions", "homework", "behavior change", "present", "actionable", "coping skills", "vicious cycle"]
    },
    "Psychodynamic Therapy": {
        "description": "Explores unconscious patterns, past experiences, and childhood events to understand current feelings and behaviors.",
        "keywords": ["unconscious", "past", "childhood", "relationships", "patterns", "insight", "dreams", "transference", "deep analysis", "long-term"]
    },
    "Schema Therapy": {
        "description": "Integrates CBT, attachment theory, and psychodynamic concepts to treat deep-seated emotional needs and core beliefs (schemas).",
        "keywords": ["schemas", "core beliefs", "emotional needs", "parenting", "modes", "vulnerability", "abandonment", "unmet needs", "long-standing"]
    },
    "DBT (Dialectical Behavior Therapy)": {
        "description": "Teaches skills in mindfulness, emotional regulation, distress tolerance, and interpersonal effectiveness.",
        "keywords": ["skills", "mindfulness", "emotion regulation", "distress tolerance", "interpersonal", "crisis", "intense emotions", "borderline", "validation"]
    }
}

# Chat questions
QUESTIONS = [
    "1/6: When you think about your challenges, do you focus more on **specific situations** and how to change your immediate **thoughts** and **actions** right now, or more on **long-standing patterns** and your **past**?",
    "2/6: How important is it for you to explore **early life experiences** and **childhood** to gain **insight** into why you feel the way you do today?",
    "3/6: Which goal resonates more with you: learning specific, **actionable skills** to manage intense **emotions** and **crisis moments**, or understanding the **origin** of your **core beliefs** and deep-seated **patterns**?",
    "4/6: When distressed, do you usually feel overwhelmed by **unstable emotions** and **relationship issues**, or are you primarily focused on breaking a specific **negative thought loop**?",
    "5/6: Do you prefer a highly **structured approach** with specific **homework** and defined steps, or a more **exploratory**, flexible conversation?",
    "6/6: If you had to describe your key struggle, would it be related to self-control, **emotional chaos**, and **intense moods**, or feelings of being **stuck** in recurring **negative thought patterns**?"
]

# Crisis keywords for emergency detection
CRISIS_KEYWORDS = [
    "suicide", "harm", "kill myself", "end my life", "suicidal", "emergency", 
    "hurt myself", "cutting", "overdose", "self-injure"
]

# --- 3. HELPER FUNCTIONS ---

def get_session_state_value(key, default):
    """Safely retrieves a session state value."""
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]

def initialize_session():
    """Initializes Streamlit session state variables."""
    get_session_state_value('messages', [{"role": "bot", "content": "Hello! I'm your Therapy Guide. I'll ask you a few questions to find the best-matched therapy style for you. Please answer honestly."}])
    get_session_state_value('current_question_index', 0)
    get_session_state_value('assessment_in_progress', True)
    get_session_state_value('scores', {key: 0 for key in THERAPY_DATA})
    get_session_state_value('show_results', False)
    get_session_state_value('page', 'Assessment')

def score_response(response, scores):
    """
    Scores the user response against therapy keywords.
    - +2 points for exact phrase match (high confidence)
    - +1 point for individual word match (general relevance)
    """
    normalized_response = response.lower()
    
    # Simple tokenization for word-based matching
    response_words = set(re.findall(r'\b\w+\b', normalized_response))

    for therapy, data in THERAPY_DATA.items():
        score = 0
        
        # Scoring Logic: 
        # 1. Check for exact phrase matches (gives higher score)
        # 2. Check for individual word match

        for keyword in data['keywords']:
            # 1. Exact phrase match (e.g., "core beliefs")
            if keyword in normalized_response:
                score += 2
            
            # 2. Individual word match (e.g., "belief" matches "beliefs")
            keyword_words = set(re.findall(r'\b\w+\b', keyword.lower()))
            if keyword_words.intersection(response_words):
                score += 1
                
        scores[therapy] += score

def check_for_crisis(response):
    """Checks if the user response contains crisis keywords."""
    return any(kw in response.lower() for kw in CRISIS_KEYWORDS)

def reset_session():
    """Clears and re-initializes the session state."""
    st.session_state.clear()
    initialize_session()
    st.session_state['messages'] = [{"role": "bot", "content": "Session reset. Let's start the assessment again! I'll ask you a few questions to find the best-matched therapy style for you."}]

def display_recommendation_card(therapy_name, data, score):
    """Displays the personalized recommendation card."""
    col1, col2 = st.columns([1, 4])
    
    # Calculate relative score for display (max score possible is rough estimate)
    max_possible_score = 30 # A reasonable max for 6 questions * max 5 keywords * 2 points

    with col1:
        st.metric(label="Match Score", value=f"{score}")

    with col2:
        st.markdown(f"### 🎯 {therapy_name}")
        st.markdown(f"**Focus:** {data['description']}")
        
        # Display keywords that were matched (for user transparency)
        all_keywords = data['keywords']
        matched_keywords = [
            kw for kw in all_keywords 
            if any(re.search(r'\b' + re.escape(w) + r'\b', ' '.join(
                [msg['content'].lower() for msg in st.session_state.messages if msg['role'] == 'user']
            )) for w in re.findall(r'\b\w+\b', kw.lower()))
        ]
        
        # Note: Showing matched words is complex and often too verbose, simplify to confidence display
        st.progress(score / max_possible_score, text=f"Confidence Level: **{int((score / max_possible_score) * 100)}%**")
        
        st.markdown(f"<p style='font-size:0.9em; color:var(--text-muted);'>*This recommendation is based on {score} alignment points across your answers.</p>", unsafe_allow_html=True)

# --- 4. STREAMLIT UI COMPONENTS ---

def apply_css():
    """Applies the custom CSS style block."""
    st.set_page_config(layout="wide", page_title="Therapy Guide", page_icon="🧘‍♀️")
    st.markdown(CSS_STYLE, unsafe_allow_html=True)

def troubleshooting_menu():
    """Displays the troubleshooting and session reset menu in the sidebar."""
    with st.expander("⚙️ Troubleshooting"):
        st.markdown("If the application is slow or visuals are broken, click below to clear the session state and restart.")
        # Ensure emoji works for clear button
        if st.button("🗑️ Clear Session & Restart", key="reset_button"):
            reset_session()
            st.rerun()

def sidebar_menu():
    """Displays the title and main actions in the sidebar."""
    with st.sidebar:
        # Title with an emoji icon for reliability
        st.title("🧘‍♀️ Therapy Guide AI")
        st.markdown("""
        This tool uses a brief, 6-question chat to match your stated needs and preferences
        to common therapeutic modalities.
        ***
        """)
        
        # Start/Reset Button
        if st.session_state.assessment_in_progress or st.session_state.show_results:
            # Use 'Start' or 'Begin' language along with emoji for reliability
            if st.button("🔄 Start New Assessment", key="sidebar_reset"):
                reset_session()
                st.rerun()
        else:
             # Use 'Begin' language along with emoji for reliability
             st.button("▶️ Begin Assessment", key="sidebar_start", on_click=lambda: st.session_state.update(assessment_in_progress=True, current_question_index=0))

        st.markdown("---")
        troubleshooting_menu()

def display_tabs():
    """Displays the main content tabs (Assessment/Results, Types, Resources)."""
    tab_assessment, tab_types, tab_resources = st.tabs(["💬 Assessment", "📚 Therapy Types", "🌐 Resources"])

    with tab_assessment:
        if st.session_state.show_results:
            display_results_page()
        else:
            run_assessment()

    with tab_types:
        st.header("📚 Explore Therapy Modalities")
        st.markdown("Each therapy style addresses different needs. Understanding the focus can help you choose the right path.")
        for name, data in THERAPY_DATA.items():
            with st.container():
                st.markdown(f"**{name}**")
                st.markdown(data['description'])
                st.markdown("---")

    with tab_resources:
        st.header("🌐 Emergency & General Resources")
        st.markdown("""
        If you are experiencing a crisis, please use these emergency contacts. This tool is **not a substitute for professional help.**
        
        ### 🚨 Crisis Hotlines (24/7)
        * **988 Suicide & Crisis Lifeline (US/Canada):** Call or text **988**
        * **Crisis Text Line:** Text **HOME** to **741741**
        * **The Trevor Project (LGBTQ youth):** Call **1-866-488-7386**
        
        ### 🔗 General Resources
        * **Psychology Today:** Find a therapist by location and specialty.
        * **SAMHSA National Helpline (US):** 1-800-662-HELP (4357) - Treatment referral and information.
        * **NAMI (National Alliance on Mental Illness):** Provides education, support, and advocacy.
        """)

def run_assessment():
    """Manages the chat flow, question display, and scoring."""
    
    # Display current chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Show question if assessment is active
    q_index = st.session_state.current_question_index
    if st.session_state.assessment_in_progress and q_index < len(QUESTIONS):
        
        # Bot asks the question
        if st.session_state.messages[-1]['content'] != QUESTIONS[q_index]:
             with st.chat_message("bot"):
                st.markdown(QUESTIONS[q_index])
             st.session_state.messages.append({"role": "bot", "content": QUESTIONS[q_index]})

        # User input logic
        user_input = st.chat_input("Type your response here...", key=f"q_{q_index}")
        
        if user_input:
            # 1. Check for Crisis
            if check_for_crisis(user_input):
                st.session_state.show_results = False
                st.session_state.assessment_in_progress = False
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.error("🚨 **Immediate Crisis Detected.** Your safety is paramount.")
                st.warning("Please stop using this tool and call or text **988** (US/Canada) immediately.")
                st.stop()
            
            # 2. Add user response to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # 3. Score the response
            score_response(user_input, st.session_state.scores)
            
            # 4. Move to next question or show results
            st.session_state.current_question_index += 1
            st.session_state.show_results = (st.session_state.current_question_index >= len(QUESTIONS))
            
            # Rerun to update chat/question
            time.sleep(0.5) # Slight delay for smooth UI transition
            st.rerun()

    elif st.session_state.show_results:
        # Final message when done
        if st.session_state.messages[-1]['role'] != 'bot' or 'Thank you for completing the assessment' not in st.session_state.messages[-1]['content']:
            with st.chat_message("bot"):
                st.markdown("Thank you for completing the assessment. Please review your personalized results below!")
            st.session_state.messages.append({"role": "bot", "content": "Thank you for completing the assessment. Please review your personalized results below!"})
        display_results_page()
    else:
        # Initial state message
        st.info("Start the assessment in the sidebar or click 'Begin Assessment' above.")


def display_results_page():
    """Displays the final scores and personalized recommendation."""
    st.header("✅ Assessment Complete: Your Personalized Recommendation")
    
    # Determine the best match
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda item: item[1], reverse=True)
    best_match_name = sorted_scores[0][0]
    best_match_score = sorted_scores[0][1]
    
    st.markdown("---")
    
    # --- Best Match Display ---
    st.subheader(f"🥇 Best Match: {best_match_name}")
    st.info(f"Based on your answers, your needs strongly align with the principles of **{best_match_name}**.", icon="💡")
    
    display_recommendation_card(
        best_match_name, 
        THERAPY_DATA[best_match_name], 
        best_match_score
    )

    st.markdown("---")
    
    # --- Score Breakdown ---
    st.subheader("📋 Full Score Breakdown")
    st.markdown("Here is how all four modalities scored based on your input:")
    
    # Display the remaining scores
    for name, score in sorted_scores[1:]:
        with st.container():
            col_name, col_prog = st.columns([1, 2])
            
            max_possible_score = 30 # Use a consistent max for comparison
            confidence_percentage = int((score / max_possible_score) * 100)

            col_name.markdown(f"**{name}**")
            col_prog.progress(score / max_possible_score, text=f"Match: **{confidence_percentage}%**")


# --- 5. MAIN APPLICATION LOGIC ---

if __name__ == "__main__":
    apply_css()
    initialize_session()
    sidebar_menu()
    display_tabs()

import streamlit as st
import random

# --------------------------
# Helper Functions
# --------------------------
def is_crisis(text: str) -> bool:
    crisis_words = ["suicide", "kill myself", "end it all", "can't go on"]
    return any(word in text.lower() for word in crisis_words)

def crisis_help():
    st.error("⚠️ It sounds like you might be in crisis.")
    st.markdown("""
    If you are in immediate danger, please **call your local emergency number right now**.  
    You are not alone — here are some resources:  

    - 📞 **988 (US Suicide & Crisis Lifeline)**  
    - 📞 **116 123 (Samaritans UK & ROI)**  
    - 🌍 [Find international hotlines here](https://findahelpline.com/)  
    """)
    st.stop()

def find_best_therapy(answers):
    """Keyword-based matching with examples and more dynamic therapy recommendations."""
    combined = " ".join(answers).lower()

    therapies = {
        "cbt": {
            "name": "Cognitive Behavioral Therapy (CBT)",
            "desc": "Helpful for reframing negative thought patterns.",
            "example": 'Learning to challenge thoughts like *"I always fail"* and replace them with balanced perspectives.',
            "keywords": ["negative thoughts", "breakup", "stress", "guilt", "self-criticism"]
        },
        "exposure": {
            "name": "Exposure Therapy",
            "desc": "Useful for gradually facing fears and reducing avoidance.",
            "example": 'If crowds trigger anxiety, starting with short visits to busy places and increasing over time.',
            "keywords": ["fear", "worry", "panic", "anxious", "phobia", "avoidance"]
        },
        "trauma": {
            "name": "Trauma-focused Therapy",
            "desc": "Designed to help process and heal from traumatic events.",
            "example": "Working safely through flashbacks and building grounding techniques.",
            "keywords": ["trauma", "flashback", "abuse", "ptsd", "violence"]
        },
        "grief": {
            "name": "Grief Counseling",
            "desc": "Supports processing emotions after loss.",
            "example": "Finding ways to honor memories while adjusting to daily life.",
            "keywords": ["sad", "loss", "grief", "mourning", "bereavement"]
        },
        "mindfulness": {
            "name": "Mindfulness-based Therapy",
            "desc": "Builds awareness and acceptance.",
            "example": "Practicing noticing your breath when stressful thoughts appear.",
            "keywords": ["stress", "overthinking", "mindfulness", "present moment", "relaxation"]
        },
        "act": {
            "name": "Acceptance & Commitment Therapy (ACT)",
            "desc": "Helps align actions with values.",
            "example": "Choosing to connect with friends even when feeling anxious.",
            "keywords": ["values", "meaning", "acceptance", "anxiety", "life purpose"]
        },
        "solution": {
            "name": "Solution-Focused Therapy",
            "desc": "Emphasizes goals and practical steps forward.",
            "example": "Identifying one small thing that went well today and building on it.",
            "keywords": ["problem solving", "goal", "solution", "practical", "improvement"]
        }
    }

    # Score each therapy based on keyword matches
    scores = {key: 0 for key in therapies}
    for key, therapy in therapies.items():
        for keyword in therapy["keywords"]:
            if keyword in combined:
                scores[key] += 1

    # Choose therapy with highest score; tie-breaker random
    max_score = max(scores.values())
    best_choices = [key for key, score in scores.items() if score == max_score]
    chosen = random.choice(best_choices)
    return therapies[chosen]

# --------------------------
# App Setup
# --------------------------
st.set_page_config(page_title="Therapy Bot", page_icon="💬", layout="centered")

if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "history" not in st.session_state:
    st.session_state.history = []  # Stores (Q, A) pairs

questions = [
    "❓ What's been bothering you lately?",
    "❓ How long have you been feeling this way?",
    "❓ How does it affect your daily life?",
    "❓ What helps you cope, even a little?",
    "❓ Have you tried therapy before? What was helpful or not helpful?",
    "❓ Do you prefer online therapy or in-person sessions?"
]

# --------------------------
# Chat UI
# --------------------------
st.title("💬 Therapy Bot")
st.markdown("This is a supportive space. Please note I'm not a substitute for professional care.")

# Show full chat history
for q, a in st.session_state.history:
    with st.chat_message("assistant"):
        st.write(q)
    with st.chat_message("user"):
        st.write(a)

# Current step
step = st.session_state.step

if step < len(questions):
    with st.chat_message("assistant"):
        st.write(questions[step])
    user_input = st.text_input("Your response:", key=f"q{step}")

    if user_input:
        if is_crisis(user_input):
            crisis_help()

        st.session_state.answers.append(user_input)
        st.session_state.history.append((questions[step], user_input))
        st.session_state.step += 1
        st.rerun()

else:
    # End of questions
    st.success("✅ Thank you for sharing. Based on your responses, here’s a suggestion:")

    suggestion = find_best_therapy(st.session_state.answers)
    with st.chat_message("assistant"):
        st.write(f"**{suggestion['name']}** — {suggestion['desc']}")
        st.caption(f"💡 Example: {suggestion['example']}")

    if st.button("🔄 Restart"):
        st.session_state.step = 0
        st.session_state.answers = []
        st.session_state.history = []
        st.rerun()

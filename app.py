# Therapy Bot Guide - Streamlit Web Application
# Mental Health Support and Resource Finder

"""
🌱 IMPROVED THERAPY BOT WITH FLEXIBLE KEYWORD MATCHING

KEY FEATURES:
✓ Detects crisis situations and shows emergency help
✓ Flexible keyword matching for therapy recommendations
✓ Offers relevant mental health resources
✓ Interactive Q&A chatbot flow using Streamlit
"""

import streamlit as st
from datetime import datetime
import re
import random

# ------------------------
# Page configuration
# ------------------------
st.set_page_config(
    page_title="Therapy Guide",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded"
)


# ------------------------
# Therapy Bot Class
# ------------------------
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
                    'anxiety', 'anxious', 'anxieties', 'depression', 'depressed',
                    'sad', 'worry', 'worried', 'panic', 'negative thoughts',
                    'fear', 'stress', 'overthinking', 'breakup', 'guilt'
                ],
                'description': 'Helps identify and change negative thought patterns and behaviors.',
                'example': 'Challenging thoughts like "I always fail" and replacing them with balanced ones.'
            },
            'DBT': {
                'name': 'Dialectical Behavior Therapy (DBT)',
                'good_for': [
                    'self harm', 'intense emotions', 'anger', 'relationships',
                    'borderline', 'unstable', 'impulsive', 'overwhelmed'
                ],
                'description': 'Focuses on managing intense emotions and improving relationships.',
                'example': 'Using breathing and distress tolerance when feeling overwhelmed.'
            },
            'Family_Therapy': {
                'name': 'Family or Couples Therapy',
                'good_for': [
                    'family problems', 'relationship issues', 'communication',
                    'conflict', 'divorce', 'breakup', 'trust', 'intimacy'
                ],
                'description': 'Helps families and couples improve communication and resolve conflicts.',
                'example': 'Learning to express feelings without fighting or shutting down.'
            },
            'Trauma_Therapy': {
                'name': 'Trauma-Focused Therapy (EMDR/CPT)',
                'good_for': [
                    'trauma', 'ptsd', 'abuse', 'flashbacks', 'violence', 'accident',
                    'pain', 'hurt', 'haunting', 'disturbing'
                ],
                'description': 'Helps process and heal from traumatic experiences safely.',
                'example': 'Working through traumatic memories using guided techniques.'
            },
            'Humanistic': {
                'name': 'Humanistic / Person-Centered Therapy',
                'good_for': [
                    'self esteem', 'identity', 'growth', 'purpose', 'authenticity',
                    'self-acceptance', 'values', 'compassion'
                ],
                'description': 'Focuses on personal growth and self-acceptance.',
                'example': 'Exploring your authentic self and building self-compassion.'
            }
        }

        # Assessment questions
        self.questions = [
            "What's been bothering you lately?",
            "How long have you been feeling this way?",
            "On a scale of 1-10, how intense are these feelings?",
            "Have you tried therapy before? What was helpful or not helpful?",
            "Do you prefer online therapy or meeting in person?",
            "Do you have health insurance or need low-cost options?"
        ]

        # Professional resources
        self.resources = {
            'Psychology Today': 'https://www.psychologytoday.com/us/therapists',
            'BetterHelp': 'https://www.betterhelp.com/',
            'Talkspace': 'https://www.talkspace.com/',
            'Open Path': 'https://openpathcollective.org/',
            'Crisis Text Line': 'https://www.crisistextline.org/',
            'SAMHSA (Treatment Locator)': 'https://findtreatment.gov/'
        }

    # ------------------------
    # Core Methods
    # ------------------------
    def check_for_crisis(self, message: str) -> bool:
        if not message:
            return False
        message_lower = message.lower()
        return any(word in message_lower for word in self.crisis_words)

    def get_crisis_help(self):
        return """
        ⚠️ **IMMEDIATE HELP AVAILABLE**

        If you are thinking about harming yourself, please reach out **right now**:
        - ☎️ **988** (Suicide & Crisis Lifeline) – 24/7 in the U.S.
        - 💬 **Text HOME to 741741** (Crisis Text Line)
        - 🌐 [Find international hotlines](https://findahelpline.com)
        """

    def find_best_therapy(self, answers):
        combined_text = " ".join(answers).lower()
        words = set(re.findall(r'\b[a-zA-Z]{3,}\b', combined_text))

        scores = {t: 0 for t in self.therapy_types}

        for therapy, info in self.therapy_types.items():
            for keyword in info["good_for"]:
                keyword_lower = keyword.lower()
                if keyword_lower in combined_text:
                    scores[therapy] += 2
                else:
                    for word in keyword_lower.split():
                        if word in words:
                            scores[therapy] += 1
                            break

        max_score = max(scores.values())
        best = random.choice([k for k, v in scores.items() if v == max_score]) if max_score > 0 else "CBT"
        return self.therapy_types[best], scores


# ------------------------
# Streamlit Application
# ------------------------
def main():
    st.title("🌱 Therapy Guide")
    st.markdown("A supportive space to find suitable therapy options and helpful resources.")

    if "bot" not in st.session_state:
        st.session_state.bot = TherapyBotGuide()
    bot = st.session_state.bot

    if "step" not in st.session_state:
        st.session_state.step = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "history" not in st.session_state:
        st.session_state.history = []

    for q, a in st.session_state.history:
        with st.chat_message("assistant"):
            st.write(q)
        with st.chat_message("user"):
            st.write(a)

    step = st.session_state.step

    if step < len(bot.questions):
        question = bot.questions[step]
        with st.chat_message("assistant"):
            st.write(question)
        user_input = st.text_input("Your answer:", key=f"q{step}")

        if user_input:
            if bot.check_for_crisis(user_input):
                st.error(bot.get_crisis_help())
                st.stop()

            st.session_state.answers.append(user_input)
            st.session_state.history.append((question, user_input))
            st.session_state.step += 1
            st.rerun()

    else:
        with st.chat_message("assistant"):
            st.success("✅ Thank you for sharing. Based on your responses:")

        best_therapy, all_scores = bot.find_best_therapy(st.session_state.answers)
        st.subheader(best_therapy['name'])
        st.markdown(best_therapy['description'])
        st.caption(f"💡 Example: {best_therapy['example']}")

        with st.expander("📊 See all scores"):
            st.json(all_scores)

        st.divider()
        st.subheader("🌍 Recommended Resources")
        for name, link in bot.resources.items():
            st.markdown(f"- [{name}]({link})")

        if st.button("🔄 Restart"):
            for key in ["step", "answers", "history"]:
                st.session_state[key] = [] if key != "step" else 0
            st.rerun()


if __name__ == "__main__":
    main()

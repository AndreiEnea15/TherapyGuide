🌱 Therapy Guide – Streamlit Web App (Version 3.0)
A supportive chatbot designed to help users explore therapy options and mental health resources. Built with Streamlit by Andrei Enea.

Live Demo: therapyguide.streamlit.app

🛠️ Core Technical Features
Heuristic Recommendation Engine: Employs a weighted scoring algorithm to match user-described symptoms against a dictionary of therapy-specific keywords (e.g., CBT, DBT, Trauma-Focused).

Direct Matches: +2 weight.

Partial/Word Matches: +1 weight.

Safety & Crisis Safeguard: A real-time monitoring layer that scans user input for high-risk strings. If detected, the app overrides standard flow to inject immediate emergency resources via a dedicated crisis UI component.

Geo-Filtering Logic: Dynamically adjusts recommended resource lists (directories, online platforms, and government services) by parsing user input for regional indicators (e.g., "Canada," "US," "Ontario").

Custom Design System: Implements a "Natural Harmony" UI using injected CSS-in-Python. This overrides default Streamlit components to provide a calming, accessibility-focused interface with custom typography and state-specific alert styling.

💻 Stack & Architecture
Frontend/Backend: Streamlit (Python)

State Management: st.session_state manages the multi-step assessment workflow and user history.

Navigation: streamlit_option_menu for a multi-page SPA (Single Page Application) feel.

Logic: Regular expressions and case-insensitive string processing.

🧠 Features
Interactive chat-based mental health assessment

Flexible keyword-matching therapy recommender

Full CSS design system (“Natural Harmony”)

Crisis detection and immediate help options

Therapy education tabs

Professional resource directory

Troubleshooting section (Clear session & restart)
⚙️ Installation
Bash

git clone https://github.com/AndreiEnea15/TherapyGuide.git
cd TherapyGuide
pip install -r requirements.txt
streamlit run app.py

🔄 Recent Updates (Version 3.0)
Major Additions by Andrei Enea

🌿 Natural Harmony Design System (Full CSS Integration)

🧠 Improved Therapy Algorithm – Flexible keyword & phrase scoring

💬 Chat-based Assessment Flow

⚠️ Crisis Help Sidebar Button

🧹 Session Troubleshooting – “Having issues? Try clearing the session”

🔗 Comprehensive Resource Tabs and Therapy Info

🩺 Disclaimer
This app is not a substitute for professional mental-health care. If you are in crisis, please seek immediate help or visit findahelpline.com.

🛠️ Troubleshooting
If you encounter issues (e.g., chat stuck, missing buttons):

Open the sidebar and expand “⚙️ Troubleshooting”.

Click “🗑️ Clear Session & Restart”.

The app will reload fresh and restore normal behavior.

# 🌱 Therapy Guide – Streamlit Web App

A supportive chatbot designed to help users explore therapy options and mental health resources.  
Built with **Streamlit** by **Andrei Enea**.

## 🧠 Features
- 6 interactive mental health questions
- Crisis word detection and emergency resources
- Flexible keyword-based therapy matching
- Therapy recommendations with examples
- Helpful online resource links

## ⚙️ Installation

```bash
git clone https://github.com/AndreiEnea15/TherapyGuide.git
cd TherapyGuide
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔄 Recent Updates (Version 2.0)

**Major Improvements by Andrei Enea**

- 🌿 Rebuilt the algorithm for **flexible keyword matching**  
  → Handles variations like *“anxious”* vs *“anxiety”*  
  → Adds weighted scoring (exact phrase = 2 pts, related word = 1 pt)
- 🧠 Added **new therapy types and keyword categories**
  → Now includes CBT, DBT, Family Therapy, Trauma Therapy, and Humanistic  
- ⚠️ Improved **crisis detection system** with more expressions
- 🌍 Added **mental health resource directory** (BetterHelp, SAMHSA, Crisis Text Line, etc.)
- 💬 Upgraded **conversation flow** — smooth, restartable chat logic
- 🧹 Simplified UI by **removing custom CSS** for better GitHub readability
- 🧾 Added **clear documentation and setup instructions**

---

## 🩺 Disclaimer
This app is **not a substitute for professional care**.  
If you are in crisis, please call your local emergency number or visit [findahelpline.com](https://findahelpline.com/).

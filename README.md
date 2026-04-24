# 🤍 GriefBot: An Empathetic AI Grief & Loss Companion

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/AI_Engine-Google_Gemini_2.0_Flash-4285F4?logo=google&logoColor=white)
![Hackathon](https://img.shields.io/badge/Status-Hackathon_Project-gold)

## 🌐 Live Demo
**[Click here to experience GriefBot Live!](https://griefbot-hackathon.streamlit.app/)**

**GriefBot** is a multimodal, emotionally intelligent AI companion designed to guide users through the isolating experience of loss. Built for the **Health & Wellbeing** hackathon track.

## 💡 The Inspiration
The mental health tech space is saturated with apps for productivity, anxiety, and daily stress - but **grief** is almost completely ignored. When someone experiences a profound loss (a loved one, a pet, a relationship, or a career), they are often left to navigate a highly non-linear, isolating journey alone. 

GriefBot bridges this gap by providing a safe, private, and judgment-free digital space for users to process their emotions, using advanced generative AI to actively listen and validate their feelings.

---

## ✨ Core Features & How They Work

### 1. 🎙️ Two-Way Voice Interaction
* **How it works:** Users can speak directly to GriefBot using their microphone (powered by `streamlit-mic-recorder`). The app transcribes the audio, sends it to the AI, and generates a spoken audio response using Google Text-to-Speech (`gTTS`). 
* **Why it matters:** Typing can feel exhausting when grieving. Voice interaction makes the companion feel deeply human and accessible.

### 2. 🧠 Empathetic AI Chat Engine
* **How it works:** Powered by **Google Gemini 2.0 Flash**, the bot is strictly prompted with custom system instructions to act as a supportive, non-medical companion. It retains conversation history to provide contextual, continuous support rather than treating every message as a blank slate.

### 3. 🗺️ Personalized Grief Mapping
* **How it works:** During onboarding, the user selects their type of loss (Person, Pet, Relationship, or Job). The app dynamically generates a custom psychological "Journey Map" showing the stages of grief specific to that loss (e.g., losing a job brings "Financial Anxiety," while losing a pet brings "Missing the Routine").

### 4. 🫁 Interactive Grounding Exercise
* **How it works:** An embedded HTML/CSS/JS animation acts as a "Breathing Bot." It visually guides the user through a 4-second box-breathing technique (Breathe In, Hold, Breathe Out).
* **Why it matters:** Severe grief is often accompanied by acute anxiety or panic attacks. This grounds the user in their physical body.

### 5. 📖 Private Memory Book
* **How it works:** A secure, local digital keepsake. Users can write down cherished memories, which are time-stamped and displayed in a beautiful, structured feed so they are never forgotten.

---

## 🛠️ Tech Stack

* **Frontend & UI:** [Streamlit](https://streamlit.io/)
* **Large Language Model:** [Google Gemini 2.0 Flash](https://ai.google.dev/) via the `google-genai` SDK
* **Voice Synthesis (TTS):** `gTTS` (Google Text-to-Speech)
* **Voice Recognition (STT):** `streamlit-mic-recorder`
* **Custom Frontend Components:** HTML/CSS/JavaScript integrated via `streamlit.components.v1`

---

## 🚀 How to Run Locally

If you want to run this project on your own machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/GriefBot.git
   cd GriefBot
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Gemini API Key:**
   Open `griefbot_app.py` in a text editor and replace the placeholder text `"YOUR_GEMINI_API_KEY_HERE"` with your actual API key from [Google AI Studio](https://aistudio.google.com/).

5. **Launch the application:**
   ```bash
   streamlit run griefbot_app.py
   ```

---

## ⚠️ Disclaimer
*GriefBot is a hackathon prototype designed for emotional support and companionship. It does not provide medical or psychiatric advice and is not a replacement for professional therapy. If you are in crisis, please contact your local emergency services.*

import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components
from gtts import gTTS
import io
from streamlit_mic_recorder import speech_to_text
from google import genai
from google.genai import types

# --- Setup the Gemini AI Connection ---
# Put your Gemini API key inside the quotes below!
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def get_real_ai_response(chat_history):
    try:
        # Build conversation history for Gemini
        gemini_contents = []
        for msg in chat_history:
            # Skip the very first greeting message
            if msg["content"] == "Hello. I'm here to support you through your grief. Take your time, there is no rush.":
                continue
            role = "model" if msg["role"] == "assistant" else "user"
            gemini_contents.append(
                types.Content(role=role, parts=[types.Part(text=msg["content"])])
            )

        # Send the full conversation to Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction="You are GriefBot, a gentle, highly empathetic, and supportive AI companion for someone experiencing grief. Keep your responses short (1 to 3 sentences), conversational, and comforting. Do not give medical advice."
            ),
            contents=gemini_contents
        )
        return response.text

    except Exception as e:
        print(f"GEMINI ERROR: {e}")
        return "I am having a little trouble connecting right now, but I am still here with you."

def generate_grief_map(loss_type):
    maps = {
        "person": ["Shock & Denial", "Pain & Guilt", "Anger & Bargaining", "Depression", "The Upward Turn", "Reconstruction", "Acceptance & Hope"],
        "pet": ["Initial Shock", "Acute Anguish", "Missing the Routine", "Guilt or Second-guessing", "Adapting Home Life", "Honoring the Memory"],
        "relationship": ["Disbelief", "Heartbreak", "Seeking Answers", "Anger & Resentment", "Rebuilding Identity", "Moving Forward"],
        "job": ["Loss of Identity", "Financial Anxiety", "Anger at Employer", "Self-Doubt", "Exploring New Paths", "Acceptance & Growth"]
    }
    return maps.get(loss_type.lower(), maps["person"])

def play_voice(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    except Exception as e:
        pass

def breathing_animation():
    html = """
    <div style="display: flex; justify-content: center; align-items: center; height: 250px; font-family: sans-serif;">
        <div id="circle" style="width: 120px; height: 120px; background-color: #8fb8d9; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white; font-size: 18px; font-weight: bold; transition: all 4s ease-in-out; box-shadow: 0 0 20px rgba(143, 184, 217, 0.5);">
            Ready?
        </div>
    </div>
    <script>
        const circle = document.getElementById('circle');
        let state = 0;
        setTimeout(() => {
            setInterval(() => {
                if(state === 0) {
                    circle.style.transform = 'scale(1.8)';
                    circle.style.backgroundColor = '#5c96c7';
                    circle.innerText = 'Breathe In...';
                    state = 1;
                } else if(state === 1) {
                    circle.style.transform = 'scale(1.8)';
                    circle.style.backgroundColor = '#3a7db8';
                    circle.innerText = 'Hold...';
                    state = 2;
                } else {
                    circle.style.transform = 'scale(1.0)';
                    circle.style.backgroundColor = '#8fb8d9';
                    circle.innerText = 'Breathe Out...';
                    state = 0;
                }
            }, 4000);
        }, 1000);
    </script>
    """
    components.html(html, height=270)

# --- App Layout ---
st.set_page_config(page_title="GriefBot", page_icon="🤍", layout="wide")

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .chat-message { padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; }
    .chat-message.user { background-color: #e6f3ff; border-left: 5px solid #0066cc; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; }
    .chat-message.bot { background-color: #ffffff; border-left: 5px solid #4CAF50; border: 1px solid #e0e0e0; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello. I'm here to support you through your grief. Take your time, there is no rush."}]
if "memories" not in st.session_state:
    st.session_state.memories = []
if "just_responded" not in st.session_state:
    st.session_state.just_responded = False

with st.sidebar:
    st.title("🤍 GriefBot")
    if st.session_state.setup_complete:
        page = st.radio("Navigation", ["Daily Check-in", "Interactive Grounding", "My Journey Map", "Memory Book"])
        st.divider()
        st.write("### Settings")
        voice_mode = st.toggle("🔊 Enable Voice Bot Output", value=True)

if not st.session_state.setup_complete:
    st.title("Welcome to a Safe Space")
    loss_type = st.selectbox("I have lost a...", ["Person", "Pet", "Relationship", "Job", "Other"])
    name = st.text_input("Name (optional)")

    if st.button("Begin Journey"):
        st.session_state.loss_type = loss_type
        st.session_state.name = name
        st.session_state.grief_map = generate_grief_map(loss_type)
        st.session_state.setup_complete = True
        st.rerun()

else:
    if page == "Daily Check-in":
        st.title("Gentle Check-in")

        for msg in st.session_state.messages:
            div_class = "chat-message user" if msg["role"] == "user" else "chat-message bot"
            st.markdown(f'<div class="{div_class}">{msg["content"]}</div>', unsafe_allow_html=True)

        if st.session_state.just_responded and voice_mode:
            play_voice(st.session_state.messages[-1]["content"])
            st.session_state.just_responded = False

        st.write("---")
        st.write("### 🎙️ Speak to GriefBot")

        voice_input = speech_to_text(language='en', start_prompt="Click to Record 🔴", stop_prompt="Stop Recording ⏹️", just_once=True, key='STT')
        text_input = st.chat_input("Or type your thoughts...")

        final_input = voice_input if voice_input else text_input

        if final_input:
            st.session_state.messages.append({"role": "user", "content": final_input})
            ai_response = get_real_ai_response(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            st.session_state.just_responded = True
            st.rerun()

    elif page == "Interactive Grounding":
        st.title("Grounding Exercise")
        st.write("Follow the visual bot below to regulate your breathing and ground yourself.")
        st.markdown("---")
        breathing_animation()

    elif page == "My Journey Map":
        st.title("Your Grief Journey")
        cols = st.columns(len(st.session_state.grief_map))
        for i, stage in enumerate(st.session_state.grief_map):
            with cols[i]:
                st.info(f"Step {i+1}\n\n**{stage}**")

    elif page == "Memory Book":
        st.title("Memory Book")
        with st.expander("Add a new memory", expanded=True):
            mem_title = st.text_input("Memory Title")
            mem_content = st.text_area("What do you remember?")
            if st.button("Save Memory"):
                if mem_title and mem_content:
                    st.session_state.memories.append({"title": mem_title, "content": mem_content, "date": datetime.now().strftime("%Y-%m-%d")})
                    st.success("Memory saved to your private book.")

        for mem in reversed(st.session_state.memories):
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #f39c12;">
                <h3 style="margin-top: 0;">{mem['title']}</h3>
                <p style="color: gray;">{mem['date']}</p>
                <p>{mem['content']}</p>
            </div>
            """, unsafe_allow_html=True)

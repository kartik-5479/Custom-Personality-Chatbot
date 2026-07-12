import requests
import urllib.parse
import streamlit as st
import json
from google import genai
from dotenv import load_dotenv
import os
from streamlit_option_menu import option_menu

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
CHAT_FILE = "chat_history.json"
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

# Page Config
st.set_page_config(page_title="AI Multiverse", page_icon="🤖")
st.markdown("""
<style>

.nav-link{
    border-radius:12px !important;
    margin-bottom:8px;
    padding:10px 15px !important;
    font-size:16px !important;
}

/* Selected Menu */
.nav-link-selected{
    background-color:#4F8BF9 !important;
    color:white !important;
}

/* Hover Effect */
.nav-link:hover{
    background-color:#30304d !important;
}

</style>
""", unsafe_allow_html=True)


# Sidebar
st.sidebar.markdown(
    """
# 🌍 AI Multiverse

### Your Personal AI Hub
"""
)
st.sidebar.success("🟢 AI Systems Online")
st.sidebar.markdown("---")
st.sidebar.caption("⚙️ Application Modules")
with st.sidebar:
    feature = option_menu(
        menu_title="⚙️ Application Modules",
        options=["AI Chat", "AI Image Generator"],
        icons=["chat-dots-fill", "image-fill"],
        menu_icon="robot",
        default_index=0,
    )

if feature == "AI Chat":

    st.markdown(
    """
    <h1 style="text-align:center;">
        🌍 AI Multiverse
    </h1>

    <h3 style="text-align:center; color:gray;">
        ✨ Chat with Different AI Personalities
    </h3>
    """,
    unsafe_allow_html=True,
)

if feature == "AI Image Generator":

    st.markdown(
    """
    <h1 style="text-align:center;">
        🎨 AI Image Generator
    </h1>

    <h3 style="text-align:center; color:gray;">
        🖼️ Turn your imagination into AI artwork
    </h3>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):

    st.subheader("👋 Welcome to AI Multiverse")

    st.caption(
        "Your personal AI workspace for chatting with unique personalities "
        "and creating AI-generated images."
    )

    st.markdown("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🤖 **10 Personalities**")

    with col2:
        st.success("🎨 **2 AI Modules**")

    with col3:
        st.warning("⚡ **Gemini AI**")

st.divider()

# ==========================================================
# 🤖 AI CHAT MODULE
# ==========================================================

if feature == "AI Chat":
    st.sidebar.subheader("Choose Personality")

    personality = st.sidebar.selectbox(
        "Select",
        [
            "Common Indian Man",
            "Crazy Salman Khan Fan",
            "Little Boy",
            "Motivational Coach",
            "Software Engineer",
            "College Professor",
            "Stand-up Comedian",
            "Entrepreneur",
            "Friendly Teacher",
            "AI Assistant"
        ]
    )

    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []

        if os.path.exists(CHAT_FILE):
            os.remove(CHAT_FILE)

        st.rerun()

# Chat History
    if "messages" not in st.session_state:

        
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, "r") as file:
                st.session_state.messages = json.load(file)
        else:
            st.session_state.messages = []

        if len(st.session_state.messages) == 0:

            st.info("💬 Start a conversation with your selected AI personality.")
            col1, col2 = st.columns(2)

        with col1:
            st.button("💡 Tell me a joke", disabled=True)
            st.button("💻 Explain Python", disabled=True)
        
        with col2:
            st.button("🚀 Motivate me", disabled=True)
            st.button("🎬 Talk like Salman Khan", disabled=True)
    else:

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

# User Input
    if prompt := st.chat_input("Type your message..."):

        st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    

        with st.chat_message("user"):
            st.write(prompt)

        instruction = f"""
    You are acting as {personality}.
    Always stay in character.
    Reply according to that personality.
    Keep your answers interesting and natural.
    """
        conversation = ""
        for msg in st.session_state.messages:
            conversation += f"{msg['role']}: {msg['content']}\n"

        with st.spinner("Thinking..."):

            try:

                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents = f"""
{instruction}
Conversation so far:
{conversation}

Continue the conversation as the assistant.
"""
    )

                answer = response.text

            except Exception as e:
                answer = f"Error: {e}"

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with open(CHAT_FILE, "w") as file:
            json.dump(st.session_state.messages, file, indent=4)

        with st.chat_message("assistant"):
            st.write(answer) 

# ==========================================================
# 🎨 AI IMAGE GENERATOR MODULE
# ==========================================================

if feature == "AI Image Generator":

    st.subheader("🎨 Create Your Image")
    st.caption(
        "Describe your idea below, choose an artistic style, and let AI bring it to life."
    )

    with st.container(border=True):

        prompt = st.text_input(
            "Describe your image",
            placeholder="A futuristic city at sunset..."
        )

        style = st.selectbox(
            "Choose Image Style",
            [
                "Realistic",
                "Anime",
                "Fantasy",
                "Cyberpunk",
                "Pixel Art",
                "Watercolor"
            ]
        )

        if st.button(
            "🎨 Generate Image",
            use_container_width=True
        ):

            if not prompt.strip():
                st.warning("⚠️ Please enter an image description.")
                st.stop()

            with st.spinner("Generating image..."):

                final_prompt = (
                    f"{prompt}, {style} style, cinematic lighting, ultra detailed"
                )

                encoded_prompt = urllib.parse.quote(final_prompt)

                image_url = (
                    f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                )

                response = requests.get(image_url)

                if response.status_code == 200:
                    st.session_state.generated_image = response.content
                else:
                    st.error("❌ Failed to generate image.")

    # Display generated image
    if st.session_state.generated_image:

        st.image(
            st.session_state.generated_image,
            caption="Generated Image",
            use_container_width=True
        )

        st.download_button(
            label="📥 Download Image",
            data=st.session_state.generated_image,
            file_name="generated_image.png",
            mime="image/png",
            use_container_width=True
        )
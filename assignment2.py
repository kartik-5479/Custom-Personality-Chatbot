import requests
import random
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
    border-radius:14px !important;
    margin-bottom:10px;
    padding:12px 18px !important;
    font-size:16px !important;
    transition: all 0.3s ease;
}

.nav-link-selected{
    background: linear-gradient(90deg,#4F8BF9,#6C63FF) !important;
    color:white !important;
    font-weight:600;
    box-shadow:0 4px 12px rgba(79,139,249,0.35);
}

.nav-link:hover{
    background:#2d2d44 !important;
    transform:translateX(4px);
}

</style>
""", unsafe_allow_html=True)


# Sidebar


st.sidebar.markdown("""
<div style="
background:#1E3A2F;
padding:16px;
border-radius:12px;
text-align:center;
margin-top:10px;
margin-bottom:10px;
">

<div style="font-size:22px;">🟢</div>

<h4 style="margin:5px 0; color:white;">
System Status
</h4>

<p style="margin:0; color:#9EF79E; font-weight:bold;">
Online
</p>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    """
<div style="text-align:center;
padding-bottom:8px;
color:#A0A0A0;
font-size:13px;">

✨ Build • Chat • Create

</div>
""",
unsafe_allow_html=True
)

st.sidebar.markdown("---")


st.sidebar.markdown("""
<div style="
background: linear-gradient(135deg,#4F8BF9,#6C63FF);
padding:18px;
border-radius:16px;
color:white;
text-align:center;
margin-bottom:15px;
">

<h3 style="margin:0;">
🚀 AI Workspace
</h3>

<p style="
font-size:14px;
margin-top:10px;
line-height:1.6;
">

Create AI images<br>
Chat with multiple AI personalities<br>
Powered by Gemini

</p>

</div>
""", unsafe_allow_html=True)

with st.sidebar:
    feature = option_menu(
        menu_title= Application Modules",
        options=["AI Chat", "AI Image Generator"],
        icons=["chat-dots-fill", "image-fill"],
        menu_icon="robot",
        default_index=0,
    )

st.sidebar.markdown("---")

st.sidebar.markdown("""
        <div style="
        text-align:center;
        font-size:13px;
        color:gray;
        padding-top:8px;
        ">

        ⚡ Powered by <b>Gemini AI</b><br>

        Version 1.0.0

        </div>
        """, 
        unsafe_allow_html=True)


if feature == "AI Chat":

    st.markdown("""
        <div style="
        background: linear-gradient(135deg,#4F8BF9,#6C63FF);
        padding:30px;
        border-radius:18px;
        text-align:center;
        color:white;
        margin-bottom:25px;
        box-shadow:0 8px 20px rgba(0,0,0,0.25);
        ">

        <h1 style="margin:0;">🌍 AI Multiverse</h1>

        <p style="font-size:18px;margin-top:10px;">
        Chat with multiple AI personalities powered by Gemini.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

if feature == "AI Image Generator":

   st.markdown("""
        <div style="
        background: linear-gradient(135deg,#4F8BF9,#6C63FF);
        padding:30px;
        border-radius:18px;
        text-align:center;
        color:white;
        margin-bottom:25px;
        box-shadow:0 8px 20px rgba(0,0,0,0.25);
        ">

        <h1 style="margin:0;">🎨 AI Image Studio</h1>

        <p style="font-size:18px;margin-top:10px;">
        Create stunning AI artwork with just a few words.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )
   

st.markdown("""
### 🚀 Platform Overview
""")
col1, col2, col3 = st.columns(3)

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🤖 10 AI Personalities")

with col2:
    st.success("🎨 AI Image Studio")

with col3:
    st.warning("⚡ Gemini Powered")

st.sidebar.markdown("---")


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

        col1, col2 = st.columns([3,1])

        with col1:
            prompt = st.text_input(
                "📝 Describe your image",
                placeholder="A futuristic city at sunset..."
            )

        with col2:
            style = st.selectbox(
                "🎨 Style",
                [
                    "Realistic",
                    "Anime",
                    "Fantasy",
                    "Cyberpunk",
                    "Pixel Art",
                    "Watercolor"
                ]
            )

        with st.expander("⚙️ Advanced Settings"):

            width = st.select_slider(
                "Image Width",
                options=[512, 768, 1024],
                value=512
            )

            height = st.select_slider(
                "Image Height",
                options=[512, 768, 1024],
                value=512
            )

            magic_enhance = st.checkbox(
                "✨ Enable Magic Enhance",
                help="Adds hidden AI quality keywords for better images."
            )
        
        surprise_prompts = [
            "An astronaut riding a horse on Mars",
            "A cyberpunk street food vendor in Tokyo",
            "A dragon flying over the Himalayas",
            "A giant panda coding on a laptop",
            "A floating castle above the clouds"
        ]

        col1, col2 = st.columns(2)

        with col1:
            surprise = st.button(
                "🎲 Surprise Me!",
                use_container_width=True
            )

        with col2:
            generate = st.button(
                "🎨 Generate Image",
                use_container_width=True
            )

        if generate or surprise:
            if surprise:
                prompt = random.choice(surprise_prompts)
                st.info(f"🎲 Surprise Prompt: {prompt}")

            if not prompt.strip():
                st.warning("⚠️ Please enter an image description.")
                st.stop()

            with st.spinner("Generating image..."):

                final_prompt = f"{prompt}, {style} style"

                if magic_enhance:
                    final_prompt += (
                        ", masterpiece, 8k resolution, highly detailed, "
                        "trending on artstation, unreal engine 5 render"
                    )

                encoded_prompt = urllib.parse.quote(final_prompt)

                image_url = (
                    f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                    f"?width={width}&height={height}"
                )

                response = requests.get(image_url)

                if response.status_code == 200:
                    st.session_state.generated_image = response.content
                else:
                    st.error("❌ Failed to generate image.")

    # Display generated image
    # Display generated image
if st.session_state.generated_image:

    st.divider()

    st.subheader("🖼️ Generated Result")

    with st.container(border=True):

        st.image(
            st.session_state.generated_image,
            use_container_width=True
        )

        st.markdown("")

        st.download_button(
            label="📥 Download High Quality Image",
            data=st.session_state.generated_image,
            file_name=f"{style.lower().replace(' ', '_')}_image.png",
            mime="image/png",
            use_container_width=True
        )

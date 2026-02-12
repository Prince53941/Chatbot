import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Page config
st.set_page_config(page_title="AI Chatbot", layout="centered")

st.title("🤖 Advanced AI Chatbot")

SYSTEM_PROMPT = """
You are a professional, highly intelligent AI assistant.
Answer clearly, accurately, and in detail.
"""

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask anything...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        response_placeholder = st.empty()
        full_response = ""

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            stream=True
        )

        for chunk in response:
            if "content" in chunk["choices"][0]["delta"]:
                full_response += chunk["choices"][0]["delta"]["content"]
                response_placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

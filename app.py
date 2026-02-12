import streamlit as st
import requests
import os

st.set_page_config(page_title="Sports AI Bot", layout="centered")
st.title("🏆 Smart Sports AI Bot")

# Get Groq API Key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
You are an expert sports analyst.
Answer only sports-related questions.
If the question is not about sports, politely say you only answer sports topics.
Give detailed but clear answers.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask anything about sports...")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": st.session_state.messages,
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
    else:
        reply = "API error. Check your key."

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

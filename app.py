import streamlit as st
import requests

st.set_page_config(page_title="Sports Chatbot", layout="centered")
st.title("🏆 Sports Chatbot (Free API)")

API_URL = "https://www.thesportsdb.com/api/v1/json/3/searchteams.php"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about any sports team (example: Barcelona, Real Madrid, India cricket)...")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        response_text = ""

        params = {"t": user_input}
        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            if data["teams"]:

                team = data["teams"][0]

                response_text = f"""
### 🏟 {team['strTeam']}

🏆 League: {team['strLeague']}  
📍 Stadium: {team['strStadium']}  
🌍 Country: {team['strCountry']}  

📝 Description:
{team['strDescriptionEN'][:500]}...
"""

            else:
                response_text = "❌ Sorry, I couldn't find that team."

        else:
            response_text = "⚠ API error. Try again."

        st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})


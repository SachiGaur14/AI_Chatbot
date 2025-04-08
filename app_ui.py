import streamlit as st
import requests

API_BASE_URL = "http://localhost:5002"  # Change if your FastAPI server is hosted elsewhere

st.set_page_config(page_title="AI Chatbot", layout="wide")
st.title("💬 AI Chatbot")

# Initialize session state variables (stores values persistently across reruns)
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "all_sessions" not in st.session_state:
    st.session_state.all_sessions = []
if "selected_title" not in st.session_state:
    st.session_state.selected_title = "New Chat"

# Fetch all chat sessions
def fetch_all_sessions():
    try:
        response = requests.get(f"{API_BASE_URL}/chat_history/")
        if response.status_code == 200:
            return response.json()
    except:
        return []
    return []

# Sidebar for chat selection
st.sidebar.header("💬 Chat Sessions")
chat_titles = ["New Chat"] + [
    session["title"] for session in fetch_all_sessions()
]
selected_title = st.sidebar.radio("Select a Chat", chat_titles)

if selected_title != st.session_state.selected_title:
    st.session_state.selected_title = selected_title
    st.session_state.chat_history = []

    if selected_title != "New Chat":
        # Fetch chat by title
        for session in fetch_all_sessions():
            if session["title"] == selected_title:
                st.session_state.session_id = session["session_id"]
                st.session_state.chat_history = session["chats"]
                break
    else:
        st.session_state.session_id = None

# Display chat history
for entry in st.session_state.chat_history:
    if entry["role"] == "user":
        st.chat_message("user").markdown(entry["parts"][0])
    else:
        st.chat_message("assistant").markdown(entry["parts"][0])

# Input box
user_message = st.chat_input("What can I help you with...")

if user_message:
    st.chat_message("user").markdown(user_message)

    if st.session_state.session_id:
        # Continue existing chat
        response = requests.post(
            f"{API_BASE_URL}/continue-chat/",
            params={"session_id": st.session_state.session_id, "message": user_message}
        )
    else:
        # Start new chat
        response = requests.post(
            f"{API_BASE_URL}/new-chat/",
            params={"message": user_message}
        )

    if response.status_code == 200:
        data = response.json()
        st.session_state.session_id = data["session_id"]
        model_reply = data["response"]
        st.chat_message("assistant").markdown(model_reply)

        # Append to history
        st.session_state.chat_history.append({"role": "user", "parts": [user_message]})
        st.session_state.chat_history.append({"role": "model", "parts": [model_reply]})

        # Reload sidebar with new title if it was a new chat
        if st.session_state.selected_title == "New Chat":
            st.rerun()

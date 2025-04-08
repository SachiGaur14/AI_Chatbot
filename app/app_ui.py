import streamlit as st
import requests
import uuid

# Base URL of the FastAPI backend
BASE_URL = "http://localhost:5000"

# Session state for user session_id
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.title("🤖 Chatbot Interface")

menu = st.sidebar.selectbox("Menu", ["New Chat", "Continue Chat", "View History"])

# 1. Start a New Chat
if menu == "New Chat":
    st.subheader("💬 Start a New Chat")
    user_message = st.text_input("You:", key="new_chat_input")

    if st.button("Send"):
        response = requests.post(f"{BASE_URL}/new-chat/", json={"message": user_message})
        if response.status_code == 200:
            reply = response.json()["response"]
            st.text_area("Bot:", value=reply, height=100)
            st.success("Chat started.")
        else:
            st.error("Failed to start chat.")

# 2. Continue Chat
elif menu == "Continue Chat":
    st.subheader("🔁 Continue Chat")
    st.text(f"Your session ID: {st.session_state.session_id}")
    user_message = st.text_input("You:", key="continue_chat_input")

    if st.button("Send Message"):
        payload = {
            "session_id": st.session_state.session_id,
            "message": user_message
        }
        response = requests.post(f"{BASE_URL}/chat/", json=payload)
        if response.status_code == 200:
            reply = response.json()["response"]
            st.text_area("Bot:", value=reply, height=100)
        else:
            st.error("Failed to get response from bot.")

# 3. View History
elif menu == "View History":
    st.subheader("📜 Chat History")
    session_input = st.text_input("Enter session ID (or leave blank for all):")

    params = {"session_id": session_input} if session_input else {}
    response = requests.get(f"{BASE_URL}/history/", params=params)

    if response.status_code == 200:
        history = response.json()
        for chat in history:
            st.markdown(f"**Session ID:** {chat['session_id']}")
            for entry in chat["chats"]:
                st.markdown(f"**You:** {entry['user_msg']}")
                st.markdown(f"-> **Bot:** {entry['bot_reply']}")
            st.markdown("---")
    else:
        st.error("Could not retrieve history.")

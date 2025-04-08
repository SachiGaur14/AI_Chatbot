import asyncio
import google.generativeai as genai
from sqlalchemy.orm import Session
from models import ChatHistory

genai.configure(api_key="AIzaSyCIqcdC-FgUNewb37-uFPnbMBrm0pU5lGg")

async def get_bot_response(prompt: str) -> str:
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def get_bot_response_with_context(session_id: str, user_message: str, db: Session) -> str:

    history = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).first()
    context = ""
    for chat in history.chats:
        context += f"User: {chat.get('user_msg')}\nBot: {chat.get('bot_reply')}\n"

    context += f"User: {user_message}\nBot:"

    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = await asyncio.to_thread(model.generate_content, context)
    return response.text

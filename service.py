import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import ChatHistory
import google.generativeai as genai
from sqlalchemy.orm.attributes import flag_modified

generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

async def new_chat_with_bot(msg: str, db_session: Session):
    session_id = str(uuid.uuid4())

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(msg)

    title = msg
    reply = response.text
    chats = [{"role": "user", "parts": [msg]}, {"role": "model", "parts": [reply]}]

    chat = ChatHistory(session_id=session_id, title=title, chats=chats)
    db_session.add(chat)
    db_session.commit()
    db_session.refresh(chat)

    return {"session_id": session_id, "response": reply}


async def continue_chat_with_bot(session_id: str, msg: str, db_session: Session):
    history = db_session.query(ChatHistory).filter(ChatHistory.session_id == session_id).first()

    if not history:
        raise HTTPException(status_code=404, detail="Chat not found.")

    chat_session = model.start_chat(history=history.chats)
    response = chat_session.send_message(msg)
    reply = response.text

    history.chats += [{"role": "user", "parts": [msg]}, {"role": "model", "parts": [reply]}]
    flag_modified(history, "chats")
    db_session.commit()

    return {"session_id": history.session_id, "title": history.title, "chats": history.chats, "response": reply}


async def get_history(session_id: str, db_session: Session):
    if session_id:
        history = db_session.query(ChatHistory).filter(ChatHistory.session_id == session_id).first()
        if not history:
            raise HTTPException(status_code=404, detail="Chat not found.")
        return {"session_id": history.session_id, "title": history.title, "chats": history.chats}
    else:
        history = db_session.query(ChatHistory).all()
        return [
            {"session_id": chat.session_id, "title": chat.title, "chats": chat.chats}
            for chat in history
        ]

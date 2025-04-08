from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas import Chat, ChatRequest, ChatResponse
from database import Base, engine, get_db
from models import ChatHistory
from services import get_bot_response, get_bot_response_with_context

app = FastAPI(title="Chatbot")

Base.metadata.create_all(bind=engine)

@app.post("/new-chat/", response_model=ChatResponse)
async def start_new_chat_with_bot(chat: Chat, db: Session = Depends(get_db)):
    bot_reply = await get_bot_response(chat.message)

    # Save chat history
    new_entry = ChatHistory(
        user_message=chat.message,
        bot_response=bot_reply,
        chats = [{"user_msg": chat.message,
                 "bot_reply": bot_reply}]
    )
    db.add(new_entry)
    db.commit()

    return ChatResponse(response=bot_reply)

@app.post("/chat/", response_model=ChatResponse)
async def chat_with_bot(chat: ChatRequest, db: Session = Depends(get_db)):
    bot_reply = await get_bot_response_with_context(chat.session_id, chat.message, db=db)

    chat_msgs = db.query(ChatHistory).filter(ChatHistory.session_id == chat.session_id).first()
    if chat_msgs:
        chat_msgs.user_message = chat.message
        chat_msgs.bot_response = bot_reply
        chat_msgs.chats = (chat_msgs.chats or []) + [{"user_msg": chat.message, "bot_reply": bot_reply}]
        print(chat_msgs.chats)
        db.add(chat_msgs)

    db.commit()
    return ChatResponse(response=bot_reply)

@app.get("/history/")
def get_history(session_id: str = None, db: Session = Depends(get_db)):
    if session_id:
        history = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).all()
    else:
        history = db.query(ChatHistory).all()

    chats = [{"session_id": h.session_id, "chats": h.chats} for h in history]
    return chats

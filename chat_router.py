import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from database import get_db
import google.generativeai as genai
from service import continue_chat_with_bot, get_history, new_chat_with_bot

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


router = APIRouter(tags=["Chatbot Routers"])

@router.post("/new-chat/")
async def new_chat(message: str, db_session: Session = Depends(get_db)):
    response = await new_chat_with_bot(message, db_session)
    return response


@router.post("/continue-chat/")
async def continue_chat(session_id: str, message: str, db_session: Session = Depends(get_db)):
    response = await continue_chat_with_bot(session_id, message, db_session)
    return response

@router.get("/chat_history/")
async def get_chat_history(session_id: str = None, db_session: Session = Depends(get_db)):
    response = await get_history(session_id, db_session)
    return response

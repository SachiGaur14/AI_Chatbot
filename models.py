from sqlalchemy import Column, String, JSON
from database import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"

    session_id = Column(String, primary_key=True, index=True)
    title = Column(String)
    chats = Column(JSON)  # Stores full history of user and model messages

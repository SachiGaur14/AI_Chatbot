import uuid
from sqlalchemy import CHAR, JSON, Column, Text
from database import Base

class ChattingHistory(Base):
    __tablename__ = "chatting_history"

    session_id = Column(CHAR(36), primary_key=True, index=True,
        nullable=False, default=lambda: str(uuid.uuid4()),)
    user_message = Column(Text)
    bot_response = Column(Text)
    chats = Column(JSON)

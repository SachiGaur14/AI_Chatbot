from fastapi import FastAPI
from chat_router import router as chat_router
from database import Base, engine


app = FastAPI(title="Chatbot")
Base.metadata.create_all(bind=engine)

app.include_router(chat_router)

# # 💬 AI Chatbot with Gemini + FastAPI + Streamlit


An interactive AI chatbot web application built using FastAPI and Streamlit, powered by Google's Gemini Generative AI model. This app supports chat with AI, saves conversation history with session IDs, and allows users to view past sessions in a sidebar.

## 🚀 Features
🤖 Chat with a Gemini-powered AI model

📂 Stores chat history using SQLite

🔁 Continue chats across sessions

📑 Session-based conversation retrieval

🖥️ Streamlit-based clean frontend interface

🔧 Built with modular and scalable FastAPI backend

## 🏗️ Tech Stack

Layer	Technology
**Backend**	FastAPI, SQLAlchemy, SQLite, 
**Frontend**	Streamlit
**AI Model**	Google Gemini (gemini-1.5-flash), 
**Environment**	dotenv (.env) support, 

## 📷 Screenshots

![🧾 Chat Interface](AI_Chatbot.png)

## 🧠 How It Works
User sends a message via the Streamlit frontend.

Backend (FastAPI) forwards the message to Gemini AI.

AI responds, and both user and model messages are stored in SQLite DB with a unique session ID.

Users can view and resume previous conversations via the sidebar.

## 🔐 .env Configuration
Create a .env file in the root directory:
GEMINI_API_KEY=your_google_genai_api_key

## 🛠️ Setup Instructions
1. Clone the Repo
git clone https://github.com/Sachi-CloudAnalogy/AI_Chatbot.git

2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Run the FastAPI Backend

uvicorn main:app --reload --port 5002

5. Launch the Streamlit Frontend
In another terminal:
streamlit run app_ui.py

## 📌 Requirements
Python 3.8+, 
Internet connection for Gemini API, 
Google Gemini API key 

#  AI-Powered Excel Mock Interviewer

## Objective
The goal is to develop a chatbot that can ask questions about Excel and, based on the answers, generate a report on the user’s performance.As of now, it is not connected to any database — it uses in-memory JSON storage to keep the values.In the future, we can save this data in a database for model improvement and fine-tuning.
### Scope
- Asking 6 Excel interview questions from a JSON.
- Collecting user answers through a chat-like interface (Streamlit).
- Scoring each answer on a 0–2 scale using AI.
- Generating a final performance report.

## How to run

#### Install Dependencies
pip install -r requirements.txt

#### Run Server
uvicorn main:app --reload

#### Run streamlit 
streamlit run streamlit.app.py

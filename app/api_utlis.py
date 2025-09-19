import streamlit as st
import requests
def get_chat_response(userAnswer,session_id):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'session_id' :  session_id,
        'answer' : userAnswer
    }
    try:
        response = requests.post("https://excel-interviewer-fpmr.onrender.com/chat", headers=headers,json=data)
        if response.status_code == 200:
          return response.json()
        else:
            st.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None  

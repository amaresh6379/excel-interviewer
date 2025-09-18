import streamlit as st
import requests
from api_utlis import get_chat_response
import json

st.title("Excel Interview")

if "name" not in st.session_state:
    st.session_state.name = None
if "email" not in st.session_state:
    st.session_state.email = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None    

if not st.session_state.name or not st.session_state.email:
    st.write("Fill in your details below to start your interview.")

    with st.form("user_details_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Start Interview")

        if submitted:
            if name.strip() and email.strip():
                st.session_state.name = name
                st.session_state.email = email
                outputData = get_chat_response('', '')
                st.session_state.session_id = outputData['session_id']
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Hi {name}, welcome to the Excel Interview! \n\n{outputData['Question']}"
                })
            else:
                st.warning("Please enter both name and email.")

else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type your answer here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        outputData = get_chat_response(prompt, st.session_state.session_id)
        if outputData.get("Question"):
          st.session_state.messages.append({"role": "assistant", "content": outputData['Question']})
          with st.chat_message("assistant"):
              st.markdown(outputData['Question'])
        elif outputData.get("report"):
            try:
                report_data = json.loads(outputData['report'])
            except:
                report_data = {"summary": outputData['report']} 
            st.subheader("Interview Report")
            if "summary" in report_data:
              st.markdown(f"**Summary:** {report_data.get('overall_skill_level',"")}")
            if "strengths" in report_data:
              st.markdown("strengths")
              for strength in report_data.get("strengths",""):
                  st.markdown(f"- {strength}")
            if "weaknesses" in report_data:
                st.markdown("weaknesses")
                for weakness in report_data.get("weaknesses",""):
                    st.markdown(f"- {weakness}")
            if "suggestions_for_improvement" in report_data:
                st.markdown("suggestions_for_improvement")
                for suggestion in report_data.get("suggestions_for_improvement",""):
                    st.markdown(f"- {suggestion}")                                      


            

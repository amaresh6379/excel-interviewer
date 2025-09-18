from fastapi import FastAPI
app =  FastAPI()
from pydantic_model import QueryInput
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
load_dotenv() 
import uuid
import json


userDetails = {}
messages = [SystemMessage(content="""
  You are an Excel Interviewer bot. Your job is to:
  1. Read the current question and the user's answer.
  2. If the user's input is an attempt to answer, evaluate it carefully and give a score (0 for wrong, 1 for partially correct, 2 for fully correct).
  3. Respond only in JSON format with the following keys:
    - "score": Integer (0, 1, 2)
  ### EXAMPLES
  #### Example 1 (Correct Answer):
  Question: "What is the shortcut to AutoSum in Excel?"
  User Answer: "Alt + ="
  Expected Output:
  {"score": 2
  #### Example 2 (Partially Correct Answer):
  Question: "What is the shortcut to AutoSum in Excel?"
  User Answer: "Ctrl + ="
  Expected Output:
  {"score": 1 
  Return only valid JSON, nothing else.
  """
)]  
excelData = [
    {
      "id": 1,
      "type": "short",
      "difficulty": "basic",
      "question": "Explain what a cell is in Excel.",
      "correctAnswer": "A cell is the intersection of a row and column where data, formulas, or functions are entered.",
      "marks": 1
    },
    {
      "id": 2,
      "type": "short",
      "difficulty": "basic",
      "question": "What is the difference between a workbook and a worksheet?",
      "correctAnswer": "A workbook is the entire Excel file (.xlsx), while a worksheet is a single sheet within the workbook.",
      "marks": 1
    },
    {
      "id": 3,
      "type": "formula",
      "difficulty": "intermediate",
      "question": "Write a formula to sum the numbers in cells A1 through A10.",
      "correctAnswer": "=SUM(A1:A10)",
      "marks": 2
    },
    {
      "id": 4,
      "type": "formula",
      "difficulty": "intermediate",
      "question": "Write a formula to count only the cells that are greater than 100 in the range B1:B20.",
      "correctAnswer": "=COUNTIF(B1:B20,\">100\")",
      "marks": 2
    },
    {
      "id": 5,
      "type": "formula",
      "difficulty": "advanced",
      "question": "Write a formula to look up the value in cell E2 in the first column of table A2:C100 and return the matching value from column 3.",
      "correctAnswer": "=VLOOKUP(E2,A2:C100,3,FALSE)",
      "marks": 3
    },
    {
      "id": 6,
      "type": "short",
      "difficulty": "advanced",
      "question": "Explain when you would prefer INDEX+MATCH over VLOOKUP.",
      "correctAnswer": "INDEX+MATCH is preferred when you need to look left, avoid column breakage, or improve performance on large data sets.",
      "marks": 3
    }
  ]

@app.post('/chat')
async def chat(queryInput : QueryInput):
  session_id =  queryInput.session_id
  global userDetails
  global messages
  global excelData
  if session_id :
    userValues = userDetails[session_id]
    chat = ChatOpenAI(model="gpt-4o",temperature=0.7)
    messages.append(HumanMessage(content=f'{{"question": "{excelData[userValues['index']]}", "answer": "{queryInput.answer}"}}'))
    response = chat(messages)                                                                                                  
    messages.append(AIMessage(content=response.content))
    data  =  json.loads(response.content)
    if 'score' in data:
        userValues['score'] = userValues['score']  +  data['score']     
    if userValues['index'] < len(excelData) - 1 :
      userValues['index'] = userValues['index'] + 1
      output = excelData[userValues['index']]['question']
      return {"Question":output ,"session_id":session_id}  
    else:
      conversation_text = json.dumps(
          [{"role": m.type, "content": m.content} for m in messages],
          indent=2
      )

      messages.append(
          SystemMessage(
              content=(
                  "You are an interview performance reviewer. "
                  "Read the full conversation below and generate a report summarizing:\n"
                  "- The user's overall Excel skill level\n"
                  "- Strengths (specific topics where they did well)\n"
                  "- Weaknesses (specific topics where they struggled)\n"
                  "- Suggestions for improvement\n\n"
                  f"Conversation:\n{conversation_text}"
              )
          )
      )
      summaryMessage = chat(messages)
      return {"report":summaryMessage}
  else:
    session_id = str(uuid.uuid4())
    userDetails[session_id] = {'score':0,'index':0}
    return {"Question":excelData[0]['question'] ,"session_id":session_id}  
    


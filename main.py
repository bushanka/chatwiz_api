import uuid
from typing import List, Union
import aiofiles
 
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

from src.llm import llm_answer
 
 
class Question(BaseModel):
    context: str
    text: str
 
 
class Answer(BaseModel):
    question: Question
    answer_text: str
    # FIXME: Need or Not? Add list if what
    documents: list
 
 
class User(BaseModel):
    user_id: str
    user_name: str
    contexts: Union[list, None] = []
    questions: Union[List[Question], None] = []
 
 
app = FastAPI()
 
users: dict[str, User] = {}
 
 
@app.get("/users/")
async def get_all_users_info():
    results = {"users": users}
    return results
 
 
@app.get("/users/{user_id}")
async def get_user_info(user_id: str):
    results = {"user": users[user_id]}
    return results
 
 
@app.post("/create_user")
async def add_user(user_name: str = 'Ivan'):
    new_user_uuid = str(uuid.uuid4())
    # FIXME: request to database - create user
    users[new_user_uuid] = User(
        user_id=new_user_uuid,
        user_name=user_name
    )
    return {
        'response_code': 200,
        'user_uuid': str(new_user_uuid)
    }
 
 
@app.post("/{user_id}/add_context")
async def add_document(user_id: str, doc_name: str, user_file: UploadFile = File(...)):
    # FIXME: request to database - add context (filename or filename1_filename2_... or different)
    # FIXME: Multiple files ??
    async with aiofiles.open(user_file.filename, "wb") as file:
        contents = await user_file.read()
        await file.write(contents)
    users[user_id].contexts.append(pdf.filename)
    return {
        'response_code': 200,
        'doc_name': f'{pdf.filename}',
        'from_uuid': user_id
    }
 
 
@app.post("/{user_id}/{context}/ask_question")
async def ask_question(user_id: str, question: Question):
    # FIXME: request ti database - add question to database
    users[user_id].questions.append(question)

    # FIXME: request to database - add llm answer to database
    llm_response, docs_used = await llm_answer(question)
    answer = Answer(
        question=question,
        answer_text=llm_response,
        documents=docs_used
    )
    
    return {
        'response_code': 200,
        'answer': answer
    }
 
 
if __name__ == '__main__':
    u = User(user_id='1234', user_name='4321')
    print(u)
import uuid
from typing import List, Union
import aiofiles
import os
 
from fastapi import FastAPI, File, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.llm import llm_answer

from yookassa import Configuration, Payment
import uuid

Configuration.account_id = '252962'
Configuration.secret_key = 'test_88ebn3FSZvhXNwCbOkaHJmYQX1arNGx2H0QzU2Yxqn8'
 
 
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


class MessageError(BaseModel):
    message: str
    details: dict


class AddedContext(BaseModel):
    contexts: Union[list, None] = []
    user_id: str

 
app = FastAPI()

origins = [
    "http://www.growth-tech.ru",  # Add your website's origin(s) here
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users: dict[str, User] = {}

plan_dict = {
    '1': "300.00",
    '2': "800.00",
    '3': "1500.00"
}

class SubscriptionPlan:
    id: int
    price: float
    max_num_of_contexts: int
    max_size_of_context: float
    max_question_length_in_chars: int
    max_number_of_chats: int
    max_number_of_queries: int
    duration: int  # в сек


@app.post("/billing/{user_id}/{plan_id}")
async def process_payment(user_id, plan_id):
    indepotence_key = uuid.uuid4()
    value = plan_dict[plan_id]

    payment = Payment.create({
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "confirmation": {
            # После усппешной оплаты юзера редиректит в прописанный url
            # если используем виджет - поставить 
            "type": "embedded",
        },
        "capture": True,
        # Описание платежа, до 128 символов
        "description": f"Заказ создан юзером {user_id}, план: {plan_id}",
        # Сохраняем его метод оплаты, если юзер дал на это разрешение
        "save_payment_method": True
    }, indepotence_key)

    return {
        "user_id": user_id,
        "plan_id": plan_id,
        "value": value,
        "confirmation_token": payment.confirmation.confirmation_token
    }
 

@app.get("/users/")
async def get_all_users_info():
    results = {"users": users}
    return results
 
 
@app.get("/users/{user_id}")
async def get_user_info(user_id: str):
    return users[user_id]
 
 
@app.post("/create_user", status_code=201, responses={
    status.HTTP_201_CREATED: {"model": User, "description": "Creates and returns User"},
})
async def add_user(user_name: str = 'Ivan'):
    new_user_uuid = str(uuid.uuid4())
    user = User(user_id=new_user_uuid, user_name=user_name)

    # FIXME: request to database - create user
    users[new_user_uuid] = user

    return user
 
 
@app.post("/{user_id}/add_context", responses={
    status.HTTP_404_NOT_FOUND: {"model": MessageError},
    status.HTTP_200_OK: {"model": AddedContext}
})
async def add_document(user_id: str, user_file: UploadFile = File(...)):
    # FIXME: request to database - add context (filename or filename1_filename2_... or different)
    # FIXME: Multiple files ??
    if user_id not in users:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={
                'message': 'uuid not found', 
                'details': {"uuid": user_id}
            }
        )
    
    user = users[user_id]

    # FIXME: Store files properly ?
    path = os.path.join(os.getcwd(), 'data', user_file.filename)
    if not os.path.isfile(path):
        async with aiofiles.open(path, "wb") as file:
            contents = await user_file.read()
            await file.write(contents)

    user.contexts.append(user_file.filename)

    return AddedContext(
        contexts=user.contexts,
        user_id=user.user_id
        
    )
 
 
@app.post("/{user_id}/{context}/ask_question", responses={
    status.HTTP_404_NOT_FOUND: {"model": MessageError},
    status.HTTP_200_OK: {"model": Answer}
})
async def ask_question(user_id: str, question: Question):
    # FIXME: request ti database - add question to database
    if user_id not in users:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={
                'message': 'uuid not found', 
                'details': {"uuid": user_id}
            }
        )
    
    users[user_id].questions.append(question)

    # FIXME: request to database - add llm answer to database
    llm_response, docs_used = await llm_answer(question)
    answer = Answer(
        question=question,
        answer_text=llm_response,
        documents=docs_used
    )
    
    return answer
 
 
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
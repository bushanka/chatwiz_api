import json
from typing import Any
from app.schemas.crud import apgvector_instance
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import json
import codecs
import logging


async def mock_model_response(some_question: str) -> str:
    return f'The answer on "{some_question}" is : 42!'


def convert_to_proper_chat_history(history):
    dict_history = json.loads(history)
    chat_history = dict_history['chat']
    # Формат подачи историй в лангчейне [(query, result["answer"])]
    converted_history = [
        (
            codecs.escape_decode(chat_history[i][1])[0].decode('utf-8'), 
            codecs.escape_decode(chat_history[i + 1][1])[0].decode('utf-8')
        ) for i in range(0, len(chat_history) - 1, 2)
    ]
    return converted_history


async def llm_model_response(user_question: str, message_history: str, context_name: str) -> str:
    user_question = codecs.escape_decode(user_question)[0].decode('utf-8')
    retriever = apgvector_instance.as_retriever(name_search_collection=context_name, k=2)
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0.5, model='gpt-3.5-turbo'),
        chain_type="stuff",
        retriever=retriever,
        verbose=True
    )
    # FIXME: Сделать конфиги, там очень много настроек в лангчейне, вплоть до промпта и тд
    # FIXME: Возвращать сурсы через return_source_documents=True в ConversationalRetrievalChain
    # TODO: По хорошему поиграть с параметрами лангчейна, иногда модель отвечает на английском и плохо, не улавливает прошлые сообщения
    chat_history = convert_to_proper_chat_history(message_history)
    result = await qa.arun({
        "question": user_question,
        "chat_history": chat_history
    })
    result = codecs.escape_decode(result)[0].decode('utf-8')
    return result


async def add_message_to_history(new_message: Any, message_history: str) -> str:
    if len(message_history) == 12:
        return message_history[:-3] + "[" + json.dumps(new_message) + ']}'
    return message_history[:-2] + ", " + json.dumps(new_message) + ']}'


async def get_new_message_history(new_message: str, message_history: str, context_name: str) -> str:
    model_response = await llm_model_response(new_message, message_history, context_name)
    wrapped_new_message = ["human", new_message]
    wrapped_response = ["ai", model_response]
    extended_mh = await add_message_to_history(wrapped_new_message, message_history)
    return await add_message_to_history(wrapped_response, extended_mh)

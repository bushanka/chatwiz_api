import codecs
import json
from typing import Any

import openai
from langchain.chains import ConversationalRetrievalChain
# from langchain.chat_models import ChatOpenAI
from langchain_community.llms import YandexGPT

from app.schemas.crud import apgvector_instance


async def mock_model_response(some_question: str) -> str:
    return f'The answer on "{some_question}" is : 42!'


def convert_to_proper_chat_history(history) -> list[tuple[Any, Any]]:
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


def convert_to_proper_chat_history_no_retriever(history):
    dict_history = json.loads(history)
    chat_history = dict_history['chat']
    # [{"role": "user", "content": "Hello world"}]
    converted_history = [
        {"role": "user", "content": codecs.escape_decode(chat_history[i][1])[0].decode('utf-8')}
        if i % 2 == 0
        else
        {"role": "assistant", "content": codecs.escape_decode(chat_history[i][1])[0].decode('utf-8')}
        for i in range(0, len(chat_history), 1)
    ]
    return converted_history


async def llm_model_response(user_question: str, message_history: str, context_name: str) -> str:
    if context_name:
        user_question = codecs.escape_decode(user_question)[0].decode('utf-8')
        retriever = apgvector_instance.as_retriever(name_search_collection=context_name, k=2)
        qa = ConversationalRetrievalChain.from_llm(
            llm=YandexGPT(
                api_key="AQVNy4GILx-3sPg3cgHIGz629H3qGqF4fsm4son2",
                folder_id="b1gv3u11tm89ukr82s0m"
            ),
            chain_type="stuff",
            retriever=retriever,
            verbose=True
        )
        # FIXME: Сделать конфиги, там очень много настроек в лангчейне, вплоть до промпта и тд
        # FIXME: Возвращать сурсы через return_source_documents=True в ConversationalRetrievalChain
        # TODO: По хорошему поиграть с параметрами лангчейна, иногда модель отвечает на английском и плохо, не улавливает прошлые сообщения
        chat_history = convert_to_proper_chat_history(message_history)
        result = qa.run({
            "question": user_question,
            "chat_history": chat_history
        })
        result = codecs.escape_decode(result)[0].decode('utf-8')
        return result
    else:
        user_question = codecs.escape_decode(user_question)[0].decode('utf-8')
        chat_history = convert_to_proper_chat_history_no_retriever(message_history)
        chat_history.append(
            {"role": "user", "content": user_question}
        )
        chat_completion_resp = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=chat_history
        )
        return chat_completion_resp.choices[0].message.content


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

import codecs
import json
from typing import Any

from langchain_community.llms import YandexGPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.tracers import ConsoleCallbackHandler

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

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

async def llm_model_response(user_question: str, message_history: str, context_name: str) -> str:
    if context_name:
        template = """Ответь на вопрос, основываясь только на следующем контексте:
        {context}

        Вопрос: {question}
        """
        model = YandexGPT(api_key="AQVNy4GILx-3sPg3cgHIGz629H3qGqF4fsm4son2", folder_id="b1gv3u11tm89ukr82s0m")
        prompt = ChatPromptTemplate.from_template(template)
        output_parser = StrOutputParser()

        user_question = codecs.escape_decode(user_question)[0].decode('utf-8')

        retriever = apgvector_instance.as_retriever(name_search_collection=context_name, k=2)
        setup_and_retrieval = RunnableParallel(
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
        )

        chain = setup_and_retrieval | prompt | model | output_parser

        result = await chain.ainvoke(user_question, config={'callbacks': [ConsoleCallbackHandler()]})
        # chat_history = convert_to_proper_chat_history(message_history)

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

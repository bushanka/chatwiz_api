import json
from typing import Any
from app.schemas.crud import apgvector_instance


async def mock_model_response(some_question: str) -> str:
    return f'The answer on "{some_question}" is : 42!'


async def llm_model_response(user_question: str, message_history: dict, context_name: str) -> str:
    res = await apgvector_instance.similarity_search(query=user_question, collection_name=context_name)
    print('\n')
    print(res)
    print('\n')
    return '42'


async def add_message_to_history(new_message: Any, message_history: str) -> str:
    return message_history[:-2] + ", " + json.dumps(new_message) + ']}'


async def get_new_message_history(new_message: str, message_history: dict, context_name: str) -> str:
    model_response = await llm_model_response(new_message, message_history, context_name)
    wrapped_new_message = ["human", new_message]
    wrapped_response = ["ai", model_response]
    extended_mh = await add_message_to_history(wrapped_new_message, message_history)
    return await add_message_to_history(wrapped_response, extended_mh)

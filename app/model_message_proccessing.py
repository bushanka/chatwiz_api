import json
from typing import Any


async def mock_model_response(some_question: str) -> str:
    return f'The answer on "{some_question}" is : 42!'


async def add_message_to_history(new_message: Any, message_history: str) -> str:
    return message_history[:-2] + ", " + json.dumps(new_message) + ']}'


async def get_new_message_history(new_message: str, message_history: str) -> str:
    model_response = await mock_model_response(new_message)
    wrapped_new_message = ["human", new_message]
    wrapped_response = ["ai", model_response]
    extended_mh = await add_message_to_history(wrapped_new_message, message_history)
    return await add_message_to_history(wrapped_response, extended_mh)

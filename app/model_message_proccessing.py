import json
from typing import Any
from app.schemas.crud import apgvector_instance
import openai
from app.llm.templates.prompt_template import qna_template
import json


async def mock_model_response(some_question: str) -> str:
    return f'The answer on "{some_question}" is : 42!'


async def llm_model_response(user_question: str, message_history: dict, context_name: str) -> str:
    res = await apgvector_instance.similarity_search(query=user_question, collection_name=context_name)


    prompt_template_copy = qna_template.format(
        context=res,
        chat_history=message_history,
        question=user_question
    )
    # TODO: Использовать langchain retriever или посмотреть как они делают и скопировать или написать AsyncPgVecotr в парадигме лангчейн либы
    print()
    print(prompt_template_copy)
    print()
    # TODO: Чекать юзер макс токенс
    chat_completion_resp = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo", 
        messages=[
            {
                "role": "user", 
                "content": prompt_template_copy
            },
        ]
    )

    completion = chat_completion_resp.choices[0]
    print()
    print(completion)
    print()
    answer = str(completion['message']['content'])
    return answer


async def add_message_to_history(new_message: Any, message_history: str) -> str:
    return message_history[:-2] + ", " + json.dumps(new_message) + ']}'


async def get_new_message_history(new_message: str, message_history: dict, context_name: str) -> str:
    model_response = await llm_model_response(new_message, message_history, context_name)
    wrapped_new_message = ["human", new_message]
    wrapped_response = ["ai", model_response]
    extended_mh = await add_message_to_history(wrapped_new_message, message_history)
    return await add_message_to_history(wrapped_response, extended_mh)

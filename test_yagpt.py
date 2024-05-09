# import codecs
# import asyncio

# from langchain.chains import ConversationalRetrievalChain
# from langchain_community.llms import YandexGPT
# from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

# from app.llm.apgvector.apgvector import AsyncPgVector


# POSTGRES_HOST='62.84.116.223'
# POSTGRES_PORT='5432'
# POSTGRES_USER='main_user'
# POSTGRES_PASSWORD='371RmUhv.%B$'
# POSTGRES_DBNAME='chatwiz_db'

# apgvector_instance = AsyncPgVector(
#     user=POSTGRES_USER,
#     password=POSTGRES_PASSWORD,
#     host=POSTGRES_HOST,
#     port=POSTGRES_PORT,
#     database=POSTGRES_DBNAME
# )

# general_system_template = r""" 
# Используй следующие фрагменты контекста, чтобы ответить на вопрос в конце. Если не знаешь ответа, просто скажи, что не знаешь, не пытайся придумать ответ:
#  ----
# {context}
# ----
# """
# general_user_template = "{question}"
# messages = [
#             SystemMessagePromptTemplate.from_template(general_system_template),
#             HumanMessagePromptTemplate.from_template(general_user_template)
# ]
# qa_prompt = ChatPromptTemplate.from_messages(messages)

# async def main():
#     await apgvector_instance.connect()
#     user_question = 'Какой пункт назначения?'
#     retriever = apgvector_instance.as_retriever(name_search_collection='1-ALEKSANDR_SERGEEVICH_BUSH.pdf', k=2)
#     qa = ConversationalRetrievalChain.from_llm(
#         llm=YandexGPT(
#             api_key="AQVNy4GILx-3sPg3cgHIGz629H3qGqF4fsm4son2",
#             folder_id="b1gv3u11tm89ukr82s0m"
#         ),
#         chain_type="stuff",
#         retriever=retriever,
#         verbose=True,
#         combine_docs_chain_kwargs={'prompt': qa_prompt}
#     )
#     # FIXME: Сделать конфиги, там очень много настроек в лангчейне, вплоть до промпта и тд
#     # FIXME: Возвращать сурсы через return_source_documents=True в ConversationalRetrievalChain
#     # TODO: По хорошему поиграть с параметрами лангчейна, иногда модель отвечает на английском и плохо, не улавливает прошлые сообщения
#     # chat_history = convert_to_proper_chat_history(message_history)
#     result = await qa.arun({
#         "question": user_question,
#         "chat_history": []
#     })
#     result = codecs.escape_decode(result)[0].decode('utf-8')
#     # return result
#     print(result)

# if __name__ == '__main__':
#     asyncio.run(main())



import asyncio
from app.llm.apgvector.apgvector import AsyncPgVector
from langchain_community.llms import YandexGPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.tracers import ConsoleCallbackHandler


model = YandexGPT(api_key="AQVNy4GILx-3sPg3cgHIGz629H3qGqF4fsm4son2", folder_id="b1gv3u11tm89ukr82s0m")

POSTGRES_HOST='62.84.116.223'
POSTGRES_PORT='5432'
POSTGRES_USER='main_user'
POSTGRES_PASSWORD='371RmUhv.%B$'
POSTGRES_DBNAME='chatwiz_db'
apgvector_instance = AsyncPgVector(
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DBNAME
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

async def main():
    await apgvector_instance.connect()
    retriever = apgvector_instance.as_retriever(name_search_collection='1-ALEKSANDR_SERGEEVICH_BUSH.pdf', k=2)


    template = """Ответь на вопрос, основываясь только на следующем контексте:
    {context}

    Вопрос: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    output_parser = StrOutputParser()

    setup_and_retrieval = RunnableParallel(
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
    )
    chain = setup_and_retrieval | prompt | model | output_parser
    
    res = await chain.ainvoke("Когда запланирован рейс?", config={'callbacks': [ConsoleCallbackHandler()]})
    print(res)


if __name__ == '__main__':
    asyncio.run(main())
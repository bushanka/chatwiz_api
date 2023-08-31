from asyncio import sleep as asleep
# from langchain.vectorstores.pgvector import PGVector
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores.pgvector import DistanceStrategy
# from langchain.chat_models import ChatOpenAI
# from langchain.chains import RetrievalQA
# from dotenv import load_dotenv
# import os



# load_dotenv()

# CONNECTION_STRING = PGVector.connection_string_from_db_params(
#     driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
#     host=os.environ.get('PS_HOSTNAME'),
#     port=int(os.environ.get('PS_PORT')),
#     database=os.environ.get('PS_DATABASE'),
#     user=os.environ.get('PS_USERNAME'),
#     password=os.environ.get('PS_PASSWORD'),
# )

# FIXME: return langchain documents list
async def llm_answer(question) -> tuple[str, list]:
    context = question.context
    question_text = question.text

    # store = PGVector(
    #         connection_string=CONNECTION_STRING, 
    #         embedding_function=OpenAIEmbeddings(), 
    #         collection_name=context.user_data['document_context'],
    #         distance_strategy=DistanceStrategy.COSINE
    #     )
    # relevant_documents = store.as_retriever().get_relevant_documents(question)
    relevant_documents = ['Hello', 'World']
    await asleep(2)

    # qa = RetrievalQA.from_chain_type(
    #         llm=ChatOpenAI(
    #         model_name='gpt-3.5-turbo',
    #         # TODO: This overloads async return, for streaming purposes
    #         # streaming=True, 
    #         # callbacks=[MyAsyncHandler(context.bot, msg.id, update.effective_chat.id, relevant_documents)]
    #         ), 
    #         chain_type='stuff', 
    #         retriever=store.as_retriever(),
    #         # return_source_documents=True
    #     )

    # gpt_answer = await qa.arun(query=question)

    return f"Your question is '{question_text}'", relevant_documents

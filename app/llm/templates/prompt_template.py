from langchain.prompts import PromptTemplate

template = """
Use the following pieces of context and previous conversation to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Context:
{context}

Previous conversation:
{chat_history}

Question:
{question}

Answer:
"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)


print(QA_CHAIN_PROMPT)

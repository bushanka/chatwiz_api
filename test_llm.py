from langchain.memory import ConversationBufferMemory
from langchain.memory import ChatMessageHistory
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from uuid import uuid4

memory = ConversationBufferMemory(memory_key="chat_history")

llm = OpenAI(temperature=0)
chatgpt = ChatOpenAI(llm=llm, verbose=True, history=memory)


async def ask(question: str) -> str:
    return await chatgpt.ask_async(question, conversation_id=str(uuid4()))
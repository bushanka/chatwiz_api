from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores.base import VectorStore, VectorStoreRetriever
from langchain.embeddings.base import Embeddings

from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    List,
    Optional,
    Type,
    TypeVar,
)

import asyncpg
from pgvector.asyncpg import register_vector
import numpy as np
from typing import List
import json
from dotenv import load_dotenv

load_dotenv()

VST = TypeVar("VST", bound="VectorStore")


# from test_embedd import test_embed

# FIXME: Мб лучше наследоваться от PgVectorStore в лангчейне?
# FIXME: Нужно имплементировать различные функции тут, чтобы полноценно работать со всеми параметрами в лангчейне
# FIXME: Например фильтры на score в документах, другие метрики расстояния....
class AsyncPgVector(VectorStore):
    """
    The `AsyncPgVector` class is an implementation of asynchronous PostgreSQL vector retrieval for
    performing similarity searches on embedded vectors.
    """
    _LANGCHAIN_DEFAULT_COLLECTION_NAME = "langchain"

    def __init__(
            self,
            host,
            port,
            user,
            password,
            database,
            embedding_function: Optional[Embeddings] = OpenAIEmbeddings(),
            collection_name: str = _LANGCHAIN_DEFAULT_COLLECTION_NAME
    ):
        self._connection_pool = None
        self._name_search_collection = None
        self.embedding_function = embedding_function
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.collection_name = collection_name

    async def connect(self):
        if not self._connection_pool:
            try:
                self._connection_pool = await asyncpg.create_pool(
                    min_size=1,
                    max_size=10,
                    command_timeout=60,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )
            except Exception as e:
                print(e)

    def __convert_records_to_document(self, records) -> List[Document]:
        docs = [
            Document(
                page_content=record['document'],
                metadata=json.loads(record['cmetadata']),
            )
            for record in records
        ]

        return docs

    def add_texts(self, texts: Iterable[str], metadatas=None, **kwargs: Any) -> List[str]:
        return super().add_texts(texts, metadatas, **kwargs)

    def from_texts(
            cls: Type[VST],
            texts: List[str],
            embedding: Embeddings,
            metadatas: Optional[List[dict]] = None,
            **kwargs: Any,
    ) -> VST:
        return super().from_texts(cls, texts, embedding, metadatas, **kwargs)

    async def similarity_search(self, query: str, k: int = 4, **kwargs: Any) -> List[Document]:
        return super().similarity_search(query, k, **kwargs)

    async def asimilarity_search(self, query: str, k: int = 4) -> List[Document]:
        '''
        The `similarity_search` function performs a similarity search by querying a collection of
        embeddings in a PostgreSQL database and returning the top k results based on the similarity to
        the input query.

        Parameters
        ----------
        query : str
            The `query` parameter is a string that represents the text query for which you want to find
        similar items in the collection.
        collection_name : str

            The `collection_name` parameter is a string that represents the name of the collection in which
        you want to perform the similarity search. This collection contains embedded vectors that
        represent the data items.

        k : int, optional
            The parameter `k` represents the number of nearest neighbors to retrieve in the similarity
        search. In this case, it is set to 5, which means that the function will return the top 5
        nearest neighbors to the query.

        Returns
        -------
            The function `similarity_search` returns list of Documents

        '''
        assert self._connection_pool is not None, 'Connection pool is not established, call await cls.connect() first'
        assert self._name_search_collection is not None, 'Name search collection is not defined, pass name in retriver kwarg'

        embedded_query = await self.embedding_function.aembed_query(query)

        async with self._connection_pool.acquire() as connection:
            await register_vector(connection)
            row = await connection.fetchrow(
                '''
                SELECT uuid
                FROM langchain_pg_collection
                WHERE name = $1
                ''',
                self._name_search_collection
            )
            try:
                res = await connection.fetch(
                    '''
                    SELECT * FROM langchain_pg_embedding
                    WHERE collection_id = $1
                    ORDER BY embedding <-> $2
                    LIMIT $3
                    ''',
                    row['uuid'],
                    np.array(embedded_query),
                    k
                )
            except TypeError:
                print(Exception("No document found"))
                return []

        return self.__convert_records_to_document(res)

    def as_retriever(self, **kwargs: Any) -> VectorStoreRetriever:
        self._name_search_collection = kwargs['name_search_collection']
        return super().as_retriever(**kwargs)


if __name__ == '__main__':
    import os
    import asyncio
    from langchain.chains import RetrievalQA
    from langchain.llms import OpenAI
    import time


    async def test_time_proceeding():
        apg = AsyncPgVector(
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host=os.environ.get('POSTGRES_HOST'),
            port=os.environ.get('POSTGRES_PORT'),
            database=os.environ.get('POSTGRES_DBNAME')
        )

        await apg.connect()

        start = time.time()
        retriever = apg.as_retriever(name_search_collection='4-!CSORT.pdf')
        print(f'{time.time() - start} sec to init retriever')

        start = time.time()
        qa = RetrievalQA.from_chain_type(llm=OpenAI(temperature=1), chain_type="stuff", retriever=retriever)
        print(f'{time.time() - start} sec to init qa chain')

        query = "Как звучал сепаратор?"
        start = time.time()
        result = 'ЖОСКА'  # await qa.arun(query)
        print(f'{time.time() - start} sec to answer')
        '''
        What did the president say about Ketanji Brown Jackson?

        The President said that Judge Ketanji Brown Jackson is one of the nation's top legal minds, 
        a former top litigator in private practice, a former federal public defender, and from a 
        family of public school educators and police officers. 
        He said she is a consensus builder and has received a broad range of 
        support from organizations such as the Fraternal Order of Police and 
        former judges appointed by Democrats and Republicans.


        Как звучал сепаратор?
        Как орган
        '''
        print('\nfinal:\n', result)

        # coros = [apg.similarity_search('стенды', '14-!CSORT.pdf') for _ in range(5)]

        # start = time.time()
        # a = await asyncio.gather(*coros)
        # print(f'{(time.time() - start):.5f} seconds')
        # return a


    asyncio.run(test_time_proceeding())

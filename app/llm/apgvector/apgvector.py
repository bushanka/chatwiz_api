from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document

import asyncpg
from pgvector.asyncpg import register_vector
import numpy as np
import time
from typing import List
import json

from app.llm.apgvector.test_embedd import test_embed


class AsyncPgVector:
    """
    The `AsyncPgVector` class is an implementation of asynchronous PostgreSQL vector retrieval for
    performing similarity searches on embedded vectors.
    """

    def __init__(
            self,
            host,
            port,
            user,
            password,
            database,
            embedding_function: OpenAIEmbeddings = OpenAIEmbeddings(),
    ):
        self.embedding_function = embedding_function
        self._connection_pool = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

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

    async def similarity_search(self, query: str, collection_name: str, k: int = 5) -> List[Document]:
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

        # TODO: uncomment in prod end delete test
        embedded_query = await self.embedding_function.aembed_query(query)
        # embedded_query = test_embed

        async with self._connection_pool.acquire() as connection:
            await register_vector(connection)
            row = await connection.fetchrow(
                '''
                SELECT uuid
                FROM langchain_pg_collection
                WHERE name = $1
                ''',
                collection_name
            )
            try:
                res = await connection.fetch(
                    '''
                    SELECT * FROM langchain_pg_embedding
                    WHERE collection_id = $1
                    ORDER BY embedding <-> $2
                    LIMIT 5
                    ''',
                    row['uuid'],
                    np.array(embedded_query)
                )
            except TypeError:
                print(Exception("No document found"))
                return []

        return self.__convert_records_to_document(res)


if __name__ == '__main__':
    async def test_time_proceeding():
        apg = AsyncPgVector(
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host=os.environ.get('POSTGRES_HOST'),
            port=os.environ.get('POSTGRES_PORT'),
            database=os.environ.get('POSTGRES_DBNAME')
        )

        await apg.connect()

        coros = [apg.similarity_search('стенды', '14-!CSORT.pdf') for _ in range(5)]

        start = time.time()
        a = await asyncio.gather(*coros)
        print(f'{(time.time() - start):.5f} seconds')
        return a


    import os
    from dotenv import load_dotenv
    import asyncio

    load_dotenv()

    asyncio.run(test_time_proceeding())

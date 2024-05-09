import os

from dotenv import load_dotenv

load_dotenv()
args = {
    "host": os.getenv("POSTGRES_HOST"),
    "db_port": os.getenv("POSTGRES_PORT"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "dbname": os.getenv("POSTGRES_DBNAME"),
    "port": os.getenv("POSTGRES_PORT"),
}
connect_str = f"postgresql+psycopg2://{args['user']}:{args['password']}@{args['host']}:{args['db_port']}/{args['dbname']}"

from langchain.vectorstores.pgvector import DistanceStrategy, PGVector
from langchain.docstore.document import Document
from langchain_community.embeddings.yandex import YandexGPTEmbeddings

embeddings = YandexGPTEmbeddings(api_key="AQVNy4GILx-3sPg3cgHIGz629H3qGqF4fsm4son2", folder_id="b1gv3u11tm89ukr82s0m")
db = PGVector.from_documents(
    documents=[Document(page_content='1')],
    embedding=embeddings,
    collection_name="delete_me_plz",
    distance_strategy=DistanceStrategy.COSINE,
    connection_string=connect_str)

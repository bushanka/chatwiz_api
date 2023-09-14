from celery import Celery

from langchain.document_loaders.pdf import AmazonTextractPDFLoader
from langchain.vectorstores.pgvector import PGVector
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from dotenv import load_dotenv
import os
import boto3


app = Celery('chatwiztasks', broker='pyamqp://guest@localhost//')

app.conf.task_routes = {'chatwiztasks.process_pdf': {'queue': 'chatwiztasks_queue'}}


load_dotenv()
args = {
    "host": os.getenv("POSTGRES_HOST"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "dbname": os.getenv("POSTGRES_DBNAME"),
    "port": os.getenv("POSTGRES_PORT"),
}
CONN_STRING = f"postgresql+asyncpg://{args['user']}:{args['password']}@{args['host']}/{args['dbname']}",

session = boto3.Session(
    aws_access_key_id=os.getenv('BUCKET_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('BUCKET_SECRET_ACCESS_KEY')
)


@app.task(name='llm.tasks.process_pdf')
def process_pdf(filename, user_id):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=255,
        chunk_overlap=20,
        length_function=len,
        add_start_index=True
    )

    s3 = session.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net')
    loader = AmazonTextractPDFLoader(
        path=str(user_id) + '-' + filename,
        client=s3
    )

    pages = loader.load_and_split(text_splitter)

    print(f'done, loaded {len(pages)} pages')

    return 'loaded'

    # print('perfoming tokenization')
    # batchsize = 5000
    # for i in tqdm(range(0, len(pages), batchsize)):
    #     PGVector.from_documents(
    #         embedding=OpenAIEmbeddings(),
    #         documents=pages[i:i+batchsize],
    #         collection_name=doc_name,
    #         connection_string=CONN_STRING,
    #         )
    # print('done')

    # return f'{doc_name} loaded'
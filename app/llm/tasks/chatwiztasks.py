import io
import os
import time
from typing import List, Optional

import boto3
import pypdf
from celery import Celery
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, TextSplitter
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings.openai import OpenAIEmbeddings


class PyPDFBytesLoader(BaseLoader):
    """Loads a PDF with pypdf given a BytesIO object and chunks at the character level.
    
    Loader also stores page numbers in metadatas.
    """

    def __init__(self, stream: io.BytesIO, text_splitter: Optional[TextSplitter] = None):
        """Initialize with BytesIO object."""

        try:
            import pypdf  # noqa:F401
        except ImportError:
            raise ValueError(
                "pypdf package not found, please install it with " "`pip install pypdf`"
            )

        self.stream = stream
        self.text_splitter = text_splitter

    def load(self) -> List[Document]:
        """Load given path as pages."""
        pdf_reader = pypdf.PdfReader(self.stream)
        return [
            Document(
                page_content=page.extract_text(),
                metadata={"page": i},
            )
            for i, page in enumerate(pdf_reader.pages)
        ]

    def load_and_split(self, ):
        if self.text_splitter is None:
            raise Exception(
                "You must pass a text splitter"
            )
        docs = self.load()
        return self.text_splitter.split_documents(docs)


app = Celery('chatwiztasks', broker=os.getenv('APP_BROKER_URI'), backend='rpc://')

app.conf.task_routes = {'chatwiztasks.process_pdf': {'queue': 'chatwiztasks_queue'}}

load_dotenv()

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get('POSTGRES_HOST'),
    port=int(os.environ.get('POSTGRES_PORT')),
    database=os.environ.get('POSTGRES_DBNAME'),
    user=os.environ.get('POSTGRES_USER'),
    password=os.environ.get('POSTGRES_PASSWORD'),
)

session = boto3.Session(
    aws_access_key_id=os.getenv('BUCKET_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('BUCKET_SECRET_ACCESS_KEY')
)

BUCKET_NAME = os.getenv('BUCKET_NAME')


@app.task(name='llm.tasks.process_pdf')
def process_pdf(filename, user_id):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=255,
        chunk_overlap=20,
        length_function=len,
        add_start_index=True
    )

    s3 = session.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net')
    normalized_filename = str(user_id) + '-' + filename

    # Получить объект
    get_object_response = s3.get_object(Bucket=BUCKET_NAME, Key=normalized_filename)
    pdf_object = get_object_response['Body'].read()

    with io.BytesIO(pdf_object) as open_pdf_file:
        loader = PyPDFBytesLoader(open_pdf_file, text_splitter)
        docs = loader.load_and_split()

    print(f'done, loaded {len(docs)} docs (pages)')

    # FIXME: Uncomment on prod

    # print('perfoming tokenization')
    batchsize = 5000
    for i in range(0, len(docs), batchsize):
        PGVector.from_documents(
            embedding=OpenAIEmbeddings(),
            documents=docs[i:i+batchsize],
            collection_name=normalized_filename,
            connection_string=CONNECTION_STRING,
            )
    # print('done')

    # For test, simulates embedding docs
    # time.sleep(3)

    return f'{normalized_filename} loaded'

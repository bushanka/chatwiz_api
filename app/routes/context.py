import asyncio
import logging
import os

import aioboto3
from celery import Celery
from celery.result import AsyncResult
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from ..models import context

app = Celery('chatwiztasks', broker='pyamqp://guest@localhost//', backend='rpc://')

load_dotenv()
session = aioboto3.Session(
    aws_access_key_id=os.getenv('BUCKET_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('BUCKET_SECRET_ACCESS_KEY')
)

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/context",
    tags=["context"],
)


# Converts a Celery tasks to an async function
# FIXME: Как нормально выйти из while-true ?
async def celery_async_wrapper(app, task_name, task_args, queue):
    delay = 0.1
    max_tries = 20

    task_id = app.send_task(task_name, [*task_args], queue=queue)
    task = AsyncResult(task_id)

    while not task.ready() and max_tries > 0:
        await asyncio.sleep(delay)
        # Через 5 итераций выходит на 2 секунды
        # Total wait: 3.1 sec после 5 итераций, далее по 2 сек делей
        # Максимум будет 33 секунды загружать файл - потом Time out 
        delay = min(delay * 2, 2)  # exponential backoff, max 2 seconds
        max_tries -= 1

    if max_tries <= 0:
        return 'Failed'

    return 'OK'


@router.post(
    "/uploadfile/",
    responses={
        status.HTTP_200_OK: {
            "description": "Return OK if upload is successful"

        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad file given"
        },
        status.HTTP_504_GATEWAY_TIMEOUT:
            {
                "description": "File was not downloaded within the allotted time"
            }
    }
)
async def create_upload_file(user_id, file: UploadFile) -> context.FileUploadStatus:
    # Get the file size (in bytes)
    file.file.seek(0, 2)
    file_size = file.file.tell()

    # move the cursor back to the beginning
    await file.seek(0)

    if file_size > 2 * 1024 * 1024:  # todo сделать проверку на максимальный размер в зависимости от пользователя
        # more than 2 MB
        raise HTTPException(status_code=400, detail="File too large")

    content_type = file.content_type
    if content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    async with session.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net') as s3:
        await s3.upload_fileobj(file.file,
                                'linkup-test-bucket',
                                str(user_id) + '-' + file.filename)

    # task_id = app.send_task('llm.tasks.process_pdf', (file.filename, user_id), queue='chatwiztasks_queue')

    result = await celery_async_wrapper(app, 'llm.tasks.process_pdf', (file.filename, user_id), 'chatwiztasks_queue')

    if result == 'OK':
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content='OK'
        )

    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content='Time out'
    )

    # return context.FileUploadStatus(
    #     task_id=str(task_id),
    #     status='pending'
    # )

# @router.post(
#     "/get_status/",
#     responses={
#         status.HTTP_200_OK: {
#             "description": "Get status of file uploading"  
#         }
#     }
# )
# async def create_upload_file(task_id: str) -> context.FileUploadStatus:
#     task = AsyncResult(task_id)
#     if not task.ready():
#         return context.FileUploadStatus(
#             task_id=str(task_id), 
#             status='pending'
#         )

#     return context.FileUploadStatus(
#         task_id=str(task_id), 
#         status='success'
#     )

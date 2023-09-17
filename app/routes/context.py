import asyncio
import logging
import os
from typing import List
import aiofiles

import aioboto3
from celery import Celery
from celery.result import AsyncResult
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
import tempfile

from starlette import status
from starlette.responses import JSONResponse

from app.models.user import AuthorisedUserInfo
from app.schemas.crud import get_subscription_plan_info, add_context, update_user, get_user_contexts_from_db
from app.schemas.db_schemas import Context
from app.security.security_api import get_current_user

from app.models.context import UserContextsInfo


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
        status.HTTP_504_GATEWAY_TIMEOUT: {
            "description": "File was not downloaded within the allotted time"
        }
    }
)
async def create_upload_file(file: UploadFile,
                             user: AuthorisedUserInfo = Depends(get_current_user)) -> JSONResponse:
    # Get the file size (in bytes)
    sub_plan_info = await get_subscription_plan_info(user.subscription_plan_id)

    file.file.seek(0, 2)
    file_size = file.file.tell()

    # move the cursor back to the beginning
    await file.seek(0)
    if user.num_of_contexts >= sub_plan_info.max_context_size:
        raise HTTPException(status_code=400, detail="Max amount of contexts already reached")

    if file_size > sub_plan_info.max_context_size * 1024 * 1024:
        # more than 2 MB
        raise HTTPException(status_code=400, detail="File too large")

    content_type = file.content_type
    if content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    async with session.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net') as s3:
        await s3.upload_fileobj(file.file,
                                'linkup-test-bucket',
                                str(user.id) + '-' + file.filename)

    # task_id = app.send_task('llm.tasks.process_pdf', (file.filename, user_id), queue='chatwiztasks_queue')

    logger.info(type(file.file))

    result = await celery_async_wrapper(app, 'llm.tasks.process_pdf', (file.filename, user.id), 'chatwiztasks_queue')
    if result == 'OK':
        context = Context(
            name=str(user.id) + '-' + file.filename,
            user_id=user.id,
            type=content_type,
            size=file_size,
            path='linkup-test-bucket' + str(user.id) + '-' + file.filename
        )

        await update_user(user_email=user.email,
                          new_values={'num_of_contexts': user.num_of_contexts + 1})
        await add_context(context)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content='OK'
        )

    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content='Time out'
    )


@router.post(
    "/get_contexts/",
    responses={
        status.HTTP_200_OK: {
            "description": "Return all user contexts"
        },
    }
)
async def get_user_contexts(user: AuthorisedUserInfo = Depends(get_current_user)) -> UserContextsInfo:
    user_contexts = await get_user_contexts_from_db(user.id)
    return user_contexts


@router.get(
    "/download_context",
    responses={
        status.HTTP_200_OK: {
            "description": "Return given context"
        },
    }
)
async def download_context(filename:str, user: AuthorisedUserInfo = Depends(get_current_user)):
    # Код для получения байтового объекта файла PDF
    async with session.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net') as s3:
        response = await s3.get_object(Bucket='linkup-test-bucket', Key=filename)
        pdf_bytes = await response['Body'].read()
    
    async with aiofiles.tempfile.NamedTemporaryFile(delete=False) as temp_file:
        await temp_file.write(pdf_bytes)
        return FileResponse(temp_file.name, media_type='multipart/form-data', filename=filename)
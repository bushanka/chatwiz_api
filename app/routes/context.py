import asyncio
import logging
import os

import aioboto3
import aiofiles
from celery import Celery
from celery.result import AsyncResult
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from starlette import status
from starlette.responses import JSONResponse

from app.models.context import UserContextsInfo, ContextInfo
from app.models.user import AuthorisedUserInfo
from app.name_checkup import check_name_safety
from app.schemas.crud import add_context, update_user, get_user_contexts_from_db, \
    delete_context, get_user_context_by_id_from_db
from app.schemas.db_schemas import Context
from app.security.security_api import get_current_user
from app.status_messages import StatusMessage

app = Celery('chatwiztasks', broker=os.getenv('APP_BROKER_URI'), backend='rpc://')

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


# @router.post(
#     "/uploadfile/",
#     responses={
#         status.HTTP_200_OK: {
#             "description": "Return OK if upload is successful"
#         },
#         status.HTTP_400_BAD_REQUEST: {
#             "description": "Bad file given"
#         },
#         status.HTTP_504_GATEWAY_TIMEOUT: {
#             "description": "File was not downloaded within the allotted time"
#         }
#     }
# )
async def create_upload_file(file: UploadFile,
                             user: AuthorisedUserInfo = Depends(get_current_user)) -> JSONResponse:
    # Get the file size (in bytes)
    if user.num_of_contexts >= user.max_context_size:
        raise HTTPException(status_code=400, detail="Max amount of contexts already reached")
    if user.action_points_used + int(os.getenv('FILE_UPLOAD')) > user.max_action_points:
        raise HTTPException(status_code=400, detail="Not enough action points to upload")
    if not check_name_safety(file.filename):
        raise HTTPException(status_code=400, detail='File name must contain only [a-zA-Z0-9], -, _, /, \\ symbols')

    usr_contexts = await get_user_contexts_from_db(user_id=user.id)
    if file.filename in {ctxt.name for ctxt in usr_contexts.contexts}:
        raise HTTPException(status_code=400, detail='File with such a name already exists')

    file.file.seek(0, 2)
    file_size = file.file.tell()

    # move the cursor back to the beginning
    await file.seek(0)

    if file_size > user.max_context_size * 1024 * 1024:
        # more than 2 MB
        raise HTTPException(status_code=400, detail="File too large")

    content_type = file.content_type
    if content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    async with session.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net') as s3:
        await s3.upload_fileobj(file.file,
                                os.getenv('BUCKET_NAME'),
                                str(user.id) + '-' + file.filename,
                                ExtraArgs={'ContentType': 'application/pdf'}
                                )

    # task_id = app.send_task('llm.tasks.process_pdf', (file.filename, user_id), queue='chatwiztasks_queue')

    logger.info(type(file.file))

    # result = await celery_async_wrapper(app, 'llm.tasks.process_pdf', (file.filename, user.id), 'chatwiztasks_queue')
    result = 'OK'
    if result == 'OK':
        context = Context(
            name=str(user.id) + '-' + file.filename,
            user_id=user.id,
            type=content_type,
            size=file_size,
            path='https://' + os.getenv('BUCKET_NAME') + '/' + str(user.id) + '-' + file.filename
        )

        await update_user(user_email=user.email,
                          new_values={'action_points_used': user.action_points_used + int(os.getenv('FILE_UPLOAD'))})
        context_added = await add_context(context)

        return context_added.id

    else:
        raise HTTPException(status_code=408, detail="Time out")


@router.get(
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
    "/get_context_by_id/",
    responses={
        status.HTTP_200_OK: {
            "description": "Return user context by id"
        },
    }
)
async def get_user_context_by_id(context_id: int, user: AuthorisedUserInfo = Depends(get_current_user)) -> ContextInfo:
    user_context_by_id = await get_user_context_by_id_from_db(context_id, user.id)
    if user_context_by_id:
        return user_context_by_id
    else:
        raise HTTPException(status_code=403, detail=f'Context {context_id} user {user.id} does not exist')


@router.post(
    "/download_context",
    responses={
        status.HTTP_200_OK: {
            "description": "Return given context"
        },
    }
)
async def download_context(filename: str, user: AuthorisedUserInfo = Depends(get_current_user)):
    # Код для получения байтового объекта файла PDF
    async with session.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net') as s3:
        response = await s3.get_object(Bucket=os.getenv('BUCKET_NAME'), Key=filename)
        pdf_bytes = await response['Body'].read()

    async with aiofiles.tempfile.NamedTemporaryFile(delete=False) as temp_file:
        await temp_file.write(pdf_bytes)
        return FileResponse(temp_file.name, media_type='multipart/form-data', filename=filename)


def change_context_name():  # todo
    pass


@router.delete('/delete_context/{context_id}',
               responses={
                   status.HTTP_200_OK: {
                       "description": "Chat has been deleted"
                   },
               }
               )
async def delete_context_handle(context_id: int, user: AuthorisedUserInfo = Depends(get_current_user)):
    if context_id not in user.context_ids:
        raise HTTPException(status_code=403, detail='Not current user context')
    context_name = await delete_context(context_id)
    async with session.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net') as s3:
        await s3.delete_object(Key=context_name,
                               Bucket=os.getenv('BUCKET_NAME'),
                               )
    return JSONResponse(status_code=200, content=StatusMessage.context_deleted.value)
    # todo удалять файл из хранилища

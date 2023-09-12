from fastapi import APIRouter, UploadFile, HTTPException
from starlette.responses import JSONResponse
from starlette import status
from dotenv import load_dotenv

import aioboto3
import logging
import os


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


@router.post(
    "/uploadfile/",
    responses={
        status.HTTP_200_OK: {
            "description": "Return OK if upload is successful"
                
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad file given"
        }
    }
)
async def create_upload_file(user_id, file: UploadFile) -> JSONResponse:
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

    return JSONResponse(status_code=200, content='File uploaded successfully')

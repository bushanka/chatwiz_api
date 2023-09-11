import logging
import shutil

from fastapi import APIRouter, UploadFile, HTTPException
from starlette import status

import boto3
from starlette.responses import JSONResponse

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/context",
    tags=["context"],
)


@router.post("/uploadfile/",
             responses={
                 status.HTTP_200_OK: {
                     "description": "Return all authorized users"
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

    s3.upload_fileobj(file.file,
                      'linkup-test-bucket',
                      str(user_id) + '-' + file.filename)  # todo check if it's possible to do it async


    return JSONResponse(status_code=200, content='File uploaded successfully')

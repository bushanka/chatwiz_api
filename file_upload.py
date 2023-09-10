import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import HTTPException
from starlette_validation_uploadfile import ValidateUploadFileMiddleware

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # Get the file size (in bytes)
    file.file.seek(0, 2)
    file_size = file.file.tell()

    # move the cursor back to the beginning
    await file.seek(0)

    if file_size > 2 * 1024 * 1024:
        # more than 2 MB
        raise HTTPException(status_code=400, detail="File too large")

    # check the content type (MIME type)
    content_type = file.content_type
    if content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # do something with the valid file
    return {"filename": file.filename}

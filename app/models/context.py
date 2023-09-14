from pydantic import BaseModel
from typing import List


class FileUploadStatus(BaseModel):
    status: str
    task_id: str
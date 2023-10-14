"""
Блок с ручками связанными с фидбеком.
"""

import logging

from fastapi import APIRouter, status, HTTPException, Depends
from starlette.responses import JSONResponse

from app.models.user import AuthorisedUserInfo
from app.schemas.crud import add_feedback
from app.schemas.db_schemas import Feedback
from app.security.security_api import get_current_user

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/feedback",
    tags=["feedback"],
)

MAX_COMMENT_LEN = 1000  # yet hardcoded in migration and sqlaclchemy schema


@router.post(
    '/',
    responses={
        status.HTTP_200_OK: {
            "description": "Feedback has been left successfully"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Comment is too long"
        }
    }
)
async def leave_feedback(comment: str,
                         user: AuthorisedUserInfo = Depends(get_current_user),
                         ):
    if len(comment) > MAX_COMMENT_LEN:
        raise HTTPException(status_code=400, detail="Comment is too long")
    new_feedback = Feedback(user_id=user.id,
                            comment_text=comment)
    await add_feedback(new_feedback)
    return JSONResponse(status_code=200, content="Feedback has been left successfully")

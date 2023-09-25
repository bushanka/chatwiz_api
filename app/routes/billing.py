import logging
import os
import uuid
import asyncio

from dotenv import load_dotenv
from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from yookassa import Configuration, Payment

from app.models import billing
from app.schemas.crud import get_subscription_plan_info
from app.security.security_api import get_current_user
from app.models.user import AuthorisedUserInfo

logger = logging.getLogger("uvicorn")

load_dotenv()
Configuration.account_id = os.getenv('YOKASSA_ACCOUNT_ID')
Configuration.secret_key = os.getenv('YOKASSA_SECRET_KEY')

router = APIRouter(
    prefix="/billing",
    tags=["billing"],
)


@router.post(
    "/createpay/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": billing.CreatedPayment,
            "description": "Create and return payment details"
        },
    }
)
async def create_payment(subscription_plan_id: int, user: AuthorisedUserInfo = Depends(get_current_user)) -> billing.CreatedPayment:
    # FIXME: Request to db via ORM to get price

    subscription_plan = await get_subscription_plan_info(subscription_plan_id)
    print(subscription_plan)
    value = subscription_plan.price
    description = 'Order 1'

    # Generate unique payment key
    indepotence_key = uuid.uuid4()

    # Create payment
    payment_coros = asyncio.to_thread(
        Payment.create,
        {
            "amount": {
                "value": value,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "embedded",
            },
            # TODO: Check what capture is
            "capture": True,
            "description": description,
            "save_payment_method": True
        }, 
        indepotence_key
    )

    payment = await payment_coros
    
    logger.info(f"Payment created {user}")

    # FIXME: Request to ORM to save payment_method, here we need user_token??

    # FIXME: We need to periodically poll the Yukassa server to check the payment status - 
    # either we do it through celery or we need to set up a webhook

    return billing.CreatedPayment(
        indepotence_key=str(indepotence_key),
        confirmation_token=payment.confirmation.confirmation_token
    )


@router.get('/hello_world')
async def hello_world(user=Depends(get_current_user)) -> JSONResponse:
    return JSONResponse(status_code=200, content=f'Hello {user.name}')


async def chek_payment():
    pass


async def confirm_purchase():
    pass


@router.post(
    "/cancelsub/",
    responses={
        status.HTTP_200_OK: {
            "model": billing.CancelSubscription,
            "description": "Cancel user subscription"
        },
    }
)
async def cancel_subscription(user: AuthorisedUserInfo = Depends(get_current_user)):
    # FIXME: Request to ORM to cancel subscription

    return billing.CancelSubscription(
        user_id=user_id
    )

# # NOTE: periodically check payment status
# from yookassa import Payment, Configuration
# payment_id = '2c8ea686-000f-5000-9000-14c437e81122'
# payment = Payment.find_one(payment_id)
# print(payment)

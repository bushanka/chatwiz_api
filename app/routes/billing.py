from fastapi import APIRouter, status
from yookassa import Configuration, Payment
from dotenv import load_dotenv

import uuid
import os
import logging

from ..models import billing, user


logger = logging.getLogger("uvicorn")

load_dotenv()
Configuration.account_id = os.getenv('YOKASSA_ACCOUNT_ID')
Configuration.secret_key = os.getenv('YOKASSA_SECRET_KEY')

router = APIRouter(
    prefix="/billing",
    tags=["billing"],
)


@router.post(
        "/createpay/{user_token}",
        status_code=status.HTTP_201_CREATED,
        responses={
            status.HTTP_201_CREATED: {
                "model": billing.CreatedPayment, 
                "description": "Create and return payment details"
            },
        }
)
async def create_payment(user_token: str) -> billing.CreatedPayment:
    # FIXME: Request to db via ORM to get price
    value = '1500.00'
    description = ' Order 1'

    # Generate unique payment key
    indepotence_key = uuid.uuid4()

    # Create payment
    payment = Payment.create({
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
    }, indepotence_key)

    logger.info(f"Payment created, user_token {user_token}")

    # FIXME: Request to ORM to save payment_method, here we nee user_token??

    # FIXME: We need to periodically poll the Yukassa server to check the payment status - 
    # either we do it through celery or we need to set up a webhook

    return billing.CreatedPayment(
        indepotence_key=str(indepotence_key),
        confirmation_token=payment.confirmation.confirmation_token
    )


@router.post(
        "/cancelsub/{user_id}",
        responses={
            status.HTTP_200_OK: {
                "model": billing.CancelSubscription, 
                "description": "Cancel user subscription"
            },
        }
)
async def cancel_subscription(user_id: str):
    # FIXME: Request to ORM to cancel subscription

    return billing.CancelSubscription(
        user_id=user_id
    )

# # NOTE: periodically check payment status
# from yookassa import Payment, Configuration
# payment_id = '2c8ea686-000f-5000-9000-14c437e81122'
# payment = Payment.find_one(payment_id)
# print(payment)
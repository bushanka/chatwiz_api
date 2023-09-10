from yookassa import Configuration, Payment
import uuid

Configuration.account_id = '252962'
Configuration.secret_key = 'test_88ebn3FSZvhXNwCbOkaHJmYQX1arNGx2H0QzU2Yxqn8'
indepotence_key = uuid.uuid4()
payment = Payment.create({
    "amount": {
        "value": "1.00",
        "currency": "RUB"
    },
    "confirmation": {
        # После усппешной оплаты юзера редиректит в прописанный url
        # если используем виджет - поставить 
        "type": "embedded",
    },
    "capture": True,
    # Описание платежа, до 128 символов
    "description": "Заказ №1",
    # Сохраняем его метод оплаты, если юзер дал на это разрешение
    "save_payment_method": True
}, indepotence_key)

# payment = Payment.create({
#     "amount": {
#         "value": "1900.00",
#         "currency": "RUB"
#     },
#     "capture": True,
#     "payment_method_id": "2c8e9c2e-000f-5000-8000-1adb158ca71c",
#     "description": "Заказ №105"
# })
print()
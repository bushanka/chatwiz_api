def reg_user(email, passwords, name, surname) -> sucsess_or_error:  # 3
    """
    При успехе создания, отправляем письмо с подтверждением + заводим дурика в базу с уникальным токеном
    :param emalil:
    :param passwords: их должно быть 2 на всякий случай
    :param name:
    :param surname:
    :return:
    """
    pass


def confirm_user_registration(user_token) -> sucsess_or_error:  # 3
    """
    Подтверждаем регистрацию или говорим, пошел нахуй
    :param user_token:
    :return:
    """


def login_user(credentials) -> sucsess_or_error:  # 3
    """
    Авторизация пользователя. Если не подтверждена регистрация - то отдельный респонд.
    :param credentials:
    :return:
    """


def change_user_password(authorised_user_token, old_password, new_passwords) -> sucsess_or_error:  # 3
    """
    тут очев
    :param authorised_user_token:
    :param old_password:
    :param new_passwords:
    :return:
    """


class AuthorisedUserInfo:
    name: str
    surname: str
    email: str


def get_user_info(authorised_user_token) -> AuthorisedUserInfo:  # 2  # todo think about it
    """

    :param authorised_user_token:
    :return:
    """


def delete_account(authorised_user_token) -> sucsess_or_error:  # 1
    """
    тут очев
    :param authorised_user_token:
    :return:
    """



class SubscriptionPlan:
    id: int
    price: float
    max_num_of_contexts: int
    max_size_of_context: float
    max_question_length_in_chars: int
    max_number_of_chats: int
    max_number_of_queries: int
    duration: int  # в сек


class UserSubscription:  # мб стоит добавить цену покупки для изменения стоимости тарифов
    id: int
    user_token: int
    subscription_plan_id: int
    current_num_of_contexts: int
    current_number_of_chats: int
    current_number_of_queries: int
    purchase_date: timestamp


def purchase_subscription(authorised_user_token, subscription_id) -> sucsess_or_error: # 2
    """

    :param authorised_user_token:
    :param subscription_id:
    :return:
    """
    # 0. Как-то по subscription_id мы получаем цену


    # 1. Создаем платеж
    from yookassa import Configuration, Payment
    import uuid

    Configuration.account_id = '252962'
    Configuration.secret_key = 'test_88ebn3FSZvhXNwCbOkaHJmYQX1arNGx2H0QzU2Yxqn8'
    indepotence_key = uuid.uuid4()
    payment = Payment.create({
        "amount": {
            "value": "100.00",
            "currency": "RUB"
        },
        # # FIXME: нужно для сохранения метода платежа - для подписки
        # "payment_method_data": {
        #     "type": "bank_card"
        # },
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
    print()
    # это ключ идемпотентности - если вновь сделать такой же запрос с этим же ключем - 2 раза списаний не будет


    # 2. По идее payment будет иметь такую стрктуру (ответ от API юкассы):

    # {
    #     "id": "23d93cac-000f-5000-8000-126628f15141",
    #     "status": "pending",
    #     "paid": false,
    #     "amount": {
    #         "value": "100.00",
    #         "currency": "RUB"
    #     },
    #     "confirmation": {
    #         "type": "redirect",
    #         FIXME: Это ссылка на оплату, отправляем пользователя на нее
    #         "confirmation_url": "https://yoomoney.ru/api-pages/v2/payment-confirm/epl?orderId=23d93cac-000f-5000-8000-126628f15141"
    #     },
    #     "created_at": "2019-01-22T14:30:45.129Z",
    #     "description": "Заказ №1",
    #     "metadata": {},
    #     "recipient": {
    #         "account_id": "100500",
    #         "gateway_id": "100700"
    #     },
    #     "refundable": false,
    #     "test": false
    # }


    # 3. Далее, после этого надо либо периодически опрашивать сервер о статусе платежа так:
    payment_id = '23d93cac-000f-5000-8000-126628f15141'
    payment = Payment.find_one(payment_id)

    # Либо подписаться на webhook и обрабатывать взодящие уведомления примерно так:
    from yookassa import Configuration, Webhook
    Configuration.configure_auth_token('<Bearer Token>')
    response = Webhook.add({
        # на какие события подписываемся
        "event": "payment.succeeded",
        # ссылка на enpoint нашего api
        "url": "https://www.example.com/notification_url",
    })


    # 4. После успешной оплаты JSON payment такой:

    # {
    #     "id": "22e18a2f-000f-5000-a000-1db6312b7767",
    #     "status": "succeeded",
    #     "paid": true,
    #     "amount": {
    #         "value": "2.00",
    #         "currency": "RUB"
    #     },
    #     "authorization_details": {
    #         "rrn": "10000000000",
    #         "auth_code": "000000",
    #         "three_d_secure": {
    #         "applied": true
    #         }
    #     },
    #     "captured_at": "2018-07-18T17:20:50.825Z",
    #     "created_at": "2018-07-18T17:18:39.345Z",
    #     "description": "Заказ №72",
    #     "metadata": {},
    #     "payment_method": {
    #         "type": "bank_card",
    #          FIXME: СОХРАНИТЬ ID в базу для автоплатежей
    #         "id": "22e18a2f-000f-5000-a000-1db6312b7767",
    #          FIXME: Надо убедиться, что тут тру - значит сохранили метод платежа в юкассе
    #         "saved": true,
    #         "card": {
    #         "first6": "555555",
    #         "last4": "4444",
    #         "expiry_month": "07",
    #         "expiry_year": "2022",
    #         "card_type": "MasterCard",
    #         "issuer_country": "RU",
    #         "issuer_name": "Sberbank"
    #         },
    #         "title": "Bank card *4444"
    #     },
    #     "refundable": true,
    #     "refunded_amount": {
    #         "value": "0.00",
    #         "currency": "RUB"
    #     },
    #     "recipient": {
    #         "account_id": "100500",
    #         "gateway_id": "100700"
    #     },
    #     "test": false
    # }


    # 5. Для автоплатежа или платежа без введения данных о карте опять, делаем так:
    payment = Payment.create({
        "amount": {
            "value": "100.00",
            "currency": "RUB"
        },
        "capture": True,
        "payment_method_id": "<Идентификатор сохраненного способа оплаты>",
        "description": "Заказ №105"
    })

    # 6. Повторяем пункт 3 для проверки статуса платежа
    # Если пользователь отозвал свое разрешение на повторные списания из кошелька ЮMoney, платеж не пройдет. 
    # В объекте cancellation_details будет указана причина отмены — permission_revoked:

    # {
    #     "id": "24a40656-000f-5000-9000-134108dd5325",
    #     "status": "canceled",
    #     "paid": false,
    #     "amount": {
    #         "value": "10.00",
    #         "currency": "RUB"
    #     },
    #     "created_at": "2019-06-25T10:08:22.531Z",
    #     "metadata": {},
    #     "payment_method": {
    #         "type": "yoo_money",
    #         "id": "249ea698-000f-5000-9000-1200128b882c",
    #         "saved": true
    #     },
    #     "recipient": {
    #         "account_id": "100500",
    #         "gateway_id": "100700"
    #     },
    #     "refundable": false,
    #     "test": false,
    #     "cancellation_details": {
    #         "party": "yoo_money",
    #         "reason": "permission_revoked"
    #     }
    # }

    # Пример возврата платежа
    from yookassa import Refund
    refund = Refund.create({
        "amount": {
            "value": "2.00",
            "currency": "RUB"
        },
        "payment_id": "21740069-000f-50be-b000-0486ffbf45b0"
    })


def change_subscription_plan():
    """
    :return:
    """
    # Базовый пример логики
    # 1. Из бд берем текущий план пользователя
    # 2.1 Создаем платежку на обновления плана: юзер доплачивает разницу подписики / кол-во оставшихся дней, например
    # 2.2 Или же, юзер просто платит заново и у него все обновляется
    # Енивей пайплайн создания платежки будет +- такой же как и в purchase_subscription


def cancel_subscription():
    """
    :return:
    """

    # По всей видимости - это на нашей стороне, 
    # то есть, когда юзер отменяет - мы должны удалить из базы его "<Идентификатор сохраненного способа оплаты>"
    # Но он так же может как-то сам это сделать через юкассу, хз как
    # На сайте с документацией написано только это:
    # "Если пользователь отозвал свое разрешение на повторные списания из кошелька ЮMoney, платеж не пройдет."
    # "В объекте cancellation_details будет указана причина отмены — permission_revoked."


def get_billing_info(authorised_user_token) -> UserSubscriptionForDisplay:
    """

    :param authorised_user_token:
    :return:
    """


class ContextType:  # очев
    id: int
    name: str
    max_size: float


class Context:
    id: int
    name: str
    context_type_id: int
    size: float  # потом трансформируется в кол-во страниц или продолжительность видео
    path: Path
    sample_questions: List[str]


class ContextInfo:  # то что нужно для отрисовки
    pass


def upload_context(authorised_user_token, raw_context) -> sucsess_or_error:
    """

    :param authorised_user_token:
    :param raw_context:
    :return:
    """


def view_context(authorised_user_token, context_id) -> Any  # тут что-то для фронта, чтоб отобразить контекст
    """
    
    :param authorised_user_token: 
    :param context_id: 
    :return: 
    """


def show_context_library(authorised_user_token) -> List[ContextInfo]:
    """

    :param authorised_user_token:
    :return:
    """


def get_context_info(authorised_user_token, context_id) -> ContextInfo:
    """

    :param authorised_user_token:
    :param context_id:
    :return:
    """


def delete_context(authorised_user_token, context_id) -> sucsess_or_error:
    """

    :param authorised_user_token:
    :param context_id:
    :return:
    """


class ChatMessage:
    id: int
    chat_id: int
    history_id: int
    send_timestamp: timestamp
    text: str


class UserMessage(ChatMessage):
    user_token: int


class Chat:
    id: int
    name: str
    user_token: int
    context_id: Optional[int]


def create_chat(authorised_user_token, name="Chat+ ...", context=None) -> sucsess_or_error:
    """

    :param authorised_user_token:
    :param name:
    :param context:
    :return:
    """


def get_chats(authorised_user_token) -> List[Chat]:
    """

    :param authorised_user_token:
    :return:
    """


def change_chat_name(authorised_user_token, chat_id, new_name) -> sucsess_or_error:
    """

    :param authorised_user_token:
    :param chat_id:
    :param new_name:
    :return:
    """


def delete_chat(authorised_user_token, chat_id) -> sucsess_or_error:
    """

    :param authorised_user_token:
    :param chat_id:
    :return:
    """


def get_recent_chats(authorised_user_token) -> List[Chat]:
    """

    :param authorised_user_token:
    :return:
    """


def summarize_context(authorised_user_token, chat_id) -> str:
    """

    :param authorised_user_token:
    :param chat_id:
    :return:
    """


def clear_chat(authorised_user_token, chat_id) -> sucsess_or_error:
    """

    :param authorised_user_token:
    :param chat_id:
    :return:
    """


class AnswerMessage(ChatMessage):
    user_message_id: int
    context_info: Any


def send_message(authorised_user_token, chat_id, message_text) -> AnswerMessage:
    """

    :param authorised_user_token:
    :param chat_id:
    :param message_text:
    :return:
    """

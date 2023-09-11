
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

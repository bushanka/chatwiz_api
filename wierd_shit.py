from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from hashlib import sha256
import re
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
import string
import secrets
import smtplib
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "userinfo"

    user_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    confirmation_token = Column(String(255), nullable=False)


def generate_conf_token(length=16):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token


def send_registration_email(user):
    # Настройки для отправки почты
    smtp_host = 'smtp.yandex.ru'
    smtp_port = 465
    smtp_username = 'no-reply@growth-tech.ru'
    smtp_password = '@zuRu@@qN2J8.ZR'

    sender_email = 'no-reply@growth-tech.ru'
    receiver_email = user.email
    support_email = 'team@growth-tech.ru'

    # Создаем объект сообщения
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Подтверждение регистрации'
    message['From'] = sender_email
    message['To'] = receiver_email
    conf_link = f'http://www.growth-tech.ru/confirm_reg/?token={user.confirmation_token}&user_id={user.user_id}'

    # Создаем HTML версию письма
    html = '''
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Подтвердите Вашу Регистрацию - Требуется активация аккаунта</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 14px;
                line-height: 1.5;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f2f2f2;
            }}
            h1 {{
                font-size: 24px;
                margin-bottom: 20px;
            }}
            p {{
                margin-bottom: 10px;
            }}
            a {{
                color: #007bff;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Подтвердите Вашу Регистрацию - Требуется активация аккаунта</h1>
            <p>Уважаемый {name},</p>
            <p>Благодарим Вас за регистрацию на нашем веб-сайте! Мы рады приветствовать Вас в нашем сообществе. Прежде чем Вы сможете воспользоваться всеми преимуществами нашей платформы, мы просим Вас подтвердить Вашу регистрацию.</p>
            <p>Для активации аккаунта, пожалуйста, <a href="{conf_link}">нажмите на ссылку</a>.</p>
            <p>Ссылка будет действительна в течение 24 часов из соображений безопасности. Если у Вас не получается кликнуть по ссылке, пожалуйста, скопируйте ее и вставьте в адресную строку Вашего браузера.</p>
            <p>Если Вы не регистрировали аккаунт на нашем веб-сайте, пожалуйста, проигнорируйте это письмо.</p>
            <p>Если у Вас возникли вопросы или нужна помощь, пожалуйста, не стесняйтесь обратиться в нашу службу поддержки по адресу <a href="mailto:{support_email}">{support_email}</a>.</p>
            <p>Спасибо,<br>Команда LinkUp</p>
        </div>
    </body>
    </html>
    '''.format(name=user.name, conf_link=conf_link, support_email=support_email)

    # Добавляем HTML версию письма к объекту сообщения
    message.attach(MIMEText(html, 'html'))

    # Отправка письма через SMTP сервер
    smtp_server = SMTP_SSL(smtp_host, port=465)
    smtp_server.login(smtp_username, smtp_password)
    smtp_server.sendmail(sender_email, receiver_email, message.as_string())

    # Disconnect
    smtp_server.quit()


args = {
    "host": "51.250.50.13",
    "user": "postgres",
    "password": "11111111",
    "dbname": "postgres",
    "port": "5432"
}

session_maker = sessionmaker(create_engine('postgresql+psycopg2://', connect_args=args
                                           ))


def validate_password(password):
    if len(password) < 5:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True


def password_encoder(password: str) -> str:
    return str(sha256(password.encode('utf-8')).hexdigest())


def email_check(email):
    session = session_maker()
    return session.execute(text(f"select exists (select * from userinfo where email = '{email}') as has_data")).one()[0]


def add_user(user_to_db, session):
    session.add(user_to_db)
    session.commit()


def handler(event, context):
    user_name = event['queryStringParameters']['name']
    user_surname = event['queryStringParameters']['surname']
    email = event['queryStringParameters']['email']
    password = event['queryStringParameters']['password']

    if not validate_password(password):
        return {
            'statusCode': 200,
            'body': '{"message": "Not valid password"}'}
    else:
        password = password_encoder(password)

    try:
        email = validate_email(email).ascii_email
    except EmailNotValidError as e:
        reply = '{"message": "' + str(e) + '"}'
        return {
            'statusCode': 200,
            'body': reply}

    if email_check(email):
        return {
            'statusCode': 200,
            'body': '{"message": "User with this email already exists"}'}

    session = session_maker()
    new_user = User(
        name=user_name,
        surname=user_surname,
        email=email,
        password=password,
        confirmation_token=generate_conf_token()
    )

    add_user(new_user, session)
    send_registration_email(new_user)
    session.close()

    return {
        'statusCode': 200,
        'body': '{"message": "Success!"}'
    }
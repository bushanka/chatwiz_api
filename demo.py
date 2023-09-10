import os

from pydantic_models.user_models import SignUpUser
from cruds import create_sign_up_user, get_emails

from email_validator import validate_email

rabbit = SignUpUser(email=validate_email('211128@228.ru'),
                    password='431121')
# qwr = create_sign_up_user(rabbit)
# print(get_emails())
# print(validate_email('1234@228.ru').ascii_email)
# emails = get_emails()
# print(emails)

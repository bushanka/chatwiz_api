from enum import Enum


class StatusMessage(Enum):
    ok = "OK"
    no_such_email = "No user with such email"
    wrong_password = "Wrong password"
    user_exists = "User with such an email already exists"
    new_user_created = "User has been created"
    password_changed = "Password has been changed"
    chat_name_changed = "Chat name has been changed"
    chat_deleted = "Chat has been deleted"
    context_deleted = "Context has been deleted"
    user_deleted = "User has been deleted"

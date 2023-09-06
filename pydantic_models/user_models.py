from pydantic import BaseModel, ConfigDict
from email_validator import validate_email, ValidatedEmail


class SignUpUser(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    email: ValidatedEmail
    password: str

    def has_good_password(self) -> bool:
        if len(self.password) < 5:
            return False
        return True

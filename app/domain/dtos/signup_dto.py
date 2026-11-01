from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, StringConstraints

FullName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


class SignupCommand(BaseModel):
    model_config = ConfigDict(frozen = True)

    full_name: FullName
    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=20)

class SignupResult(BaseModel):
    model_config = ConfigDict(frozen = True)

    user_id: str
    email: EmailStr
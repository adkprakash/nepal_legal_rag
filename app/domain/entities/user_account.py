from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserAccount(BaseModel):
    model_config = ConfigDict(frozen = True)

    user_id: str
    full_name: str
    email: EmailStr
    password_hash: str
    created_at: datetime
    role: str = "user"
    is_active: bool = True
    
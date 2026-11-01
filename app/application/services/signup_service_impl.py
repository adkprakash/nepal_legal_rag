from datetime import datetime, timezone
from uuid import uuid4

from app.domain.dtos.signup_dto import SignupCommand, SignupResult
from app.domain.entities.user_account import UserAccount
from app.domain.gateways import PasswordHasher
from app.domain.repositories import UserRepository 
from app.domain.services.signup_service import SignupService

class SignupServiceImpl(SignupService):
    def __init__(self, users: UserRepository, password_hasher: PasswordHasher)-> None:
        self.user_repository = users
        self.password_hasher = password_hasher

    def signup(self, command: SignupCommand) -> SignupResult:
        user= UserAccount(
            user_id=str(uuid4()),
            full_name=command.full_name,
            email=command.email.lower(),
            password_hash=self.password_hasher.hash(command.password.get_secret_value()),
            created_at=datetime.now(timezone.utc),
        )
        self.user_repository.create(user)
        return SignupResult(user_id=user.user_id, email=user.email)
        

import pytest
from pydantic import ValidationError

from app.application.services.signup_service_impl import SignupServiceImpl
from app.domain.dtos.signup_dto import SignupCommand
from app.domain.entities.user_account import UserAccount
from app.domain.gateways import PasswordHasher
from app.domain.repositories import EmailAlreadyRegisteredError, UserRepository


class FakeUserRepository(UserRepository):
    def __init__(self) -> None:
        self.users: dict[str, UserAccount] = {}

    def create(self, user: UserAccount) -> None:
        if user.email in self.users:
            raise EmailAlreadyRegisteredError
        self.users[user.email] = user


class FakePasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return f"hashed_{password}"


def test_signup_normalises_email_and_hashes_password() -> None:
    users = FakeUserRepository()
    service = SignupServiceImpl(users=users, password_hasher=FakePasswordHasher())

    result = service.signup(
        SignupCommand(
            email="Ram@Example.com", full_name="  Ram Sharma ", password="horse-battery-staple"
        )
    )

    assert result.email == "ram@example.com"
    saved = users.users["ram@example.com"]
    assert saved.user_id == result.user_id
    assert saved.full_name == "Ram Sharma"
    assert saved.password_hash == "hashed_horse-battery-staple"


def test_signup_rejects_duplicate_email() -> None:
    service = SignupServiceImpl(users=FakeUserRepository(), password_hasher=FakePasswordHasher())
    service.signup(
        SignupCommand(email="ram@example.com", full_name="Ram", password="horse-battery-staple")
    )

    with pytest.raises(EmailAlreadyRegisteredError):
        service.signup(
            SignupCommand(email="RAM@example.com", full_name="Ram", password="another-password")
        )


def test_signup_rejects_bad_input() -> None:
    with pytest.raises(ValidationError):
        SignupCommand(email="not-an-email", full_name="Ram", password="horse-battery-staple")
    with pytest.raises(ValidationError):
        SignupCommand(email="ram@example.com", full_name="Ram", password="short")
    with pytest.raises(ValidationError):
        SignupCommand(email="ram@example.com", full_name="   ", password="horse-battery-staple")

from pwdlib import PasswordHash

from app.domain.gateways import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):
    def __init__(self) -> None:
        self.password_hasher = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self.password_hasher.hash(password)

from abc import ABC, abstractmethod

class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        "Return a one way has of the password"
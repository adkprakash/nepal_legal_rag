from abc import ABC, abstractmethod

from app.domain.dtos.signup_dto import SignupCommand, SignupResult

class SignupService(ABC):
    @abstractmethod
    def signup(self, command: SignupCommand) -> SignupResult:
        """Register a new user. Raises EmailAlreadyRegisteredError if the email is already taken."""
from abc import ABC, abstractmethod

from app.domain.entities.user_account import UserAccount

class EmailAlreadyRegisteredError(Exception):
    """Raised when trying to register an email that is already in use."""
    
class UserRepository(ABC):
    @abstractmethod
    def create(self, user: UserAccount) -> None:
        """Create a new user account."""
        pass
    
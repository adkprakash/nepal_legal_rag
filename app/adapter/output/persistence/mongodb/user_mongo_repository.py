from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from app.domain.entities.user_account import UserAccount
from app.domain.repositories import UserRepository, EmailAlreadyRegisteredError


class UserMongoRepository(UserRepository):
    def __init__(self, collection: Collection)-> None:
        self.collection = collection

    def create(self, user: UserAccount) -> None:
        try:
            self.collection.insert_one(user.model_dump())
        except DuplicateKeyError as exc:
            raise EmailAlreadyRegisteredError from exc
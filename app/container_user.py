from pymongo import MongoClient

from app.adapter.output.persistence.mongodb.user_mongo_repository import UserMongoRepository
from app.adapter.output.security.argon2_password_hasher import Argon2PasswordHasher
from app.application.services.signup_service_impl import SignupServiceImpl
from app.domain.services.signup_service import SignupService
from core.config import settings

mongo_client: MongoClient = MongoClient(settings.mongo_uri, tz_aware=True)
mongo_db = mongo_client[settings.mongo_db_name]

signup_service: SignupService = SignupServiceImpl(
    users=UserMongoRepository(mongo_db["users"]),
    password_hasher=Argon2PasswordHasher(),
)

def get_signup_service() -> SignupService:
    return signup_service
    
from fastapi import APIRouter, Depends, HTTPException, status


from app.container_user import get_signup_service
from app.domain.dtos.signup_dto import SignupCommand, SignupResult
from app.domain.repositories import EmailAlreadyRegisteredError
from app.domain.services.signup_service import SignupService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

class SignupResponse(SignupResult):
    message: str 

@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
def signup(
    command: SignupCommand,
    service: SignupService = Depends(get_signup_service),
) -> SignupResponse:
    try:
        result = service.signup(command)
    except EmailAlreadyRegisteredError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        ) from None
    return SignupResponse(
        user_id=result.user_id,
        email=result.email,
        message="User registered successfully",
    )
    
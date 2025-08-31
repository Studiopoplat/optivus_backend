from fastapi import APIRouter, Depends
from app.schemas.auth_schemas import (
    LoginRequest, RegisterRequest, TwoFAVerifyRequest,
    PasswordResetRequest, PasswordResetConfirmRequest,
    TokenResponse, TwoFARequiredResponse
)
from app.services import auth_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse | TwoFARequiredResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await auth_service.login(payload, db)


@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterRequest):
    return await auth_service.register(payload)


@router.post("/2fa/verify", response_model=TokenResponse)
async def verify_2fa(payload: TwoFAVerifyRequest):
    return await auth_service.verify_2fa(payload)


@router.post("/password/reset")
async def password_reset(payload: PasswordResetRequest):
    return await auth_service.password_reset(payload)


@router.post("/password/reset/confirm")
async def password_reset_confirm(payload: PasswordResetConfirmRequest):
    return await auth_service.password_reset_confirm(payload)

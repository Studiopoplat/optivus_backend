from fastapi import APIRouter, Depends
from app.schemas.user_schemas import (
    ChangePasswordRequest, SetPinRequest, ChangePinRequest, VerifyPinRequest,
    UserUpdateRequest, UserProfileResponse
)
from app.services import user_service
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(user=Depends(get_current_user)):
    return await user_service.get_profile(user)


@router.patch("/profile", response_model=UserProfileResponse)
async def update_profile(payload: UserUpdateRequest, user=Depends(get_current_user)):
    return await user_service.update_profile(user, payload)


@router.post("/change-password")
async def change_password(payload: ChangePasswordRequest, user=Depends(get_current_user)):
    return await user_service.change_password(user, payload)


@router.post("/set-pin")
async def set_pin(payload: SetPinRequest, user=Depends(get_current_user)):
    return await user_service.set_pin(user, payload)


@router.patch("/change-pin")
async def change_pin(payload: ChangePinRequest, user=Depends(get_current_user)):
    return await user_service.change_pin(user, payload)


@router.post("/verify-pin")
async def verify_pin(payload: VerifyPinRequest, user=Depends(get_current_user)):
    return await user_service.verify_user_pin(user, payload)

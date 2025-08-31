from fastapi import APIRouter, Depends
from app.schemas.kyc_schemas import KYCSubmitRequest, KYCStatusResponse
from app.services import kyc_service
from app.dependencies import get_current_user

router = APIRouter(prefix="/kyc", tags=["KYC"])


@router.get("/status", response_model=KYCStatusResponse)
async def get_kyc_status(user=Depends(get_current_user)):
    return await kyc_service.get_status(user)


@router.post("/submit")
async def submit_kyc(payload: KYCSubmitRequest, user=Depends(get_current_user)):
    return await kyc_service.submit(user, payload)

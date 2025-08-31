from fastapi import APIRouter, Depends
from app.schemas.admin_schemas import AdminStatsResponse, AdminUserResponse
from app.services import admin_service
from app.dependencies import get_current_admin
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats", response_model=AdminStatsResponse)
async def get_stats(admin=Depends(get_current_admin)):
    return await admin_service.get_stats(admin)


@router.get("/users", response_model=List[AdminUserResponse])
async def list_users(admin=Depends(get_current_admin)):
    return await admin_service.list_users(admin)


@router.get("/kyc")
async def list_kyc_requests(admin=Depends(get_current_admin)):
    return await admin_service.list_kyc_requests(admin)


@router.post("/kyc/{kyc_id}/process")
async def process_kyc(kyc_id: str, decision: str, admin=Depends(get_current_admin)):
    return await admin_service.process_kyc(admin, kyc_id, decision)


@router.get("/withdrawals")
async def list_withdrawals(admin=Depends(get_current_admin)):
    return await admin_service.list_withdrawals(admin)


@router.post("/withdrawals/{withdrawal_id}/approve")
async def approve_withdrawal(withdrawal_id: str, admin=Depends(get_current_admin)):
    return await admin_service.approve_withdrawal(admin, withdrawal_id)


@router.post("/withdrawals/{withdrawal_id}/deny")
async def deny_withdrawal(withdrawal_id: str, admin=Depends(get_current_admin)):
    return await admin_service.deny_withdrawal(admin, withdrawal_id)


@router.get("/transactions")
async def list_all_transactions(admin=Depends(get_current_admin)):
    return await admin_service.list_transactions(admin)

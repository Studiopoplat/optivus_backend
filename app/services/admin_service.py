from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime
from typing import List

from app.database import get_db
from app.schemas.admin_schemas import AdminStatsResponse, AdminUserResponse


# -----------------------------
# ADMIN DASHBOARD STATS
# -----------------------------
async def get_stats(admin, db: AsyncSession = Depends(get_db)) -> AdminStatsResponse:
    # Total users
    res_users = await db.execute(text("SELECT COUNT(*) FROM users"))
    total_users = res_users.scalar() or 0

    # Total referral earnings (all users)
    res_ref = await db.execute(
        text("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'referral_bonus'")
    )
    total_user_referral_earnings = str(res_ref.scalar() or 0)

    # Admin referral earnings (example: master admin = first admin user)
    res_admin = await db.execute(
        text("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'referral_bonus' AND user_id = :aid"),
        {"aid": admin["id"]},
    )
    admin_referral_earnings = str(res_admin.scalar() or 0)

    # Pending withdrawals
    res_wdr = await db.execute(text("SELECT COUNT(*) FROM withdrawals WHERE status = 'pending'"))
    pending_withdrawals_count = res_wdr.scalar() or 0

    # Protocol balance = sum of all user balances
    res_bal = await db.execute(text("SELECT COALESCE(SUM(balance), 0) FROM users"))
    protocol_balance = str(res_bal.scalar() or 0)

    return AdminStatsResponse(
        total_users=total_users,
        total_user_referral_earnings=total_user_referral_earnings,
        admin_referral_earnings=admin_referral_earnings,
        pending_withdrawals_count=pending_withdrawals_count,
        protocol_balance=protocol_balance,
    )


# -----------------------------
# USERS
# -----------------------------
async def list_users(admin, db: AsyncSession = Depends(get_db)) -> List[AdminUserResponse]:
    query = text("SELECT * FROM users ORDER BY created_at DESC")
    result = await db.execute(query)
    records = result.fetchall()

    return [
        AdminUserResponse(
            id=str(r.id),
            email=r.email,
            username=r.username,
            role=r.role,
            status=r.status,
            withdrawal_status=r.withdrawal_status,
            is_kyc_verified=r.is_kyc_verified,
            balance=str(r.balance),
        )
        for r in records
    ]


# -----------------------------
# KYC
# -----------------------------
async def list_kyc_requests(admin, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM kyc WHERE status = 'pending'")
    result = await db.execute(query)
    return [dict(r) for r in result.fetchall()]


async def process_kyc(admin, kyc_id: str, decision: str, db: AsyncSession = Depends(get_db)):
    if decision not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Decision must be 'approved' or 'rejected'")

    # Update KYC record
    update_q = text(
        "UPDATE kyc SET status = :st, reviewed_by = :aid, reviewed_at = :dt WHERE id = :id"
    )
    await db.execute(update_q, {"st": decision, "aid": admin["id"], "dt": datetime.utcnow(), "id": kyc_id})

    # If approved, mark user as verified
    if decision == "approved":
        user_update_q = text(
            "UPDATE users SET is_kyc_verified = true WHERE id = (SELECT user_id FROM kyc WHERE id = :id)"
        )
        await db.execute(user_update_q, {"id": kyc_id})

    await db.commit()
    return {"message": f"KYC {kyc_id} {decision}"}


# -----------------------------
# WITHDRAWALS
# -----------------------------
async def list_withdrawals(admin, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM withdrawals ORDER BY requested_at DESC")
    result = await db.execute(query)
    return [dict(r) for r in result.fetchall()]


async def approve_withdrawal(admin, withdrawal_id: str, db: AsyncSession = Depends(get_db)):
    if admin["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    query = text("UPDATE withdrawals SET status = 'approved' WHERE id = :wid")
    await db.execute(query, {"wid": withdrawal_id})
    await db.commit()
    return {"message": f"Withdrawal {withdrawal_id} approved"}


async def deny_withdrawal(admin, withdrawal_id: str, db: AsyncSession = Depends(get_db)):
    if admin["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    query = text("UPDATE withdrawals SET status = 'denied' WHERE id = :wid")
    await db.execute(query, {"wid": withdrawal_id})
    await db.commit()
    return {"message": f"Withdrawal {withdrawal_id} denied"}


# -----------------------------
# TRANSACTIONS
# -----------------------------
async def list_transactions(admin, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM transactions ORDER BY created_at DESC")
    result = await db.execute(query)
    return [dict(r) for r in result.fetchall()]

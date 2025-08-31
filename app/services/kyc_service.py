from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime
from uuid import uuid4

from app.database import get_db
from app.schemas.kyc_schemas import KYCSubmitRequest, KYCStatusResponse


# -----------------------------
# GET USER KYC STATUS
# -----------------------------
async def get_status(user, db: AsyncSession = Depends(get_db)) -> KYCStatusResponse:
    query = text("""
        SELECT status 
        FROM kyc 
        WHERE user_id = :uid 
        ORDER BY submitted_at DESC 
        LIMIT 1
    """)
    result = await db.execute(query, {"uid": user["id"]})
    record = result.fetchone()

    if not record:
        return KYCStatusResponse(status="pending")  # Default before any submission

    return KYCStatusResponse(status=record.status)


# -----------------------------
# SUBMIT KYC DOCUMENTS
# -----------------------------
async def submit(user, payload: KYCSubmitRequest, db: AsyncSession = Depends(get_db)):
    # Ensure user doesn’t already have a pending KYC
    check_q = text("SELECT id FROM kyc WHERE user_id = :uid AND status = 'pending'")
    result = await db.execute(check_q, {"uid": user["id"]})
    if result.fetchone():
        raise HTTPException(status_code=400, detail="You already have a pending KYC submission")

    kid = str(uuid4())
    insert_q = text("""
        INSERT INTO kyc (id, user_id, document_type, document_front_url, document_back_url, status, submitted_at)
        VALUES (:id, :uid, :doctype, :front, :back, 'pending', :submitted)
    """)
    await db.execute(insert_q, {
        "id": kid,
        "uid": user["id"],
        "doctype": payload.document_type,
        "front": payload.document_front_url,
        "back": payload.document_back_url,
        "submitted": datetime.utcnow(),
    })
    await db.commit()

    return {"message": "KYC submitted successfully", "kyc_id": kid}

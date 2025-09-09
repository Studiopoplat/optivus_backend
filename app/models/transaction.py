from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime
from uuid import UUID


class Transaction(BaseModel):
    id: UUID
    user_id: UUID
    type: Literal["deposit", "withdrawal", "referral_bonus", "admin_credit"]
    amount: str
    currency: str = "GBP"
    status: Literal["pending", "completed", "failed"] = "pending"
    reference: str
    created_at: datetime
    referee_id: Optional[UUID] = None   
    tier: Optional[int] = None         
    note: Optional[str] = None          



class TransactionCreate(BaseModel):
    type: Literal["deposit", "withdrawal", "referral_bonus", "admin_credit"]
    amount: str
    currency: str = "GBP"
    reference: str
    referee_id: Optional[UUID] = None
    tier: Optional[int] = None
    note: Optional[str] = None


from pydantic import BaseModel
from typing import Literal


# -----------------------------
# Responses
# -----------------------------

class AdminStatsResponse(BaseModel):
    total_users: int
    total_user_referral_earnings: str
    admin_referral_earnings: str
    pending_withdrawals_count: int
    protocol_balance: str


class AdminUserResponse(BaseModel):
    id: str
    email: str
    username: str
    role: Literal["user", "admin"]
    status: Literal["active", "frozen"]
    withdrawal_status: Literal["active", "paused"]
    is_kyc_verified: bool
    balance: str

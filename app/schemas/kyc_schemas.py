from pydantic import BaseModel
from typing import Optional, Literal


# -----------------------------
# Requests
# -----------------------------

class KYCSubmitRequest(BaseModel):
    document_type: str
    document_front_url: str
    document_back_url: Optional[str] = None


# -----------------------------
# Responses
# -----------------------------

class KYCStatusResponse(BaseModel):
    status: Literal["pending", "approved", "rejected"]

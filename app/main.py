from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    auth,
    users,
    kyc,
    transactions,
    withdrawals,
    admin,
    public,
    team,   # 👈 NEW import
)

app = FastAPI(
    title="Optivus Backend",
    version="1.0.0",
    description="FastAPI backend with Supabase + Stripe",
)

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(kyc.router)
app.include_router(transactions.router)
app.include_router(withdrawals.router)
app.include_router(admin.router)
app.include_router(public.router)
app.include_router(team.router)  # 👈 NEW line

@app.get("/")
async def root():
    return {"message": "Optivus API is running 🚀"}

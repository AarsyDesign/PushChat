import os
from fastapi import FastAPI, Request, Query, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from database import init_pushchat_db, get_tenant_balance, deduct_credit_for_dm

app = FastAPI(title="Pushchat API", version="1.0.0")

VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "pushchat_meta_verify_2026")

@app.on_event("startup")
def on_startup():
    init_pushchat_db()

@app.get("/")
def read_root():
    return {
        "service": "Pushchat Engine",
        "version": "1.0.0",
        "status": "ONLINE",
        "features": ["Comment-to-DM", "Instagram Reels Auto-Reply", "Shared PushNotif QRIS Balance"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "pushchat"}

# Endpoint Webhook Meta Verification (GET challenge dari Meta)
@app.get("/api/v1/meta/webhook")
def verify_meta_webhook(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return Response(content=hub_challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Verification token mismatch")

# Endpoint Penerima Event Webhook Meta (POST event komentar / DM)
@app.post("/api/v1/meta/webhook")
async def receive_meta_webhook(request: Request):
    payload = await request.json()
    # Logika ekstraksi comment & trigger auto-DM
    return JSONResponse(status_code=200, content={"status": "EVENT_RECEIVED"})

# Endpoint Cek Saldo Terpadu
@app.get("/api/v1/tenant/{tenant_id}/balance")
def check_shared_balance(tenant_id: str):
    balance = get_tenant_balance(tenant_id)
    return {
        "tenant_id": tenant_id,
        "shared_pushnotif_credits": balance,
        "unit_rate_dm": 1
    }

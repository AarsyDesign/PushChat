import os
from fastapi import FastAPI, Request, Query, Response, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
from database import (
    init_pushchat_db, 
    get_tenant_balance, 
    deduct_credit_for_dm,
    list_rules,
    create_rule,
    toggle_rule,
    delete_rule
)

app = FastAPI(title="Pushchat Engine", version="1.0.0")

VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "pushchat_meta_verify_2026")

@app.on_event("startup")
def on_startup():
    init_pushchat_db()

# Serve static dashboard
@app.get("/")
def serve_dashboard():
    dashboard_path = os.path.join(os.path.dirname(__file__), "static", "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return {"status": "ONLINE", "message": "Dashboard not found"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "pushchat"}

# API Rules Management
class RuleCreatePayload(BaseModel):
    rule_name: str
    trigger_keywords: str
    reply_public_comment: Optional[str] = ""
    reply_dm_text: str
    button_label: Optional[str] = ""
    button_url: Optional[str] = ""
    require_follow: Optional[bool] = False

@app.get("/api/v1/rules")
def get_rules(tenant_id: str = Query("tenant_default")):
    rules = list_rules(tenant_id)
    return {"status": "success", "rules": rules}

@app.post("/api/v1/rules")
def add_rule(payload: RuleCreatePayload, tenant_id: str = Query("tenant_default")):
    rule_id = create_rule(tenant_id, payload.dict())
    return {"status": "success", "rule_id": rule_id}

@app.post("/api/v1/rules/{rule_id}/toggle")
def switch_rule(rule_id: str, tenant_id: str = Query("tenant_default")):
    new_state = toggle_rule(rule_id, tenant_id)
    if new_state is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"status": "success", "is_active": new_state}

@app.delete("/api/v1/rules/{rule_id}")
def remove_rule(rule_id: str, tenant_id: str = Query("tenant_default")):
    delete_rule(rule_id, tenant_id)
    return {"status": "success", "message": "Rule deleted"}

# Webhook Verification Meta
@app.get("/api/v1/meta/webhook")
def verify_meta_webhook(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return Response(content=hub_challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Verification token mismatch")

@app.post("/api/v1/meta/webhook")
async def receive_meta_webhook(request: Request):
    payload = await request.json()
    return JSONResponse(status_code=200, content={"status": "EVENT_RECEIVED"})

# Shared Balance API
@app.get("/api/v1/tenant/{tenant_id}/balance")
def check_shared_balance(tenant_id: str):
    balance = get_tenant_balance(tenant_id)
    return {
        "tenant_id": tenant_id,
        "shared_pushnotif_credits": balance,
        "unit_rate_dm": 1
    }

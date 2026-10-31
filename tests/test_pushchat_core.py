import os
import pytest
import sqlite3
import tempfile
from fastapi.testclient import TestClient

# Isolasi database saat pengujian
test_dir = tempfile.mkdtemp()
test_pushnotif_db = os.path.join(test_dir, "test_pushnotif.db")
test_pushchat_db = os.path.join(test_dir, "test_pushchat.db")

os.environ["PUSHNOTIF_DB_PATH"] = test_pushnotif_db
os.environ["PUSHCHAT_DB_PATH"] = test_pushchat_db

import database
database.PUSHNOTIF_DB_PATH = test_pushnotif_db
database.PUSHCHAT_DB_PATH = test_pushchat_db

from main import app

@pytest.fixture(scope="session", autouse=True)
def setup_databases():
    # Setup mock pushnotif db
    conn = sqlite3.connect(test_pushnotif_db)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE tenants (
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        credits INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE credit_ledger (
        id TEXT PRIMARY KEY,
        tenant_id TEXT,
        tx_type TEXT,
        amount_rp INTEGER,
        credits_delta INTEGER,
        balance_after INTEGER,
        description TEXT,
        created_at TEXT
    )
    """)
    cursor.execute("INSERT INTO tenants (id, name, email, credits) VALUES ('tnt_test', 'Tester', 'test@test.com', 100)")
    conn.commit()
    conn.close()
    
    database.init_pushchat_db()

def test_health_check():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "pushchat"}

def test_shared_balance_and_deduction():
    client = TestClient(app)
    
    # Cek saldo awal 100
    res = client.get("/api/v1/tenant/tnt_test/balance")
    assert res.status_code == 200
    assert res.json()["shared_pushnotif_credits"] == 100
    
    # Tes pemotongan 1 kredit untuk Auto-DM
    success = database.deduct_credit_for_dm("tnt_test", "Rule Promo", "pembeli_ig", 1)
    assert success is True
    
    # Cek saldo sisa 99
    res = client.get("/api/v1/tenant/tnt_test/balance")
    assert res.json()["shared_pushnotif_credits"] == 99

def test_rule_crud():
    client = TestClient(app)
    
    # 1. Tambah rule
    payload = {
        "rule_name": "Promo Diskon 50%",
        "trigger_keywords": "diskon, promo, mau",
        "reply_public_comment": "Cek DM ya kak!",
        "reply_dm_text": "Ini kupon diskon 50%: PROMO50",
        "button_label": "Klaim Kupon",
        "button_url": "https://tokoku.id/kupon",
        "require_follow": True
    }
    r = client.post("/api/v1/rules?tenant_id=tnt_test", json=payload)
    assert r.status_code == 200
    rule_id = r.json()["rule_id"]

    # 2. List rules
    r_list = client.get("/api/v1/rules?tenant_id=tnt_test")
    assert r_list.status_code == 200
    rules = r_list.json()["rules"]
    assert len(rules) == 1
    assert rules[0]["rule_name"] == "Promo Diskon 50%"
    assert rules[0]["require_follow"] == 1

    # 3. Toggle rule
    r_toggle = client.post(f"/api/v1/rules/{rule_id}/toggle?tenant_id=tnt_test")
    assert r_toggle.status_code == 200
    assert r_toggle.json()["is_active"] == 0

    # 4. Delete rule
    r_del = client.delete(f"/api/v1/rules/{rule_id}?tenant_id=tnt_test")
    assert r_del.status_code == 200
    
    r_list2 = client.get("/api/v1/rules?tenant_id=tnt_test")
    assert len(r_list2.json()["rules"]) == 0

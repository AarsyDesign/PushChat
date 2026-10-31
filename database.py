import os
import sqlite3
import uuid
from datetime import datetime, timezone

PUSHNOTIF_DB_PATH = os.getenv("PUSHNOTIF_DB_PATH", "/opt/data/work/pushnotif/pushnotif.db")
PUSHCHAT_DB_PATH = os.getenv("PUSHCHAT_DB_PATH", "/opt/data/work/pushchat/pushchat.db")

def init_pushchat_db():
    conn = sqlite3.connect(PUSHCHAT_DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tabel akun media sosial yang terhubung
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ig_connected_accounts (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        platform TEXT NOT NULL, -- 'instagram', 'threads'
        account_username TEXT NOT NULL,
        account_id TEXT NOT NULL,
        access_token TEXT NOT NULL,
        status TEXT DEFAULT 'ACTIVE',
        created_at TEXT NOT NULL
    )
    """)

    # 2. Tabel aturan trigger Comment-to-DM
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auto_dm_rules (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        rule_name TEXT NOT NULL,
        trigger_keywords TEXT NOT NULL, -- format comma-separated: 'mau, link, harga'
        reply_public_comment TEXT, -- balasan publik: 'Cek DM ya kak!'
        reply_dm_text TEXT NOT NULL, -- isi pesan DM privat
        button_label TEXT, -- e.g. 'Beli Sekarang'
        button_url TEXT, -- e.g. 'https://tokoku.com/promo'
        is_active INTEGER DEFAULT 1,
        total_triggered INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """)

    # 3. Tabel log eksekusi DM
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dm_dispatch_logs (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        rule_id TEXT,
        platform TEXT NOT NULL,
        recipient_username TEXT NOT NULL,
        trigger_comment TEXT,
        status TEXT NOT NULL, -- 'SUCCESS', 'FAILED', 'OUT_OF_CREDITS'
        credits_deducted INTEGER DEFAULT 1,
        created_at TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def get_tenant_balance(tenant_id: str) -> int:
    """Mengambil saldo kredit resmi dari shared database PushNotif"""
    try:
        conn = sqlite3.connect(PUSHNOTIF_DB_PATH)
        row = conn.execute("SELECT credits FROM tenants WHERE id = ?", (tenant_id,)).fetchone()
        conn.close()
        return row[0] if row else 0
    except Exception:
        return 0

def deduct_credit_for_dm(tenant_id: str, rule_name: str, recipient: str, credits_needed: int = 1) -> bool:
    """Pemotongan kredit atomik dari saldo PushNotif dengan pencatatan ledger resmi"""
    try:
        conn = sqlite3.connect(PUSHNOTIF_DB_PATH)
        cursor = conn.cursor()
        
        # Cek saldo saat ini
        row = cursor.execute("SELECT credits FROM tenants WHERE id = ?", (tenant_id,)).fetchone()
        if not row or row[0] < credits_needed:
            conn.close()
            return False
            
        current_credits = row[0]
        new_balance = current_credits - credits_needed
        
        # Potong saldo di tabel tenants
        cursor.execute("UPDATE tenants SET credits = ? WHERE id = ?", (new_balance, tenant_id))
        
        # Catat ke buku besar (credit_ledger) PushNotif
        ledger_id = f"tx_pc_{uuid.uuid4().hex[:10]}"
        now_str = datetime.now(timezone.utc).isoformat()
        cursor.execute("""
            INSERT INTO credit_ledger (id, tenant_id, tx_type, amount_rp, credits_delta, balance_after, description, created_at)
            VALUES (?, ?, 'USAGE', 0, ?, ?, ?, ?)
        """, (
            ledger_id,
            tenant_id,
            -credits_needed,
            new_balance,
            f"Pushchat Auto-DM to @{recipient} (Rule: {rule_name})",
            now_str
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deducting credits: {e}")
        return False

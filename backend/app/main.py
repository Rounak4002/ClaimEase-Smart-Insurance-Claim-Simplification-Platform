from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI(title="ClaimEase API")

DB_NAME = "claimease.db"

class Claim(BaseModel):
    id: int | None = None
    user_name: str
    claim_type: str
    status: str = "Submitted"

def get_db():
    return sqlite3.connect(DB_NAME)

@app.on_event("startup")
def startup():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            claim_type TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.post("/claims")
def submit_claim(claim: Claim):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO claims (user_name, claim_type, status) VALUES (?, ?, ?)",
        (claim.user_name, claim.claim_type, claim.status)
    )
    conn.commit()
    conn.close()
    return {"message": "Claim submitted successfully"}

@app.get("/claims", response_model=List[Claim])
def get_claims():
    conn = get_db()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM claims").fetchall()
    conn.close()
    return [
        Claim(id=r[0], user_name=r[1], claim_type=r[2], status=r[3])
        for r in rows
    ]

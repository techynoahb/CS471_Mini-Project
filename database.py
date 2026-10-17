# Purpose: Implementation of the backend sqlite database that inventory.py pulls from.

from dataclasses import dataclass

import sqlite3
from contextlib import contextmanager

TEST_MODE = False

def set_test_mode(config: bool):
    global TEST_MODE
    TEST_MODE = config

class CondConnect(sqlite3.Connection):
    def commit(self):
        if TEST_MODE:
            return
        super().commit()

@dataclass
class InventoryItem:
    rfid: str
    object: str
    status: str
    transactionTime: str
    checkoutCount: int

@contextmanager
def rfid_db():
    db_con = sqlite3.connect("inventory.db", factory=CondConnect)
    cursor = db_con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventoryTable (
            rfid TEXT PRIMARY KEY,
            object TEXT,
            status TEXT,
            transactionTime TIMESTAMP,
            checkoutCount INTEGER NOT NULL DEFAULT 0
        );
    """)
    columns = {column[1] for column in cursor.execute("PRAGMA table_info(inventoryTable)")}
    if "checkoutCount" not in columns:
        cursor.execute(
            "ALTER TABLE inventoryTable ADD COLUMN checkoutCount INTEGER NOT NULL DEFAULT 0"
        )
    cursor.close()
    db_con.commit()
    try:
        yield db_con
    finally:
        db_con.close()

def get_item(rfid):
    with rfid_db() as db_con:
        cursor = db_con.cursor()
        try:
            item = cursor.execute("SELECT * FROM inventoryTable WHERE rfid = (?)", (rfid,)).fetchone()
            return InventoryItem(*item) if item else None
        except Exception as e:
            print(f"Error fetching item: {e}")
            return None

def list_items():
    with rfid_db() as db_con:
        cursor = db_con.cursor()
        return [InventoryItem(*row) for row in cursor.execute(
            "SELECT rfid, object, status, transactionTime, checkoutCount "
            "FROM inventoryTable ORDER BY object, rfid"
        ).fetchall()]

def log_scan(rfid, status, time):
    with rfid_db() as db_con:
        cursor = db_con.cursor()
        cursor.execute("""
            UPDATE inventoryTable
            SET status = (?), transactionTime = (?),
                checkoutCount = checkoutCount + CASE WHEN ? = 'checked out' THEN 1 ELSE 0 END
            WHERE rfid = (?);
        """, (status, time, status, rfid,))
        db_con.commit()

def add_item(rfid, name, time):
    with rfid_db() as db_con:
        cursor = db_con.cursor()
        cursor.execute("""
            INSERT INTO inventoryTable(rfid, object, status, transactionTime)
            VALUES (?, ?, ?, ?);
        """, (rfid, name, "checked in", time,))
        db_con.commit()

def remove_item(rfid):
    with rfid_db() as db_con:
        cursor = db_con.cursor()
        cursor.execute("""
            DELETE FROM inventoryTable WHERE rfid = (?);
        """, (rfid,))
        db_con.commit()

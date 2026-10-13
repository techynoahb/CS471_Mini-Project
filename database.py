# Purpose: Implementation of the backend sqlite database that inventory.py pulls from.

import sqlite3
from contextlib import contextmanager

# TODO: Add proper behavior for -t or --test in CLI

@contextmanager
def rfid_db():
    db_con = sqlite3.connect("inventory.db")
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

def get_item(rfid): # TODO: Return item as dict, or its own class, anything other than a tuple
    with rfid_db() as db_con:
        cursor = db_con.cursor()
        try:
            item = cursor.execute("SELECT * FROM inventoryTable WHERE rfid = (?)", (rfid,)).fetchone()
            return item
        except Exception as e:
            print(e)
            return None

def list_items():
    with rfid_db() as db_con:
        cursor = db_con.cursor()
        return cursor.execute(
            "SELECT rfid, object, status, transactionTime, checkoutCount "
            "FROM inventoryTable ORDER BY object, rfid"
        ).fetchall()

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

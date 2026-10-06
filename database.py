# Purpose: Implementation of the backend sqlite database that inventory.py pulls from.

import sqlite3
from contextlib import contextmanager

# TODO: Add proper behavior for -t or --test in CLI
# TODO: Rework unit tests to match functionality

@contextmanager
def rfid_db():
    db_con = sqlite3.connect("inventory.db")
    cursor = db_con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventoryTable (
            rfid TEXT PRIMARY KEY,
            object TEXT,
            status TEXT,
            transactionTime TIMESTAMP
        );
    """)
    cursor.close()
    db_con.commit()
    try:
        yield db_con
    finally:
        db_con.close()

def get_item(rfid): # TODO: Return item as dict, or its own class, anything other than a tuple
    with rfid_db() as db_con:
        cursor = db_con.cursor()
        item = cursor.execute("SELECT * FROM inventoryTable WHERE rfid = (?)", (rfid,)).fetchone()
        return item

def log_scan(rfid, status, time): # TODO: Clarify if it should be 1 new row for every check-in/out?
    with rfid_db() as db_con:
        cursor = db_con.cursor()
        cursor.execute("""
            UPDATE inventoryTable
            SET status = (?), transactionTime = (?)
            WHERE rfid = (?);
        """, (status, time, rfid,))
        db_con.commit()

def add_item(rfid, name, time):
    with rfid_db() as db_con:
        cursor = db_con.cursor()
        cursor.execute("""
            INSERT INTO inventoryTable(rfid, object, status, transactionTime)
            VALUES (?, ?, ?, ?);
        """, (rfid, name, "checked in", time,))
        db_con.commit()

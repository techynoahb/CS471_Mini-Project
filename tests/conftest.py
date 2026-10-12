from contextlib import contextmanager
from datetime import datetime
import os
import sqlite3
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database

@contextmanager
def mock_db_factory(db_path):
    db_con = sqlite3.connect(str(db_path))
    db_con.row_factory = sqlite3.Row
    cursor = db_con.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inventoryTable (
            rfid TEXT PRIMARY KEY,
            object TEXT,
            status TEXT,
            transactionTime TIMESTAMP,
            checkoutCount INTEGER NOT NULL DEFAULT 0
        );
        """
    )

    cursor.execute(
        """INSERT OR IGNORE INTO inventoryTable (rfid, object, status, transactionTime) VALUES (?, ?, ?, ?);""",
        (str(0).zfill(10), "Test Object", "checked in", datetime(2026, 1, 1, 0, 0, 0, 0)),
    )

    cursor.close()
    db_con.commit()
    try:
        yield db_con
    finally:
        db_con.close()


@pytest.fixture
def mock_db(tmp_path):
    db_path = tmp_path / "inventory.db"
    with mock_db_factory(db_path) as db_con:
        yield db_con


@pytest.fixture(autouse=True)
def mock_inventory_db(monkeypatch, tmp_path):
    db_path = tmp_path / "inventory.db"

    @contextmanager
    def patched_rfdb():
        with mock_db_factory(db_path) as db_con:
            yield db_con

    monkeypatch.setattr(database, "rfid_db", patched_rfdb)

#Unit tests for inventory.py

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import database
import inventory

#swaps in fresh db before each test
@pytest.fixture(autouse=True)
def fresh_db(monkeypatch):
    monkeypatch.setattr(database, "items", {"1234567": {"name": "Laptop", "status": "checked in"}})

def test_valid_rfid():
    assert inventory.is_valid_rfid("1234567")
    assert inventory.is_valid_rfid("3333333")

def test_not_valid_rfid():
    assert not inventory.is_valid_rfid("0")
    assert not inventory.is_valid_rfid("000000")

def test_is_new_rfid():
    assert inventory.is_new_tag("9999999")
    assert not inventory.is_new_tag("1234567")

def test_process_scan_toggles_status():
    assert "Laptop checked out" in inventory.process_scan("1234567")
    assert "Laptop checked in" in inventory.process_scan("1234567")

def test_register_item():
    assert inventory.register_item("9999999", "Tripod") == "Registered Tripod with tag 9999999"
    assert database.get_item("9999999")["name"] == "Tripod"
    assert inventory.register_item("9999999", "Tripod") == "Tag 9999999 is already registered"


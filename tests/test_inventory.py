# Unit tests for inventory.py

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inventory
import database

def test_valid_rfid():
    assert inventory.is_valid_rfid("1234567890")
    assert inventory.is_valid_rfid("3333333333")

def test_not_valid_rfid():
    assert not inventory.is_valid_rfid("0")
    assert not inventory.is_valid_rfid("000000")

def test_is_new_rfid():
    assert inventory.is_new_tag("9999999999")
    assert not inventory.is_new_tag("0000000000")

def test_process_scan_toggles_status():
    assert "Registered" in inventory.register_item("1234567890", "Laptop")
    assert "Laptop checked out" in inventory.process_scan("1234567890")
    assert "Laptop checked in" in inventory.process_scan("1234567890")
    assert database.get_item("1234567890")[4] == 1

def test_register_item():
    assert inventory.register_item("9999999999", "Tripod") == "Registered Tripod with tag 9999999999"
    assert database.get_item("9999999999")[1] == "Tripod"
    assert inventory.register_item("9999999999", "Tripod") == "Tag 9999999999 is already registered"

def test_get_inventory_lists_item_details():
    inventory.register_item("1234567890", "Laptop")
    inventory.process_scan("1234567890")

    item = inventory.get_inventory()[0]
    assert item[0] == "1234567890"
    assert item[1] == "Laptop"
    assert item[2] == "checked out"
    assert item[4] == 1

def test_unregister_item():
    inventory.register_item("1234567890", "Laptop")
    inventory.unregister_item("1234567890")
    assert database.get_item("1234567890") is None


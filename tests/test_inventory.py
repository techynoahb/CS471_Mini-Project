#Unit tests for inventory.py

import inventory

def test_valid_rfid():
    assert inventory.is_valid_rfid("1234567")
    assert inventory.is_valid_rfid("3333333")

def test_not_valid_rfid():
    assert not inventory.is_valid_rfid("0")
    assert not inventory.is_valid_rfid("000000")





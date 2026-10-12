# Purpose: Implementation of script that communicates between scanner_cli.py and database.py

from datetime import datetime
import database

def is_valid_rfid(code):
    return str(code).isdigit() and len(str(code)) == 10

def process_scan(rfid):
    if not is_valid_rfid(rfid):
        return f"Invalid RFID tag: {rfid}"

    item = database.get_item(rfid)
    if item is None:
        return f"No item found for tag {rfid}"
    new_status = "checked in" if item[2] == "checked out" else "checked out"
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database.log_scan(rfid, new_status, time)

    return f"{item[1]} {new_status} at {time}"

def is_new_tag(rfid):
    return is_valid_rfid(rfid) and database.get_item(rfid) is None

def get_inventory():
    return database.list_items()

#item registration: if a valid rfid is entered but not yet stored, then ask user to enter a name, if not return the rfid
def register_item(rfid, name):
    if not is_valid_rfid(rfid):
        return f"Invalid RFID tag: {rfid}"
    if database.get_item(rfid) is not None:
        return f"Tag {rfid} is already registered"
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database.add_item(rfid, name, time)
    return f"Registered {name} with tag {rfid}"

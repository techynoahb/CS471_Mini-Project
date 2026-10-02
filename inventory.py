# Purpose: Implementation of script that communicates between scanner_cli.py and database.py
from datetime import datetime
import database

def is_valid_rfid(code):
    return str(code).isdigit() and len(str(code)) == 7

def process_scan(rfid):
    if not is_valid_rfid(rfid):
        return f"Invalid RFID tag: {rfid}"

    item = database.get_item(rfid)
    if item is None:
        return f"No item found for tag {rfid}"

    new_status = "checked in" if item["status"] == "checked out" else "checked out"
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database.log_scan(rfid, new_status, time)

    return f"{item['name']} {new_status} at {time}"

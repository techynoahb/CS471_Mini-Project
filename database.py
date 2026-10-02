# Purpose: Implementation of the backend sqlite database that inventory.py pulls from.

#Temporary stub just for demo purposes and this will be replaced with sqlite.

items = {
    "1234567": {"name": "Laptop", "status": "checked in"},
    "7654321": {"name": "Projector", "status": "checked in"},
    "1111111": {"name": "Camera", "status": "checked out"},
    }

def get_item(rfid):
    return items.get(rfid)

def log_scan(rfid, status, time):
    items[rfid]["status"] = status

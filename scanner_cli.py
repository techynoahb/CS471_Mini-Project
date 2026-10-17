import argparse
import database
import inventory

# Purpose: Implement the front-end command-line interface for interacting with the program.
# Should communicate with inventory.py

def scan_loop():
    # A USB RFID reader types the tag ID + Enter, just like a keyboard.
    print("Ready to scan  (enter q or press Ctrl+C to return to the menu)")
    try:
        while True:
            tag = input("> ").strip()
            if tag.lower() == "q":
                print("Returning to main menu")
                return
            if inventory.is_new_tag(tag):
                name = input("New tag, enter item name (blank to skip): ").strip()
                if name:
                    print(inventory.register_item(tag, name))
            else:
                print(inventory.process_scan(tag))
    except KeyboardInterrupt:
        print("\nReturning to main menu")

def display_inventory():
    rows = [
        (str(item.object or ""), str(item.rfid), str(item.status or ""), str(item.transactionTime or ""), str(item.checkoutCount))
        for item in inventory.get_inventory()
    ]
    if not rows:
        print("No items are registered.")
        return
    headers = ("Item", "RFID", "Status", "Last transaction", "Times checked out")
    widths = [max(len(header), *(len(row[index]) for row in rows)) for index, header in enumerate(headers)]
    border = "+-" + "-+-".join("-" * width for width in widths) + "-+"

    print("\nInventory")
    print(border)
    print("| " + " | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)) + " |")
    print(border)
    for row in rows:
        print("| " + " | ".join(value.ljust(widths[index]) for index, value in enumerate(row)) + " |")
    print(border)

def main():
    parser = argparse.ArgumentParser(
        description="RFID scanner script that logs scans of RFID tags and their respective item lookup"
    )
    parser.add_argument(
        "-t", "--test",
        action="store_true",
        help="Test the software without committing any changes to the database"
    )
    parser.add_argument(
        "-c", "--code",
        help="Manually enter an RFID tag when scan mode is selected"
    )
    args = parser.parse_args()
    database.set_test_mode(args.test)
    if args.test:
        print("Test mode enabled")

    try:
        while True:
            print("\n+------------------------------+")
            print("|       RFID INVENTORY        |")
            print("+------------------------------+")
            print("| 1. Scan RFID tags           |")
            print("| 2. View database inventory  |")
            print("| 3. Delete tags              |")
            print("| 0. Exit                     |")
            print("+------------------------------+")
            choice = input("Select an option: ").strip()
            match choice:
                case "1":
                    if args.code:
                        print("Manual RFID tag entry mode enabled.")
                        print(inventory.process_scan(args.code))
                        args.code = None
                    else:
                        scan_loop()
                case "2":
                    display_inventory()
                    input("\nPress Enter to continue...")
                case "3":
                    if args.code:
                        print("Manual RFID tag entry mode enabled.")
                    target_tag = args.code if args.code else input("Enter a tag to delete from the database: ")
                    confirm = input(f"Confirm deletion of {target_tag}? (Y/N) ")
                    if confirm.strip().upper() in ["YES", "Y"]:
                        print(inventory.unregister_item(target_tag))
                case "0":
                    if args.test:
                        print("Test mode: Did not commit any changes to inventory.db")
                    print("\nGoodbye")
                    return
                case _:
                    print("Please choose 1, 2, or 0.")
    except (KeyboardInterrupt, EOFError):
        if args.test:
            print("Test mode: Did not commit any changes to inventory.db")
        print("\nExiting")


if __name__ == "__main__":
    main()

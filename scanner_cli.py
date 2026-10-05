import argparse
import inventory

# Purpose: Implement the front-end command-line interface for interacting with the program.
# Should communicate with inventory.py

def main():
    parser = argparse.ArgumentParser(
        description="RFID scanner script that logs scans of RFID tags and their respective item lookup" # WiP
    )
    parser.add_argument(
        "-t", "--test",
        action="store_true",
        help="Test the software without committing any changes to the database"
    )
    parser.add_argument(
        "-c", "--code",
        action="store",
        help="Manually enter RFID tag"
    )

    args = parser.parse_args()
    if args.test:
        print("Test mode enabled") # TODO: Should set bool to not commit any transactions to database
    if args.code:
        print("Manual RFID tag entry mode enabled.")
        print(inventory.process_scan(args.code))
        return

   # A USB RFID reader types the tag ID + Enter, just like a keyboard.
    print("Ready to scan  (Ctrl+C to quit)")
    try:
        while True:
            tag = input("> ").strip()
            if inventory.is_new_tag(tag):
                name = input("New tag, enter item name (blank to skip): ").strip()
                if name:
                    print(inventory.register_item(tag, name))
            else:
                print(inventory.process_scan(tag))
    except (KeyboardInterrupt, EOFError):
        print("\nExiting")


if __name__ == "__main__":
    main()

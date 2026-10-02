import argparse
import inventory

# Purpose: Implement the front-end command-line interface for interacting with the program.
# Should communicate with inventory.py

def is_valid_rfid(code):
    if not str(code).isdigit():
        return False
    if len(str(code)) != 7:
        return False
    return True

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
        if not is_valid_rfid(args.code):
            raise ValueError("Invalid RFID tag") # TODO: Decide behavior, just printout and exit? Or manual input?
        print(f"Manual RFID tag entry mode enabled: {args.code}")
        print(inventory.process_scan(args.code))
        return

   # A USB RFID reader types the tag ID + Enter, just like a keyboard.
    print("Ready to scan  (Ctrl+C to quit)")
    try:
        while True:
            print(inventory.process_scan(input("> ").strip()))
    except (KeyboardInterrupt, EOFError):
        print("\nExiting")


if __name__ == "__main__":
    main()

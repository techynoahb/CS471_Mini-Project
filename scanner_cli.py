import argparse

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
        # Should communicate with inventory.py to log the RFID tag scan

    # TODO: Implement default behavior for RFID USB input w/o system arguments


if __name__ == "__main__":
    main()

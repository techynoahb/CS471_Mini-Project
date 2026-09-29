import argparse

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
    args = parser.parse_args()

if __name__ == "__main__":
    main()

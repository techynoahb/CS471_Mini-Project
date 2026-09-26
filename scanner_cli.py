import argparse
from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    parser = argparse.ArgumentParser(
        description="RFID scanner script" # WiP
    )
    parser.add_argument(
        "-t", "--test",
        action="store_true",
        help="Test the software without committing any changes long-term"
    )
    args = parser.parse_args()
    if args.test:
        return "The script is in test mode."
    return "The script is in default mode."

if __name__ == "__main__":
    app.run()
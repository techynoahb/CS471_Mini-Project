import argparse
import random
import sqlite3
from flask import Flask, request
from faker import Faker

app = Flask(__name__)

parser = argparse.ArgumentParser(
    description="RFID scanner script" # WiP
)
parser.add_argument(
    "-t", "--test",
    action="store_true",
    help="Test the software without committing any changes long-term"
)
args = parser.parse_args()

def build_mock_db():
    fake = Faker()
    db_con = sqlite3.connect(":memory:", check_same_thread=False)
    cur = db_con.cursor()
    cur.execute("CREATE TABLE testTable (id INTEGER, obj STRING);")
    for i in range(10_000):
        cur.execute("INSERT INTO testTable (id, obj) VALUES (?, ?);", (str(i).zfill(4), fake.word()))
    db_con.commit()
    return db_con

@app.route("/test", methods=["GET", "POST"])
def test_page(mock_db=build_mock_db()):
    result = None
    error = None
    if request.method == "POST":
        raw = request.form.get("number", "")
        if raw.isdigit() and 0 <= int(raw) <= 9999:
            query_id = str(int(raw)).zfill(4)
            row = mock_db.execute("SELECT obj FROM testTable WHERE id = ?;", (query_id,)).fetchone()
            result = row[0] if row else "No entry found."
        else:
            error = "Enter a number between 0 and 9999."

    return f"""
    <h2>Test Mode</h2>
    <form method="post">
        <input type="number" name="number" min="0" max="9999" required>
        <button type="submit">Look up</button>
    </form>
    {f"<p><b>Error:</b> {error}</p>" if error else ""}
    {f"<p><b>Result:</b> {result}</p>" if result is not None else ""}
    """

@app.route("/", methods=["GET", "POST"])
def main():
    if args.test:
        return test_page()
    return "The script is in default mode."

if __name__ == "__main__":
    app.run()

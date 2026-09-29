# This is optional and will be deleted if there isn't enough time to implement.
from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    return "This is a placeholder page for if there is time to implement a dashboard to complement the software."

if __name__ == "__main__":
    app.run()

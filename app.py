from flask import Flask, render_template, request, session, redirect, url_for
import json
import os

app = Flask(__name__)
app.secret_key = "riddler_secret"  # Needed for sessions

# Load riddles from JSON
def load_riddles():
    with open("riddles.json", "r") as f:
        return json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    riddles = load_riddles()

    # Start fresh session
    if "index" not in session:
        session["index"] = 0

    current_index = session["index"]
    if current_index >= len(riddles):
        return render_template("index.html", question="You’ve solved them all... for now.", finished=True)

    current_riddle = riddles[current_index]

    message = ""
    if request.method == "POST":
        answer = request.form["answer"].strip().lower()
        if answer == current_riddle["answer"].lower():
            session["index"] += 1
            return redirect(url_for("index"))
        else:
            message = "Not quite... but closer than you think."

    return render_template("index.html", question=current_riddle["question"], message=message, finished=False)

if __name__ == "__main__":
    app.run(debug=True)

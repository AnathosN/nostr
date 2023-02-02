from flask import Flask, request, render_template
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to the Flask app!"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        identifier = request.form.get("identifier")
        hex_key = request.form.get("hex_key")

        nostr_file = os.path.join(".well-known", "nostr.json")
        if os.path.exists(nostr_file):
            with open(nostr_file, "r") as f:
                data = json.load(f)
                data["names"][identifier] = hex_key
        else:
            data = {"names": {identifier: hex_key}}

        with open(nostr_file, "w") as f:
            json.dump(data, f, indent=4)

        return display()

    return render_template("register.html")

@app.route("/display")
def display():
    nostr_file = os.path.join(".well-known", "nostr.json")
    if os.path.exists(nostr_file):
        with open(nostr_file, "r") as f:
            data = json.load(f)
            content = ""
            for identifier, hex_key in data["names"].items():
                content += f"{identifier}: {hex_key}<br>"
            return content
    else:
        return "nostr.json file not found!"

if __name__ == "__main__":
    app.run()

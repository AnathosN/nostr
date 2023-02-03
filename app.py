from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import json
import os

app = Flask(__name__, static_folder='templates/img')
app.secret_key = "N05TRD4MU5"

#root page
@app.route("/")
def index():
    return render_template("index.html")

#home frame
@app.route("/home")
def home():
    return render_template("home.html")

#info frame
@app.route("/info")
def info():
    return render_template("info.html")

#register method
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Input Profile Name
        identifier = request.form["identifier"]
        # Input hex pub key
        hex_key = request.form["hex_key"]
        # Store in nostr.json file
        nostr_file = os.path.join(".well-known", "nostr.json")
        if not os.path.exists(nostr_file):
            data = {"names": {}}
        else:
            with open(nostr_file, "r") as f:
                data = json.load(f)
        if identifier in data["names"] and data["names"][identifier] == hex_key:
            return render_template("duplicate.html")
        data["names"][identifier] = hex_key
        with open(nostr_file, "w") as f:
            json.dump(data, f, indent=4)
        session["identifier"] = identifier
        return redirect(url_for("display"))
    return render_template("register.html")

#display method
@app.route("/display")
def display():
    identifier = session.get("identifier", None)
    if identifier is not None:
        nostr_file = os.path.join(".well-known", "nostr.json")
        if os.path.exists(nostr_file):
            with open(nostr_file, "r") as f:
                data = json.load(f)
                content = []
                if identifier in data["names"]:
                    content.append((identifier, data["names"][identifier], f"{identifier}@nostr.lnadresse.de"))
                return render_template("display.html", content=content)
        else:
            return "nostr.json file not found!"
    else:
        return redirect(url_for("register"))

#display all entries
@app.route("/display_all")
def display_all():
    nostr_file = os.path.join(".well-known", "nostr.json")
    if os.path.exists(nostr_file):
        with open(nostr_file, "r") as f:
            data = json.load(f)
            names = [(identifier, hex_key, f"{identifier}@nostr.landresse.de") for identifier, hex_key in data["names"].items()]
            return render_template("list.html", names=names)
    else:
        return "nostr.json file not found!"
    
@app.route("/.well-known/nostr.json")
def nostr_json():
    identifier = request.args.get("name")
    nostr_file = os.path.join(".well-known", "nostr.json")
    if os.path.exists(nostr_file):
        with open(nostr_file, "r") as f:
            data = json.load(f)
            if identifier in data["names"]:
                hex_key = data["names"][identifier]
                response = jsonify({"names": {identifier: hex_key}})
                return response
            else:
                return jsonify({"error": "Identifier not found"}), 404
    else:
        return jsonify({"error": "nostr.json file not found!"}), 404


if __name__ == "__main__":
    app.run()

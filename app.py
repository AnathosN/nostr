from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "N05TRD4MU5"

#root page
@app.route("/")
def index():
    return "Loading registration...", 302, {'Refresh': '3; url=/register'}

#register method
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        identifier = request.form["identifier"]
        # Generate hex key
        hex_key = request.form["hex_key"]
        # Store in nostr.json file
        nostr_file = os.path.join(".well-known", "nostr.json")
        if not os.path.exists(nostr_file):
            data = {"names": {}}
        else:
            with open(nostr_file, "r") as f:
                data = json.load(f)
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

if __name__ == "__main__":
    app.run()

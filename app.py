from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import json
import os
import ssl
import time
from binascii import unhexlify
from nostr.key import PublicKey

app = Flask(__name__, static_folder='templates/img')
app.secret_key = "N05TRD4MU5"

#test page
@app.route("/test")
def test():
    user_agent = request.user_agent.string
    version = 'desktop'
    if 'mobile' in user_agent.lower():
        version = 'mobile'
    return render_template("test.html", version=version)

#root page
@app.route("/")
def index():
    user_agent = request.user_agent.string
    version = 'desktop'
    if 'mobile' in user_agent.lower():
        version = 'mobile'
    return render_template("index.html", version=version)

#home frame
@app.route("/home")
def home():
    return render_template("home.html")

#check user agent
@app.route("/agent")
def agent():
    user_agent = request.user_agent.string
    version = 'desktop'
    if 'mobile' in user_agent.lower():
        version = 'mobile'
    return jsonify({'user_agent': user_agent, 'version': version})

#check domain
@app.route("/domain")
def domain():
    domain = request.host.split(":")[0].split(",")[0]
    return domain

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
        #verify/convert public key
        if len(hex_key) != 64:
            if hex_key.startswith("npub"):
                # Convert the public key from Bech32 to hex
                pk = PublicKey.from_npub(hex_key)
                hex_key = PublicKey.hex(pk)
        else:
            if hex_key.isalnum() != True:
                return f"The input public key is invalid. {hex_key}"
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

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        public_key = request.form["hex_key"]
        if public_key is None:
            return "No public key provided", 400
        else:
            if public_key.startswith("npub"):
                # Convert the public key from Bech32 to hex
                pk = PublicKey.from_npub(public_key)
                hex_key = PublicKey.hex(pk)
                return f"The input public key is valid. {hex_key}"
            else:
                return f"The input public key is invalid. {public_key}"
    return render_template("verify.html")

#display method
@app.route("/display")
def display():
    domain = request.host.split(":")[0].split(",")[0]
    identifier = session.get("identifier", None)
    if identifier is not None:
        nostr_file = os.path.join(".well-known", "nostr.json")
        if os.path.exists(nostr_file):
            with open(nostr_file, "r") as f:
                data = json.load(f)
                content = []
                if identifier in data["names"]:
                    content.append((identifier, data["names"][identifier], f"{identifier}@{domain}"))
                return render_template("display.html", content=content)
        else:
            return "nostr.json file not found!"
    else:
        return redirect(url_for("register"))

#display all entries
@app.route("/display_all")
def display_all():
    domain = request.host.split(":")[0].split(",")[0]
    nostr_file = os.path.join(".well-known", "nostr.json")
    if os.path.exists(nostr_file):
        with open(nostr_file, "r") as f:
            data = json.load(f)
            names = [(identifier, hex_key, f"{identifier}@{domain}") for identifier, hex_key in data["names"].items()]
            return render_template("list.html", names=names)
    else:
        return "nostr.json file not found!"
    
@app.route("/purge", methods=["GET", "POST"])
def purge():
    nostr_file = os.path.join(".well-known", "nostr.json")
    if os.path.exists(nostr_file):
        with open(nostr_file, "w") as f:
            json.dump({"names": {}}, f, indent=4)
    return redirect(url_for("home"))

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        # Input identifier
        identifier = request.form["identifier"]
        # Load the nostr.json file
        nostr_file = os.path.join(".well-known", "nostr.json")
        with open(nostr_file, "r") as f:
            data = json.load(f)
        # Check if identifier exists in the file
        if identifier in data["names"]:
            hex_key = data["names"][identifier]
            session["identifier"] = identifier
            session["hex_key"] = hex_key
            # Render the confirm deletion page
            return redirect(url_for("confirm_delete"))
        else:
            # Identifier not found
            return "This identifier does not exist."
    return render_template("delete.html")

@app.route("/confirm_delete", methods=["GET", "POST"])
def confirm_delete():
    if request.method == "POST":
        identifier = session.get("identifier", None)
        hex_key = session.get("hex_key", None)
        if identifier is not None:
            # Load the nostr.json file
            nostr_file = os.path.join(".well-known", "nostr.json")
            with open(nostr_file, "r") as f:
                data = json.load(f)
            # Delete the entry from the file
            del data["names"][identifier]
            with open(nostr_file, "w") as f:
                json.dump(data, f, indent=4)
            # Redirect to the confirm page
            return redirect(url_for("confirm"))
        else:
            # Identifier not found
            return "This identifier does not exist."
    return render_template("delete_input.html")

@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    if request.method == "POST":
        return redirect(url_for("register"))
    return render_template("confirm.html")

    
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

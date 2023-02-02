from flask import Flask, request, render_template
import json
import os

app = Flask(__name__)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        identifier = request.form["identifier"]
        hex_key = request.form["hex_key"]
        filename = ".well-known/nostr.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
        else:
            data = {"names": {}}
        data["names"][identifier] = hex_key
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        return "Identifier and hex key registered successfully!"
    return render_template("register.html")

if __name__ == "__main__":
    app.run()

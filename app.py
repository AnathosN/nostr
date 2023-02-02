from flask import Flask, request, render_template
import json

app = Flask(__name__)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        identifier = request.form["identifier"]
        hex_key = request.form["hex_key"]
        with open(".well-known/nostr.json", "r") as f:
            data = json.load(f)
        data["names"][identifier] = hex_key
        with open(".well-known/nostr.json", "w") as f:
            json.dump(data, f, indent=4)
        return "Identifier and hex key registered successfully!"
    return render_template("register.html")

if __name__ == "__main__":
    app.run()


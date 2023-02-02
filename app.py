from flask import Flask, request, render_template
import os
import json

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        identifier = request.form['identifier']
        hex_key = request.form['hex_key']

        filename = ".well-known/nostr.json"
        if os.path.exists(filename):
            with open(filename, "r") as json_file:
                data = json.load(json_file)
                names = data["names"]
                names[identifier] = hex_key
                with open(filename, "w") as json_file:
                    json.dump(data, json_file, indent=4)
        else:
            with open(filename, "w") as json_file:
                data = {"names": {}}
                data["names"][identifier] = hex_key
                json.dump(data, json_file, indent=4)
        
        if os.path.exists(filename):
            return "Success: The file was created successfully and the data was appended successfully."
        else:
            return "Error: The file was not created successfully."
    
    return render_template('register.html')

@app.route('/display')
def display():
    filename = ".well-known/nostr.json"
    if os.path.exists(filename):
        with open(filename, "r") as json_file:
            data = json.load(json_file)
            names = data["names"]
            return render_template('display.html', names=names)
    else:
        return "Error: The file was not found."

if __name__ == '__main__':
    app.run()

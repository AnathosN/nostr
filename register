import json
from flask import Flask, request, render_template

app = Flask(__name__)

def write_to_file(identifier, hex_key):
    try:
        with open('.well-known/nostr.json') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    data["names"][identifier] = hex_key
    with open('.well-known/nostr.json', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        identifier = request.form['identifier']
        hex_key = request.form['hex_key']
        write_to_file(identifier, hex_key)
        return 'Successfully registered identifier and hex key!'
    return render_template('register.html')

if __name__ == '__main__':
    app.run()

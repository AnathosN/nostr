import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        identifier = request.form['identifier']
        hex_key = request.form['hex_key']

        well_known_dir = os.path.join(app.root_path, '.well-known')
        if not os.path.exists(well_known_dir):
            os.makedirs(well_known_dir)

        nostr_file = os.path.join(well_known_dir, 'nostr.json')
        if os.path.exists(nostr_file):
            with open(nostr_file, 'r') as f:
                data = json.load(f)
                data['names'][identifier] = hex_key
        else:
            data = {'names': {identifier: hex_key}}

        with open(nostr_file, 'w') as f:
            json.dump(data, f, indent=4)

        return redirect(url_for('display'))

    return render_template('register.html')

@app.route('/display')
def display():
    well_known_dir = os.path.join(app.root_path, '.well-known')
    nostr_file = os.path.join(well_known_dir, 'nostr.json')
    if os.path.exists(nostr_file):
        with open(nostr_file, 'r') as f:
            data = json.load(f)
            names = data.get('names', {})
            return render_template('display_nostr.html', names=names)

    return 'No data found in nostr.json'

if __name__ == '__main__':
    app.run(debug=True)

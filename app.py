from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from difflib import get_close_matches

app = Flask(__name__)
DATA_FILE = 'words.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    query = request.args.get('search', '').lower()
    words = load_data()
    results = []

    if query:
        # Wir suchen in Somali (so) und Deutsch (de)
        all_keys = [w['so'].lower() for w in words] + [w['de'].lower() for w in words]
        matches = get_close_matches(query, all_keys, n=3, cutoff=0.4)
        
        results = [w for w in words if w['so'].lower() in matches or w['de'].lower() in matches]
    
    return render_template('index.html', results=results, query=query)

@app.route('/add', methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        new_entry = {
            "so": request.form['so'],
            "de": request.form['de'],
            "explanation": request.form['explanation'],
            "uses": int(request.form['uses'] or 0),
            "example": request.form['example']
        }
        data = load_data()
        data.append(new_entry)
        save_data(data)
        return redirect(url_for('index'))
    return render_template('add_word.html')

@app.route('/terminal', methods=['POST'])
def terminal():
    raw_input = request.json.get('command', '').strip()
    cmd = raw_input.lower()
    words = load_data()

    if cmd == "list":
        output = [f"{w['so']} -> {w['de']}" for w in words]
    elif cmd == "count":
        output = f"Anzahl der Wörter: {len(words)}"
    elif cmd.startswith("info "):
        search_term = cmd.replace("info ", "")
        found = [f"{w['so']}: {w['explanation']} (Uses: {w['uses']})" for w in words if search_term in w['so'].lower()]
        output = found if found else "Kein Wort gefunden."
    elif cmd == "clear":
        output = "Terminal bereinigt..."
    else:
        output = f"Befehl '{cmd}' unbekannt. (list, count, info [wort], clear)"

    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(debug=True)

import os
import json
import random
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

QUESTION_DATA = 'questions.json'
USER_DATA = 'users.json'

def load_json(file_path, default):
    if not os.path.exists(file_path):
        return default
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return default

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        if not username:
            return "Name required"
        session['user'] = username
        data = load_json(USER_DATA, {"leaderboard": {}})
        if username not in data['leaderboard']:
            data['leaderboard'][username] = 0
            save_json(USER_DATA, data)
        return redirect(url_for('quiz'))
    return render_template('login.html')

@app.route('/quiz')
def quiz():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('quiz.html')

@app.route('/get_questions')
def get_questions():
    all_qs = load_json(QUESTION_DATA, [])
    if not all_qs:
        return jsonify([])
    count = min(len(all_qs), 10)
    return jsonify(random.sample(all_qs, count))

@app.route('/update_score', methods=['POST'])
def update_score():
    if 'user' not in session:
        return jsonify({"status": "error"}), 403
    points = request.json.get('points', 0)
    data = load_json(USER_DATA, {"leaderboard": {}})
    current_user = session['user']
    data['leaderboard'][current_user] = data['leaderboard'].get(current_user, 0) + points
    save_json(USER_DATA, data)
    return jsonify({"status": "success"})

@app.route('/leaderboard')
def leaderboard():
    data = load_json(USER_DATA, {"leaderboard": {}})
    lb = data.get("leaderboard", {})
    sorted_lb = sorted(lb.items(), key=lambda x: x[1], reverse=True)[:20]
    return render_template('leaderboard.html', rankers=sorted_lb)

@app.route('/api/leaderboard')
def api_leaderboard():
    data = load_json(USER_DATA, {"leaderboard": {}})
    lb = data.get("leaderboard", {})
    sorted_lb = sorted(lb.items(), key=lambda x: x[1], reverse=True)[:20]
    return jsonify(sorted_lb)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

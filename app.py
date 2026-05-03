import json
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'kairox_lamp_secure_key'

USER_DATA = 'users.json'
QUESTION_DATA = 'questions.json'

def load_json(filename, default):
    if not os.path.exists(filename):
        return default
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except:
            return default

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('quiz'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        if not username: return "Name required"
        session['user'] = username
        data = load_json(USER_DATA, {"leaderboard": {}})
        if username not in data['leaderboard']:
            data['leaderboard'][username] = 0
            save_json(USER_DATA, data)
        return redirect(url_for('quiz'))
    return render_template('login.html')

@app.route('/quiz')
def quiz():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('quiz.html')

@app.route('/get_questions')
def get_questions():
    all_qs = load_json(QUESTION_DATA, [])
    return jsonify(random.sample(all_qs, min(len(all_qs), 10)))

@app.route('/get_questions')
def get_questions():
    all_qs = load_json(QUESTION_DATA, [])
    return jsonify(random.sample(all_qs, min(len(all_qs), 10)))

@app.route('/api/leaderboard')
def api_leaderboard():
    data = load_json(USER_DATA, {"leaderboard": {}})
    lb = data.get("leaderboard", {})
    sorted_lb = sorted(lb.items(), key=lambda x: x[1], reverse=True)[:20]
    return jsonify(sorted_lb)


@app.route('/update_score', methods=['POST'])
def update_score():
    if 'user' not in session: return jsonify({"status": "error"})
    points = request.json.get('points', 0)
    data = load_json(USER_DATA, {"leaderboard": {}})
    data['leaderboard'][session['user']] = data['leaderboard'].get(session['user'], 0) + points
    save_json(USER_DATA, data)
    return jsonify({"status": "success", "new_total": data['leaderboard'][session['user']]})

@app.route('/leaderboard')
def leaderboard():
    data = load_json(USER_DATA, {"leaderboard": {}})
    lb = data.get("leaderboard", {})
    # SHOW TOP 20 IN ORDER
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

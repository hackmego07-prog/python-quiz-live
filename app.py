import os
import json
import random
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = 'kairox_secret_key'

# Updated path logic for Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTION_DATA = os.path.join(BASE_DIR, 'questions.json')
USER_DATA = os.path.join(BASE_DIR, 'users.json')

def load_json(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            return "Username is required", 400
        session['user'] = username
        return redirect(url_for('quiz'))
    return render_template('login.html')

@app.route('/quiz')
def quiz():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('quiz.html')

@app.route('/get_questions')
def get_questions():
    all_qs = load_json(QUESTION_DATA)
    if not all_qs:
        return jsonify([])
    # Pick 10 random questions
    selected = random.sample(all_qs, min(len(all_qs), 10))
    return jsonify(selected)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

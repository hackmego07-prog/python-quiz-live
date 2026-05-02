import json
import os
import random
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

# 1. Create the App FIRST
app = Flask(__name__)
app.secret_key = 'python_qote_live'

# 2. Now you can add the Sitemap route
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory('.', 'sitemap.xml')

# --- FILE PATHS ---
USER_DATA = 'users.json'
QUESTION_DATA = 'questions.json'

# --- DATABASE HELPERS ---
def load_users():
    if not os.path.exists(USER_DATA):
        return {"accounts": {}, "leaderboard": {}}
    with open(USER_DATA, 'r') as f:
        return json.load(f)

def save_users(data):
    with open(USER_DATA, 'w') as f:
        json.dump(data, f, indent=4)

# --- ROUTES ---

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('quiz'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('username').strip()
        pw = request.form.get('password').strip()
        data = load_users()

        # 1. CHECK IF USER EXISTS
        if name in data['accounts']:
            # Verify Password
            if check_password_hash(data['accounts'][name], pw):
                session['user'] = name
                return redirect(url_for('quiz'))
            else:
                return "Incorrect Password! Go back and try again.", 401
        
        # 2. CREATE NEW USER IF NOT FOUND
        else:
            data['accounts'][name] = generate_password_hash(pw)
            save_users(data)
            session['user'] = name
            return redirect(url_for('quiz'))

    return render_template('login.html')

@app.route('/quiz')
def quiz():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # LOAD YOUR EXISTING QUESTIONS
    try:
        with open(QUESTION_DATA, 'r') as f:
            all_q = json.load(f)
        
        # PICK 10 RANDOM ONES (or all if less than 10)
        num_to_pick = min(len(all_q), 10)
        selected_q = random.sample(all_q, num_to_pick)
        
        return render_template('quiz.html', questions=selected_q, username=session['user'])
    except Exception as e:
        return f"Error loading questions.json: {e}"

@app.route('/save_score', methods=['POST'])
def save_score():
    if 'user' not in session:
        return jsonify({"status": "error"}), 403
    
    score = request.get_json().get('score')
    name = session['user']
    data = load_users()

        # 1. Get the points from the round just finished
    new_points = request.get_json().get('score')
    name = session['user']
    data = load_users()

    # 2. Add these points to their lifetime total
    # If they are new, they start at 0
    current_total = data['leaderboard'].get(name, 0)
    data['leaderboard'][name] = current_total + new_points
    
    # 3. Save the updated total back to the file
    save_users(data)
    return jsonify({"status": "success"})

@app.route('/leaderboard')
def leaderboard():
    data = load_users()
    # 1. Get the leaderboard dictionary from your users.json
    leaderboard_data = data.get("leaderboard", {})
    
    # 2. Sort users by score (highest to lowest)
    # This turns the dictionary into a list of tuples: [('username', score), ...]
    sorted_rankers = sorted(leaderboard_data.items(), key=lambda x: x[1], reverse=True)
    
    # 3. Take only the TOP 20
    top_20 = sorted_rankers[:20]
    
    return render_template('leaderboard.html', rankers=top_20)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

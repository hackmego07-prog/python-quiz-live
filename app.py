import os
import json
import random # <--- 1. MAKE SURE THIS IS AT THE VERY TOP
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

QUESTION_DATA = 'questions.json'

def load_json(file_path, default):
    if not os.path.exists(file_path):
        return default
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return default

# ... (rest of your login/quiz routes here) ...

@app.route('/get_questions')
def get_questions():
    try:
        # Load questions safely
        all_qs = load_json(QUESTION_DATA, [])
        
        # If file is empty or missing, return an empty list instead of crashing
        if not all_qs or len(all_qs) == 0:
            return jsonify([])
            
        # Select 10 questions (or fewer if total is less than 10)
        count = min(len(all_qs), 10)
        selected = random.sample(all_qs, count)
        return jsonify(selected)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify([]) # Prevents the red error in your logs

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

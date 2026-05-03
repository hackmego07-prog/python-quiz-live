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
    import random
    all_qs = load_json('questions.json', [])
    
    if not all_qs:
        return jsonify([])
        
    count = min(len(all_qs), 10)
    return jsonify(random.sample(all_qs, count))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

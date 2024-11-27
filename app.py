from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from anthropic import Anthropic
import os
import logging
import random

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')

FEEDBACK_MESSAGES = {
    'perfect': [
        "🌟 Nuostabu! Tobulas tekstas! 🏆",
        "🚀 WOW! Čia tai bent - nė vienos klaidos! ⭐",
        "🎯 100 iš 100! Tu tikras genijus! 🧠",
        "🦄 OMG! Čia tiesiog super! ✨",
    ],
    'good': [
        "😎 Beveik tobula! Dar biški ir būsi top! 💫",
        "🎮 Pro lygio tekstas! 🎯",
        "💪 Labai gerai! Tik kelios smulkios klaidelės! 🌟",
        "🎸 Nice! Beveik idealiai! 🤘",
    ],
    'average': [
        "👾 Normaliai! Bet gali dar geriau! 💪",
        "🎮 Progresas matosi! Dar biški! 🎯",
        "🌈 Vidutiniškai, bet jau gerėja! 🎯",
        "🎪 Ne blogai, bet dar yra kur tobulėti! 🔥",
    ],
    'needs_work': [
        "😅 Reikia dar padirbėti! Bet tu tikrai gali! 💪",
        "🎮 Challenge accepted! Kitą kartą bus geriau! 🌟",
        "🌱 Kiekviena klaida - tai galimybė tobulėti! 🆙",
        "🎨 Nešvaistyk laiko liūdėjimui - geriau mokykis! 💫",
    ]
}

def get_random_feedback(error_count):
    if error_count == 0:
        return random.choice(FEEDBACK_MESSAGES['perfect'])
    elif error_count <= 2:
        return random.choice(FEEDBACK_MESSAGES['good'])
    elif error_count <= 5:
        return random.choice(FEEDBACK_MESSAGES['average'])
    else:
        return random.choice(FEEDBACK_MESSAGES['needs_work'])

def process_with_claude(text):
    prompt = f"""
Analyze this Lithuanian text. Please:
1. Check for spelling and grammar errors
2. Add stress marks where needed
3. Fix punctuation
4. Count the total number of corrections made

Text:
\"""
{text}
\"""

Return only a JSON object with:
{{
    "corrected_text": "corrected text here",
    "error_count": number of errors found
}}
"""

    try:
        response = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            temperature=0.1,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        import json
        result = json.loads(response.content[0].text.strip())
        result['feedback'] = get_random_feedback(result['error_count'])
        
        return result
    except Exception as e:
        app.logger.error(f"API klaida: {e}")
        return {
            "corrected_text": text,
            "error_count": 0,
            "feedback": "😅 Atsiprašome, įvyko klaida! Bandykite dar kartą! 🔄"
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data['text']
    result = process_with_claude(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

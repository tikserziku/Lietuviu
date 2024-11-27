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

if not anthropic_api_key:
    app.logger.error("Anthropic API raktas nerastas.")
else:
    anthropic = Anthropic(api_key=anthropic_api_key)

FEEDBACK_MESSAGES = {
    'perfect': [
        "🌟 Nerealu! Viskas tobulai! 🏆",
        "🚀 WOW! Rašai kaip profesionalas! ⭐",
        "🎯 Šaunuolis! Viskas teisingai! 🧠",
        "🦄 Super! Nė vienos klaidos! ✨",
    ],
    'good': [
        "😎 Beveik tobulai! Dar truputį ir būsi TOP! 💫",
        "🎮 Pro lygio tekstas! Liko tik smulkmenos! 🎯",
        "💪 Labai gerai! Jau beveik tobulai! 🌟",
        "🎸 Nice! Tik kelios mažos klaidelės! 🤘",
    ],
    'average': [
        "👾 Neblogai, bet gali dar geriau! 💪",
        "🎮 Progresas matosi! Dar padirbėk! 🎯",
        "🌈 Jau neblogai, bet yra ką tobulinti! 🎯",
        "🎪 Vidutiniškai, bet tu gali geriau! 🔥",
    ],
    'needs_work': [
        "😅 Reikia dar padirbėti! Nesijaudink, kartu pavyks! 💪",
        "🎮 Challenge mode ON! Bandyk dar kartą! 🌟",
        "🌱 Kiekviena klaida - tai pamoka! 🆙",
        "🎨 Keep calm ir mokykis toliau! 💫",
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
Tu esi labai kvalifikuotas lietuvių kalbos mokytojas. Išanalizuok šį tekstą:

1. Rask visas rašybos klaidas (neteisingai parašyti žodžiai)
2. Rask gramatikos klaidas
3. Patikrink skyrybą
4. Pažymėk kirčiuotus skiemenis VISADA naudodamas akūto ženklą (´) virš kirčiuotos balsės
5. Perskaičiuok VISAS klaidas

Pavyzdys kirčiavimo:
- Lãbas → Lábas
- Rýtas → Rýtas
- Mokykla → Mokyklà

Tekstas analizei:
\"""
{text}
\"""

Pateik rezultatą JSON formatu:
{{
    "corrected_text": "pataisytas tekstas su kirčiais",
    "error_count": bendras klaidų skaičius,
    "errors_found": ["klaida1", "klaida2", ...]
}}"""

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
            "errors_found": [],
            "feedback": "😅 Atsiprašome, įvyko klaida! Bandykite dar kartą! 🔄"
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({
            "corrected_text": "",
            "error_count": 0,
            "feedback": "Prašome įvesti tekstą!"
        })
    
    result = process_with_claude(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

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

# Словарь с забавными комментариями на разные уровни ошибок
FEEDBACK_MESSAGES = {
    'perfect': [
        "🔥 Nerealu! Tu čia kaip koks genijus! 🌟",
        "🚀 Vauuu, čia tikras kosmosas! Tobula! ⭐",
        "🎯 Šimtas iš šimto! Esi protingesnis už GPT! 🧠",
        "🦄 OMG! Čia tiesiog idealu! Neįtikėtina! ✨",
    ],
    'good': [
        "😎 Beveik tobula! Dar truputis ir būsi legendinis! 💫",
        "🎮 Level: PRO! Liko tik keli boss'ai įveikti! 🎯",
        "💪 Stipru! Beveik kaip Einšteinas! 🧪",
        "🎸 Čia tai bent! Rašai geriau nei ChatGPT! 🤖",
    ],
    'average': [
        "👾 Nėra blogai, bet gali dar geriau! Push'inam toliau! 💪",
        "🎮 Level up needed! Bet jau neblogai kapoji! 🎯",
        "🌈 Visai neblogai! Dar biški patreniruosim ir bus perfect! 🎯",
        "🎪 Jau gerėja! Dar truputis praktikos ir būsi boss! 🔥",
    ],
    'needs_work': [
        "😅 Ups... Reikia dar padirbėti! Bet nesijaudink - visi nuo to pradeda! 💪",
        "🎮 Tutorial mode: ON! Kartu išmoksim! 🌟",
        "🌱 Viskas gerai! Kiekviena klaida - naujas level up! 🆙",
        "🎨 Klaidos - tai tik steppingstones į tobulumą! 💫",
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
Išanalizuokite šį tekstą ir pateikite:
1. Ištaisytą tekstą su visais kirčiais ir skyrybos ženklais
2. Kiek ir kokių klaidų rasta (skaičių)

Pradinis tekstas:
\"""
{text}
\"""

Pateikite atsakymą JSON formatu:
{{
    "corrected_text": "ištaisytas tekstas",
    "error_count": klaidų skaičius
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
        
        # Парсим JSON из ответа
        import json
        result = json.loads(response.content[0].text.strip())
        
        # Добавляем забавный комментарий
        result['feedback'] = get_random_feedback(result['error_count'])
        
        return result
    except Exception as e:
        app.logger.error(f"Klaida kviečiant Claude API: {e}")
        return {
            "corrected_text": "Įvyko klaida apdorojant tekstą. Bandykite dar kartą vėliau.",
            "error_count": 0,
            "feedback": "😅 Ups... Kažkas neveikia! Pabandyk dar kartą! 🔄"
        }

@app.route('/process', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data['text']
    result = process_with_claude(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run()

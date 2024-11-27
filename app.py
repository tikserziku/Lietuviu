from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from anthropic import Anthropic
import os
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')

if not anthropic_api_key:
    app.logger.error("Anthropic API raktas nerastas.")
else:
    anthropic = Anthropic(api_key=anthropic_api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data['text']
    
    processed_text = process_with_claude(text)
    return jsonify({'processed_text': processed_text})

def process_with_claude(text):
    prompt = f"""
Išanalizuokite ir ištaisykite šį tekstą. Būtina:
1. Ištaisyti visas rašybos ir gramatikos klaidas
2. Sudėti teisingus skyrybos ženklus
3. Pridėti kirčius žodžiuose naudojant simbolį ´ virš kirčiuotos balsės
4. Suskirstyti tekstą į logines pastraipas, jei reikia
5. Išsaugoti pradinę prasmę ir teksto stilių

Pradinis tekstas:
\"""
{text}
\"""

Prašome grąžinti tik ištaisytą tekstą, be papildomų paaiškinimų.
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
        
        processed_text = response.content[0].text.strip()
        return processed_text
    except Exception as e:
        app.logger.error(f"Klaida kviečiant Claude API: {e}")
        return "Įvyko klaida apdorojant tekstą. Bandykite dar kartą vėliau."

if __name__ == '__main__':
    app.run()

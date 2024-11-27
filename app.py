from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from anthropic import Anthropic
import os
import logging

app = Flask(__name__)
CORS(app)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получение API-ключа Anthropic из переменных окружения
anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')

if not anthropic_api_key:
    app.logger.error("API-ключ Anthropic не найден. Пожалуйста, установите переменную окружения ANTHROPIC_API_KEY.")
else:
    anthropic = Anthropic(api_key=anthropic_api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data['text']

    # Обработка текста с помощью Claude
    processed_text = process_with_claude(text)

    return jsonify({'processed_text': processed_text})

def process_with_claude(text):
    prompt = f"""
Проверьте текст на ошибки, расставьте знаки препинания и добавьте ударения в русских словах, используя символы, принятые в литовской орфографии. Представьте результат в виде исправленного текста.

Текст:
\"""
{text}
\"""

Исправленный текст:
"""

    try:
        # Вызов Claude API
        response = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Извлечение ответа
        processed_text = response.content[0].text.strip()
        return processed_text
    except Exception as e:
        app.logger.error(f"Ошибка при вызове Claude API: {e}")
        return "Произошла ошибка при обработке текста. Пожалуйста, попробуйте позже."

if __name__ == '__main__':
    app.run()

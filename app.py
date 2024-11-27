from flask import Flask, request, jsonify, render_template
import openai
import os
import logging

app = Flask(__name__)

# Настройка логирования (опционально)
logging.basicConfig(level=logging.INFO)

# Получение API-ключа OpenAI из переменных окружения
openai_api_key = os.environ.get('OPENAI_API_KEY')

if not openai_api_key:
    # Если API-ключ не найден, выводим сообщение об ошибке
    app.logger.error("API-ключ OpenAI не найден. Пожалуйста, установите переменную окружения OPENAI_API_KEY.")
else:
    openai.api_key = openai_api_key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data['text']

    # Обработка текста с помощью OpenAI
    processed_text = process_with_ai(text)

    return jsonify({'processed_text': processed_text})

def process_with_ai(text):
    prompt = f"""
Проверьте текст на ошибки, расставьте знаки препинания и добавьте ударения в русских словах, используя символы, принятые в литовской орфографии. Представьте результат в виде исправленного текста.

Текст:
\"\"\"
{text}
\"\"\"

Исправленный текст:
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )

        # Извлечение ответа
        processed_text = response['choices'][0]['message']['content'].strip()
        return processed_text
    except Exception as e:
        app.logger.error(f"Ошибка при обращении к OpenAI API: {e}")
        return "Произошла ошибка при обработке текста. Пожалуйста, попробуйте позже."

if __name__ == '__main__':
    app.run()

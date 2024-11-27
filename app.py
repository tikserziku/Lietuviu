from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Установите ваш API-ключ OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

# Остальная часть вашего кода...


@app.route('/process', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data['text']

    # Обработка текста с помощью OpenAI GPT-4
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
        # Логирование ошибки
        app.logger.error(f"Ошибка при вызове OpenAI API: {e}")
        # Возврат сообщения об ошибке клиенту (опционально, для отладки)
        return f"Произошла ошибка при обработке текста: {e}"



if __name__ == '__main__':
    app.run(debug=True)

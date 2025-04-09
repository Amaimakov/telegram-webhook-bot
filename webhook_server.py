from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = '7972885283:AAHWM_qsGypl1DqscOMF6y9ZhGDJlYuA3II'
CHAT_ID = '400623032'

@app.route('/', methods=['GET'])
def index():
    return "✅ Бот готов к приёму заявок"

@app.route('/notify', methods=['POST'])
def notify():
    print(">>> 📥 Пришёл запрос на /notify")

    data = request.json
    subject = data.get('subject', 'Без темы')
    description = data.get('description', 'Нет описания')
    inc_number = data.get('inc_number', 'не указано')
    city = data.get('city', 'не указано')
    office = data.get('office', 'не указано')
    type_ = data.get('type', 'не указано')
    initiator = data.get('initiator', 'не указано')
    assigned = data.get('assigned', 'не указано')

    message = (
    f"📦 *Новая заявка:*\n"
    f"📅 *Дата:* {subject} {description}\n"
    f"🆔 *Номер:* `{inc_number}`\n"
    f"🏢 *Город:* {city}\n"
    f"📍 *Офис:* {office}\n"
    f"📄 *Тип:* {type_}\n"
    f"👤 *Инициатор:* {initiator}\n"
    f"👨‍🔧 *Назначено:* {assigned}"
)


    response = requests.post(
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
        data={
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
    )

    print(">> STATUS:", response.status_code)
    print(">> RESPONSE:", response.text)

    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(port=5050)

from flask import Flask, request, abort
import requests
import os

app = Flask(__name__)

BOT_TOKEN = '7972885283:AAHWM_qsGypl1DqscOMF6y9ZhGDJlYuA3II'

# Фильтрация по назначенным логинам
ASSIGNED_MAP = {
    "AMaimakov": "400623032",
    "AZambylov": "604088724",
    "AKenzhebayev": "511448822",
    "AShutov": "462834861",
    "MZhenis": "5871381787",
    "AIgilik": "275155417",
    "ASAmangeldi": "6264174204"
}

@app.route('/', methods=['GET'])
def index():
    return "✅ Бот работает и фильтрует по assigned"

@app.route('/notify', methods=['POST'])
def notify():
    print(">>> 📥 Пришёл запрос на /notify")

    data = request.json
    subject = data.get('created', 'Без даты')
    time = data.get('time', '')
    inc_number = data.get('inc_number', 'не указан')
    city = data.get('city', 'не указан')
    office = data.get('office', 'не указан')
    type_ = data.get('type', 'не указан')
    initiator = data.get('initiator', 'не указан')
    assigned = data.get('assigned', 'не указан')

    # 👤 Найдём chat_id по логину
    chat_id = ASSIGNED_MAP.get(assigned)
    if not chat_id:
        print(f"⛔️ Логин '{assigned}' не найден — заявка проигнорирована.")
        return {'status': 'skipped'}, 200

    # 💬 Формируем сообщение
    message = (
        f"📦 *Новая заявка:*\n"
        f"📅 *Дата:* {subject} {time}\n"
        f"🆔 *Номер:* `{inc_number}`\n"
        f"🏢 *Город:* {city}\n"
        f"📍 *Офис:* {office}\n"
        f"📄 *Тип:* {type_}\n"
        f"👤 *Инициатор:* {initiator}\n"
        f"👨‍🔧 *Назначено:* {assigned}"
    )

    # 📬 Отправим сообщение
    response = requests.post(
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
        data={
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
    )

    print(f">> ✅ Отправлено для: {assigned} ({chat_id})")
    print(">> STATUS:", response.status_code)
    print(">> RESPONSE:", response.text)

    return {'status': 'ok'}, 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

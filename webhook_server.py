from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = '7972885283:AAHWM_qsGypl1DqscOMF6y9ZhGDJlYuA3II'

# Список назначенных логинов (в ВЕРХНЕМ регистре)
ASSIGNED_MAP = {
    "AMAIMAKOV": "400623032",
    "AZAMBYLOV": "604088724",
    "AKENZHEBAYEV": "511448822",
    "ASHUTOV": "462834861",
    "AIGILIK": "275155417",
    "MZHENIS": "5871381787"
}

@app.route('/', methods=['GET'])
def index():
    return "✅ Бот работает и фильтрует по assigned"

@app.route('/notify', methods=['POST'])
def notify():
    print(">>> 📥 Пришёл запрос на /notify")

    try:
        data = request.get_json(force=True)
        if data is None:
            print("⚠️ request.get_json вернул None")
            return {'status': 'invalid json'}, 400
        else:
            print(">> RAW JSON:", data)
    except Exception as e:
        print("⚠️ Исключение при получении JSON:", e)
        return {'status': 'json error'}, 400

    # ✅ Если это команда от Telegram
    if 'message' in data:
        msg = data['message']
        chat = msg.get('chat', {})
        user_id = chat.get('id')
        first_name = chat.get('first_name', 'пользователь')
        text = msg.get('text', '')

        if text == '/myid':
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={
                    "chat_id": user_id,
                    "text": f"👋 Привет, {first_name}!\nТвой chat_id: `{user_id}`",
                    "parse_mode": "Markdown"
                }
            )
            print(f">> 📤 Отправлен chat_id пользователю {user_id}")
            return {'status': 'myid sent'}, 200

    # 🧾 Если это заявка от Service Desk
    subject = data.get('created', 'Без даты')
    time = data.get('time', '')
    inc_number = data.get('inc_number', 'не указан')
    city = data.get('city', 'не указан')
    office = data.get('office', 'не указан')
    type_ = data.get('type', 'не указан')
    initiator = data.get('initiator', 'не указан')
    assigned = data.get('assigned', 'не указан')

    # 🔠 Поиск логина без учёта регистра
    chat_id = ASSIGNED_MAP.get(assigned.strip().upper())
    if not chat_id:
        print(f"⛔️ Логин '{assigned}' не найден — заявка проигнорирована.")
        return {'status': 'skipped'}, 200

    # 💬 Формирование сообщения
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

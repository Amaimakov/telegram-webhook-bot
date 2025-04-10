from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = '7972885283:AAHWM_qsGypl1DqscOMF6y9ZhGDJlYuA3II'

ASSIGNED_MAP = {
    "AMAIMAKOV": "400623032",
    "AZAMBYLOV": "604088724",
    "AKENZHEBAYEV": "511448822",
    "ASHUTOV": "462834861",
    "AIGILIK": "275155417",
    "MZHENIS": "5871381787"
}

@app.route('/notify', methods=['POST'])
def notify():
    print(">>> 📥 Пришёл запрос на /notify")
    
    # Логируем сырые данные запроса
    print(">> RAW JSON:", request.get_data(as_text=True))

    data = request.get_json(force=True)

    # ✅ Обработка команды /myid от Telegram
    if 'message' in data:
        msg = data['message']
        chat = msg.get('chat', {})
        user_id = chat.get('id')
        first_name = chat.get('first_name', 'пользователь')
        text = msg.get('text', '')

        if text == '/myid':
            print(f">> ПОЛУЧЕНА КОМАНДА /myid от {user_id}")
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={
                    "chat_id": user_id,
                    "text": f"👋 Привет, {first_name}!\nТвой chat_id: `{user_id}`",
                    "parse_mode": "Markdown"
                }
            )
            return {'status': 'myid sent'}, 200

    # 🧾 Обработка заявки
    subject = data.get('created', '')
    time = data.get('time', '')
    inc_number = data.get('inc_number', '')
    city = data.get('city', '')
    office = data.get('office', '')
    type_ = data.get('type', '')
    initiator = data.get('initiator', '')
    assigned = data.get('assigned', '')

    chat_id = ASSIGNED_MAP.get(assigned.strip().upper())
    if not chat_id:
        return {'status': 'skipped'}, 200

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

    requests.post(
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
        data={
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
    )

    return {'status': 'ok'}, 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

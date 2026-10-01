import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# جلب الإعدادات من متغيرات البيئة في Vercel
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('ADMIN_CHAT_ID')

@app.route('/webhook', methods=['POST'])
def salla_webhook():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        event = data.get('event', 'حدث جديد')
        payload = data.get('data', {})
        
        # استخراج بعض التفاصيل الشائعة (حسب نوع الحدث في سلة)
        order_id = payload.get('id', 'غير معروف')
        total = payload.get('total', {}).get('text', 'غير متوفر')
        customer_name = payload.get('customer', {}).get('name', 'عميل')

        # صياغة رسالة التنبيه لتليجرام
        message = (
            f"🔔 **تنبيه جديد من متجر سلة**\n\n"
            f"📌 **الحدث:** {event}\n"
            f"🆔 **رقم الطلب:** {order_id}\n"
            f"👤 **اسم العميل:** {customer_name}\n"
            f"💰 **المبلغ الإجمالي:** {total}"
        )

        # إرسال الرسالة إلى تليجرام
        if BOT_TOKEN and CHAT_ID:
            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload_data = {
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(telegram_url, json=payload_data)
            
            if response.status_code != 200:
                print(f"Telegram Error: {response.text}")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Salla Webhook Server is Running Successfully!"

if __name__ == '__main__':
    app.run(debug=True)

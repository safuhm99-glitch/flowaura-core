import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# إعدادات بوت تيليجرام (تأكد من ضبط المتغيرات في بيئة العمل على Vercel)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "PUT_YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "PUT_YOUR_CHAT_ID_HERE")


def send_telegram_message(message):
  if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    try:
      requests.post(url, json=payload, timeout=5)
    except Exception as e:
      print(f"Error sending telegram message: {e}")


@app.route("/", methods=["GET"])
def home():
  return jsonify({
      "status": "online",
      "project": "FlowAura Agency Automation",
      "version": "2.0",
  })


@app.route("/", methods=["POST"])
@app.route("/api/index", methods=["POST"])
@app.route("/webhook/salla", methods=["POST"])
def salla_webhook():
  try:
    data = request.json or {}
    event = data.get("event")
    order = data.get("data", {})

    # التحقق من إتمام الطلب وعملية الدفع بنجاح
    if event in [
        "order.created",
        "order.updated",
        "payment.captured",
        "order.status.updated",
    ]:
      order_id = order.get("id", "غير محدد")
      customer_name = order.get("customer", {}).get("name", "عميل FlowAura")
      customer_phone = order.get("customer", {}).get("mobile", "غير متوفر")
      total_amount = order.get("amounts", {}).get("total", {}).get("text", "")

      # استخراج اسم الخدمة المطلوبة
      items = order.get("items", [])
      services_list = []
      for item in items:
        name = item.get("name", "خدمة رقمية")
        qty = item.get("quantity", 1)
        services_list.append(f"- {name} (الكمية: {qty})")

      services_text = (
          "\n".join(services_list)
          if services_list
          else "طلب خدمة رقمية عامة"
      )

      # رسالة التنبيه الفورية التي ستصلكِ على تيليجرام
      notification_text = (
          f"🚨 *طلب جديد في متجر FlowAura!*\n\n"
          f"📦 *رقم الطلب:* #{order_id}\n"
          f"👤 *اسم العميل:* {customer_name}\n"
          f"📱 *الجوال:* {customer_phone}\n"
          f"💰 *المبلغ الإجمالي:* {total_amount}\n\n"
          f"🛠 *الخدمات المطلوبة:*\n{services_text}\n\n"
          f"✨ *الحالة:* جاري المعالجة والتسليم الآلي..."
      )

      send_telegram_message(notification_text)

    return jsonify({"status": "success", "message": "Webhook processed"}), 200

  except Exception as e:
    print(f"Webhook Error: {e}")
    return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)

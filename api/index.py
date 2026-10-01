import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# إعدادات متغيرات البيئة من Vercel
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def send_telegram_message(chat_id, message):
  """دالة لإرسال الرسائل عبر تيليجرام (سواء للإدارة أو للعميل إذا توفر الشات)"""
  if TELEGRAM_BOT_TOKEN and chat_id:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    try:
      requests.post(url, json=payload, timeout=5)
    except Exception as e:
      print(f"Error sending telegram message: {e}")


def generate_ai_content(service_type, customer_notes):
  """محرك الذكاء الاصطناعي لتوليد المحتوى أو تفاصيل الخدمة آلياً"""
  if not OPENAI_API_KEY:
    return "تم استلام الطلب بنجاح (مفتاح الذكاء الاصطناعي غير معرّف حالياً)."

  prompt = (
      f"قم بإنشاء محتوى أو خطبة تسويقية/هيكلية لخدمة: {service_type}. "
      f"بناءً على طلب وملاحظات العميل التالية: {customer_notes}"
  )

  try:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json=data,
        headers=headers,
        timeout=15,
    )
    result = response.json()
    return result["choices"][0]["message"]["content"]
  except Exception as e:
    print(f"AI Generation Error: {e}")
    return "عذراً، حدث خطأ أثناء التوليد الآلي، سيتم مراجعة الطلب يدويياً."


@app.route("/", methods=["GET"])
def home():
  return jsonify({
      "status": "online",
      "project": "FlowAura AI Automation Engine",
      "version": "4.0",
  })


@app.route("/", methods=["POST"])
@app.route("/api/index", methods=["POST"])
@app.route("/webhook/salla", methods=["POST"])
def salla_webhook():
  try:
    data = request.json or {}
    event = data.get("event")
    order = data.get("data", {})

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

      # استخراج تفاصيل المنتجات وملاحظات العميل
      items = order.get("items", [])
      service_type = "خدمة رقمية"
      customer_notes = "لا توجد ملاحظات إضافية"

      for item in items:
        name = item.get("name", "")
        if "هبوط" in name.lower() or "landing" in name.lower():
          service_type = "تصميم صفحة هبوط"
        elif "3d" in name.lower() or "ثلاثي" in name.lower():
          service_type = "تصميم ثلاثي الأبعاد (3D)"
        elif "هوية" in name.lower() or "branding" in name.lower():
          service_type = "هوية بصرية"

      # استدعاء الذكاء الاصطناعي لتوليد المحتوى أو الأصول الآلية للخدمة
      ai_output = generate_ai_content(service_type, customer_notes)

      # تنبيه الإدارة (لكِ) بالتفاصيل وما تم توليده
      admin_message = (
          f"🤖 *تم تنفيذ طلب آلياً عبر الذكاء الاصطناعي!*\n\n"
          f"📦 *رقم الطلب:* #{order_id}\n"
          f"🛠 *الخدمة:* {service_type}\n"
          f"👤 *العميل:* {customer_name} ({customer_phone})\n"
          f"💰 *المبلغ:* {total_amount}\n\n"
          f"📝 *مخرجات الذكاء الاصطناعي:*\n{ai_output}"
      )

      # إرسال التنبيه إلى شات الإدارة الخاص بكِ
      if TELEGRAM_CHAT_ID:
        send_telegram_message(TELEGRAM_CHAT_ID, admin_message)

    return jsonify({"status": "success", "ai_engine": "active"}), 200

  except Exception as e:
    print(f"Webhook Error: {e}")
    return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)

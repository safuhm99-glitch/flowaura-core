import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# إعدادات بوت تيليجرام (متوافقة مع متغيرات بيئة العمل في Vercel)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "PUT_YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "PUT_YOUR_CHAT_ID_HERE")


def send_telegram_message(message):
  """دالة مخصصة لإرسال الإشعارات إلى بوت تيليجرام الخاص بكِ"""
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
      "project": "FlowAura Agency Automation & AI Engine",
      "version": "3.0",
  })


@app.route("/", methods=["POST"])
@app.route("/api/index", methods=["POST"])
@app.route("/webhook/salla", methods=["POST"])
def salla_webhook():
  try:
    data = request.json or {}
    event = data.get("event")
    order = data.get("data", {})

    # مراقبة الأحداث الخاصة بإنشاء أو تحديث الطلبات وعمليات الدفع
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

      # استخراج المنتجات والخدمات المطلوبة بدقة
      items = order.get("items", [])
      services_list = []
      service_type = "خدمة رقمية عامة"
      
      for item in items:
        name = item.get("name", "تصميم رقمي")
        qty = item.get("quantity", 1)
        services_list.append(f"- {name} (الكمية: {qty})")
        
        # تصنيف نوع الخدمة ذكياً بناءً على اسم المنتج
        if "3d" in name.lower() or "ثلاثي" in name.lower():
          service_type = "تصميم ثلاثي الأبعاد (3D)"
        elif "هوية" in name.lower() or "branding" in name.lower():
          service_type = "هوية بصرية متكاملة"

      services_text = "\n".join(services_list) if services_list else "طلب خاص"

      # --- محرك التسليم الآلي (الرد التلقائي للعميل أو توجيه مسار العمل) ---
      # هنا يمكنكِ تخصيص الروابط أو الملفات التي تُسلّم آلياً حسب نوع الخدمة
      delivery_instruction = "جاري مراجعة متطلباتك وبدء العمل الإبداعي."
      if "ثلاثي" in service_type:
        delivery_instruction = "سيتم إرسال نموذج المعاينة الأولية خلال 24 ساعة."
      elif "هوية" in service_type:
        delivery_instruction = "تم استلام استبيان الهوية وبدء مرحلة الأفكار."

      # رسالة التنبيه الإدارية الشاملة التي ستصلكِ على تيليجرام
      notification_text = (
          f"🚀 *طلب مشروع جديد قيد التنفيذ!*\n\n"
          f"📦 *رقم الطلب:* #{order_id}\n"
          f"🎨 *تصنيف الخدمة:* {service_type}\n"
          f"👤 *اسم العميل:* {customer_name}\n"
          f"📱 *الجوال:* {customer_phone}\n"
          f"💰 *المبلغ الإجمالي:* {total_amount}\n\n"
          f"🛠 *تفاصيل المنتجات:*\n{services_text}\n\n"
          f"⚙️ *حالة التسليم الآلي:* {delivery_instruction}\n"
          f"✨ *الإجراء:* بانتظار لمستك الإبداعية للبدء فوراً!"
      )

      # إرسال التنبيه إلى جهازكِ عبر البوت
      send_telegram_message(notification_text)

    return jsonify({"status": "success", "message": "Automation engine processed successfully"}), 200

  except Exception as e:
    print(f"Webhook Error: {e}")
    return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)

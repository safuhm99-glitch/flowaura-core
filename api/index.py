import os
import smtplib
from email.message import EmailMessage
from flask import Flask, jsonify, request
from openai import OpenAI

app = Flask(__name__)

# تهيئة عميل OpenAI تلقائياً من متغيرات البيئة إن وجدت
client = OpenAI()


@app.route("/")
def home():
  return "Smart Pulse AI Server is Running Successfully!"


@app.route("/send-email", methods=["POST"])
def send_email():
  try:
    data = request.json
    recipient = data.get("email")
    product_name = data.get("product", "المنتج الرقمي")

    # توليد رد أو محتوى ذكي عبر الذكاء الاصطناعي اختياري
    prompt = f"اكتب رسالة شكر ترحيبية قصيرة لعميل اشترى {product_name}."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )
    ai_message = response.choices[0].message.content

    # إعدادات البريد الإلكتروني عبر Gmail SMTP
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    msg = EmailMessage()
    msg.set_content(ai_message)
    msg["Subject"] = f"طلبك جاهز: {product_name}"
    msg["From"] = sender_email
    msg["To"] = recipient

    # الاتصال بسيرفر جوجل وإرسال البريد
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
      server.login(sender_email, sender_password)
      server.send_message(msg)

    return (
        jsonify({"status": "success", "message": "تم إرسال البريد بنجاح!"}),
        200,
    )

  except Exception as e:
    return jsonify({"status": "error", "message": str(e)}), 500

from fastapi import FastAPI, Request, HTTPException
import smtplib
import requests
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI(title="FlowAura & SmartPulseAI Core", version="1.0")

VERIFY_TOKEN = "smartpulse_verify_2026"
WHATSAPP_TOKEN = "ضع_رمز_الوصول_الدائم_هنا"
PHONE_NUMBER_ID = "966580414481"

SMTP_SERVER = "mail.smartpulseai.net"
SMTP_PORT = 465
EMAIL_USER = "info@smartpulseai.net"
EMAIL_PASSWORD = "Ss778811&"

@app.get("/")
async def root():
    return {"status": "online", "message": "FlowAura & SmartPulseAI Core is running successfully!"}

@app.get("/api/index")
@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return int(challenge)
        else:
            raise HTTPException(status_code=403, detail="Verification token mismatch")
    raise HTTPException(status_code=400, detail="Invalid parameters")

@app.post("/api/index")
@app.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()
    try:
        entry = body["entry"][0]
        change = entry["changes"][0]
        value = change["value"]
        
        if "messages" in value:
            phone_id = value["metadata"]["phone_number_id"]
            from_phone = value["messages"][0]["from"]
            msg_body = value["messages"][0]["text"]["body"]
            
            print(f"تم استلام رسالة من {from_phone}: {msg_body}")
            send_whatsapp_message(phone_id, from_phone, "أهلاً بك! أنا مساعدك الذكي في منصة FlowAura، جاري تحليل طلبك...")
            
        return {"status": "success"}
    except Exception as e:
        return {"status": "ignored", "reason": str(e)}

def send_whatsapp_message(phone_id, recipient_phone, text):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_phone,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(
        f"https://graph.facebook.com/v17.0/{phone_id}/messages",
        headers=headers,
        json=payload
    )
    return response.json()

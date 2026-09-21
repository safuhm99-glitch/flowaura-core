from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Smart Pulse AI & FlowAura</title>
        <style>
            body { font-family: sans-serif; background: #f0f2f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center; }
            .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #0070f3; margin-bottom: 10px; }
            p { color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Smart Pulse AI & FlowAura</h1>
            <p>المنصة السحابية تعمل بنجاح وجاهزة لخدمتكم!</p>
        </div>

        <!-- كود الشات بوت الذكي لمنصة Smart Pulse AI -->
        <div id="smart-chatbot-widget" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
          <button id="chatbot-toggle-btn" style="background-color: #0070f3; color: white; border: none; border-radius: 50%; width: 60px; height: 60px; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.15); font-size: 24px;">💬</button>
          
          <div id="chatbot-window" style="display: none; width: 320px; height: 450px; background: white; border-radius: 12px; box-shadow: 0 5px 25px rgba(0,0,0,0.2); position: absolute; bottom: 75px; right: 0; flex-direction: column; overflow: hidden; font-family: sans-serif;">
            <div style="background: #0070f3; color: white; padding: 15px; font-weight: bold; display: flex; justify-content: space-between; align-items: center;">
              <span>مساعد Smart Pulse AI</span>
              <button id="chatbot-close-btn" style="background: none; border: none; color: white; font-size: 16px; cursor: pointer;">✕</button>
            </div>
            <div id="chatbot-messages" style="flex: 1; padding: 15px; overflow-y: auto; font-size: 14px; color: #333; background: #f9f9f9; text-align: right;">
              <div style="background: #e6f0ff; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                أهلاً بك في منصتنا السحابية <b>Smart Pulse AI</b>! كيف يمكنني مساعدتك اليوم؟
              </div>
            </div>
            <div style="padding: 10px; border-top: 1px solid #eee; display: flex; background: white;">
              <input type="text" id="chatbot-input" placeholder="اكتب استفسارك هنا..." style="flex: 1; border: 1px solid #ddd; padding: 8px; border-radius: 6px; outline: none; font-size: 13px;">
              <button id="chatbot-send-btn" style="background: #0070f3; color: white; border: none; padding: 8px 12px; margin-right: 5px; border-radius: 6px; cursor: pointer;">إرسال</button>
            </div>
          </div>
        </div>

        <script>
          const toggleBtn = document.getElementById('chatbot-toggle-btn');
          const closeBtn = document.getElementById('chatbot-close-btn');
          const chatWindow = document.getElementById('chatbot-window');
          const sendBtn = document.getElementById('chatbot-send-btn');
          const inputField = document.getElementById('chatbot-input');
          const messagesContainer = document.getElementById('chatbot-messages');

          chatWindow.style.display = 'none';

          toggleBtn.addEventListener('click', () => {
            chatWindow.style.display = chatWindow.style.display === 'none' ? 'flex' : 'none';
          });

          closeBtn.addEventListener('click', () => {
            chatWindow.style.display = 'none';
          });

          sendBtn.addEventListener('click', () => {
            const text = inputField.value.trim();
            if (text) {
              messagesContainer.innerHTML += `<div style="text-align: left; background: #0070f3; color: white; padding: 8px; border-radius: 8px; margin-bottom: 10px; margin-left: 20px;">${text}</div>`;
              inputField.value = '';
              messagesContainer.scrollTop = messagesContainer.scrollHeight;

              setTimeout(() => {
                messagesContainer.innerHTML += `<div style="background: #e6f0ff; color: #333; padding: 8px; border-radius: 8px; margin-bottom: 10px; margin-right: 20px;">شكراً لتواصلك! تم استلام استفسارك وسيتم تحويله أو الرد عليك عبر البريد الرسمي.</div>`;
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
              }, 1000);
            }
          });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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

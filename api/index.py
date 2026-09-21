from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import smtplib
from email.message import EmailMessage
import os

app = FastAPI(title="SmartPulseAI Core & Dashboard", version="2.0")

# إعدادات البريد الإلكتروني الرسمي
SMTP_SERVER = "mail.smartpulseai.net"
SMTP_PORT = 465
EMAIL_USER = "info@smartpulseai.net"
EMAIL_PASSWORD = "Ss778811&"

# هيكل بيانات الخدمات، الباقات، والخصومات (يمكنك تعديلها في أي وقت)
PRICING_PLANS = {
    "basic": {"name": "الباقة الأساسية", "price": "199 ريال", "discount": "لا يوجد حالياً"},
    "pro": {"name": "الباقة الاحترافية (Micro-SaaS)", "price": "499 ريال", "discount": "خصم 20% لفترة محدودة"},
    "enterprise": {"name": "باقة الشركات", "price": "999 ريال", "discount": "خصم خاص عند الدفع السنوي"}
}

# قائمة مؤقتة لتخزين بيانات العملاء والطلبات (يمكن ربطها بقاعدة بيانات لاحقاً)
LEADS_DATABASE = []

# 1. نقطة النهاية الرئيسية للموقع
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>SmartPulseAI</title></head>
        <body style="font-family: Arial; direction: rtl; text-align: center; padding: 50px;">
            <h1>مرحباً بك في منصة SmartPulseAI</h1>
            <p>المنصة تعمل بنجاح وجاهزة لاستقبال العملاء والخدمات الذكية.</p>
            <a href="/dashboard" style="background: #0070f3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">الذهاب إلى لوحة التحكم (Dashboard)</a>
        </body>
    </html>
    """

# 2. استقبال بيانات العملاء (Leads) وحفظها وإرسال إشعار للإيميل
@app.post("/api/lead")
async def collect_lead(request: Request):
    data = await request.json()
    name = data.get("name", "عميل جديد")
    phone = data.get("phone", "غير متوفر")
    email = data.get("email", "غير متوفر")
    message = data.get("message", "استفسار عام")
    
    lead_info = {"name": name, "phone": phone, "email": email, "message": message}
    LEADS_DATABASE.append(lead_info)
    
    # إرسال إشعار إلى بريدك الرسمي
    try:
        msg = EmailMessage()
        msg.set_content(f"تم استلام عميل/طلب جديد:\n\nالاسم: {name}\nالهاتف: {phone}\nالبريد: {email}\nالرسالة: {message}")
        msg['Subject'] = "طلب جديد عبر منصة SmartPulseAI"
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER
        
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print(f"خطأ في إرسال البريد: {e}")
        
    return {"status": "success", "message": "تم حفظ البيانات وإرسال الإشعار بنجاح"}

# 3. استعراض الباقات والخصومات الحالية
@app.get("/api/pricing")
async def get_pricing():
    return {"plans": PRICING_PLANS}

# 4. لوحة التحكم المستقلة (Dashboard) لمتابعة سير العمل والعملاء والردود
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    leads_html = "".join([f"<li><b>{l['name']}</b> - {l['phone']} - {l['email']} | الرسالة: {l['message']}</li>" for l in LEADS_DATABASE])
    if not leads_html:
        leads_html = "<li>لا توجد بيانات مسجلة حتى الآن.</li>"
        
    return f"""
    <html>
        <head>
            <title>لوحة التحكم - SmartPulseAI</title>
            <meta charset="utf-8">
        </head>
        <body style="font-family: Arial; direction: rtl; padding: 30px; background: #f9f9f9;">
            <h1>لوحة تحكم SmartPulseAI (Dashboard)</h1>
            <hr>
            <h3>📊 حالة النظام: <span style="color: green;">يعمل بكفاءة على Vercel</span></h3>
            <h3>🏷️ الباقات والأسعار الحالية:</h3>
            <ul>
                <li><b>{PRICING_PLANS['basic']['name']}</b>: {PRICING_PLANS['basic']['price']} ({PRICING_PLANS['basic']['discount']})</li>
                <li><b>{PRICING_PLANS['pro']['name']}</b>: {PRICING_PLANS['pro']['price']} ({PRICING_PLANS['pro']['discount']})</li>
                <li><b>{PRICING_PLANS['enterprise']['name']}</b>: {PRICING_PLANS['enterprise']['price']} ({PRICING_PLANS['enterprise']['discount']})</li>
            </ul>
            <hr>
            <h3>👥 سجل العملاء والطلبات الجديدة:</h3>
            <ul>
                {leads_html}
            </ul>
            <br>
            <a href="/" style="background: #333; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px;">العودة للموقع الرئيسي</a>
        </body>
    </html>
    """

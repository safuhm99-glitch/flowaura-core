from datetime import datetime
from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import parse_qs, urlparse
import requests

# قراءة التوكن ومعرف الأدمن من متغيرات البيئة بأمان تام
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

def send_telegram_message(chat_id, message, reply_markup=None):
    """دالة لإرسال رسائل أو تنبيهات إلى تليجرام"""
    if not TELEGRAM_BOT_TOKEN:
        return None
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.json()
    except Exception as e:
        print(f"Error sending telegram message: {e}")
        return None

# قاعدة بيانات مؤقتة للطلبات والاسترجاع
ORDERS_DB = [
    {
        "id": 1,
        "type": "📦 منتج / وسيط",
        "query": "ساعة ذكية بسعر اقتصادي",
        "offer": "أفضل سعر موفر: 180 ريال",
        "status": "تمت المساومة بنجاح ✓",
        "date": "2026-09-24"
    }
]
REFUNDS_DB = []

# قاموس اللغات (عربي / إنجليزي)
TRANSLATIONS = {
    "ar": {
        "dir": "rtl",
        "lang": "ar",
        "title": "متجر FlowAura الذكي",
        "subtitle": "المساعد الذكي الآلي للوساطة والتجارة",
        "desc": "أرسل طلبك الجديد وسيتم معالجته وإشعارك فوراً.",
        "order_type_1": "📦 منتج مادي (بحث عن أرخص سعر)",
        "order_type_2": "⚡ خدمة فورية (تصميم، برمجة، استشارات)",
        "query_placeholder": "اكتب تفاصيل طلبك هنا...",
        "send_btn": "إرسال الطلب 🚀",
        "refund_title": "🔄 قسم طلبات الاسترجاع",
        "refund_desc": "هل واجهتك مشكلة وتريد استرجاع طلب سابق؟",
        "order_id_placeholder": "رقم الطلب المراد استرجاعه (مثال: 1)",
        "reason_placeholder": "اكتب سبب الاسترجاع بالتفصيل...",
        "refund_btn": "تقديم طلب الاسترجاع ⚠️",
        "dashboard_link": "لوحة التحكم وسجل الطلبات 📊",
        "switch_lang": "Switch to English 🇬🇧",
        "switch_lang_url": "?lang=en"
    },
    "en": {
        "dir": "ltr",
        "lang": "en",
        "title": "FlowAura Smart Store",
        "subtitle": "AI-Powered Automated Assistant for Commerce & Brokerage",
        "desc": "Submit your new request and it will be processed instantly.",
        "order_type_1": "📦 Physical Product (Best Price Search)",
        "order_type_2": "⚡ Instant Service (Design, Dev, Consulting)",
        "query_placeholder": "Type your request details here...",
        "send_btn": "Submit Request 🚀",
        "refund_title": "🔄 Refund Requests Section",
        "refund_desc": "Facing an issue and want to refund a previous order?",
        "order_id_placeholder": "Order ID to refund (e.g., 1)",
        "reason_placeholder": "Type the reason for refund in detail...",
        "refund_btn": "Submit Refund Request ⚠️",
        "dashboard_link": "Dashboard & Orders Log 📊",
        "switch_lang": "التحويل للعربية 🇸🇦",
        "switch_lang_url": "?lang=ar"
    }
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # استخراج اللغة من الـ Query Parameters (افتراضياً العربية)
        query_params = parse_qs(parsed_path.query)
        lang = query_params.get("lang", ["ar"])[0]
        if lang not in TRANSLATIONS:
            lang = "ar"
        t = TRANSLATIONS[lang]

        if path == "/set-webhook":
            if not TELEGRAM_BOT_TOKEN:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Error: TELEGRAM_BOT_TOKEN is missing.")
                return
            host = self.headers.get("Host")
            protocol = "https" if "localhost" not in host else "http"
            webhook_url = f"{protocol}://{host}/"
            tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={webhook_url}"
            resp = requests.get(tg_url).json()
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            return

        if path == "/dashboard":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            orders_html = ""
            for o in ORDERS_DB:
                orders_html += f"""
                <tr style="border-bottom: 1px solid #334155;">
                    <td style="padding: 12px; color: #38bdf8;">#{o['id']}</td>
                    <td style="padding: 12px;"><b>{o['type']}</b></td>
                    <td style="padding: 12px; color: #f8fafc;">{o['query']}</td>
                    <td style="padding: 12px; color: #4ade80;">{o['offer']}</td>
                    <td style="padding: 12px; color: #fbbf24;">{o['status']}</td>
                    <td style="padding: 12px; color: #94a3b8;">{o['date']}</td>
                </tr>
                """

            html_content = f"""
            <!DOCTYPE html>
            <html lang="{t['lang']}" dir="{t['dir']}">
            <head>
                <meta charset="UTF-8">
                <title>Dashboard - FlowAura</title>
                <style>
                    body {{ font-family: Tahoma, sans-serif; background: #0f172a; color: white; margin: 0; padding: 20px; }}
                    .container {{ max-width: 1100px; margin: auto; background: #1e293b; padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
                    .logo-area {{ text-align: center; margin-bottom: 20px; }}
                    .logo-area img {{ width: 90px; height: 90px; border-radius: 50%; border: 2px solid #38bdf8; object-fit: cover; }}
                    h1, h2 {{ color: #38bdf8; text-align: center; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 30px; }}
                    th {{ background: #334155; padding: 12px; text-align: {('left' if t['dir']=='ltr' else 'right')}; color: #38bdf8; }}
                    .btn {{ display: inline-block; background: #2563eb; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="logo-area">
                        <img src="https://www.smartpulseai.net/logo.png" alt="Logo" onerror="this.style.display='none'">
                    </div>
                    <h1>📊 FlowAura Dashboard & Orders Log</h1>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Type</th>
                                <th>Details</th>
                                <th>Offer</th>
                                <th>Status</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>{orders_html}</tbody>
                    </table>
                    <div style="text-align: center;"><a href="/?lang={lang}" class="btn">Back to Store</a></div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            html_content = f"""
            <!DOCTYPE html>
            <html lang="{t['lang']}" dir="{t['dir']}">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{t['title']}</title>
                <style>
                    body {{ font-family: Tahoma, sans-serif; background: #0f172a; color: white; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
                    .card {{ background: #1e293b; padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); width: 100%; max-width: 600px; text-align: center; margin: 20px; }}
                    .logo-container img {{ width: 90px; height: 90px; border-radius: 50%; border: 2px solid #38bdf8; object-fit: cover; }}
                    h1 {{ color: #38bdf8; margin-bottom: 5px; font-size: 24px; }}
                    .subtitle {{ color: #94a3b8; font-size: 13px; margin-bottom: 20px; }}
                    h3 {{ color: #f87171; margin-top: 30px; margin-bottom: 10px; font-size: 20px; }}
                    p {{ color: #94a3b8; font-size: 14px; margin-bottom: 20px; }}
                    select, textarea, input {{ width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; font-size: 15px; margin-bottom: 12px; box-sizing: border-box; }}
                    textarea {{ height: 80px; resize: none; }}
                    button {{ background: #2563eb; color: white; border: none; padding: 12px 25px; border-radius: 8px; font-size: 16px; cursor: pointer; width: 100%; transition: background 0.3s; }}
                    button:hover {{ background: #1d4ed8; }}
                    .refund-btn {{ background: #dc2626; }}
                    .lang-bar {{ margin-bottom: 15px; text-align: {('left' if t['dir']=='ltr' else 'right')}; }}
                    .lang-bar a {{ background: #334155; color: #38bdf8; padding: 6px 12px; border-radius: 6px; text-decoration: none; font-size: 13px; }}
                    .links {{ margin-top: 20px; }}
                    .links a {{ color: #38bdf8; text-decoration: none; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="lang-bar">
                        <a href="{t['switch_lang_url']}">{t['switch_lang']}</a>
                    </div>
                    <div class="logo-container">
                        <img src="https://www.smartpulseai.net/logo.png" alt="Logo" onerror="this.style.display='none'">
                    </div>
                    <h1>{t['title']}</h1>
                    <div class="subtitle">{t['subtitle']}</div>
                    <p>{t['desc']}</p>
                    
                    <form action="/submit-order?lang={lang}" method="POST">
                        <select name="order_type">
                            <option value="📦 منتج / وسيط">{t['order_type_1']}</option>
                            <option value="⚡ خدمة فورية">{t['order_type_2']}</option>
                        </select>
                        <textarea name="query" placeholder="{t['query_placeholder']}"></textarea>
                        <button type="submit">{t['send_btn']}</button>
                    </form>

                    <hr style="border: 0; border-top: 1px solid #334155; margin: 25px 0;">

                    <h3>{t['refund_title']}</h3>
                    <p>{t['refund_desc']}</p>
                    <form action="/submit-refund?lang={lang}" method="POST">
                        <input type="text" name="order_id" placeholder="{t['order_id_placeholder']}">
                        <textarea name="reason" placeholder="{t['reason_placeholder']}"></textarea>
                        <button type="submit" class="refund-btn">{t['refund_btn']}</button>
                    </form>

                    <div class="links">
                        <a href="/dashboard?lang={lang}">{t['dashboard_link']}</a>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode("utf-8"))

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        lang = query_params.get("lang", ["ar"])[0]

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        if path == "/submit-order":
            params = parse_qs(post_data)
            order_type = params.get("order_type", ["📦 Order"])[0]
            user_query = params.get("query", ["New Order"])[0]
            
            new_id = len(ORDERS_DB) + 1
            ORDERS_DB.append({
                "id": new_id,
                "type": order_type,
                "query": user_query,
                "offer": "AI Negotiated Offer",
                "status": "Processing ✓",
                "date": datetime.now().strftime("%Y-%m-%d")
            })

            if ADMIN_CHAT_ID:
                send_telegram_message(ADMIN_CHAT_ID, f"🚨 New Order #{new_id}\nType: {order_type}\nDetails: {user_query}")

            self.send_response(303)
            self.send_header('Location', f'/dashboard?lang={lang}')
            self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')

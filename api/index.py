from datetime import datetime
from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import parse_qs, urlparse
import requests

# قراءة التوكن ومعرف الأدمن من متغيرات البيئة بأمان تام لتجنب تنبيهات الأمان
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")


def send_telegram_message(chat_id, message, reply_markup=None):
  """دالة لإرسال رسائل أو ردود إلى تليجرام"""
  if not TELEGRAM_BOT_TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN is not set.")
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


# قاعدة بيانات مؤقتة للطلبات
ORDERS_DB = [
    {
        "id": 1,
        "type": "📦 منتج / وسيط",
        "query": "ساعة ذكية بسعر اقتصادي",
        "offer": "أفضل سعر موفر: 180 ريال (خصم 20%)",
        "status": "تمت المساومة بنجاح ✓",
        "date": "2026-09-24",
    },
    {
        "id": 2,
        "type": "⚡ خدمة فورية",
        "query": "تصميم شعار احترافي للمتجر",
        "offer": "مزود خدمة ذكي آلي - تسليم فوري",
        "status": "تم التنفيذ بالذكاء الاصطناعي",
        "date": "2026-09-24",
    },
]


class handler(BaseHTTPRequestHandler):

  def do_GET(self):
    parsed_path = urlparse(self.path)
    path = parsed_path.path

    # مسار ربط الـ Webhook تلقائياً
    if path == "/set-webhook":
      if not TELEGRAM_BOT_TOKEN:
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Error: TELEGRAM_BOT_TOKEN is missing in environment.")
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
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <title>لوحة تحكم متجر FlowAura الذكي</title>
                <style>
                    body {{ font-family: Tahoma, sans-serif; background: #0f172a; color: white; margin: 0; padding: 20px; }}
                    .container {{ max-width: 1100px; margin: auto; background: #1e293b; padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
                    h1 {{ color: #38bdf8; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                    th {{ background: #334155; padding: 12px; text-align: right; color: #38bdf8; }}
                    .btn {{ display: inline-block; background: #2563eb; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; margin-top: 20px; }}
                    .btn:hover {{ background: #1d4ed8; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>لوحة تحكم متجر FlowAura الذكي</h1>
                    <p>مرحباً بكِ، صفية. هذه سجلات الطلبات والعروض الواردة:</p>
                    <table>
                        <thead>
                            <tr>
                                <th>رقم الطلب</th>
                                <th>نوع الطلب</th>
                                <th>تفاصيل الطلب</th>
                                <th>محاكاة العرض / المساومة</th>
                                <th>الحالة</th>
                                <th>التاريخ</th>
                            </tr>
                        </thead>
                        <tbody>
                            {orders_html}
                        </tbody>
                    </table>
                    <a href="/" class="btn">العودة للرئيسية</a>
                </div>
            </body>
            </html>
            """
      self.wfile.write(html_content.encode("utf-8"))

    else:
      self.send_response(200)
      self.send_header("Content-type", "text/html; charset=utf-8")
      self.end_headers()

      html_content = """
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>متجر FlowAura الذكي</title>
                <style>
                    body { font-family: Tahoma, sans-serif; background: #0f172a; color: white; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
                    .card { background: #1e293b; padding: 40px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); width: 100%; max-width: 600px; text-align: center; margin: 20px; }
                    h1 { color: #38bdf8; margin-bottom: 10px; }
                    p { color: #94a3b8; margin-bottom: 30px; }
                    select, textarea { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; font-size: 16px; margin-bottom: 15px; box-sizing: border-box; }
                    textarea { height: 90px; resize: none; }
                    button { background: #2563eb; color: white; border: none; padding: 12px 25px; border-radius: 8px; font-size: 16px; cursor: pointer; width: 100%; transition: background 0.3s; }
                    button:hover { background: #1d4ed8; }
                    .links { margin-top: 20px; }
                    .links a { color: #38bdf8; text-decoration: none; margin: 0 10px; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>متجر FlowAura الذكي</h1>
                    <p>مساعدك التجاري والخدمي. اطلب منتجاً أو خدمة وسيتولى النظام معالجتها وإرسال إشعارك!</p>
                    
                    <form action="/submit-order" method="POST">
                        <select name="order_type">
                            <option value="📦 منتج / وسيط">📦 منتج مادي (بحث عن أرخص سعر)</option>
                            <option value="⚡ خدمة فورية">⚡ خدمة فورية (تصميم، برمجة، استشارات)</option>
                        </select>
                        <textarea name="query" placeholder="اكتب تفاصيل طلبك هنا..."></textarea>
                        <button type="submit">إرسال الطلب 🚀</button>
                    </form>

                    <div class="links">
                        <a href="/dashboard">لوحة التحكم وسجل الطلبات</a>
                    </div>
                </div>
            </body>
            </html>
            """
      self.wfile.write(html_content.encode("utf-8"))

  def do_POST(self):
    parsed_path = urlparse(self.path)
    path = parsed_path.path

    content_length = int(self.headers.get("Content-Length", 0))
    post_data = self.rfile.read(content_length).decode("utf-8")

    # 1. استقبال الطلبات القادمة من الواجهة (Dashboard)
    if path == "/submit-order":
      params = parse_qs(post_data)
      order_type = params.get("order_type", ["📦 منتج / وسيط"])[0]
      user_query = params.get("query", ["طلب جديد"])[0]

      simulated_offer = (
          "تم التفاوض آلياً: تم توفير خصم خاص من الموردين"
          if "منتج" in order_type
          else "جاهز للتسليم الفوري بالذكاء الاصطناعي"
      )
      simulated_status = "جاري المعالجة ✓"

      current_date = datetime.now().strftime("%Y-%m-%d")
      new_id = len(ORDERS_DB) + 1
      ORDERS_DB.append({
          "id": new_id,
          "type": order_type,
          "query": user_query,
          "offer": simulated_offer,
          "status": simulated_status,
          "date": current_date,
      })

      # إرسال إشعار لكِ على تليجرام إذا توفرت معرفات الأدمن
      if ADMIN_CHAT_ID:
        telegram_msg = (
            "🚨 *طلب جديد تم استقباله في متجر FlowAura!*\n\n"
            f"🆔 *رقم الطلب:* #{new_id}\n"
            f"📦 *نوع الطلب:* {order_type}\n"
            f"📝 *التفاصيل:* {user_query}\n"
            f"💡 *العرض:* {simulated_offer}"
        )
        send_telegram_message(ADMIN_CHAT_ID, telegram_msg)

      self.send_response(303)
      self.send_header("Location", "/dashboard")
      self.end_headers()

    # 2. استقبال الرسائل القادمة من بوت تليجرام التفاعلي (مثل /start)
    else:
      try:
        data = json.loads(post_data)
        if "message" in data:
          chat_id = data["message"]["chat"]["id"]
          text = data["message"].get("text", "")

          if text.startswith("/start"):
            welcome_msg = (
                "مرحباً بكِ يا صفية في بوت *FlowAura Store* 🌟\n\n"
                "أنا مساعدك الذكي لاستقبال الطلبات وإدارتها."
            )
            keyboard = {
                "inline_keyboard": [[{
                    "text": "🌐 زيارة لوحة التحكم والطلب",
                    "url": f"https://{self.headers.get('Host')}/dashboard",
                }]]
            }
            send_telegram_message(chat_id, welcome_msg, keyboard)
          else:
            send_telegram_message(
                chat_id,
                "تم استلام رسالتك بنجاح! سيتم معالجة طلبك قريباً بواسطة النظام"
                " الذكي.",
            )
      except Exception as e:
        print(f"Webhook Error: {e}")

      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))

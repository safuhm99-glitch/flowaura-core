from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse

# قاعدة بيانات مؤقتة متطورة تدعم محاكاة عروض الأسعار والمساومة الآلية
ORDERS_DB = [
    {
        "id": 1,
        "type": "📦 منتج / وسيط",
        "query": "ساعة ذكية بسعر اقتصادي",
        "offer": "أفضل سعر موفر: 180 ريال (خصم 20%)",
        "status": "تمت المساومة بنجاح ✓",
        "date": "2026-09-21",
    },
    {
        "id": 2,
        "type": "⚡ خدمة فورية",
        "query": "تصميم شعار احترافي للمتجر",
        "offer": "مزود خدمة ذكي آلي - تسليم فوري",
        "status": "تم التنفيذ بالذكاء الاصطناعي",
        "date": "2026-09-21",
    },
]


class handler(BaseHTTPRequestHandler):

  def do_GET(self):
    parsed_path = urlparse(self.path)
    path = parsed_path.path

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
                <title>لوحة تحكم الوسيط الذكي - Omni-Flow</title>
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
                    <h1>لوحة تحكم الوسيط الذكي والخدمات (Omni-Flow Dashboard)</h1>
                    <p>مرحباً بكِ، صفية. هذه هي سجلات الطلبات، نتائج البحث، وعروض الأسعار والمساومات الآلية:</p>
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
                <title>المتظومة الذكية الشاملة - Omni-Flow</title>
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
                    <h1>المتظومة الذكية الشاملة (Omni-Flow)</h1>
                    <p>مساعدك التجاري والخدمي الآلي. حدد نوع طلبك ودع الوسيط الذكي يتولى البحث، المساومة، أو التنفيذ الفوري!</p>
                    
                    <form action="/submit-order" method="POST">
                        <select name="order_type">
                            <option value="📦 منتج / وسيط">📦 منتج مادي (بحث عن أرخص سعر / تجارة عكسية)</option>
                            <option value="⚡ خدمة فورية">⚡ خدمة فورية (تصميم، ترجمة، برمجة، استشارات)</option>
                        </select>
                        <textarea name="query" placeholder="اكتب تفاصيل طلبك هنا بوضوح... (مثال: ابحث عن جوال ايفون 18 برو ماكس بأقل سعر، أو أحتاج تصميم شعار)"></textarea>
                        <button type="submit">إرسال الطلب للوسيط الذكي 🚀</button>
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

    if path == "/submit-order":
      content_length = int(self.headers.get("Content-Length", 0))
      post_data = self.rfile.read(content_length).decode("utf-8")
      params = parse_qs(post_data)

      order_type = params.get("order_type", ["📦 منتج / وسيط"])[0]
      user_query = params.get("query", ["طلب جديد"])[0]

      # محاكاة ذكية لعرض السعر والمساومة بناءً على نوع الطلب
      if "منتج" in order_type:
        simulated_offer = (
            "تم التفاوض آلياً: تم توفير خصم 15% من أفضل مورد عالمي"
        )
        simulated_status = "جاري تأكيد الشحن ✓"
      else:
        simulated_offer = (
            "تمت مطابقة المزود الآلي - جاهز للتسليم الفوري بالذكاء الاصطناعي"
        )
        simulated_status = "مكتمل وجاهز ⚡"

      new_id = len(ORDERS_DB) + 1
      ORDERS_DB.append({
          "id": new_id,
          "type": order_type,
          "query": user_query,
          "offer": simulated_offer,
          "status": simulated_status,
          "date": "2026-09-21",
      })

      self.send_response(303)
      self.send_header("Location", "/dashboard")
      self.end_headers()

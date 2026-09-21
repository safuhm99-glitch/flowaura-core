from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse

# تخزين مؤقت للطلبات (سجل العملاء والوسيط الذكي)
ORDERS_DB = [
    {
        "id": 1,
        "type": "منتج",
        "query": "ساعة ذكية بسعر اقتصادي",
        "status": "جارٍ البحث والمساومة...",
        "date": "2026-09-21",
    },
    {
        "id": 2,
        "type": "خدمة",
        "query": "تصميم شعار احترافي للمتجر",
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

      # تصميم لوحة التحكم مع عرض سجل طلبات الوسيط الذكي
      orders_html = ""
      for o in ORDERS_DB:
        orders_html += f"""
                <tr style="border-bottom: 1px solid #eee;">
                    <td style="padding: 12px;">#{o['id']}</td>
                    <td style="padding: 12px;"><b>{o['type']}</b></td>
                    <td style="padding: 12px;">{o['query']}</td>
                    <td style="padding: 12px; color: #2563eb;">{o['status']}</td>
                    <td style="padding: 12px; color: #666;">{o['date']}</td>
                </tr>
                """

      html_content = f"""
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <title>لوحة التحكم - المنظومة الذكية الشاملة (Omni-Flow)</title>
                <style>
                    body {{ font-family: Tahoma, sans-serif; background: #f8fafc; margin: 0; padding: 20px; }}
                    .container {{ max-width: 1000px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
                    h1 {{ color: #1e293b; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                    th {{ background: #f1f5f9; padding: 12px; text-align: right; color: #334155; }}
                    .btn {{ display: inline-block; background: #2563eb; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>لوحة تحكم الوسيط الذكي (Omni-Flow Dashboard)</h1>
                    <p>مرحباً بكِ، صفية. هذه هي سجلات الطلبات وعمليات البحث والمساومة الآلية للعملاء:</p>
                    <table>
                        <thead>
                            <tr>
                                <th>رقم الطلب</th>
                                <th>النوع</th>
                                <th>تفاصيل الطلب</th>
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
      # الصفحة الرئيسية (واجهة المستخدم والمساعد الذكي)
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
                    body { font-family: Tahoma, sans-serif; background: #0f172a; color: white; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
                    .card { background: #1e293b; padding: 40px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); width: 100%; max-width: 600px; text-align: center; }
                    h1 { color: #38bdf8; margin-bottom: 10px; }
                    p { color: #94a3b8; margin-bottom: 30px; }
                    textarea { width: 100%; height: 100px; padding: 12px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; font-size: 16px; resize: none; margin-bottom: 15px; }
                    button { background: #2563eb; color: white; border: none; padding: 12px 25px; border-radius: 8px; font-size: 16px; cursor: pointer; width: 100%; transition: background 0.3s; }
                    button:hover { background: #1d4ed8; }
                    .links { margin-top: 20px; }
                    .links a { color: #38bdf8; text-decoration: none; margin: 0 10px; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>المتظومة الذكية الشاملة (Omni-Flow)</h1>
                    <p>مساعدك التجاري والخدمي الآلي بالكامل. اكتب طلبك ودع الوسيط الذكي يتولى البحث أو المساومة نيابة عنك!</p>
                    
                    <form action="/submit-order" method="POST">
                        <textarea name="query" placeholder="اكتب ما تبحث عنه هنا... (مثال: أريد شراء هاتف بأرخص سعر، أو أحتاج تصميم موقع إلكتروني)"></textarea>
                        <button type="submit">إرسال الطلب للوسيط الذكي 🚀</button>
                    </form>

                    <div class="links">
                        <a href="/dashboard">لوحة التحكم</a>
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

      user_query = params.get("query", ["طلب جديد"])[0]

      # إضافة الطلب الجديد إلى قاعدة البيانات المؤقتة
      new_id = len(ORDERS_DB) + 1
      ORDERS_DB.append({
          "id": new_id,
          "type": "بحث ذكي / خدمة",
          "query": user_query,
          "status": "جاري التحليل والمساومة الآلية...",
          "date": "2026-09-21",
      })

      # إعادة توجيه المستخدم إلى لوحة التحكم لرؤية طلبه مسجلاً
      self.send_response(303)
      self.send_header("Location", "/dashboard")
      self.end_headers()

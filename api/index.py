# handler.py - Flora Aura (وضع التجربة المجانية المؤقتة)

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse

class FloraAuraTestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>فلورا اورا | Flora Aura - تجربة النظام</title>
            <style>
                body { background-color: #0d1117; color: #f0f6fc; font-family: Tahoma, sans-serif; text-align: center; padding: 50px; }
                .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 30px; max-width: 500px; margin: 0 auto; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
                h1 { color: #f78166; }
                p { color: #8b949e; line-height: 1.6; }
                .badge { background: #238636; color: white; padding: 5px 12px; border-radius: 20px; font-size: 14px; display: inline-block; margin-bottom: 15px; }
                .btn { display: inline-block; background: #f78166; color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 20px; transition: 0.3s; }
                .btn:hover { background: #da3633; }
            </style>
        </head>
        <body>
            <div class="card">
                <span class="badge">وضع التجربة المجانية (Test Mode)</span>
                <h1>Flora Aura | فلورا اورا</h1>
                <p>مرحباً بكِ في بيئة الاختبار الخاصة بالنظام. يمكنكِ الآن تجربة تدفق طلب "خدمة الهوية البصرية" مجاناً بالكامل للتأكد من سلاسة العمل وتفاعل الواجهة.</p>
                <a href="https://wa.me/966580414481?text=مرحباً، أود تجربة النظام واختبار طلب خدمة الهوية البصرية مجاناً." class="btn" target="_blank">جرب الخدمة الآن مجاناً</a>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=FloraAuraTestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on http://localhost:{port} in Test Mode...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()

from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            event_data = json.loads(post_data.decode('utf-8'))
            
            # استخراج بيانات الطلب من سلة
            event_type = event_data.get('event', 'unknown')
            data = event_data.get('data', {})
            customer = data.get('customer', {})
            customer_name = customer.get('name', 'عميل جديد')
            customer_mobile = customer.get('mobile', 'غير متوفر')
            order_id = data.get('id', 'N/A')
            total = data.get('total', {}).get('string', '0 SAR')
            
            # إرسال تنبيه آلي إلى تليجرام عند حدوث طلب جديد
            telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
            chat_id = os.environ.get('TELEGRAM_CHAT_ID')
            
            if telegram_token and chat_id:
                message = (
                    f"🚨 طلب جديد عبر FlowAura!\n\n"
                    f"📦 رقم الطلب: {order_id}\n"
                    f"👤 العميل: {customer_name}\n"
                    f"📱 الجوال: {customer_mobile}\n"
                    f"💰 المتبقي/الإجمالي: {total}\n"
                    f"⚙️ الحدث: {event_type}"
                )
                url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
                payload = json.dumps({"chat_id": chat_id, "text": message}).encode('utf-8')
                req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
                try:
                    urllib.request.urlopen(req)
                except Exception as ex:
                    print(f"Telegram Error: {ex}")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_msg = {"status": "success", "message": "FlowAura webhook processed successfully"}
            self.wfile.write(json.dumps(response_msg).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_msg = {"status": "error", "message": str(e)}
            self.wfile.write(json.dumps(error_msg).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html_content = """
        <html>
            <head><title>FlowAura Core System</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 50px; background-color: #0f172a; color: #f8fafc;">
                <h1>🚀 FlowAura Engine is Online!</h1>
                <p>نظام الأتمتة لخدمات (Landing Pages, 3D, Branding) يعمل بكفاءة تامة ومتصل مع سلة وتليجرام.</p>
            </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

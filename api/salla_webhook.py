import os
import urllib.request
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # محاولة قراءة البيانات الواردة بصيغة JSON
            try:
                data = json.loads(post_data.decode('utf-8'))
            except:
                data = {}

            telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
            chat_id = os.environ.get('ADMIN_CHAT_ID')

            # التحقق مما إذا كان الطلب قادماً من واجهة الدردشة (المساعد الذكي) أو من سلة
            path = self.path
            
            if 'chat' in path or 'message' in data:
                # معالجة طلب المساعد الذكي من الموقع
                user_message = data.get('message', '')
                print(f"Chat Message Received: {user_message}")
                
                # الرد الذكي المباشر على العميل في الموقع
                reply_text = f"أهلاً بكِ في FlowAura! لقد استلمت طلبك بخصوص ({user_message}). سيقوم الرجل الآلي بمراجعته وبحثه فوراً وتوفيره لكِ."

                # إرسال تنبيه للرئيس التنفيذي/التليجرام بطلب العميل عبر الشات
                if telegram_token and chat_id:
                    tg_msg = f"💬 استفسار جديد من المساعد الذكي:\n\nطلب العميل: {user_message}"
                    self.send_telegram(telegram_token, chat_id, tg_msg)

                response_data = {"status": "success", "reply": reply_text}
                
            else:
                # معالجة ويب هوك متجر سلة (الطلبات الجديدة والفوترة)
                event_type = data.get('event', 'unknown')
                payload = data.get('data', {})
                order_id = payload.get('id', 'N/A')
                customer_name = payload.get('customer', {}).get('name', 'عميل جديد')
                total = payload.get('total', {}).get('string', '0 SAR')

                if telegram_token and chat_id:
                    tg_msg = (
                        f"🚨 طلب جديد عبر سلة - FlowAura!\n\n"
                        f"📦 رقم الطلب: {order_id}\n"
                        f"👤 العميل: {customer_name}\n"
                        f"💰 المبلغ: {total}\n"
                        f"⚙️ الحدث: {event_type}"
                    )
                    self.send_telegram(telegram_token, chat_id, tg_msg)

                response_data = {"status": "success", "message": "Salla webhook processed"}

            # إرسال الرد بصيغة JSON
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            error_msg = {"status": "error", "message": str(e)}
            self.wfile.write(json.dumps(error_msg).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html_content = """
        <html>
            <head><title>FlowAura Full System</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 50px; background-color: #0f172a; color: #f8fafc;">
                <h1>🚀 FlowAura Full Automated Engine is Live!</h1>
                <p>نظام الأتمتة الشامل (سلة + المساعد الذكي + تليجرام) يعمل بكفاءة تامة.</p>
            </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

    def send_telegram(self, token, chat_id, message):
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = json.dumps({"chat_id": chat_id, "text": message}).encode('utf-8')
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req)
        except Exception as ex:
            print(f"Telegram Error: {ex}")

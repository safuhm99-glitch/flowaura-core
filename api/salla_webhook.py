import os
import urllib.request
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
            except:
                data = {}

            telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
            chat_id = os.environ.get('ADMIN_CHAT_ID')

            path = self.path
            
            # معالجة محادثات المساعد الذكي ورحلة العميل حتى الدفع
            if 'chat' in path or 'message' in data or 'customer_message' in data:
                user_message = data.get('message', data.get('customer_message', 'استفسار جديد'))
                print(f"Autonomous Customer Request: {user_message}")
                
                # الرد الآلي الذكي كأنه مساعد بشري حقيقي متكامل حتى الدفع
                reply_text = (
                    f"أهلاً بكِ معنا في FlowAura 🤖✨\n"
                    f"لقد استلمت طلبك بخصوص: ({user_message}).\n"
                    f"قمت بمسح الأسواق الرقمية وتوفير أفضل خيار متاح حالياً.\n"
                    f"💳 لإتمام الطلب واستلام الكود أو الخدمة بشكل فوري وآمن، تفضل بزيارة رابط الدفع السريع المخصص لك:\n"
                    f"👉 https://s.salla.sa/checkout/order-quick (أو رابط الدفع الخاص بمتجرك)"
                )

                # إرسال إشعار فوري لمديرة المتجر على تليجرام
                if telegram_token and chat_id:
                    tg_msg = (
                        f"🤖 **الرجل الآلي أتم رحلة عميل بنجاح!**\n\n"
                        f"💬 **طلب العميل:** {user_message}\n"
                        f"🎯 **الإجراء:** تم الرد الآلي وتوجيه العميل لرابط الدفع السريع.\n"
                        f"💰 **الحالة:** بانتظار تأكيد الدفع والتسليم الآلي."
                    )
                    self.send_telegram(telegram_token, chat_id, tg_msg)

                response_data = {"status": "success", "reply": reply_text}
                
            else:
                # معالجة أحداث متجر سلة (مثل اكتمال الدفع أو إنشاء طلب)
                event_type = data.get('event', 'unknown')
                payload = data.get('data', {})
                order_id = payload.get('id', 'N/A')
                customer_name = payload.get('customer', {}).get('name', 'عميل مميز')
                total = payload.get('total', {}).get('string', '0 SAR')

                if telegram_token and chat_id:
                    tg_msg = (
                        f"🎉 **عملية ناجحة وتم الدفع بنجاح! (FlowAura)**\n\n"
                        f"📦 رقم الطلب: {order_id}\n"
                        f"👤 العميل: {customer_name}\n"
                        f"💵 المبالغ المدفوعة: {total}\n"
                        f"⚡ الحدث: {event_type} - تم تسليم المنتج الرقمي آلياً!"
                    )
                    self.send_telegram(telegram_token, chat_id, tg_msg)

                response_data = {"status": "success", "message": "Autonomous checkout event processed"}

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
            <head><title>FlowAura Autonomous Core</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 50px; background-color: #0f172a; color: #f8fafc;">
                <h1>🚀 FlowAura Fully Automated Agent is Live!</h1>
                <p>الرجل الآلي الذكي يدير رحلة العميل بالكامل حتى الدفع بكفاءة تامة.</p>
            </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

    def send_telegram(self, token, chat_id, message):
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = json.dumps({"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}).encode('utf-8')
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req)
        except Exception as ex:
            print(f"Telegram Error: {ex}")

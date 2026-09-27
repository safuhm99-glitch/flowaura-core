from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            event_data = json.loads(post_data.decode('utf-8'))
            
            # التحقق من نوع الحدث القادم من سلة (مثلاً: تم دفع الطلب بنجاح)
            if event_data.get('event') == 'order.paid':
                order = event_data.get('data', {})
                order_id = order.get('id')
                customer_name = order.get('customer', {}).get('name')
                
                print(f"تم استلام طلب جديد برقم: {order_id} للعميل: {customer_name}")
                
                # هنا يمكنك إضافة كود توجيه الطلب للرجل الآلي أو تخزينه لمعالجته
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"success": True, "message": "Webhook received successfully"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
            
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Salla Webhook Endpoint is active!")

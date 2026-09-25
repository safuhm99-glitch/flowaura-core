from http.server import BaseHTTPRequestHandler
import json
import urllib.request
from urllib.parse import urlparse, parse_qs

TELEGRAM_BOT_TOKEN = "8900192914:AAGDSW3TEefl4xxPxhshaWjo4k4jbSKmkVU"
TELEGRAM_CHAT_ID = "1998418269"

SERVER_ORDERS = [
    { "id": 3, "date": "2026-09-25", "type": "خدمة رقمية", "details": "اشتراك شاهد", "status": "قيد المراجعة", "phone": "0533319433" },
    { "id": 2, "date": "2026-09-25", "type": "منتج مادي", "details": "حقيبة يد ماركة", "status": "قيد المراجعة", "phone": "0533319433" },
    { "id": 1, "date": "2026-09-25", "type": "منتج مادي", "details": "كفر ايباد", "status": "قيد المراجعة", "phone": "0500000000" }
]

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FlowAura - لوحة تحكم المشرفة</title>
    <style>
        body {
            font-family: Tahoma, Arial, sans-serif;
            background-color: #0b1329;
            color: #ffffff;
            margin: 0;
            padding: 15px;
            direction: rtl;
            text-align: right;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #131b36;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #1e293b;
        }
        .header {
            text-align: center;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 15px;
            margin-bottom: 15px;
        }
        .logo { font-size: 35px; margin-bottom: 5px; }
        h1 { color: #60a5fa; font-size: 20px; margin: 0; }
        p { color: #94a3b8; font-size: 12px; margin: 5px 0 0 0; }
        .btn {
            background: #3b82f6; color: white; border: none; padding: 12px;
            border-radius: 6px; width: 100%; font-size: 15px; font-weight: bold;
            cursor: pointer; margin-top: 5px;
        }
        .btn-success { background: #10b981; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 11px; }
        th, td { padding: 8px; border-bottom: 1px solid #1e293b; text-align: center; }
        th { color: #93c5fd; background: #0f172a; }
        .status-select { background: #0f172a; color: #4ade80; border: 1px solid #3b82f6; padding: 5px; border-radius: 4px; font-size: 11px; }
    </style>
</head>
<body>

<div class="container" id="dash-view">
    <div class="header">
        <div class="logo">📊</div>
        <h1>لوحة تحكم المشرفة (البوت الذكي)</h1>
        <p>إدارة الطلبات الواردة وتحديث حالاتها تلقائياً</p>
    </div>

    <button class="btn btn-success" type="button" style="margin-bottom: 10px;" onclick="loadAdminOrders()">🔄 تحديث القائمة</button>

    <table>
        <thead>
            <tr>
                <th>الرقم والتاريخ</th>
                <th>النوع والتفاصيل</th>
                <th>الجوال</th>
                <th>حالة الطلب</th>
            </tr>
        </thead>
        <tbody id="ordersTableBody"></tbody>
    </table>
</div>

<script>
    async function loadAdminOrders() {
        try {
            const response = await fetch('/?get_orders=true');
            const orders = await response.json();
            const tbody = document.getElementById("ordersTableBody");
            if (!tbody) return;
            tbody.innerHTML = "";
            orders.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><b>#${order.id}</b><br>${order.date}</td>
                    <td><b>${order.type}</b><br>${order.details}</td>
                    <td>${order.phone || 'غير متوفر'}</td>
                    <td>
                        <select class="status-select" onchange="updateOrderStatus(${order.id}, this.value)">
                            <option value="قيد المراجعة" ${order.status === 'قيد المراجعة' ? 'selected' : ''}>قيد المراجعة</option>
                            <option value="جاري البحث وتوفير السعر" ${order.status === 'جاري البحث وتوفير السعر' ? 'selected' : ''}>جاري البحث وتوفير السعر</option>
                            <option value="تم توفير المنتج / بانتظار الدفع" ${order.status === 'تم توفير المنتج / بانتظار الدفع' ? 'selected' : ''}>تم توفير المنتج / بانتظار الدفع</option>
                            <option value="تم التنفيذ بنجاح" ${order.status === 'تم التنفيذ بنجاح' ? 'selected' : ''}>تم التنفيذ بنجاح</option>
                            <option value="ملغي" ${order.status === 'ملغي' ? 'selected' : ''}>ملغي</option>
                        </select>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } catch (e) {
            console.log("خطأ في جلب الطلبات", e);
        }
    }

    async function updateOrderStatus(id, status) {
        await fetch('/?action=update_status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: id, status: status })
        });
    }

    loadAdminOrders();
    setInterval(loadAdminOrders, 10000);
</script>

</body>
</html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if "get_orders=true" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(SERVER_ORDERS, ensure_ascii=False).encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(HTML_CONTENT.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8')) if post_data else {}

            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            action = query_params.get("action", [None])[0]

            if "message" in data:
                message = data["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "").strip()

                # رد البوت المباشر للعميل
                if text.startswith("/start"):
                    reply_text = "✨ أهلاً بك في بوت FlowAura للوساطة والبحث والاستشارات!\n\n💬 أرسل استشارتك أو طلبك وسنقوم بخدمتك فوراً."
                else:
                    reply_text = "✅ تم استلام طلبك واستهداف استشارتك بنجاح! سيتم مراجعتها من قِبل الإدارة والتواصل معك قريباً."
                    
                    # تسجيل الطلب في السيرفر
                    new_id = (max([o.get("id", 0) for o in SERVER_ORDERS]) + 1) if SERVER_ORDERS else 1
                    SERVER_ORDERS.insert(0, {
                        "id": new_id,
                        "date": "2026-09-25",
                        "type": "استشارة / طلب ذكي",
                        "details": text,
                        "phone": f"Telegram ID: {chat_id}",
                        "status": "قيد المراجعة"
                    })

                    # إرسال تنبيه للمشرفة
                    try:
                        alert_msg = f"🚨 طلب جديد عبر البوت!\n\n📌 رقم الطلب: #{new_id}\n💬 التفاصيل: {text}"
                        alert_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                        payload_alert = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": alert_msg}).encode('utf-8')
                        urllib.request.urlopen(urllib.request.Request(alert_url, data=payload_alert, headers={'Content-Type': 'application/json'}))
                    except Exception as ex:
                        print("Admin Alert Error:", ex)

                # إرسال الرد للعميل في محادثته الخاصة
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                payload = json.dumps({"chat_id": chat_id, "text": reply_text}).encode('utf-8')
                urllib.request.urlopen(urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}))

            elif action == "update_status":
                order_id = data.get("id")
                new_status = data.get("status")
                for order in SERVER_ORDERS:
                    if order.get("id") == order_id:
                        order["status"] = new_status
                        break

            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False).encode('utf-8'))

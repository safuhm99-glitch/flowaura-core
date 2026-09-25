from http.server import BaseHTTPRequestHandler
import json
import urllib.request
from urllib.parse import urlparse, parse_qs

TELEGRAM_BOT_TOKEN = "8900192914:AAGDSW3TEefl4xxPxhshaWjo4k4jbSKmkVU"
TELEGRAM_CHAT_ID = "1998418269"

SERVER_ORDERS = [
    { "id": 1, "date": "2026-09-25", "type": "منتج مادي", "details": "كفر ايباد", "status": "قيد المراجعة", "phone": "0500000000" }
]

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FlowAura - متجر الوساطة الذكي</title>
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
        .form-group { margin-bottom: 12px; }
        label { display: block; margin-bottom: 5px; font-size: 13px; color: #94a3b8; }
        select, textarea, input {
            width: 100%; padding: 10px; border-radius: 6px;
            border: 1px solid #1e293b; background: #0f172a; color: white;
            box-sizing: border-box; font-size: 14px;
        }
        .btn {
            background: #3b82f6; color: white; border: none; padding: 12px;
            border-radius: 6px; width: 100%; font-size: 15px; font-weight: bold;
            cursor: pointer; margin-top: 5px;
        }
        .btn-warning { background: #f59e0b; }
        .btn-success { background: #10b981; }
        .btn-dashboard {
            background: #1e293b; color: #60a5fa; border: 2px solid #3b82f6;
            padding: 12px; border-radius: 6px; width: 100%; font-size: 14px;
            font-weight: bold; cursor: pointer; margin-top: 15px;
        }
        .section-box { margin-top: 20px; border-top: 1px solid #1e293b; padding-top: 15px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 11px; }
        th, td { padding: 8px; border-bottom: 1px solid #1e293b; text-align: center; }
        th { color: #93c5fd; background: #0f172a; }
        .status-select { background: #0f172a; color: #4ade80; border: 1px solid #3b82f6; padding: 5px; border-radius: 4px; font-size: 11px; }
        .tracking-result { margin-top: 15px; background: #0f172a; padding: 12px; border-radius: 8px; border: 1px solid #3b82f6; display: none; }
    </style>
</head>
<body>

<div class="container" id="store-view">
    <div class="header">
        <div class="logo">⚡</div>
        <h1>FlowAura</h1>
        <p>متجر الوساطة والبحث الذكي للطلبات</p>
    </div>

    <div>
        <div style="color: #93c5fd; font-weight: bold; margin-bottom: 10px;">📦 أطلب ما تحتاجه (وساطة وبحث)</div>
        <div class="form-group">
            <label>نوع الطلب</label>
            <select id="serviceType" onchange="updatePlaceholder()">
                <option value="منتج مادي">منتج مادي (بحث عن أرخص سعر / توفير)</option>
                <option value="خدمة رقمية">خدمة رقمية / وساطة برمجية</option>
                <option value="استشارة تجارية">استشارة تجارية متخصصة</option>
                <option value="طلب استرجاع">طلب استرجاع 🔄</option>
            </select>
        </div>
        <div class="form-group">
            <label>رقم الجوال (للتواصل وتتبع الطلب)</label>
            <input type="text" id="clientPhone" placeholder="مثال: 05xxxxxxxx">
        </div>
        <div class="form-group">
            <label id="detailsLabel">تفاصيل طلبك (اكتب المواصفات، الماركة، أو الرابط بدقة)</label>
            <textarea id="orderDetails" rows="3" placeholder="مثال: أريد جهاز آيفون 15 برو ماكس لون تيتانيوم بسعر مناسب..."></textarea>
        </div>
        <button class="btn" type="button" onclick="submitData()">🚀 إرسال الطلب وإصدار رقم التتبع</button>
    </div>

    <div class="section-box">
        <div style="color: #fde047; font-weight: bold; margin-bottom: 10px;">🔍 هل لديك طلب سابق؟ تتبع حالته الآن</div>
        <button class="btn btn-warning" type="button" onclick="switchAria('tracking-view')">🔍 تتبع حالة طلبي برقم الطلب</button>
    </div>

    <div class="section-box">
        <button class="btn-dashboard" type="button" onclick="switchAria('admin-login-view')">🔒 دخول المشرفة (لوحة التحكم)</button>
    </div>
</div>

<div class="container" id="admin-login-view" style="display: none;">
    <div class="header">
        <div class="logo">🔒</div>
        <h1>تسجيل دخول المشرفة</h1>
        <p>الرجاء إدخال كلمة المرور الخاصة للوحة</p>
    </div>

    <div class="form-group">
        <label>كلمة المرور (الافتراضية: 1234)</label>
        <input type="password" id="adminPassInput" placeholder="أدخل كلمة المرور">
    </div>
    <button class="btn btn-success" type="button" onclick="verifyAdminPassword()">دخول لوحة التحكم</button>
    <div id="loginError" style="color: #fca5a5; font-size: 12px; text-align: center; margin-top: 10px; display: none;">كلمة المرور غير صحيحة!</div>

    <button class="btn" type="button" style="margin-top: 20px; background: #1e293b; border: 1px solid #3b82f6;" onclick="switchAria('store-view')">← العودة للرئيسية</button>
</div>

<div class="container" id="tracking-view" style="display: none;">
    <div class="header">
        <div class="logo">🔍</div>
        <h1>تتبع الطلب</h1>
        <p>استعلم عن حالة طلبك فوراً</p>
    </div>

    <div class="form-group">
        <label>أدخل رقم الطلب الخاص بك</label>
        <input type="number" id="trackId" placeholder="مثال: 1">
    </div>
    <button class="btn btn-success" type="button" onclick="trackOrder()">بحث عن الطلب</button>

    <div id="trackingResultBox" class="tracking-result"></div>

    <button class="btn" type="button" style="margin-top: 20px; background: #1e293b; border: 1px solid #3b82f6;" onclick="switchAria('store-view')">← العودة للرئيسية</button>
</div>

<div class="container" id="dash-view" style="display: none;">
    <div class="header">
        <div class="logo">📊</div>
        <h1>لوحة تحكم المشرفة</h1>
        <p>إدارة الطلبات وتحديث الحالات</p>
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

    <button class="btn" type="button" style="margin-top: 20px; background: #1e293b; border: 1px solid #3b82f6;" onclick="switchAria('store-view')">← خروج والعودة للرئيسية</button>
</div>

<script>
    function updatePlaceholder() {
        const type = document.getElementById("serviceType").value;
        const detailsInput = document.getElementById("orderDetails");
        const label = document.getElementById("detailsLabel");

        if (type === "استشارة تجارية") {
            label.innerText = "تفاصيل الاستشارة التجارية (اطرح سؤالك أو موضوع الاستشارة بدقة):";
            detailsInput.placeholder = "مثال: أود استشارة بخصوص تسعير منتج رقمي وكيفية استخراج السجل التجاري...";
        } else if (type === "خدمة رقمية") {
            label.innerText = "تفاصيل الخدمة الرقمية أو الوساطة البرمجية:";
            detailsInput.placeholder = "مثال: أريد ربط بوابة دفع أو تعديل سكربت برمجي...";
        } else if (type === "طلب استرجاع") {
            label.innerText = "تفاصيل طلب الاسترجاع (رقم الطلب وسبب الاسترجاع):";
            detailsInput.placeholder = "مثال: رقم الطلب #5 - السبب: المنتج وصل متضرر...";
        } else {
            label.innerText = "تفاصيل طلبك (اكتب المواصفات، الماركة، أو الرابط بدقة):";
            detailsInput.placeholder = "مثال: أريد جهاز آيفون 15 برو ماكس لون تيتانيوم بسعر مناسب...";
        }
    }

    function switchAria(viewId) {
        document.getElementById('store-view').style.display = 'none';
        document.getElementById('tracking-view').style.display = 'none';
        document.getElementById('dash-view').style.display = 'none';
        document.getElementById('admin-login-view').style.display = 'none';
        document.getElementById(viewId).style.display = 'block';
        document.getElementById('loginError').style.display = 'none';
        const passInput = document.getElementById('adminPassInput');
        if(passInput) passInput.value = '';
    }

    function verifyAdminPassword() {
        let pass = document.getElementById('adminPassInput').value;
        if (pass === "1234") {
            switchAria('dash-view');
            loadAdminOrders();
        } else {
            document.getElementById('loginError').style.display = 'block';
        }
    }

    async function submitData() {
        const type = document.getElementById("serviceType").value;
        const details = document.getElementById("orderDetails").value;
        const phone = document.getElementById("clientPhone").value;
        const today = new Date().toISOString().split('T')[0];

        if (!details.trim() || !phone.trim()) { 
            alert("الرجاء إدخال رقم الجوال وتفاصيل الطلب بدقة"); 
            return; 
        }

        try {
            const res = await fetch('/?action=new_order', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: type, details: details, phone: phone, date: today })
            });
            const data = await res.json();
            if(data.status === "success") {
                alert("✅ تم إرسال طلبك بنجاح!\nرقم طلبك الخاص هو: " + data.new_id + "\nاحتفظ به لتتبع حالة طلبك.");
                document.getElementById("orderDetails").value = "";
                document.getElementById("clientPhone").value = "";
            } else {
                alert("حدث خطأ أثناء الإرسال");
            }
        } catch (e) {
            alert("حدث خطأ في الاتصال بالسيرفر");
        }
    }

    async function trackOrder() {
        const orderId = document.getElementById("trackId").value;
        const resultBox = document.getElementById("trackingResultBox");
        if(!orderId) { alert("أدخل رقم الطلب أولاً"); return; }

        try {
            const response = await fetch('/?get_orders=true');
            const orders = await response.json();
            const found = orders.find(o => o.id == orderId);

            resultBox.style.display = "block";
            if(found) {
                resultBox.innerHTML = `
                    <div style="color: #93c5fd; font-weight: bold; margin-bottom: 5px;">📦 تفاصيل طلبك رقم (#${found.id})</div>
                    <div style="font-size: 13px; margin: 4px 0;"><b>النوع:</b> ${found.type}</div>
                    <div style="font-size: 13px; margin: 4px 0;"><b>التفاصيل:</b> ${found.details}</div>
                    <div style="font-size: 13px; margin: 4px 0;"><b>تاريخ الطلب:</b> ${found.date}</div>
                    <div style="font-size: 14px; margin-top: 8px; color: #4ade80;"><b>الحالة الحالية:</b> ${found.status}</div>
                `;
            } else {
                resultBox.innerHTML = `<span style="color: #fca5a5;">عذراً، لم يتم العثور على طلب بهذا الرقم. تأكد من الرقم وصحته.</span>`;
            }
        } catch(e) {
            resultBox.style.display = "block";
            resultBox.innerHTML = "حدث خطأ في الاتصال بالسيرفر.";
        }
    }

    async function loadAdminOrders() {
        try {
            const response = await fetch('/?get_orders=true');
            const orders = await response.json();
            const tbody = document.getElementById("ordersTableBody");
            tbody.innerHTML = "";
            orders.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><b>#${order.id}</b><br>${order.date}</td>
                    <td><b>${order.type}</b><br>${order.details}</td>
                    <td>${order.phone || 'غير متوفر'}</td>
                    <td>
                        <select class="status-select" onchange="updateStatus(${order.id}, this.value)">
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

    async function updateStatus(orderId, newStatus) {
        try {
            await fetch('/?action=update_status', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: orderId, status: newStatus })
            });
        } catch (e) {
            console.log("خطأ في تحديث الحالة", e);
        }
    }
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
            if not action:
                action = data.get("action")

            if "message" in data:
                chat_id = data["message"]["chat"]["id"]
                reply_text = "✨ أهلاً بك في متجر FlowAura للوساطة والبحث الذكي!\n\nاضغط على الزر بالأسفل لفتح المتجر وتقديم طلبك أو تتبعه:"
                
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "🛒 افتح متجر وساطة الطلبات", "web_app": {"url": "https://smartpulseai.net"}}]
                    ]
                }
                payload = json.dumps({"chat_id": chat_id, "text": reply_text, "reply_markup": keyboard}).encode('utf-8')
                urllib.request.urlopen(urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}))

            elif action == "update_status":
                order_id = data.get("id")
                new_status = data.get("status")
                for order in SERVER_ORDERS:
                    if order.get("id") == order_id:
                        order["status"] = new_status
                        break

            elif action == "new_order":
                service_type = data.get('type')
                details = data.get('details')
                phone = data.get('phone', 'غير متوفر')
                order_date = data.get('date', '2026-09-25')

                new_id = (max([o.get("id", 0) for o in SERVER_ORDERS]) + 1) if SERVER_ORDERS else 1

                SERVER_ORDERS.insert(0, {
                    "id": new_id,
                    "date": order_date,
                    "type": service_type,
                    "details": details,
                    "phone": phone,
                    "status": "قيد المراجعة"
                })

                try:
                    msg = f"🚨 طلب وساطة جديد عبر FlowAura!\n\n📌 رقم الطلب: #{new_id}\n📱 الجوال: {phone}\n🏷️ النوع: {service_type}\n📝 التفاصيل: {details}"
                    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                    payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": msg}).encode('utf-8')
                    urllib.request.urlopen(urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}))
                except Exception as ex:
                    print("Telegram Error:", ex)

                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "new_id": new_id}, ensure_ascii=False).encode('utf-8'))
                return

            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False).encode('utf-8'))

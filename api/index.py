from http.server import BaseHTTPRequestHandler
import json
import urllib.request

TELEGRAM_BOT_TOKEN = "8900192914:AAGDSW3TEefl4xxPxhshaWjo4k4jbSKmkVU"
TELEGRAM_CHAT_ID = "1998418269"
CHANNEL_USERNAME = "@A_ToolsX"

# قائمة مركزية لحفظ الطلبات على السيرفر لضمان مزامنتها مع البوت
SERVER_ORDERS = [
    { "date": "2026-09-25", "type": "منتج مادي", "details": "كفر ايباد", "status": "قيد المراجعة" },
    { "date": "2026-09-25", "type": "طلب استرجاع 🔄", "details": "رقم الطلب: حقيبه - السبب: بسبب تأكل", "status": "قيد المراجعة" }
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
        .btn-danger { background: #ef4444; }
        .btn-dashboard {
            background: #1e293b; color: #60a5fa; border: 2px solid #3b82f6;
            padding: 14px; border-radius: 6px; width: 100%; font-size: 15px;
            font-weight: bold; cursor: pointer; margin-top: 20px;
        }
        .section-box { margin-top: 20px; border-top: 1px solid #1e293b; padding-top: 15px; }
        .toast-msg { margin-top: 10px; padding: 10px; border-radius: 6px; font-size: 13px; text-align: center; display: none; }
        .toast-success { background: rgba(74, 222, 128, 0.15); color: #4ade80; border: 1px solid #4ade80; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 12px; }
        th, td { padding: 10px; border-bottom: 1px solid #1e293b; text-align: center; }
        th { color: #93c5fd; background: #0f172a; }
    </style>
</head>
<body>

<div class="container" id="store-view">
    <div class="header">
        <div class="logo">⚡</div>
        <h1>FlowAura</h1>
        <p>المساعد الذكي للوساطة والتجارة</p>
    </div>

    <!-- قسم الطلبات -->
    <div>
        <div style="color: #93c5fd; font-weight: bold; margin-bottom: 10px;">📦 أرسل طلبك الجديد</div>
        <div class="form-group">
            <label>نوع الخدمة / المنتج</label>
            <select id="serviceType" onchange="toggleSections()">
                <option value="منتج مادي">منتج مادي (بحث عن أرخص سعر)</option>
                <option value="خدمة رقمية">خدمة رقمية / وساطة برمجية</option>
                <option value="استشارة تجارية">استشارة تجارية متخصصة</option>
            </select>
        </div>
        <div class="form-group">
            <label>تفاصيل الطلب</label>
            <textarea id="orderDetails" rows="3" placeholder="اكتب تفاصيل طلبك هنا..."></textarea>
        </div>
        <button class="btn" onclick="submitData('order')">🚀 إرسال الطلب وإضافته للوحة التحكم</button>
        <div id="order-toast" class="toast-msg toast-success">تم إرسال طلبك وتنبيه البوت بنجاح!</div>
    </div>

    <!-- قسم الاسترجاع -->
    <div class="section-box" id="return-section">
        <div style="color: #fca5a5; font-weight: bold; margin-bottom: 10px;">🔄 قسم طلبات الاسترجاع</div>
        <div class="form-group">
            <label>رقم الطلب المراد استرجاعه</label>
            <input type="text" id="returnId" placeholder="مثال: 1">
        </div>
        <div class="form-group">
            <label>سبب الاسترجاع</label>
            <textarea id="returnReason" rows="2" placeholder="اكتب السبب بالتفصيل..."></textarea>
        </div>
        <button class="btn btn-danger" onclick="submitData('return')">⚠️ تقديم طلب الاسترجاع</button>
        <div id="return-toast" class="toast-msg toast-success">تم تقديم طلب الاسترجاع وإرساله للبوت بنجاح.</div>
    </div>

    <!-- قسم الدعم الفني -->
    <div class="section-box" id="support-section" style="display: none;">
        <div style="color: #fde047; font-weight: bold; margin-bottom: 10px;">🛠️ قسم الدعم الفني والتعديلات</div>
        <div class="form-group">
            <label>رقم الخدمة / المشروع</label>
            <input type="text" id="supportId" placeholder="مثال: 102">
        </div>
        <div class="form-group">
            <label>تفاصيل التعديل أو الدعم المطلوبة</label>
            <textarea id="supportReason" rows="2" placeholder="اكتب التعديلات..."></textarea>
        </div>
        <button class="btn btn-warning" onclick="submitData('support')">🔧 إرسال طلب الدعم والتعديل</button>
        <div id="support-toast" class="toast-msg toast-success">تم إرسال طلب الدعم بنجاح.</div>
    </div>

    <div>
        <button class="btn-dashboard" onclick="switchToDashboard()">📊 الانتقال إلى لوحة التحكم وسجل الطلبات</button>
    </div>
</div>

<!-- لوحة التحكم -->
<div class="container" id="dash-view" style="display: none;">
    <div class="header">
        <div class="logo">📊</div>
        <h1>لوحة التحكم</h1>
        <p>سجل الطلبات والعمليات الفورية</p>
    </div>

    <button class="btn" style="background: #10b981; margin-bottom: 10px;" onclick="loadOrders()">🔄 تحديث وجلب القائمة من السيرفر</button>

    <table>
        <thead>
            <tr>
                <th>التاريخ</th>
                <th>نوع الطلب</th>
                <th>التفاصيل</th>
                <th>الحالة</th>
            </tr>
        </thead>
        <tbody id="ordersTableBody"></tbody>
    </table>

    <button class="btn" style="margin-top: 20px; background: #1e293b; border: 1px solid #3b82f6;" onclick="document.getElementById('dash-view').style.display='none'; document.getElementById('store-view').style.display='block';">← العودة للمتجر</button>
</div>

<script>
    async function loadOrders() {
        try {
            const response = await fetch('/?get_orders=true');
            const orders = await response.json();
            const tbody = document.getElementById("ordersTableBody");
            tbody.innerHTML = "";
            orders.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${order.date}</td><td>${order.type}</td><td>${order.details}</td><td><span style="color: #4ade80; font-weight: bold;">${order.status}</span></td>`;
                tbody.appendChild(row);
            });
        } catch (e) {
            console.log("خطأ في جلب الطلبات", e);
        }
    }

    function switchToDashboard() {
        loadOrders();
        document.getElementById('store-view').style.display = 'none';
        document.getElementById('dash-view').style.display = 'block';
    }

    function toggleSections() {
        var serviceType = document.getElementById("serviceType").value;
        var returnSection = document.getElementById("return-section");
        var supportSection = document.getElementById("support-section");
        if (serviceType === "منتج مادي") {
            returnSection.style.display = "block";
            supportSection.style.display = "none";
        } else {
            returnSection.style.display = "none";
            supportSection.style.display = "block";
        }
    }

    function showToast(toastId) {
        var toast = document.getElementById(toastId);
        toast.style.display = "block";
        setTimeout(() => toast.style.display = "none", 4000);
    }

    async function submitData(actionType) {
        let type = "", details = "", toastId = "";
        const today = new Date().toISOString().split('T')[0];

        if (actionType === 'order') {
            type = document.getElementById("serviceType").value;
            details = document.getElementById("orderDetails").value;
            toastId = 'order-toast';
            if (!details.trim()) { alert("الرجاء كتابة تفاصيل الطلب"); return; }
            document.getElementById("orderDetails").value = "";
        } else if (actionType === 'return') {
            const rId = document.getElementById("returnId").value;
            const rReason = document.getElementById("returnReason").value;
            if (!rId.trim() || !rReason.trim()) { alert("الرجاء إدخال رقم الطلب والسبب"); return; }
            type = "طلب استرجاع 🔄";
            details = `رقم الطلب: ${rId} - السبب: ${rReason}`;
            toastId = 'return-toast';
            document.getElementById("returnId").value = "";
            document.getElementById("returnReason").value = "";
        } else if (actionType === 'support') {
            const sId = document.getElementById("supportId").value;
            const sReason = document.getElementById("supportReason").value;
            if (!sId.trim() || !sReason.trim()) { alert("الرجاء إدخال رقم المشروع والتفاصيل"); return; }
            type = "دعم وتعديل 🛠️";
            details = `رقم المشروع: ${sId} - التفاصيل: ${sReason}`;
            toastId = 'support-toast';
            document.getElementById("supportId").value = "";
            document.getElementById("supportReason").value = "";
        }

        showToast(toastId);

        try {
            await fetch('/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: type, details: details, date: today })
            });
            loadOrders();
        } catch (e) {
            console.log(e);
        }
    }
</script>

</body>
</html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # التحقق مما إذا كان الطلب يطلب جلب بيانات القائمة
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

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))

            if "message" in data:
                chat_id = data["message"]["chat"]["id"]
                user_id = data["message"]["from"]["id"]
                
                check_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatMember?chat_id={CHANNEL_USERNAME}&user_id={user_id}"
                is_member = True
                try:
                    with urllib.request.urlopen(urllib.request.Request(check_url)) as response:
                        res_data = json.loads(response.read().decode('utf-8'))
                        if res_data.get("result", {}).get("status") not in ["creator", "administrator", "member"]:
                            is_member = False
                except:
                    pass

                if not is_member:
                    reply_text = f"🚨 للأسف لا يمكنك استخدام البوت، يجب عليك أولاً الاشتراك في قناتنا:\nhttps://t.me/A_ToolsX"
                else:
                    reply_text = f"✨ مرحباً بك يا صفية في بوت FlowAura Store\n\nأنا مساعدك الذكي لاستقبال الطلبات وإدارتها."
                    
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "🌐 زيارة لوحة التحكم والطلب", "web_app": {"url": "https://smartpulseai.net"}}]
                    ]
                }
                payload = json.dumps({"chat_id": chat_id, "text": reply_text, "reply_markup": keyboard}).encode('utf-8')
                urllib.request.urlopen(urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}))

            elif "type" in data and "details" in data:
                service_type = data.get('type')
                details = data.get('details')
                order_date = data.get('date', '2026-09-25')

                # إضافة الطلب الجديد إلى قائمة السيرفر المركزية مباشرة
                SERVER_ORDERS.insert(0, {
                    "date": order_date,
                    "type": service_type,
                    "details": details,
                    "status": "قيد المراجعة"
                })

                if TELEGRAM_BOT_TOKEN != "YOUR_BOT_TOKEN":
                    msg = f"🚨 تنبيه جديد عبر FlowAura!\n\n📌 النوع: {service_type}\n📝 التفاصيل: {details}"
                    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                    payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": msg}).encode('utf-8')
                    urllib.request.urlopen(urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}))

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
        except Exception as e:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "error": str(e)}).encode('utf-8'))

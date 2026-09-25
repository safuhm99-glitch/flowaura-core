from http.server import BaseHTTPRequestHandler
import json
import urllib.request
from urllib.parse import urlparse, parse_qs

TELEGRAM_BOT_TOKEN = "8900192914:AAGDSW3TEefl4xxPxhshaWjo4k4jbSKmkVU"
TELEGRAM_CHAT_ID = "1998418269"

SERVER_ORDERS = [
    { "id": 3, "date": "2026-09-25", "type": "خدمة رقمية", "details": "اشتراك شاهد VIP لمدة شهر", "status": "قيد المراجعة", "phone": "0533319433" },
    { "id": 2, "date": "2026-09-25", "type": "منتج مادي", "details": "حقيبة يد ماركة", "status": "قيد المراجعة", "phone": "0533319433" },
    { "id": 1, "date": "2026-09-25", "type": "منتج مادي", "details": "كفر ايباد", "status": "قيد المراجعة", "phone": "0500000000" }
]

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FlowAura - متجر الوساطة والخدمات الرقمية الذكي</title>
    <style>
        :root {
            --bg-color: #0b1329;
            --container-bg: #131b36;
            --text-color: #ffffff;
            --muted-color: #94a3b8;
            --accent-color: #3b82f6;
            --border-color: #1e293b;
            --input-bg: #0f172a;
        }
        [data-theme="light"] {
            --bg-color: #f1f5f9;
            --container-bg: #ffffff;
            --text-color: #0f172a;
            --muted-color: #64748b;
            --accent-color: #2563eb;
            --border-color: #e2e8f0;
            --input-bg: #f8fafc;
        }
        body {
            font-family: Tahoma, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 15px;
            direction: rtl;
            text-align: right;
            transition: background 0.3s, color 0.3s;
        }
        .container {
            max-width: 650px;
            margin: 0 auto;
            background: var(--container-bg);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 15px;
            margin-bottom: 15px;
            position: relative;
        }
        .logo { font-size: 35px; margin-bottom: 5px; }
        h1 { color: var(--accent-color); font-size: 20px; margin: 0; }
        p { color: var(--muted-color); font-size: 12px; margin: 5px 0 0 0; }
        
        /* Theme Toggle Button */
        .theme-btn {
            position: absolute;
            top: 0;
            left: 0;
            background: var(--border-color);
            color: var(--text-color);
            border: none;
            padding: 6px 10px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
        }

        /* Tabs Navigation */
        .tabs {
            display: flex;
            gap: 5px;
            margin-bottom: 15px;
            background: var(--input-bg);
            padding: 5px;
            border-radius: 8px;
            overflow-x: auto;
        }
        .tab-btn {
            flex: 1;
            background: none;
            border: none;
            color: var(--muted-color);
            padding: 8px;
            font-size: 11px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 6px;
            white-space: nowrap;
            transition: 0.2s;
        }
        .tab-btn.active {
            background: var(--accent-color);
            color: white;
        }

        .tab-content { display: none; }
        .tab-content.active { display: block; }

        .form-group { margin-bottom: 12px; }
        label { display: block; margin-bottom: 5px; font-size: 13px; color: var(--muted-color); }
        select, textarea, input {
            width: 100%; padding: 10px; border-radius: 6px;
            border: 1px solid var(--border-color); background: var(--input-bg); color: var(--text-color);
            box-sizing: border-box; font-size: 14px;
        }
        .btn {
            background: var(--accent-color); color: white; border: none; padding: 12px;
            border-radius: 6px; width: 100%; font-size: 15px; font-weight: bold;
            cursor: pointer; margin-top: 5px;
        }
        .btn-warning { background: #f59e0b; color: white; }
        .btn-success { background: #10b981; color: white; }
        
        /* AI Concierge Chat Box */
        .chat-box {
            background: var(--input-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px;
            height: 150px;
            overflow-y: auto;
            margin-bottom: 10px;
            font-size: 13px;
        }
        .chat-msg { margin-bottom: 8px; padding: 6px 10px; border-radius: 6px; width: fit-content; max-width: 85%; }
        .chat-msg.bot { background: var(--border-color); color: var(--text-color); }
        .chat-msg.user { background: var(--accent-color); color: white; margin-left: auto; }

        /* Calculator */
        .calc-box {
            background: var(--input-bg);
            padding: 12px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            margin-top: 10px;
        }

        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 11px; }
        th, td { padding: 8px; border-bottom: 1px solid var(--border-color); text-align: center; }
        th { color: var(--accent-color); background: var(--input-bg); }
        .status-select { background: var(--input-bg); color: #4ade80; border: 1px solid var(--accent-color); padding: 5px; border-radius: 4px; font-size: 11px; }
        .tracking-result { margin-top: 15px; background: var(--input-bg); padding: 12px; border-radius: 8px; border: 1px solid var(--accent-color); display: none; }
    </style>
</head>
<body data-theme="dark">

<div class="container">
    <div class="header">
        <button class="theme-btn" onclick="toggleTheme()">💡 تغيير الوضع</button>
        <div class="logo">⚡</div>
        <h1>FlowAura</h1>
        <p>متجر الوساطة والخدمات الرقمية الذكي</p>
    </div>

    <!-- تبيويبات التنقل (Tabs) -->
    <div class="tabs">
        <button class="tab-btn active" onclick="switchTab(event, 'tab-order')">📦 طلب جديد</button>
        <button class="tab-btn" onclick="switchTab(event, 'tab-ai')">🤖 المساعد الذكي</button>
        <button class="tab-btn" onclick="switchTab(event, 'tab-track')">🔍 تتبع طلب</button>
        <button class="tab-btn" onclick="switchTab(event, 'tab-calc')">💰 حاسبة التوفير</button>
        <button class="tab-btn" onclick="switchTab(event, 'tab-admin')">🔒 الإدارة</button>
    </div>

    <!-- 1. قسم طلب جديد و نظام الاستلام الآمن (Escrow) -->
    <div id="tab-order" class="tab-content active">
        <div style="color: var(--accent-color); font-weight: bold; margin-bottom: 10px;">📦 أطلب ما تحتاجه (وساطة وبحث وخدمات)</div>
        <div class="form-group">
            <label>نوع الطلب</label>
            <select id="serviceType" onchange="updateLabel()">
                <option value="منتج مادي">منتج مادي (بحث عن أرخص سعر / توفير)</option>
                <option value="خدمة رقمية">خدمة رقمية / اشتراكات وبرمجة</option>
                <option value="استشارة تجارية">استشارة تجارية متخصصة</option>
                <option value="طلب استرجاع">طلب استرجاع 🔄</option>
            </select>
        </div>
        <div class="form-group">
            <label>رقم الجوال (للتواصل وتتبع الطلب)</label>
            <input type="text" id="clientPhone" placeholder="مثال: 05xxxxxxxx">
        </div>
        <div class="form-group">
            <label id="detailsLabel">تفاصيل طلبك (اكتب المواصفات بدقة)</label>
            <textarea id="orderDetails" rows="3" placeholder="اكتب تفاصيل طلبك بدقة..."></textarea>
        </div>
        <div style="font-size: 11px; color: var(--muted-color); margin-bottom: 10px; background: var(--input-bg); padding: 8px; border-radius: 6px;">
            🛡️ <b>نظام الاستلام الآمن (Escrow):</b> أموالك محفوظة لدينا ولا تُتحول للمزود إلا بعد استلام طلبك ومطابقته للمواصفات تماماً.
        </div>
        <button class="btn" type="button" onclick="submitOrder()">🚀 إرسال الطلب وإصدار رقم التتبع</button>
    </div>

    <!-- 2. قسم المساعد الذكي (AI Concierge) -->
    <div id="tab-ai" class="tab-content">
        <div style="color: var(--accent-color); font-weight: bold; margin-bottom: 10px;">🤖 المساعد الذكي الفوري</div>
        <div class="chat-box" id="chatBox">
            <div class="chat-msg bot">مرحباً بك! أنا مساعد FlowAura الذكي. اسألني عن أي خدمة رقمية، منتج تبحث عن سعره، أو استشارة وسأرشدك فوراً.</div>
        </div>
        <div style="display: flex; gap: 5px;">
            <input type="text" id="chatInput" placeholder="اكتب سؤالك هنا..." onkeypress="if(event.key === 'Enter') sendAIChat()">
            <button class="btn" style="margin-top:0; width: 80px;" onclick="sendAIChat()">إرسال</button>
        </div>
    </div>

    <!-- 3. قسم تتبع الطلبات -->
    <div id="tab-track" class="tab-content">
        <div style="color: #fde047; font-weight: bold; margin-bottom: 10px;">🔍 تتبع حالة طلبك برقم الطلب</div>
        <div class="form-group">
            <label>أدخل رقم الطلب الخاص بك</label>
            <input type="number" id="trackId" placeholder="مثال: 1">
        </div>
        <button class="btn btn-warning" type="button" onclick="searchOrder()">بحث عن الطلب</button>
        <div id="trackingResultBox" class="tracking-result"></div>
    </div>

    <!-- 4. قسم حاسبة التوفير الذكية -->
    <div id="tab-calc" class="tab-content">
        <div style="color: var(--accent-color); font-weight: bold; margin-bottom: 10px;">📊 حاسبة التوفير الذكية</div>
        <p>احسب كم يمكنك أن توفر سنوياً معنا في مشترياتك وخدماتك الرقمية والوساطة:</p>
        <div class="form-group">
            <label>متوسط مشترياتك الشهرية المتوقعة (بالريال)</label>
            <input type="number" id="monthlySpend" placeholder="مثال: 2000" oninput="calculateSavings()">
        </div>
        <div class="calc-box">
            <div style="font-size: 13px; margin-bottom: 5px;">💵 نسبة التوفير التقريبية المتوقعة (15%):</div>
            <div id="savingsResult" style="font-size: 18px; font-weight: bold; color: #4ade80;">0 ريال سنوياً</div>
        </div>
    </div>

    <!-- 5. قسم لوحة تحكم المشرفة -->
    <div id="tab-admin" class="tab-content">
        <div id="admin-login-area">
            <div style="color: var(--accent-color); font-weight: bold; margin-bottom: 10px;">🔒 دخول المشرفة للوحة التحكم</div>
            <div class="form-group">
                <label>كلمة المرور (الافتراضية: 1234)</label>
                <input type="password" id="adminPassInput" placeholder="أدخل كلمة المرور">
            </div>
            <button class="btn btn-success" type="button" onclick="verifyAdmin()">دخول</button>
            <div id="loginError" style="color: #fca5a5; font-size: 12px; text-align: center; margin-top: 10px; display: none;">كلمة المرور غير صحيحة!</div>
        </div>

        <div id="admin-dash-area" style="display: none;">
            <div style="color: var(--accent-color); font-weight: bold; margin-bottom: 10px;">📊 إدارة الطلبات</div>
            <button class="btn btn-success" type="button" style="margin-bottom: 10px;" onclick="loadAdminOrders()">🔄 تحديث القائمة</button>
            <table>
                <thead>
                    <tr>
                        <th>الرقم والتاريخ</th>
                        <th>النوع والتفاصيل</th>
                        <th>الجوال</th>
                        <th>الحالة</th>
                    </tr>
                </thead>
                <tbody id="ordersTableBody"></tbody>
            </table>
        </div>
    </div>

</div>

<script>
    function toggleTheme() {
        const body = document.body;
        if (body.getAttribute('data-theme') === 'dark') {
            body.setAttribute('data-theme', 'light');
        } else {
            body.setAttribute('data-theme', 'dark');
        }
    }

    function switchTab(evt, tabId) {
        const contents = document.querySelectorAll('.tab-content');
        contents.forEach(c => c.classList.remove('active'));
        const btns = document.querySelectorAll('.tab-btn');
        btns.forEach(b => b.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        evt.currentTarget.classList.add('active');
    }

    function updateLabel() {
        const type = document.getElementById("serviceType").value;
        const detailsInput = document.getElementById("orderDetails");
        const label = document.getElementById("detailsLabel");

        if (type === "استشارة تجارية") {
            label.innerText = "تفاصيل الاستشارة التجارية:";
            detailsInput.placeholder = "مثال: أريد استشارة بخصوص فتح متجر إلكتروني...";
        } else if (type === "خدمة رقمية") {
            label.innerText = "تفاصيل الخدمة الرقمية:";
            detailsInput.placeholder = "مثال: أريد اشتراك شاهد VIP، أو تصميم وبرمجة موقع...";
        } else {
            label.innerText = "تفاصيل طلبك (المواصفات، المقاس، الرابط بدقة):";
            detailsInput.placeholder = "مثال: أريد فستان سهرة أو بحث عن أرخص سعر لمنتج معين...";
        }
    }

    function sendAIChat() {
        const input = document.getElementById('chatInput');
        const chatBox = document.getElementById('chatBox');
        const text = input.value.trim();
        if(!text) return;

        chatBox.innerHTML += `<div class="chat-msg user">${text}</div>`;
        input.value = '';

        setTimeout(() => {
            let reply = "أهلاً بك! بناءً على طلبك، أنصحك بتقديم طلب عبر تبويب (طلب جديد) وسنقوم بتوفير أرخص سعر أو الخدمة المطلوبة فوراً وبضمان الاستلام الآمن.";
            if(text.includes("اشتراك") || text.includes("شاهد")) {
                reply = "يتوفر لدينا توفير الاشتراكات الرقمية بضمان كامل ومراسلة عبر تليجرام، يمكنك طلبها مباشرة من تبويب 'طلب جديد'.";
            } else if(text.includes("سعر") || text.includes("بحث")) {
                reply = "نحن نمتلك فريق بحث احترافي لمقارنة الأسعار وإيجاد أرخص سعر لمشترياتك المادية بدقة!";
            }
            chatBox.innerHTML += `<div class="chat-msg bot">${reply}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 500);
    }

    function calculateSavings() {
        const spend = parseFloat(document.getElementById('monthlySpend').value) || 0;
        const annual = spend * 12 * 0.15;
        document.getElementById('savingsResult').innerText = annual.toLocaleString() + " ريال سنوياً";
    }

    function verifyAdmin() {
        let pass = document.getElementById('adminPassInput').value;
        if (pass === "1234") {
            document.getElementById('admin-login-area').style.display = 'none';
            document.getElementById('admin-dash-area').style.display = 'block';
            loadAdminOrders();
        } else {
            document.getElementById('loginError').style.display = 'block';
        }
    }

    async function submitOrder() {
        const type = document.getElementById("serviceType").value;
        const details = document.getElementById("orderDetails").value;
        const phone = document.getElementById("clientPhone").value;
        const today = new Date().toISOString().split('T')[0];

        if (!details.trim() || !phone.trim()) {
            alert("الرجاء إدخال رقم الجوال وتفاصيل الطلب");
            return;
        }

        try {
            const res = await fetch('/?action=new_order', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: type, details: details, phone: phone, date: today })
            });
            const data = await res.json();
            if (data.status === "success") {
                alert("✅ تم إرسال طلبك بنجاح! رقم طلبك هو: " + data.new_id);
                document.getElementById("orderDetails").value = "";
                document.getElementById("clientPhone").value = "";
            } else {
                alert("حدث خطأ أثناء الإرسال");
            }
        } catch (e) {
            alert("حدث خطأ في الاتصال");
        }
    }

    async function searchOrder() {
        const orderId = document.getElementById("trackId").value;
        const resultBox = document.getElementById("trackingResultBox");
        if (!orderId) { alert("أدخل رقم الطلب أولاً"); return; }

        try {
            const response = await fetch('/?get_orders=true');
            const orders = await response.json();
            const found = orders.find(o => o.id == orderId);

            resultBox.style.display = "block";
            if (found) {
                resultBox.innerHTML = `
                    <div style="color: var(--accent-color); font-weight: bold; margin-bottom: 5px;">📦 تفاصيل طلبك رقم (#${found.id})</div>
                    <div style="font-size: 13px; margin: 4px 0;"><b>النوع:</b> ${found.type}</div>
                    <div style="font-size: 13px; margin: 4px 0;"><b>التفاصيل:</b> ${found.details}</div>
                    <div style="font-size: 13px; margin: 4px 0;"><b>الحالة:</b> ${found.status}</div>
                `;
            } else {
                resultBox.innerHTML = `<span style="color: #fca5a5;">عذراً، لم يتم العثور على طلب بهذا الرقم.</span>`;
            }
        } catch (e) {
            resultBox.style.display = "block";
            resultBox.innerHTML = "حدث خطأ في الاتصال.";
        }
    }

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

    async function updateOrderStatus(orderId, newStatus) {
        await fetch('/?action=update_status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: parseInt(orderId), status: newStatus })
        });
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

            if "message" in data:
                message = data["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "").strip()

                if text.startswith("/start"):
                    reply_text = "✨ أهلاً بك في متجر FlowAura للوساطة والخدمات الرقمية!\n\n🤖 أنا مساعدك الذكي، يمكنني استقبال طلباتك، خدماتك الرقمية، استشاراتك، أو مساعدتك في تتبع طلباتك فوراً."
                else:
                    new_id = (max([o.get("id", 0) for o in SERVER_ORDERS]) + 1) if SERVER_ORDERS else 1
                    SERVER_ORDERS.insert(0, {
                        "id": new_id,
                        "date": "2026-09-25",
                        "type": "طلب عبر تيليجرام (تلقائي)",
                        "details": text,
                        "phone": f"Telegram ID: {chat_id}",
                        "status": "قيد المراجعة"
                    })
                    reply_text = f"🤖✅ تم استلام طلبك وعمليات البحث الخاصة به بنجاح!\n\n📌 رقم طلبك: #{new_id}"

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
                    msg = f"🚨 طلب جديد عبر الموقع!\n\n📌 رقم الطلب: #{new_id}\n📱 الجوال: {phone}\n🏷️ النوع: {service_type}\n📝 التفاصيل: {details}"
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

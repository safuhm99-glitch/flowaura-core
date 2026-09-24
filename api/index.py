from http.server import BaseHTTPRequestHandler
import json

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ar" dir="rtl" id="html-root">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FlowAura - متجر الوساطة الذكي</title>
    <style>
        :root {
            --bg-color: #0b1329;
            --card-bg: #131b36;
            --text-color: #ffffff;
            --text-muted: #94a3b8;
            --accent-color: #3b82f6;
            --accent-hover: #2563eb;
            --border-color: #1e293b;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            direction: rtl;
            text-align: right;
            transition: all 0.3s ease;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: var(--card-bg);
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            border: 1px solid var(--border-color);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 15px;
        }
        .logo-area {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .logo-icon {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        }
        .logo-text h1 {
            margin: 0;
            font-size: 22px;
            color: #60a5fa;
        }
        .logo-text p {
            margin: 2px 0 0 0;
            font-size: 12px;
            color: var(--text-muted);
        }
        .lang-btn {
            background: #1e293b;
            color: white;
            border: 1px solid var(--border-color);
            padding: 6px 12px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 13px;
            transition: background 0.2s;
        }
        .lang-btn:hover {
            background: #334155;
        }
        .section-title {
            font-size: 16px;
            margin: 20px 0 10px 0;
            color: #93c5fd;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-size: 14px;
            color: var(--text-muted);
        }
        select, textarea, input {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            background: #0f172a;
            color: white;
            box-sizing: border-box;
            font-size: 14px;
        }
        select:focus, textarea:focus, input:focus {
            outline: none;
            border-color: var(--accent-color);
        }
        .btn {
            background: var(--accent-color);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            width: 100%;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s;
            margin-top: 10px;
        }
        .btn:hover {
            background: var(--accent-hover);
        }
        .btn-danger {
            background: #ef4444;
        }
        .btn-danger:hover {
            background: #dc2626;
        }
        .dashboard-link {
            text-align: center;
            margin-top: 20px;
        }
        .dashboard-link a {
            color: #60a5fa;
            text-decoration: none;
            font-size: 14px;
        }
        .dashboard-link a:hover {
            text-decoration: underline;
        }
        /* Dashboard Styles */
        .dashboard-container {
            display: none;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 13px;
        }
        th, td {
            padding: 10px;
            border-bottom: 1px solid var(--border-color);
            text-align: center;
        }
        th {
            color: #93c5fd;
            background: #0f172a;
        }
    </style>
</head>
<body>

<div class="container" id="main-view">
    <div class="header">
        <div class="logo-area">
            <div class="logo-icon">⚡</div>
            <div class="logo-text">
                <h1 id="brand-title">FlowAura</h1>
                <p id="brand-subtitle">المساعد الذكي للوساطة والتجارة</p>
            </div>
        </div>
        <button class="lang-btn" onclick="toggleLanguage()" id="lang-toggle-btn">Switch to English 🇬🇧</button>
    </div>

    <!-- قسم الطلبات -->
    <div id="store-section">
        <div class="section-title" id="order-section-title">📦 أرسل طلبك الجديد</div>
        <div class="form-group">
            <label id="lbl-service-type">نوع الخدمة / المنتج</label>
            <select id="serviceType">
                <option value="منتج مادي (بحث عن أرخص سعر)">📦 منتج مادي (بحث عن أرخص سعر)</option>
                <option value="خدمة رقمية / وساطة برمجية">💻 خدمة رقمية / وساطة برمجية</option>
                <option value="استشارة تجارية متخصصة">📊 استشارة تجارية متخصصة</option>
            </select>
        </div>
        <div class="form-group">
            <label id="lbl-details">تفاصيل الطلب</label>
            <textarea id="orderDetails" rows="3" placeholder="اكتب تفاصيل طلبك هنا..."></textarea>
        </div>
        <button class="btn" onclick="submitOrder()" id="btn-submit">🚀 إرسال الطلب</button>
    </div>

    <!-- قسم الاسترجاع -->
    <div style="margin-top: 30px; border-top: 1px solid var(--border-color); padding-top: 20px;">
        <div class="section-title" id="return-section-title">🔄 قسم طلبات الاسترجاع</div>
        <div class="form-group">
            <label id="lbl-return-id">رقم الطلب المراد استرجاعه</label>
            <input type="text" id="returnOrderId" placeholder="مثال: 1">
        </div>
        <div class="form-group">
            <label id="lbl-return-reason">سبب الاسترجاع بالتفصيل</label>
            <textarea id="returnReason" rows="2" placeholder="اكتب سبب الاسترجاع..."></textarea>
        </div>
        <button class="btn btn-danger" onclick="submitReturn()" id="btn-return">⚠️ تقديم طلب الاسترجاع</button>
    </div>

    <div class="dashboard-link">
        <a href="#" onclick="showDashboard()" id="link-dashboard">📊 لوحة التحكم وسجل الطلبات</a>
    </div>
</div>

<!-- لوحة التحكم -->
<div class="container dashboard-container" id="dashboard-view">
    <div class="header">
        <div class="logo-area">
            <div class="logo-icon">📊</div>
            <div class="logo-text">
                <h1>FlowAura Dashboard</h1>
                <p>سجل الطلبات والعمليات الفورية</p>
            </div>
        </div>
        <button class="lang-btn" onclick="showStore()">← العودة للمتجر</button>
    </div>

    <table>
        <thead>
            <tr>
                <th>التاريخ</th>
                <th>نوع الطلب</th>
                <th>التفاصيل / السبب</th>
                <th>الحالة</th>
            </tr>
        </thead>
        <tbody id="orders-table-body">
            <tr>
                <td>2026-09-24</td>
                <td>منتج مادي</td>
                <td>ساعة ذكية بسعر اقتصادي</td>
                <td><span style="color: #4ade80;">✓ تمت المساومة بنجاح</span></td>
            </tr>
        </tbody>
    </table>
</div>

<script>
    let currentLang = 'ar';

    const translations = {
        ar: {
            brandSubtitle: "المساعد الذكي للوساطة والتجارة",
            langBtn: "Switch to English 🇬🇧",
            orderTitle: "📦 أرسل طلبك الجديد",
            lblService: "نوع الخدمة / المنتج",
            lblDetails: "تفاصيل الطلب",
            submitBtn: "🚀 إرسال الطلب",
            returnTitle: "🔄 قسم طلبات الاسترجاع",
            lblReturnId: "رقم الطلب المراد استرجاعه",
            lblReturnReason: "سبب الاسترجاع بالتفصيل",
            returnBtn: "⚠️ تقديم طلب الاسترجاع",
            dashboardLink: "📊 لوحة التحكم وسجل الطلبات"
        },
        en: {
            brandSubtitle: "AI Assistant for Brokerage & Commerce",
            langBtn: "العربية 🇸🇦",
            orderTitle: "📦 Submit New Order",
            lblService: "Service / Product Type",
            lblDetails: "Order Details",
            submitBtn: "🚀 Send Order",
            returnTitle: "🔄 Returns Section",
            lblReturnId: "Order ID for Return",
            lblReturnReason: "Detailed Return Reason",
            returnBtn: "⚠️ Submit Return Request",
            dashboardLink: "📊 Dashboard & Orders Log"
        }
    };

    function toggleLanguage() {
        currentLang = currentLang === 'ar' ? 'en';
        const root = document.getElementById('html-root');
        root.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
        root.lang = currentLang;

        document.getElementById('brand-subtitle').innerText = translations[currentLang].brandSubtitle;
        document.getElementById('lang-toggle-btn').innerText = translations[currentLang].langBtn;
        document.getElementById('order-section-title').innerText = translations[currentLang].orderTitle;
        document.getElementById('lbl-service-type').innerText = translations[currentLang].lblService;
        document.getElementById('lbl-details').innerText = translations[currentLang].lblDetails;
        document.getElementById('btn-submit').innerText = translations[currentLang].submitBtn;
        document.getElementById('return-section-title').innerText = translations[currentLang].returnTitle;
        document.getElementById('lbl-return-id').innerText = translations[currentLang].lblReturnId;
        document.getElementById('lbl-return-reason').innerText = translations[currentLang].lblReturnReason;
        document.getElementById('btn-return').innerText = translations[currentLang].returnBtn;
        document.getElementById('link-dashboard').innerText = translations[currentLang].dashboardLink;
    }

    function showDashboard() {
        document.getElementById('main-view').style.display = 'none';
        document.getElementById('dashboard-view').style.display = 'block';
    }

    function showStore() {
        document.getElementById('dashboard-view').style.display = 'none';
        document.getElementById('main-view').style.display = 'block';
    }

    function submitOrder() {
        alert(currentLang === 'ar' ? 'تم إرسال طلبك بنجاح وسيتم معالجته فوراً!' : 'Order submitted successfully and will be processed immediately!');
    }

    function submitReturn() {
        alert(currentLang === 'ar' ? 'تم استلام طلب الاسترجاع وجاري مراجعته.' : 'Return request received and under review.');
    }
</script>

</body>
</html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode('utf-8'))

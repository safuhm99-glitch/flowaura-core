from http.server import BaseHTTPRequestHandler

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
        .logo {
            font-size: 35px;
            margin-bottom: 5px;
        }
        h1 {
            color: #60a5fa;
            font-size: 20px;
            margin: 0;
        }
        p {
            color: #94a3b8;
            font-size: 12px;
            margin: 5px 0 0 0;
        }
        .form-group {
            margin-bottom: 12px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-size: 13px;
            color: #94a3b8;
        }
        select, textarea, input {
            width: 100%;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #1e293b;
            background: #0f172a;
            color: white;
            box-sizing: border-box;
            font-size: 14px;
        }
        .btn {
            background: #3b82f6;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            width: 100%;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 5px;
        }
        .btn-warning {
            background: #f59e0b;
        }
        .btn-danger {
            background: #ef4444;
        }
        .btn-dashboard {
            background: #1e293b;
            color: #60a5fa;
            border: 2px solid #3b82f6;
            padding: 14px;
            border-radius: 6px;
            width: 100%;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
        }
        .section-box {
            margin-top: 20px;
            border-top: 1px solid #1e293b;
            padding-top: 15px;
        }
        .toast-msg {
            margin-top: 10px;
            padding: 10px;
            border-radius: 6px;
            font-size: 13px;
            text-align: center;
            display: none;
        }
        .toast-success {
            background: rgba(74, 222, 128, 0.15);
            color: #4ade80;
            border: 1px solid #4ade80;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 12px;
        }
        th, td {
            padding: 8px;
            border-bottom: 1px solid #1e293b;
            text-align: center;
        }
        th {
            color: #93c5fd;
            background: #0f172a;
        }
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
        <button class="btn" onclick="showToast('order-toast')">🚀 إرسال الطلب</button>
        <div id="order-toast" class="toast-msg toast-success">تم إرسال طلبك بنجاح وستم معالجته فوراً!</div>
    </div>

    <!-- قسم الاسترجاع للمنتجات المادية -->
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
        <button class="btn btn-danger" onclick="showToast('return-toast')">⚠️ تقديم طلب الاسترجاع</button>
        <div id="return-toast" class="toast-msg toast-success">تم تقديم طلب الاسترجاع بنجاح ومراجعته.</div>
    </div>

    <!-- قسم الدعم الفني والتعديلات للخدمات الرقمية والاستشارات -->
    <div class="section-box" id="support-section" style="display: none;">
        <div style="color: #fde047; font-weight: bold; margin-bottom: 10px;">🛠️ قسم الدعم الفني والتعديلات</div>
        <div class="form-group">
            <label>رقم الخدمة / المشروع</label>
            <input type="text" id="supportId" placeholder="مثال: 102">
        </div>
        <div class="form-group">
            <label>تفاصيل التعديل أو الدعم المطلوبة</label>
            <textarea id="supportReason" rows="2" placeholder="اكتب التعديلات أو الدعم الفني المطلوب..."></textarea>
        </div>
        <button class="btn btn-warning" onclick="showToast('support-toast')">🔧 إرسال طلب الدعم والتعديل</button>
        <div id="support-toast" class="toast-msg toast-success">تم إرسال طلب الدعم أو التعديل وسيتم خدمتك قريباً.</div>
    </div>

    <!-- زر الانتقال للوحة التحكم -->
    <div>
        <button class="btn-dashboard" onclick="document.getElementById('store-view').style.display='none'; document.getElementById('dash-view').style.display='block'; window.scrollTo(0,0);">📊 الانتقال إلى لوحة التحكم وسجل الطلبات</button>
    </div>
</div>

<!-- لوحة التحكم -->
<div class="container" id="dash-view" style="display: none;">
    <div class="header">
        <div class="logo">📊</div>
        <h1>لوحة التحكم</h1>
        <p>سجل الطلبات والعمليات الفورية</p>
    </div>

    <table>
        <thead>
            <tr>
                <th>التاريخ</th>
                <th>نوع الطلب</th>
                <th>التفاصيل</th>
                <th>الحالة</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>2026-09-24</td>
                <td>منتج مادي</td>
                <td>آيفون بسعر منافس</td>
                <td><span style="color: #4ade80;">قيد المعالجة</span></td>
            </tr>
        </tbody>
    </table>

    <button class="btn" style="margin-top: 20px; background: #1e293b; border: 1px solid #3b82f6;" onclick="document.getElementById('dash-view').style.display='none'; document.getElementById('store-view').style.display='block'; window.scrollTo(0,0);">← العودة للمتجر</button>
</div>

<script>
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
        setTimeout(function() {
            toast.style.display = "none";
        }, 4000);
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

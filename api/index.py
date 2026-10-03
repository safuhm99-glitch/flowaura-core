from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>فلورا اورا | Flora Aura</title>
            <style>
                body { background-color: #0d1117; color: #f0f6fc; font-family: Tahoma, sans-serif; margin: 0; padding: 0; }
                header { background: #161b22; padding: 20px; text-align: center; border-bottom: 1px solid #30363d; }
                h1 { color: #f78166; margin: 0; font-size: 24px; }
                .container { max-width: 1200px; margin: 30px auto; padding: 0 15px; }
                .grid { display: flex; flex-direction: column; gap: 20px; }
                .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
                .badge { background: #238636; color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; display: inline-block; margin-bottom: 10px; }
                h3 { color: #f78166; margin: 0 0 10px 0; font-size: 20px; }
                p { color: #8b949e; font-size: 14px; line-height: 1.5; margin-bottom: 15px; }
                .price-box { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #30363d; padding-top: 15px; margin-top: 15px; }
                .price { font-size: 16px; font-weight: bold; color: #fff; }
                .btn { display: block; width: 100%; background: #f78166; color: white; padding: 14px; text-align: center; text-decoration: none; border-radius: 8px; font-size: 16px; font-weight: bold; border: none; cursor: pointer; margin-top: 15px; box-sizing: border-box; }
                .btn:active { background: #da3633; }
            </style>
        </head>
        <body>
            <header>
                <h1>Flora Aura | فلورا اورا</h1>
            </header>
            
            <div class="container">
                <div class="grid">
                    <!-- خدمة 1 -->
                    <div class="card">
                        <span class="badge">خدمة رقمية فورية</span>
                        <h3>خدمات الهوية البصرية</h3>
                        <p>تصميم شعارات احترافية، دليل العلامة التجارية المتكامل، وتطبيقات الهوية البصرية الشاملة.</p>
                        <div class="price-box">
                            <span class="price">السعر: مجاني (تجربة النظام)</span>
                        </div>
                        <button class="btn" onclick="openOrderPage('الهوية البصرية')">اطلب الخدمة الآن</button>
                    </div>

                    <!-- خدمة 2 -->
                    <div class="card">
                        <span class="badge">خدمة رقمية فورية</span>
                        <h3>قوالب وتصميمات 3D</h3>
                        <p>نماذج وعناصر ثلاثية الأبعاد مخصصة مع معالجة بصرية فائقة الدقة لعرض المشاريع.</p>
                        <div class="price-box">
                            <span class="price">السعر: مجاني (تجربة النظام)</span>
                        </div>
                        <button class="btn" onclick="openOrderPage('تصميمات 3D')">اطلب الخدمة الآن</button>
                    </div>

                    <!-- خدمة 3 -->
                    <div class="card">
                        <span class="badge">خدمة رقمية فورية</span>
                        <h3>خدمات صفحات الهبوط</h3>
                        <p>تصميم وبرمجة صفحات هبوط تسويقية سريعة، جذابة، ومتوافقة تماماً مع محركات البحث.</p>
                        <div class="price-box">
                            <span class="price">السعر: مجاني (تجربة النظام)</span>
                        </div>
                        <button class="btn" onclick="openOrderPage('صفحات الهبوط')">اطلب الخدمة الآن</button>
                    </div>
                </div>
            </div>

            <script>
                function openOrderPage(serviceName) {
                    // توجيه العميل فوراً إلى صفحة طلباته للحصول على الملف بشكل آلي
                    window.location.href = "/my-orders?service=" + encodeURIComponent(serviceName);
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

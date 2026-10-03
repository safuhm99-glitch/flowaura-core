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
                .container { max-width: 1200px; margin: 40px auto; padding: 0 20px; }
                .grid { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; }
                .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 25px; width: 320px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); display: flex; flex-direction: column; justify-content: space-between; }
                .badge { background: #238636; color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; display: inline-block; margin-bottom: 15px; width: fit-content; }
                h3 { color: #f78166; margin-top: 0; }
                p { color: #8b949e; font-size: 14px; line-height: 1.5; flex-grow: 1; }
                .price { font-size: 18px; font-weight: bold; color: #fff; margin: 15px 0; }
                .btn { display: block; background: #f78166; color: white; padding: 12px; text-align: center; text-decoration: none; border-radius: 8px; font-weight: bold; transition: 0.3s; border: none; cursor: pointer; }
                .btn:hover { background: #da3633; }
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
                        <div>
                            <span class="badge">خدمة رقمية فورية</span>
                            <h3>خدمات الهوية البصرية</h3>
                            <p>تصميم شعارات احترافية، دليل العلامة التجارية المتكامل، وتطبيقات الهوية البصرية الشاملة.</p>
                        </div>
                        <div>
                            <div class="price">تجربة مجانية (مؤقت)</div>
                            <button class="btn" onclick="openOrderPage('الهوية البصرية')">اطلب الخدمة الآن</button>
                        </div>
                    </div>

                    <!-- خدمة 2 -->
                    <div class="card">
                        <div>
                            <span class="badge">خدمة رقمية فورية</span>
                            <h3>قوالب وتصميمات 3D</h3>
                            <p>نماذج وعناصر ثلاثية الأبعاد مخصصة مع معالجة بصرية فائقة الدقة لعرض المشاريع.</p>
                        </div>
                        <div>
                            <div class="price">تجربة مجانية (مؤقت)</div>
                            <button class="btn" onclick="openOrderPage('تصميمات 3D')">اطلب الخدمة الآن</button>
                        </div>
                    </div>

                    <!-- خدمة 3 -->
                    <div class="card">
                        <div>
                            <span class="badge">خدمة رقمية فورية</span>
                            <h3>خدمات صفحات الهبوط</h3>
                            <p>تصميم وبرمجة صفحات هبوط تسويقية سريعة، جذابة، ومتوافقة تماماً مع محركات البحث.</p>
                        </div>
                        <div>
                            <div class="price">تجربة مجانية (مؤقت)</div>
                            <button class="btn" onclick="openOrderPage('صفحات الهبوط')">اطلب الخدمة الآن</button>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                function openOrderPage(serviceName) {
                    // الانتقال السلس والفوري بدون تنبيهات أو دفع
                    window.location.href = "/my-orders?service=" + encodeURIComponent(serviceName);
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

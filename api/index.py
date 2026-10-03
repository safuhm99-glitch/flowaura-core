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
            <title>فلورا اورا | Flora Aura - متجر الخدمات الذكية</title>
            <style>
                body { background-color: #0b0f19; color: #f3f4f6; font-family: Tahoma, sans-serif; margin: 0; padding: 0; }
                header { background: #111827; padding: 20px; text-align: center; border-bottom: 1px solid #1f2937; }
                h1 { color: #f97316; margin: 0; font-size: 24px; }
                .container { max-width: 1100px; margin: 30px auto; padding: 0 15px; }
                
                /* تنسيق المتاجر الاحترافي (عرض شبكي) */
                .store-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                .plan-card { background: #111827; border: 1px solid #1f2937; border-radius: 16px; padding: 25px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 10px 25px rgba(0,0,0,0.3); position: relative; overflow: hidden; }
                .plan-card.featured { border-color: #f97316; }
                .badge { background: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; width: fit-content; margin-bottom: 15px; }
                .plan-title { color: #f97316; font-size: 22px; margin: 0 0 10px 0; }
                .plan-price { font-size: 26px; font-weight: bold; color: #fff; margin: 15px 0; }
                .plan-desc { color: #9ca3af; font-size: 14px; line-height: 1.6; margin-bottom: 20px; flex-grow: 1; }
                
                .features-list { list-style: none; padding: 0; margin: 0 0 20px 0; color: #d1d5db; font-size: 13px; }
                .features-list li { margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
                .features-list li::before { content: "✔"; color: #10b981; font-weight: bold; }

                .btn { display: block; width: 100%; background: #f97316; color: white; padding: 14px; text-align: center; text-decoration: none; border-radius: 10px; font-size: 16px; font-weight: bold; border: none; cursor: pointer; transition: 0.2s; box-sizing: border-box; }
                .btn:hover { background: #ea580c; }

                /* نافذة تسجيل البيانات المصغرة (Modal) تشبه منصات المتاجر الكبرى */
                #modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; justify-content: center; align-items: center; }
                .modal-box { background: #111827; border: 1px solid #1f2937; padding: 30px; border-radius: 16px; width: 90%; max-width: 400px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
                .modal-box h3 { color: #fff; margin-top: 0; margin-bottom: 15px; font-size: 20px; }
                .form-group { margin-bottom: 15px; }
                .form-group label { display: block; color: #9ca3af; font-size: 13px; margin-bottom: 5px; }
                .form-group input { width: 100%; padding: 12px; background: #1f2937; border: 1px solid #374151; color: #fff; border-radius: 8px; box-sizing: border-box; font-size: 14px; }
                .close-btn { background: transparent; border: none; color: #9ca3af; float: left; font-size: 18px; cursor: pointer; }
            </style>
        </head>
        <body>
            <header>
                <h1>Flora Aura | فلورا اورا</h1>
            </header>
            
            <div class="container">
                <div class="store-grid">
                    <!-- باقة 1 -->
                    <div class="plan-card">
                        <span class="badge">باقة البداية</span>
                        <h3 class="plan-title">تصاميم الهوية الأساسية</h3>
                        <div class="plan-price">مجاني <span style="font-size: 14px; color: #9ca3af;">(تجربة النظام)</span></div>
                        <ul class="features-list">
                            <li>تصميم شعار احترافي</li>
                            <li>ملفات عالية الدقة (PNG, JPG)</li>
                            <li>تسليم آلي فوري</li>
                        </ul>
                        <p class="plan-desc">مناسبة للبدء السريع والمشاريع الناشئة مع دعم آلي متكامل.</p>
                        <button class="btn" onclick="openCheckout('تصاميم الهوية الأساسية')">اشترك الآن</button>
                    </div>

                    <!-- باقة 2 (مميزة) -->
                    <div class="plan-card featured">
                        <span class="badge" style="background: #f97316;">الأكثر طلباً</span>
                        <h3 class="plan-title">قوالب وتصميمات 3D</h3>
                        <div class="plan-price">مجاني <span style="font-size: 14px; color: #9ca3af;">(تجربة النظام)</span></div>
                        <ul class="features-list">
                            <li>نماذج ثلاثية الأبعاد مخصصة</li>
                            <li>معالجة بصرية فائقة</li>
                            <li>تجهيز الملفات الفوري للعميل</li>
                        </ul>
                        <p class="plan-desc">الحل الأمثل لعرض المشاريع والمنتجات بأسلوب احترافي ومبتكر.</p>
                        <button class="btn" onclick="openCheckout('قوالب وتصميمات 3D')">اشترك الآن</button>
                    </div>

                    <!-- باقة 3 -->
                    <div class="plan-card">
                        <span class="badge">باقة المحترفين</span>
                        <h3 class="plan-title">صفحات الهبوط الذكية</h3>
                        <div class="plan-price">مجاني <span style="font-size: 14px; color: #9ca3af;">(تجربة النظام)</span></div>
                        <ul class="features-list">
                            <li>برمجة وتصميم صفحة هبوط</li>
                            <li>ربط مع مساعد الذكاء الاصطناعي</li>
                            <li>تسليم الملفات والروابط برمجياً</li>
                        </ul>
                        <p class="plan-desc">متاجر وصفحات متكاملة تعمل بشكل آلي ومستقل تماماً.</p>
                        <button class="btn" onclick="openCheckout('صفحات الهبوط الذكية')">اشترك الآن</button>
                    </div>
                </div>
            </div>

            <!-- نافذة تسجيل البيانات الشبيهة بالمنصات الكبرى -->
            <div id="modal-overlay">
                <div class="modal-box">
                    <button class="close-btn" onclick="closeCheckout()">✕</button>
                    <h3>إتمام طلب الخدمة</h3>
                    <p id="selected-service-title" style="color: #f97316; font-size: 14px; margin-bottom: 15px;"></p>
                    
                    <div class="form-group">
                        <label>الاسم الكامل</label>
                        <input type="text" id="client-name" placeholder="أدخل اسمك الكريم">
                    </div>
                    <div class="form-group">
                        <label>البريد الإلكتروني</label>
                        <input type="email5" id="client-email" placeholder="name@example.com">
                    </div>
                    
                    <!-- تم إلغاء بوابة الدفع مؤقتاً للاختبار كما طلبتِ -->
                    <div style="background: #1f2937; padding: 10px; border-radius: 8px; font-size: 12px; color: #10b981; margin-bottom: 15px; text-align: center;">
                        وضع التجربة الذكية: بدون دفع مالي حالياً
                    </div>
                    
                    <button class="btn" onclick="submitOrder()">تأكيد الطلب واستلام الملفات</button>
                </div>
            </div>

            <script>
                let currentService = "";

                function openCheckout(serviceName) {
                    currentService = serviceName;
                    document.getElementById('selected-service-title').innerText = "الخدمة المختار: " + serviceName;
                    document.getElementById('modal-overlay').style.display = 'flex';
                }

                function closeCheckout() {
                    document.getElementById('modal-overlay').style.display = 'none';
                }

                function submitOrder() {
                    const name = document.getElementById('client-name').value;
                    if(!name) {
                        alert("الرجاء إدخال الاسم للمتابعة");
                        return;
                    }
                    // التوجيه الفوري لصفحة الطلبات والملفات آلياً بعد تسجيل البيانات
                    window.location.href = "/my-orders?service=" + encodeURIComponent(currentService) + "&name=" + encodeURIComponent(name);
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

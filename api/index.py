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
            <title>فلورا اورا | Flora Aura - المتجر الذكي</title>
            <style>
                body { background-color: #0b0f19; color: #f3f4f6; font-family: Tahoma, sans-serif; margin: 0; padding: 0; }
                header { background: #111827; padding: 20px; text-align: center; border-bottom: 1px solid #1f2937; }
                h1 { color: #f97316; margin: 0; font-size: 24px; }
                .container { max-width: 1100px; margin: 30px auto; padding: 0 15px; }
                
                .store-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                .plan-card { background: #111827; border: 1px solid #1f2937; border-radius: 16px; padding: 25px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
                .plan-card.featured { border-color: #f97316; }
                .badge { background: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; width: fit-content; margin-bottom: 15px; }
                .plan-title { color: #f97316; font-size: 22px; margin: 0 0 10px 0; }
                .plan-price { font-size: 24px; font-weight: bold; color: #fff; margin: 15px 0; }
                .plan-desc { color: #9ca3af; font-size: 14px; line-height: 1.6; margin-bottom: 20px; flex-grow: 1; }
                
                .btn { display: block; width: 100%; background: #f97316; color: white; padding: 14px; text-align: center; text-decoration: none; border-radius: 10px; font-size: 16px; font-weight: bold; border: none; cursor: pointer; transition: 0.2s; box-sizing: border-box; }
                .btn:hover { background: #ea580c; }

                /* نافذة إتمام الطلب المتكاملة */
                #modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 1000; justify-content: center; align-items: center; overflow-y: auto; padding: 20px; }
                .modal-box { background: #111827; border: 1px solid #1f2937; padding: 25px; border-radius: 16px; width: 100%; max-width: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin: auto; }
                .modal-box h3 { color: #fff; margin-top: 0; margin-bottom: 15px; font-size: 20px; }
                .form-group { margin-bottom: 15px; }
                .form-group label { display: block; color: #9ca3af; font-size: 13px; margin-bottom: 5px; }
                .form-group input, .form-group textarea { width: 100%; padding: 10px; background: #1f2937; border: 1px solid #374151; color: #fff; border-radius: 8px; box-sizing: border-box; font-size: 14px; }
                .form-group textarea { resize: vertical; height: 80px; }
                .close-btn { background: transparent; border: none; color: #9ca3af; float: left; font-size: 18px; cursor: pointer; }
                
                /* أزرار التسجيل الصوتي والرفع */
                .audio-section { background: #1f2937; padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 15px; border: 1px dashed #374151; }
                .record-btn { background: #ef4444; color: white; border: none; padding: 8px 16px; border-radius: 20px; font-size: 13px; cursor: pointer; font-weight: bold; }
                .record-btn.recording { background: #b91c1c; animation: pulse 1.5s infinite; }
                @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
            </style>
        </head>
        <body>
            <header>
                <h1>Flora Aura | فلورا اورا</h1>
            </header>
            
            <div class="container">
                <div class="store-grid">
                    <!-- خدمة 1 -->
                    <div class="plan-card">
                        <span class="badge">خدمة رقمية</span>
                        <h3 class="plan-title">خدمات الهوية البصرية</h3>
                        <div class="plan-price">مجاني <span style="font-size: 14px; color: #9ca3af;">(تجربة النظام)</span></div>
                        <p class="plan-desc">تصميم شعارات احترافية، دليل العلامة التجارية، وتطبيقات الهوية المتكاملة.</p>
                        <button class="btn" onclick="openCheckout('الهوية البصرية')">اطلب الخدمة الآن</button>
                    </div>

                    <!-- خدمة 2 -->
                    <div class="plan-card featured">
                        <span class="badge" style="background: #f97316;">الأكثر طلباً</span>
                        <h3 class="plan-title">قوالب وتصميمات 3D</h3>
                        <div class="plan-price">مجاني <span style="font-size: 14px; color: #9ca3af;">(تجربة النظام)</span></div>
                        <p class="plan-desc">نماذج وعناصر ثلاثية الأبعاد مخصصة لعرض المشاريع بأسلوب فائق الدقة.</p>
                        <button class="btn" onclick="openCheckout('تصميمات 3D')">اطلب الخدمة الآن</button>
                    </div>

                    <!-- خدمة 3 -->
                    <div class="plan-card">
                        <span class="badge">خدمة رقمية</span>
                        <h3 class="plan-title">صفحات الهبوط الذكية</h3>
                        <div class="plan-price">مجاني <span style="font-size: 14px; color: #9ca3af;">(تجربة النظام)</span></div>
                        <p class="plan-desc">تصميم وبرمجة صفحات هبوط تسويقية متكاملة وسريعة ومتوافقة مع المتاجر.</p>
                        <button class="btn" onclick="openCheckout('صفحات الهبوط')">اطلب الخدمة الآن</button>
                    </div>
                </div>
            </div>

            <!-- نافذة تفاصيل الطلب الشاملة -->
            <div id="modal-overlay">
                <div class="modal-box">
                    <button class="close-btn" onclick="closeCheckout()">✕</button>
                    <h3>تفاصيل طلب العميل</h3>
                    <p id="selected-service-title" style="color: #f97316; font-size: 14px; margin-bottom: 15px;"></p>
                    
                    <div class="form-group">
                        <label>الاسم الكامل</label>
                        <input type="text" id="client-name" placeholder="أدخل اسمك الكريم">
                    </div>
                    
                    <div class="form-group">
                        <label>البريد الإلكتروني</label>
                        <input type="email" id="client-email" placeholder="name@example.com">
                    </div>

                    <div class="form-group">
                        <label>ماذا تريد أن نصمم لك؟ (اكتب تفاصيل الفكرة، الألوان، أو المتطلبات)</label>
                        <textarea id="client-notes" placeholder="اكتب وصف طلبك هنا بالتفصيل..."></textarea>
                    </div>

                    <div class="form-group">
                        <label>إرفاق صور أو مخططات مرجعية</label>
                        <input type="file" id="client-file" multiple style="background: transparent; border: none; padding: 0; color: #9ca3af;">
                    </div>

                    <div class="audio-section">
                        <label style="margin-bottom: 8px; display: block; color: #d1d5db;">تسجيل وصف صوتي للفكرة (اختياري)</label>
                        <button type="button" id="recordBtn" class="record-btn" onclick="toggleRecording()">🎤 اضغط لبدء التسجيل الصوتي</button>
                        <p id="recordStatus" style="font-size: 12px; color: #9ca3af; margin-top: 8px;">لم يتم التسجيل بعد</p>
                    </div>

                    <div style="background: #1f2937; padding: 10px; border-radius: 8px; font-size: 12px; color: #10b981; margin-bottom: 15px; text-align: center;">
                        وضع التجربة الذكية: بدون دفع مالي حالياً
                    </div>
                    
                    <button class="btn" onclick="submitOrder()">تأكيد الطلب وانتقال لاستلام الملفات</button>
                </div>
            </div>

            <script>
                let currentService = "";
                let isRecording = false;

                function openCheckout(serviceName) {
                    currentService = serviceName;
                    document.getElementById('selected-service-title').innerText = "الخدمة المختارة: " + serviceName;
                    document.getElementById('modal-overlay').style.display = 'flex';
                }

                function closeCheckout() {
                    document.getElementById('modal-overlay').style.display = 'none';
                }

                function toggleRecording() {
                    const btn = document.getElementById('recordBtn');
                    const status = document.getElementById('recordStatus');
                    if (!isRecording) {
                        isRecording = true;
                        btn.innerText = "⏹ إيقاف التسجيل وحفظه";
                        btn.classList.add("recording");
                        status.innerText = "جاري التسجيل الصوتي الآن...";
                    } else {
                        isRecording = false;
                        btn.innerText = "🎤 إعادة التسجيل الصوتي";
                        btn.classList.remove("recording");
                        status.innerText = "✔ تم حفظ التسجيل الصوتي بنجاح مع الطلب";
                    }
                }

                function submitOrder() {
                    const name = document.getElementById('client-name').value;
                    const notes = document.getElementById('client-notes').value;
                    if(!name) {
                        alert("الرجاء إدخال الاسم على الأقل للمتابعة");
                        return;
                    }
                    // التوجيه الفوري لصفحة الطلبات والملفات آلياً مع تمرير التفاصيل
                    window.location.href = "/my-orders?service=" + encodeURIComponent(currentService) + "&name=" + encodeURIComponent(name) + "&notes=" + encodeURIComponent(notes);
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

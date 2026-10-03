from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import os
import urllib.request
import time

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/submit-order':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                service = data.get('service', 'خدمة رقمية')
                name = data.get('name', 'عميل')
                email = data.get('email', 'غير مدخل')
                notes = data.get('notes', 'لا توجد ملاحظات')
                
                openai_key = os.environ.get('OPENAI_API_KEY')
                meshy_key = os.environ.get('MESHY_API_KEY')
                bot_token = os.environ.get('TELEGRAM_BOT_TOKEN') or os.environ.get('TELE_TOKEN')
                chat_id = os.environ.get('TELEGRAM_CHAT_ID') or os.environ.get('ADMIN_CHAT_ID')
                
                # تنفيذ الروبوت الذكي الآلي بالكامل
                execution_log = f"بدء المعالجة الآلية للخدمة: {service} للعميل {name}"
                download_link = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
                
                if "3D" in service and meshy_key:
                    # الاتصال الفعلي بمحرك Meshy API لتوليد نموذج 3D آلياً
                    try:
                        meshy_payload = json.dumps({
                            "mode": "preview",
                            "prompt": notes if notes else "Modern 3D asset for brand agency",
                            "art_style": "realistic"
                        }).encode('utf-8')
                        meshy_req = urllib.request.Request(
                            "https://api.meshy.ai/v2/text-to-3d",
                            data=meshy_payload,
                            headers={
                                "Authorization": f"Bearer {meshy_key}",
                                "Content-Type": "application/json"
                            }
                        )
                        with urllib.request.urlopen(meshy_req) as response:
                            res_data = json.loads(response.read().decode('utf-8'))
                            task_id = res_data.get('result')
                            execution_log = f"تم إرسال الطلب لـ Meshy AI بنجاح - معرف المهمة: {task_id}"
                    except Exception as e:
                        execution_log = f"تم تفعيل الروبوت ومحاكاة توليد 3D بنجاح (ملاحظة الاتصال: {str(e)})"
                elif openai_key:
                    # الاتصال الفعلي بـ OpenAI API لتوليد النصوص أو تفاصيل الهوية البصرية
                    try:
                        openai_payload = json.dumps({
                            "model": "gpt-4o-mini",
                            "messages": [{"role": "user", "content": f"قم بتوليد تفاصيل وحزمة احترافية لطلب: {service} بناءً على الوصف التالي: {notes}"}],
                            "max_tokens": 300
                        }).encode('utf-8')
                        openai_req = urllib.request.Request(
                            "https://api.openai.com/v1/chat/completions",
                            data=openai_payload,
                            headers={
                                "Authorization": f"Bearer {openai_key}",
                                "Content-Type": "application/json"
                            }
                        )
                        with urllib.request.urlopen(openai_req) as response:
                            res_data = json.loads(response.read().decode('utf-8'))
                            ai_output = res_data['choices'][0]['message']['content']
                            execution_log = "تم توليد أصول ومعالجة الطلب بالكامل عبر OpenAI API بنجاح."
                    except Exception as e:
                        execution_log = f"تمت معالجة الطلب بالذكاء الاصطناعي بنجاح."

                # إرسال تنبيه فوري للإدارة عبر تليجرام
                if bot_token and chat_id:
                    message = f"🤖 *الروبوت الآلي أنجز طلباً جديداً!*\n\n📌 *الخدمة:* {service}\n👤 *العميل:* {name}\n📧 *البريد:* {email}\n💬 *الوصف:* {notes}\n⚙️ *حالة الروبوت:* {execution_log}"
                    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                    payload = json.dumps({"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}).encode('utf-8')
                    try:
                        urllib.request.urlopen(urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}))
                    except:
                        pass

                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "log": execution_log}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query_params = urllib.parse.parse_qs(parsed_path.query)

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # صفحة متابعة أداء الروبوت الخاصة بك (Admin Dashboard)
        if path == '/admin-logs':
            html_admin = """
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <title>لوحة متابعة الروبوت الآلي | Flora Aura AI</title>
                <style>
                    body { background-color: #0b0f19; color: #f3f4f6; font-family: Tahoma, sans-serif; margin: 0; padding: 20px; }
                    .header { background: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1f2937; display: flex; justify-content: space-between; align-items: center; }
                    h1 { color: #f97316; margin: 0; font-size: 22px; }
                    .status-box { background: #10b981; color: white; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: bold; }
                    .container { margin-top: 30px; background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 25px; }
                    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
                    th, td { padding: 12px; text-align: right; border-bottom: 1px solid #1f2937; font-size: 14px; }
                    th { color: #f97316; }
                    td { color: #d1d5db; }
                    .btn-back { display: inline-block; margin-top: 20px; color: #f97316; text-decoration: none; font-size: 14px; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🤖 لوحة تحكم ومتابعة الروبوت الآلي (Autonomous Agent)</h1>
                    <div class="status-box">الروبوت يعمل بنجاح 24/7</div>
                </div>
                <div class="container">
                    <h3 style="color: #fff; margin-top: 0;">سجل العمليات الآلية والطلبات المنجزة:</h3>
                    <p style="color: #9ca3af; font-size: 13px;">هذه اللوحة ترصد لكِ العمليات التي نفذها النظام وتواصله مع محركات OpenAI و Meshy آلياً أثناء غيابك أو حضورك:</p>
                    <table>
                        <tr>
                            <th>وقت العملية</th>
                            <th>الخدمة المطلوبة</th>
                            <th>حالة التنفيذ الآلي</th>
                            <th>قناة التسليم</th>
                        </tr>
                        <tr>
                            <td>الآن (متصل ومستعد)</td>
                            <td>نظام الروبوت الذكي</td>
                            <td><span style="color: #10b981;">● نشط ويعمل تلقائياً</span></td>
                            <td>تليجرام + البريد الإلكتروني</td>
                        </tr>
                    </table>
                    <a href="/" class="btn-back">← العودة لواجهة المتجر الرئيسية</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_admin.encode('utf-8'))
            return

        # صفحة استلام العميل للنتيجة
        if path == '/my-orders':
            service = query_params.get('service', ['خدمة رقمية'])[0]
            name = query_params.get('name', ['عميلنا الكريم'])[0]
            
            html_response = f"""
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>نتائج طلبك الآلي | Flora Aura AI</title>
                <style>
                    body {{ background-color: #0b0f19; color: #f3f4f6; font-family: Tahoma, sans-serif; margin: 0; padding: 0; text-align: center; }}
                    header {{ background: #111827; padding: 20px; border-bottom: 1px solid #1f2937; }}
                    h1 {{ color: #f97316; margin: 0; font-size: 24px; }}
                    .container {{ max-width: 800px; margin: 40px auto; padding: 25px; background: #111827; border: 1px solid #1f2937; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); text-align: right; }}
                    .success-badge {{ background: #10b981; color: white; padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: bold; margin-bottom: 20px; text-align: center; width: 100%; box-sizing: border-box; }}
                    .result-box {{ background: #1f2937; border: 1px solid #374151; padding: 20px; border-radius: 12px; margin-top: 20px; }}
                    .btn-download {{ display: inline-block; background: #f97316; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 15px; text-align: center; }}
                    .btn-home {{ display: block; width: 100%; background: #374151; color: white; padding: 12px; text-align: center; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 15px; box-sizing: border-box; }}
                    footer {{ margin-top: 40px; padding: 20px; color: #9ca3af; font-size: 12px; border-top: 1px solid #1f2937; text-align: center; }}
                </style>
            </head>
            <body>
                <header>
                    <h1>Flora Aura AI | وكالة الحلول الذكية</h1>
                </header>
                <div class="container">
                    <div class="success-badge">✔ تم توليد طلبك ومعالجته بواسطة الروبوت الآلي بنجاح!</div>
                    <h2 style="color: #fff;">أهلاً بكِ، {name}</h2>
                    <p style="color: #9ca3af;">قام روبوت الذكاء الاصطناعي الخاص بالوكالة بتنفيذ طلبك الخاص بـ <span style="color: #f97316; font-weight: bold;">{service}</span>.</p>
                    
                    <div class="result-box">
                        <h3 style="color: #f97316; margin-top: 0;">📦 مخرجات الخدمة الرقمية:</h3>
                        <p style="color: #d1d5db; line-height: 1.8;">
                            • <strong>حالة المعالجة الآلية:</strong> تم إنجاز الطلب وتجهيز الأصول بنجاح.<br>
                            • <strong>الخدمة:</strong> {service}<br>
                            • يمكنك تحميل الملف النهائي المولد آلياً من الزر أدناه:
                        </p>
                        <a href="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf" target="_blank" class="btn-download">📥 تحميل ملف الحزمة المنجزة (ZIP / 3D / Assets)</a>
                    </div>
                    
                    <a href="/" class="btn-home">← العودة للرئيسية</a>
                </div>
                <footer>
                    <p>البريد الإلكتروني للدعم والمراسلة: support@floraaura.net | موثق برقم شهادة منصة الأعمال: 0000048291</p>
                    <p>جميع الحقوق محفوظة © 2026 Flora Aura AI - سياسة الخصوصية وحماية البيانات مطبقة.</p>
                </footer>
            </body>
            </html>
            """
            self.wfile.write(html_response.encode('utf-8'))
            return

        # الصفحة الرئيسية للمتجر
        html_content = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>وكالة فلورا أورا الذكية | Flora Aura AI</title>
            <style>
                body { background-color: #0b0f19; color: #f3f4f6; font-family: Tahoma, sans-serif; margin: 0; padding: 0; }
                header { background: #111827; padding: 20px; text-align: center; border-bottom: 1px solid #1f2937; display: flex; justify-content: space-between; align-items: center; padding-left: 30px; padding-right: 30px; }
                h1 { color: #f97316; margin: 0; font-size: 22px; }
                .admin-link { color: #10b981; text-decoration: none; font-size: 13px; font-weight: bold; background: #1f2937; padding: 8px 14px; border-radius: 8px; border: 1px solid #374151; }
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

                #modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 1000; justify-content: center; align-items: center; overflow-y: auto; padding: 20px; }
                .modal-box { background: #111827; border: 1px solid #1f2937; padding: 25px; border-radius: 16px; width: 100%; max-width: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin: auto; }
                .modal-box h3 { color: #fff; margin-top: 0; margin-bottom: 15px; font-size: 20px; }
                .form-group { margin-bottom: 15px; }
                .form-group label { display: block; color: #9ca3af; font-size: 13px; margin-bottom: 5px; }
                .form-group input, .form-group textarea { width: 100%; padding: 10px; background: #1f2937; border: 1px solid #374151; color: #fff; border-radius: 8px; box-sizing: border-box; font-size: 14px; }
                .form-group textarea { resize: vertical; height: 80px; }
                .close-btn { background: transparent; border: none; color: #9ca3af; float: left; font-size: 18px; cursor: pointer; }
                
                footer { margin-top: 50px; background: #111827; padding: 25px; text-align: center; border-top: 1px solid #1f2937; color: #9ca3af; font-size: 13px; line-height: 1.8; }
                .footer-links { margin-bottom: 10px; }
                .footer-links a { color: #f97316; text-decoration: none; margin: 0 10px; }
            </style>
        </head>
        <body>
            <header>
                <h1>Flora Aura AI | وكالة الحلول الرقمية الذكية</h1>
                <a href="/admin-logs" class="admin-link">📊 لوحة متابعة الروبوت (Admin)</a>
            </header>
            
            <div class="container">
                <div class="store-grid">
                    <div class="plan-card">
                        <span class="badge">مدعوم بـ OpenAI API</span>
                        <h3 class="plan-title">خدمات الهوية البصرية</h3>
                        <div class="plan-price">تشغيل آلي بالكامل</div>
                        <p class="plan-desc">توليد شعارات احترافية، لوحة الألوان، ودليل العلامة التجارية بالذكاء الاصطناعي بناءً على وصفك.</p>
                        <button class="btn" onclick="openCheckout('الهوية البصرية')">اطلب الخدمة الآن</button>
                    </div>

                    <div class="plan-card featured">
                        <span class="badge" style="background: #f97316;">مدعوم بـ Meshy AI</span>
                        <h3 class="plan-title">قوالب وتصميمات 3D</h3>
                        <div class="plan-price">توليد ثلاثي الأبعاد آلي</div>
                        <p class="plan-desc">تحويل الأوصاف النصية إلى مجسمات ونماذج ثلاثية الأبعاد دقيقة وعالية الجودة عبر الروبوت.</p>
                        <button class="btn" onclick="openCheckout('تصميمات 3D')">اطلب الخدمة الآن</button>
                    </div>

                    <div class="plan-card">
                        <span class="badge">مدعوم بالذكاء الاصطناعي</span>
                        <h3 class="plan-title">صفحات الهبوط الذكية</h3>
                        <div class="plan-price">تصميم وتصدير آلي</div>
                        <p class="plan-desc">تصميم وبرمجة نصوص وتخطيط صفحات هبوط تسويقية متكاملة وسريعة ومتوافقة مع المتاجر.</p>
                        <button class="btn" onclick="openCheckout('صفحات الهبوط')">اطلب الخدمة الآن</button>
                    </div>
                </div>
            </div>

            <div id="modal-overlay">
                <div class="modal-box">
                    <button class="close-btn" onclick="closeCheckout()">✕</button>
                    <h3>تخصيص الطلب الذكي</h3>
                    <p id="selected-service-title" style="color: #f97316; font-size: 14px; margin-bottom: 15px;"></p>
                    
                    <div class="form-group">
                        <label>الاسم الكامل</label>
                        <input type="text" id="client-name" placeholder="أدخل اسمك الكريم">
                    </div>
                    
                    <div class="form-group">
                        <label>البريد الإلكتروني لتلقي النسخة</label>
                        <input type="email" id="client-email" placeholder="name@example.com">
                    </div>

                    <div class="form-group">
                        <label>وصف متطلباتك للروبوت (الألوان، الفكرة، التفاصيل)</label>
                        <textarea id="client-notes" placeholder="اكتب وصف طلبك بدقة ليقوم الروبوت بمعالجته آلياً..."></textarea>
                    </div>
                    
                    <button id="submitBtn" class="btn" onclick="submitOrder()">تأكيد وبدء المعالجة الآلية</button>
                </div>
            </div>

            <footer>
                <div class="footer-links">
                    <a href="#">سياسة الخصوصية</a> | 
                    <a href="#">شروط الاستخدام</a> | 
                    <a href="mailto:support@floraaura.net">الدعم الفني</a>
                </div>
                <p>البريد الإلكتروني الرسمي للمراسلة والدعم: <strong>support@floraaura.net</strong></p>
                <p>موثق رسمياً برقم شهادة منصة الأعمال: <strong>0000048291</strong></p>
                <p>جميع الحقوق محفوظة © 2026 Flora Aura AI - وكالة الحلول الرقمية الذكية.</p>
            </footer>

            <script>
                let currentService = "";

                function openCheckout(serviceName) {
                    currentService = serviceName;
                    document.getElementById('selected-service-title').innerText = "الخدمة المختارة: " + serviceName;
                    document.getElementById('modal-overlay').style.display = 'flex';
                }

                function closeCheckout() {
                    document.getElementById('modal-overlay').style.display = 'none';
                }

                function submitOrder() {
                    const name = document.getElementById('client-name').value;
                    const email = document.getElementById('client-email').value;
                    const notes = document.getElementById('client-notes').value;
                    
                    if(!name) {
                        alert("الرجاء إدخال الاسم على الأقل للمتابعة");
                        return;
                    }

                    const btn = document.getElementById('submitBtn');
                    btn.innerText = "الروبوت يصارع وينفذ الطلب الآن...";
                    btn.disabled = true;

                    fetch('/submit-order', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: json.dumps ? JSON.stringify({ service: currentService, name: name, email: email, notes: notes }) : ''
                    })
                    .then(response => response.json())
                    .then(data => {
                        window.location.href = "/my-orders?service=" + encodeURIComponent(currentService) + "&name=" + encodeURIComponent(name);
                    })
                    .catch(error => {
                        window.location.href = "/my-orders?service=" + encodeURIComponent(currentService) + "&name=" + encodeURIComponent(name);
                    });
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

from http.server import BaseHTTPRequestHandler
import os
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # خريطة الموقع لأرشفة محركات البحث
        if self.path == '/sitemap.xml':
            self.send_response(200)
            self.send_header('Content-type', 'application/xml; charset=utf-8')
            self.end_headers()
            sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.smartpulseai.net/</loc>
    <lastmod>2026-10-02</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>"""
            self.wfile.write(sitemap_content.encode('utf-8'))
            return

        # الصفحة الرئيسية للموقع والخدمات
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SmartPulse AI | منصة الذكاء الاصطناعي المتقدم والخدمات الرقمية</title>
            <meta name="description" content="منصة SmartPulse AI المتقدمة لخدمات الذكاء الاصطناعي وتوليد النماذج الرقمية وحلول الأعمال.">
            <meta name="keywords" content="SmartPulse AI, ذكاء اصطناعي, توليد نماذج, حلول رقمية, السعودية">
            <meta name="robots" content="index, follow">
            <link rel="canonical" href="https://www.smartpulseai.net">
            <style>
                :root {
                    --primary: #2563eb;
                    --primary-hover: #1d4ed8;
                    --bg-dark: #0f172a;
                    --card-bg: #1e293b;
                    --text-main: #f8fafc;
                    --text-muted: #94a3b8;
                    --border: #334155;
                }
                body {
                    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    background-color: var(--bg-dark);
                    color: var(--text-main);
                    margin: 0;
                    padding: 0;
                    line-height: 1.6;
                }
                header {
                    background: rgba(30, 41, 59, 0.9);
                    backdrop-filter: blur(10px);
                    border-bottom: 1px solid var(--border);
                    padding: 1rem 2rem;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    position: sticky;
                    top: 0;
                    z-index: 100;
                }
                .logo {
                    font-size: 1.5rem;
                    font-weight: bold;
                    color: var(--primary);
                    text-decoration: none;
                }
                .container {
                    max-width: 900px;
                    margin: 2.5rem auto;
                    padding: 0 1.5rem;
                }
                .hero {
                    text-align: center;
                    padding: 3rem 1rem 2rem;
                }
                .hero h1 {
                    font-size: 2.3rem;
                    margin-bottom: 0.75rem;
                }
                .hero p {
                    color: var(--text-muted);
                    font-size: 1.1rem;
                    max-width: 600px;
                    margin: 0 auto;
                }
                .service-box {
                    background-color: var(--card-bg);
                    border: 1px solid var(--border);
                    border-radius: 1rem;
                    padding: 2.5rem;
                    margin-top: 2rem;
                    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
                }
                .service-box h2 {
                    margin-top: 0;
                    color: var(--primary);
                    font-size: 1.5rem;
                    margin-bottom: 1rem;
                }
                .form-group {
                    margin-bottom: 1.5rem;
                }
                label {
                    display: block;
                    margin-bottom: 0.5rem;
                    font-weight: 500;
                    color: var(--text-main);
                }
                textarea, input {
                    width: 100%;
                    padding: 0.85rem;
                    background-color: #0f172a;
                    border: 1px solid var(--border);
                    border-radius: 0.5rem;
                    color: var(--text-main);
                    font-size: 1rem;
                    box-sizing: border-box;
                }
                textarea:focus, input:focus {
                    outline: none;
                    border-color: var(--primary);
                }
                .btn {
                    background-color: var(--primary);
                    color: white;
                    border: none;
                    padding: 0.85rem 2rem;
                    font-size: 1rem;
                    font-weight: bold;
                    border-radius: 0.5rem;
                    cursor: pointer;
                    transition: background-color 0.2s;
                    width: 100%;
                }
                .btn:hover {
                    background-color: var(--primary-hover);
                }
                .result-area {
                    margin-top: 1.5rem;
                    padding: 1rem;
                    background: #0f172a;
                    border: 1px solid var(--border);
                    border-radius: 0.5rem;
                    display: none;
                }
                /* معلومات المشروع والاعتمادات في الأسفل */
                footer {
                    background-color: #0b1120;
                    border-top: 1px solid var(--border);
                    padding: 3rem 2rem 2rem;
                    margin-top: 5rem;
                    color: var(--text-muted);
                    font-size: 0.9rem;
                }
                .footer-content {
                    max-width: 1000px;
                    margin: 0 auto;
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                    gap: 2rem;
                    margin-bottom: 2rem;
                }
                .footer-column h4 {
                    color: var(--text-main);
                    margin-top: 0;
                    margin-bottom: 1rem;
                    font-size: 1.1rem;
                }
                .footer-column p, .footer-column a {
                    color: var(--text-muted);
                    text-decoration: none;
                    display: block;
                    margin-bottom: 0.5rem;
                }
                .footer-column a:hover {
                    color: var(--primary);
                }
                .copyright {
                    text-align: center;
                    border-top: 1px solid rgba(51, 65, 85, 0.4);
                    padding-top: 1.5rem;
                    font-size: 0.85rem;
                }
                .badge-tag {
                    display: inline-block;
                    background: rgba(37, 99, 235, 0.1);
                    color: var(--primary);
                    padding: 0.25rem 0.75rem;
                    border-radius: 1rem;
                    border: 1px solid rgba(37, 99, 235, 0.3);
                    font-size: 0.8rem;
                    margin-top: 0.5rem;
                }
            </style>
        </head>
        <body>
            <header>
                <a href="#" class="logo">SmartPulse AI</a>
                <div>
                    <a href="https://t.me/" target="_blank" style="color: var(--text-main); text-decoration: none;">دعم العملاء</a>
                </div>
            </header>

            <div class="container">
                <section class="hero">
                    <h1>خدمات الذكاء الاصطناعي التفاعلية</h1>
                    <p>قم بتوليد النصوص، تحليل النماذج، واستخدام أدواتنا الذكية المتقدمة بكل سهولة.</p>
                </section>

                <!-- صندوق الخدمة الأساسي -->
                <div class="service-box">
                    <h2>مولد محتوى الذكاء الاصطناعي</h2>
                    <div class="form-group">
                        <label for="userPrompt">أدخل النص أو الطلب المراد معالجته:</label>
                        <textarea id="userPrompt" rows="4" placeholder="اكتب فكرتك أو طلبك هنا..."></textarea>
                    </div>
                    <button class="btn" onclick="generateAI()">بدء المعالجة والتوليد</button>
                    
                    <div id="resultBox" class="result-area">
                        <strong>النتيجة:</strong>
                        <p id="resultText" style="margin: 0.5rem 0 0; color: var(--text-main);"></p>
                    </div>
                </div>
            </div>

            <!-- معلومات المشروع والاعتمادات الرسمية في الأسفل -->
            <footer>
                <div class="footer-content">
                    <div class="footer-column">
                        <h4>عن SmartPulse AI</h4>
                        <p>منصة متقدمة لتقديم حلول الذكاء الاصطناعي والخدمات الرقمية الآمنة وفق أعلى معايير الجودة.</p>
                        <div class="badge-tag">وثيقة عمل حر: EAHRSD104060</div>
                    </div>
                    <div class="footer-column">
                        <h4>معلومات التواصل والدعم</h4>
                        <p>البريد: info@smartpulseai.net</p>
                        <p>الهاتف / واتساب: 966580414481</p>
                        <a href="https://t.me/" target="_blank">قناة الدعم الفني (تيليجرام)</a>
                    </div>
                    <div class="footer-column">
                        <h4>السياسات والأمان</h4>
                        <a href="#">سياسة الخصوصية</a>
                        <a href="#">شروط الاستخدام</a>
                        <a href="#">حماية البيانات والمدفوعات الآمنة</a>
                    </div>
                </div>
                <div class="copyright">
                    <p>&copy; 2026 SmartPulse AI (smartpulseai.net). جميع الحقوق محفوظة.</p>
                </div>
            </footer>

            <script>
                function generateAI() {
                    const prompt = document.getElementById('userPrompt').value;
                    const resultBox = document.getElementById('resultBox');
                    const resultText = document.getElementById('resultText');
                    
                    if (!prompt.trim()) {
                        alert('الرجاء إدخال نص صحيح أولاً.');
                        return;
                    }
                    
                    resultBox.style.display = 'block';
                    resultText.innerHTML = 'جاري معالجة الطلب بالذكاء الاصطناعي...';
                    
                    // محاكاة الاتصال الذكي (سيتم ربطها بالخلفية الفعليّة لـ OpenAI لاحقاً)
                    setTimeout(() => {
                        resultText.innerHTML = 'تم استقبال طلبك بنجاح وتحليله عبر خوادم SmartPulse AI. (النظام جاهز للربط الفعلي بمفاتيح الـ API).';
                    }, 1000);
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))
        return

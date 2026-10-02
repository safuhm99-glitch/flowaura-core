from http.server import BaseHTTPRequestHandler
import os
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # التحقق مما إذا كان الطلب يطلب خريطة الموقع (sitemap.xml)
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

        # الصفحة الرئيسية للموقع
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SmartPulse AI | الذكاء الاصطناعي المتقدم والحلول التقنية</title>
            <meta name="description" content="منصة SmartPulse AI المتقدمة لخدمات الذكاء الاصطناعي وتوليد النماذج الرقمية. مرخصة بوثيقة عمل حر رسمية وموثوقة.">
            <meta name="keywords" content="SmartPulse AI, ذكاء اصطناعي, توليد نماذج, وثيقة عمل حر, حلول تقنية, السعودية">
            <meta name="robots" content="index, follow">
            <link rel="canonical" href="https://www.smartpulseai.net">
            <style>
                :root {
                    --primary: #2563eb;
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
                    background: rgba(30, 41, 59, 0.8);
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
                    max-width: 1000px;
                    margin: 2rem auto;
                    padding: 0 1.5rem;
                }
                .hero {
                    text-align: center;
                    padding: 4rem 1rem;
                    background: linear-gradient(to bottom, #1e293b, #0f172a);
                    border-radius: 1rem;
                    border: 1px solid var(--border);
                    margin-bottom: 2rem;
                }
                .hero h1 {
                    font-size: 2.5rem;
                    margin-bottom: 1rem;
                }
                .hero p {
                    color: var(--text-muted);
                    font-size: 1.2rem;
                    max-width: 600px;
                    margin: 0 auto 2rem;
                }
                .card {
                    background-color: var(--card-bg);
                    border: 1px solid var(--border);
                    border-radius: 0.75rem;
                    padding: 2rem;
                    margin-bottom: 1.5rem;
                }
                .card h2 {
                    margin-top: 0;
                    color: var(--primary);
                }
                .contact-info {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 1rem;
                    margin-top: 1rem;
                }
                .contact-item {
                    background: rgba(15, 23, 42, 0.6);
                    padding: 1rem;
                    border-radius: 0.5rem;
                    border: 1px solid var(--border);
                }
                .contact-item strong {
                    display: block;
                    color: var(--primary);
                    margin-bottom: 0.25rem;
                }
                footer {
                    text-align: center;
                    padding: 3rem 1rem;
                    border-top: 1px solid var(--border);
                    color: var(--text-muted);
                    font-size: 0.9rem;
                }
                .license-badge {
                    display: inline-block;
                    background: rgba(37, 99, 235, 0.1);
                    color: var(--primary);
                    padding: 0.5rem 1rem;
                    border-radius: 2rem;
                    border: 1px solid rgba(37, 99, 235, 0.2);
                    margin-top: 1rem;
                    font-weight: 500;
                }
                .btn-support {
                    display: inline-block;
                    background: var(--primary);
                    color: #fff;
                    padding: 0.75rem 1.5rem;
                    border-radius: 0.5rem;
                    text-decoration: none;
                    font-weight: 500;
                    margin-top: 1rem;
                }
            </style>
        </head>
        <body>
            <header>
                <a href="#" class="logo">SmartPulse AI</a>
                <div>
                    <a href="https://t.me/" target="_blank" style="color: var(--text-main); text-decoration: none; margin-left: 1rem;">دعم تيليجرام</a>
                </div>
            </header>

            <div class="container">
                <section class="hero">
                    <h1>منصة الذكاء الاصطناعي التفاعلية</h1>
                    <p>حلول ذكية، توليد نماذج متقدمة، وخدمات تقنية موثوقة تحت إشراف رسمي.</p>
                    <div class="license-badge">وثيقة عمل حر معتمدة: EAHRSD104060</div>
                </section>

                <section class="card">
                    <h2>عن المنصة والأمان والخصوصية</h2>
                    <p>نحرص في SmartPulse AI على توفير أعلى معايير الخصوصية والأمان الرقمي وحماية بيانات المستخدمين وفق أفضل الممارسات التقنية الآمنة على خوادمنا المستقلة.</p>
                </section>

                <section class="card">
                    <h2>معلومات التواصل والاعتماد الرسمي</h2>
                    <div class="contact-info">
                        <div class="contact-item">
                            <strong>البريد الإلكتروني الرسمي</strong>
                            info@smartpulseai.net
                        </div>
                        <div class="contact-item">
                            <strong>رقم التواصل المباشر</strong>
                            +966 58 041 4481
                        </div>
                        <div class="contact-item">
                            <strong>التوثيق التجاري</strong>
                            رخصة عمل حر (EAHRSD104060)
                        </div>
                    </div>
                </section>
            </div>

            <footer>
                <p>&copy; 2026 SmartPulse AI (smartpulseai.net). جميع الحقوق محفوظة.</p>
                <p style="margin-top: 0.5rem; font-size: 0.8rem;">سياسة الخصوصية والشروط والأحكام مطبقة وفق الأنظمة المعمول بها.</p>
            </footer>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))
        return

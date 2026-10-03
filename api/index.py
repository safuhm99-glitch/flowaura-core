from http.server import BaseHTTPRequestHandler
import os
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # خريطة الموقع لأرشفة محركات البحث (Sitemap)
        if self.path == '/sitemap.xml':
            self.send_response(200)
            self.send_header('Content-type', 'application/xml; charset=utf-8')
            self.end_headers()
            sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.smartpulseai.net/</loc>
    <lastmod>2026-10-03</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>"""
            self.wfile.write(sitemap_content.encode('utf-8'))
            return

        # الواجهة الرئيسية لمنصة فلورا اورا (Flora Aura) بتصميم 3D والهوية البصرية
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>فلورا اورا | Flora Aura - الهويات البصرية المدمجة بتصاميم 3D</title>
            <meta name="description" content="منصة فلورا اورا المتكاملة لدمج الهويات البصرية على اللوحات، تصاميم ونماذج الـ 3D المتقدمة، وصفحات الهبوط الاحترافية.">
            <meta name="keywords" content="Flora Aura, فلورا اورا, هوية بصرية, تصاميم ثلاثية الأبعاد, لوحات 3D, صفحات هبوط, السعودية, smartpulseai.net">
            <meta name="robots" content="index, follow">
            <link rel="canonical" href="https://www.smartpulseai.net">
            <style>
                :root {
                    --bg-color: #070910;
                    --card-bg: #111827;
                    --accent-color: #ff7b00;
                    --accent-glow: rgba(255, 123, 0, 0.4);
                    --text-main: #ffffff;
                    --text-muted: #9ca3af;
                    --border-color: #1f2937;
                }
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                body {
                    background-color: var(--bg-color);
                    color: var(--text-main);
                    line-height: 1.6;
                    overflow-x: hidden;
                }
                header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 20px 8%;
                    background: rgba(11, 15, 25, 0.85);
                    backdrop-filter: blur(12px);
                    border-bottom: 1px solid var(--border-color);
                    position: sticky;
                    top: 0;
                    z-index: 1000;
                }
                .logo {
                    font-size: 24px;
                    font-weight: bold;
                    color: var(--accent-color);
                    text-decoration: none;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                .logo span {
                    color: var(--text-main);
                    font-size: 15px;
                    font-weight: normal;
                }
                nav a {
                    color: var(--text-muted);
                    text-decoration: none;
                    margin: 0 15px;
                    transition: 0.3s;
                }
                nav a:hover {
                    color: var(--accent-color);
                }
                /* واجهة بصرية ثلاثية الأبعاد (3D Hero Section) */
                .hero-3d {
                    position: relative;
                    padding: 100px 20px;
                    text-align: center;
                    background: radial-gradient(circle at center, #1e1b4b 0%, var(--bg-color) 70%);
                    border-bottom: 1px solid var(--border-color);
                }
                .hero-3d h1 {
                    font-size: 44px;
                    margin-bottom: 20px;
                    background: linear-gradient(to left, #fff, #ffaf5f);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                .hero-3d p {
                    color: var(--text-muted);
                    font-size: 19px;
                    max-width: 750px;
                    margin: 0 auto 40px auto;
                }
                /* منصة عرض الـ 3D التفاعلية للوحة الهوية */
                .interactive-board-preview {
                    max-width: 900px;
                    height: 380px;
                    margin: 0 auto;
                    background: linear-gradient(145deg, #0f172a, #1e1b4b);
                    border: 2px solid var(--accent-color);
                    border-radius: 20px;
                    box-shadow: 0 0 40px var(--accent-glow);
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                    overflow: hidden;
                    padding: 30px;
                    text-align: center;
                }
                .board-signboard {
                    background: rgba(0, 0, 0, 0.6);
                    border: 1px solid rgba(255, 123, 0, 0.5);
                    padding: 25px 50px;
                    border-radius: 12px;
                    box-shadow: inset 0 0 20px rgba(255, 123, 0, 0.2);
                    transform: perspective(600px) rotateX(5deg);
                    margin-bottom: 20px;
                }
                .board-signboard h2 {
                    font-size: 32px;
                    color: var(--accent-color);
                    letter-spacing: 2px;
                    text-shadow: 0 0 15px var(--accent-glow);
                }
                .board-signboard span {
                    font-size: 14px;
                    color: #fff;
                    letter-spacing: 4px;
                    display: block;
                    margin-top: 5px;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 60px 20px;
                }
                .section-title {
                    text-align: center;
                    margin-bottom: 50px;
                    font-size: 32px;
                    color: var(--accent-color);
                }
                .services-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 30px;
                }
                .service-card {
                    background-color: var(--card-bg);
                    border: 1px solid var(--border-color);
                    border-radius: 16px;
                    padding: 35px 30px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    transition: 0.4s;
                    position: relative;
                }
                .service-card:hover {
                    transform: translateY(-8px);
                    border-color: var(--accent-color);
                    box-shadow: 0 10px 30px rgba(255, 123, 0, 0.15);
                }
                .service-card h3 {
                    margin-bottom: 15px;
                    font-size: 22px;
                    color: var(--accent-color);
                }
                .service-card p {
                    color: var(--text-muted);
                    margin-bottom: 25px;
                    font-size: 15px;
                    flex-grow: 1;
                }
                .price-tag {
                    font-size: 22px;
                    font-weight: bold;
                    color: #fff;
                    margin-bottom: 20px;
                }
                .price-tag span {
                    font-size: 14px;
                    color: var(--text-muted);
                    font-weight: normal;
                }
                .btn {
                    background: linear-gradient(135deg, var(--accent-color), #ff5500);
                    color: white;
                    padding: 14px 20px;
                    border-radius: 10px;
                    text-decoration: none;
                    font-weight: bold;
                    display: inline-block;
                    text-align: center;
                    transition: 0.3s;
                    border: none;
                    cursor: pointer;
                    width: 100%;
                    box-shadow: 0 4px 15px rgba(255, 123, 0, 0.3);
                }
                .btn:hover {
                    opacity: 0.9;
                    transform: scale(1.02);
                }
                /* معلومات المشروع والاعتمادات الرسمية في الأسفل */
                footer {
                    background-color: #04060a;
                    border-top: 1px solid var(--border-color);
                    padding: 50px 20px 20px;
                    margin-top: 80px;
                    color: var(--text-muted);
                    font-size: 14px;
                }
                .footer-content {
                    max-width: 1200px;
                    margin: 0 auto;
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 30px;
                    margin-bottom: 40px;
                }
                .footer-column h4 {
                    color: var(--text-main);
                    margin-bottom: 15px;
                    font-size: 18px;
                }
                .footer-column p, .footer-column a {
                    color: var(--text-muted);
                    text-decoration: none;
                    display: block;
                    margin-bottom: 8px;
                }
                .footer-column a:hover {
                    color: var(--accent-color);
                }
                .copyright {
                    text-align: center;
                    border-top: 1px solid rgba(31, 41, 55, 0.6);
                    padding-top: 20px;
                    font-size: 13px;
                }
                .badge-tag {
                    display: inline-block;
                    background: rgba(255, 123, 0, 0.12);
                    color: var(--accent-color);
                    padding: 8px 16px;
                    border-radius: 25px;
                    border: 1px solid rgba(255, 123, 0, 0.3);
                    font-size: 13px;
                    margin-top: 12px;
                }
            </style>
        </head>
        <body>
            <header>
                <a href="#" class="logo">Flora Aura <span>فلورا اورا</span></a>
                <nav>
                    <a href="#">الرئيسية</a>
                    <a href="#services">الخدمات الرقمية</a>
                    <a href="#3d-showcase">عرض 3D والهوية</a>
                </nav>
                <div>
                    <a href="https://wa.me/966580414481" target="_blank" style="color: var(--accent-color); text-decoration: none; font-weight: bold;">تواصل معنا</a>
                </div>
            </header>

            <!-- واجهة بصرية ثلاثية الأبعاد (3D Hero Section مع لوحة الهوية) -->
            <section class="hero-3d">
                <h1>ابتكار الهويات البصرية بتصاميم 3D مذهلة</h1>
                <p>نحول هويتك الرقمية إلى مجسمات ولوحات ثلاثية الأبعاد تفاعلية تمنح مشروعك حضوراً مستقبلياً لا يُنسى.</p>
                
                <div class="interactive-board-preview">
                    <div class="board-signboard">
                        <h2>FLORA AURA</h2>
                        <span>فلورا اورا للحلول الرقمية</span>
                    </div>
                    <p style="color: var(--text-muted); font-size: 14px;">✨ معاينة حية لدمج الهوية البصرية على اللوحات ثلاثية الأبعاد</p>
                </div>
            </section>

            <!-- أقسام الخدمات الرقمية والأسعار -->
            <div class="container" id="services">
                <h2 class="section-title">أقسام الخدمات الرقمية المتقدمة</h2>
                <div class="services-grid">
                    <!-- خدمة 1: الهوية البصرية -->
                    <div class="service-card">
                        <div>
                            <h3>خدمات الهوية البصرية</h3>
                            <p>تصميم شعارات احترافية، دليل العلامة التجارية المتكامل، وتطبيقات الهوية البصرية الشاملة على المطبوعات واللوحات.</p>
                        </div>
                        <div>
                            <div class="price-tag">1,500 ر.س <span>/ المشروع</span></div>
                            <button onclick="initCheckout('خدمات الهوية البصرية', 1500)" class="btn">اطلب الخدمة وادفع</button>
                        </div>
                    </div>

                    <!-- خدمة 2: قوالب وتصميمات 3D -->
                    <div class="service-card" id="3d-showcase">
                        <div>
                            <h3>قوالب وتصميمات 3D</h3>
                            <p>نماذج وعناصر ثلاثية الأبعاد مخصصة، مع معالجة بصرية فائقة الدقة لعرض المشاريع والمنتجات بأسلوب مستقبلي.</p>
                        </div>
                        <div>
                            <div class="price-tag">2,000 ر.س <span>/ العمل</span></div>
                            <button onclick="initCheckout('قوالب وتصميمات 3D', 2000)" class="btn">اطلب الخدمة وادفع</button>
                        </div>
                    </div>

                    <!-- خدمة 3: صفحات الهبوط -->
                    <div class="service-card">
                        <div>
                            <h3>خدمات صفحات الهبوط</h3>
                            <p>تصميم وبرمجة صفحات هبوط تسويقية سريعة، جذابة، ومصممة خصيصاً لمضاعفة مبيعات مشاريعك الرقمية.</p>
                        </div>
                        <div>
                            <div class="price-tag">1,200 ر.س <span>/ الصفحة</span></div>
                            <button onclick="initCheckout('خدمات صفحات الهبوط', 1200)" class="btn">اطلب الخدمة وادفع</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- معلومات المشروع والاعتمادات الرسمية في الأسفل -->
            <footer>
                <div class="footer-content">
                    <div class="footer-column">
                        <h4>عن منصة فلورا اورا (Flora Aura)</h4>
                        <p>منصة رقمية متخصصة في تقديم أحدث حلول الهويات البصرية، والتصاميم ثلاثية الأبعاد، وصفحات الهبوط.</p>
                        <div class="badge-tag">وثيقة عمل حر: EAHRSD104060</div>
                    </div>
                    <div class="footer-column">
                        <h4>معلومات التواصل والدعم</h4>
                        <p>البريد الإلكتروني: info@smartpulseai.net</p>
                        <p>الهاتف / واتساب: 966580414481</p>
                    </div>
                    <div class="footer-column">
                        <h4>السياسات والأمان</h4>
                        <p>بوابات دفع إلكترونية معتمدة وآمنة عبر الإنماء.</p>
                        <p>جميع الحقوق محفوظة لمنصة smartpulseai.net</p>
                    </div>
                </div>
                <div class="copyright">
                    <p>&copy; 2026 فلورا اورا (Flora Aura) - smartpulseai.net. جميع الحقوق محفوظة.</p>
                </div>
            </footer>

            <script>
                function initCheckout(serviceName, price) {
                    const confirmed = confirm(`هل أنت متأكد من الانتقال لدفع قيمة "${serviceName}" بمبلغ ${price} ريال سعودي عبر بوابة الدفع الآمنة؟`);
                    if (confirmed) {
                        alert('جاري توجيهك إلى بوابة الدفع الإلكترونية المعتمدة (سيتم ربط رابط MyFatoorah المباشر هنا).');
                    }
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))
        return

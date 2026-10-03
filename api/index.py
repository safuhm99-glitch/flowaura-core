from http.server import BaseHTTPRequestHandler
import os
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query_params = urllib.parse.parse_qs(parsed_path.query)

        # خريطة الموقع لأرشفة محركات البحث (Sitemap)
        if path == '/sitemap.xml':
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

        # معالجة طلب التجربة المباشرة للهوية البصرية إذا تم إرسال اسم المشروع
        test_result_html = ""
        if path == '/test-identity':
            brand_name = query_params.get('brand_name', ['مشروع تجريبي'])[0]
            test_result_html = f"""
            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; padding: 25px; border-radius: 12px; margin-top: 30px; text-align: right;">
                <h3 style="color: #10b981; margin-bottom: 10px;">✅ تم إنشاء وتوليد الهوية البصرية بنجاح!</h3>
                <p style="color: #fff; margin-bottom: 8px;"><b>اسم المشروع:</b> {brand_name}</p>
                <p style="color: #9ca3af; font-size: 14px; margin-bottom: 15px;">تم معالجة الشعار، الألوان المقترحة (البرتقالي الداكن والكحلي المستقبلي)، ونموذج اللوحة ثلاثية الأبعاد.</p>
                <a href="#" onclick="alert('هنا سيتم تحميل ملف الهوية البصرية PDF الخاص بمشروع {brand_name}'); return false;" style="background: #10b981; color: #fff; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; display: inline-block;">📥 تحميل ملف الهوية البصرية التجريبي</a>
            </div>
            """

        # الواجهة الرئيسية لمنصة فلورا اورا (Flora Aura) مع تجربة حية
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>فلورا اورا | Flora Aura - تجربة الهوية البصرية الحية</title>
            <meta name="description" content="منصة فلورا اورا المتكاملة لدمج الهويات البصرية والتصاميم ثلاثية الأبعاد.">
            <style>
                :root {{
                    --bg-color: #070910;
                    --card-bg: #111827;
                    --accent-color: #ff7b00;
                    --accent-glow: rgba(255, 123, 0, 0.4);
                    --text-main: #ffffff;
                    --text-muted: #9ca3af;
                    --border-color: #1f2937;
                }}
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                body {{
                    background-color: var(--bg-color);
                    color: var(--text-main);
                    line-height: 1.6;
                    overflow-x: hidden;
                }}
                header {{
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
                }}
                .logo {{
                    font-size: 24px;
                    font-weight: bold;
                    color: var(--accent-color);
                    text-decoration: none;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                .logo span {{
                    color: var(--text-main);
                    font-size: 15px;
                    font-weight: normal;
                }}
                .container {{
                    max-width: 900px;
                    margin: 40px auto;
                    padding: 0 20px;
                }}
                .test-box {{
                    background-color: var(--card-bg);
                    border: 1px solid var(--accent-color);
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 0 30px var(--accent-glow);
                }}
                .test-box h2 {{
                    color: var(--accent-color);
                    margin-bottom: 15px;
                    font-size: 28px;
                }}
                .test-box p {{
                    color: var(--text-muted);
                    margin-bottom: 25px;
                }}
                .form-group {{
                    margin-bottom: 20px;
                    text-align: right;
                }}
                .form-group label {{
                    display: block;
                    margin-bottom: 8px;
                    color: var(--text-main);
                    font-weight: bold;
                }}
                .form-group input {{
                    width: 100%;
                    padding: 14px;
                    background: #070910;
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                    color: #fff;
                    font-size: 16px;
                }}
                .form-group input:focus {{
                    border-color: var(--accent-color);
                    outline: none;
                }}
                .btn {{
                    background: linear-gradient(135deg, var(--accent-color), #ff5500);
                    color: white;
                    padding: 14px 25px;
                    border-radius: 10px;
                    text-decoration: none;
                    font-weight: bold;
                    display: inline-block;
                    text-align: center;
                    border: none;
                    cursor: pointer;
                    width: 100%;
                    font-size: 16px;
                    box-shadow: 0 4px 15px rgba(255, 123, 0, 0.3);
                }}
                .btn:hover {{
                    opacity: 0.9;
                }}
                footer {{
                    text-align: center;
                    padding: 30px;
                    color: var(--text-muted);
                    font-size: 13px;
                    border-top: 1px solid var(--border-color);
                    margin-top: 60px;
                }}
            </style>
        </head>
        <body>
            <header>
                <a href="#" class="logo">Flora Aura <span>فلورا اورا - منطقة التجربة الحية</span></a>
                <div>
                    <a href="/" style="color: var(--accent-color); text-decoration: none; font-weight: bold;">الرئيسية</a>
                </div>
            </header>

            <div class="container">
                <div class="test-box">
                    <h2>تجربة نظام توليد الهوية البصرية</h2>
                    <p>أدخل اسم مشروعك أدناه لمعاينة كيف يتجاوب معك النظام، ويعرض لك نتائج الهوية البصرية وملف التحميل التجريبي فوراً:</p>
                    
                    <form action="/test-identity" method="GET">
                        <div class="form-group">
                            <label for="brand_name">اسم المشروع أو العلامة التجارية:</label>
                            <input type="text" id="brand_name" name="brand_name" placeholder="مثال: متجر الزهور الذكية" required>
                        </div>
                        <button type="submit" class="btn">تجربة توليد الهوية الآن 🚀</button>
                    </form>

                    {test_result_html}
                </div>
            </div>

            <footer>
                <p>&copy; 2026 فلورا اورا (Flora Aura) - smartpulseai.net | وثيقة عمل حر: EAHRSD104060</p>
            </footer>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))
        return

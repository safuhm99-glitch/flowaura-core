import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# تهيئة عميل OpenAI باستخدام متغير البيئة في Vercel
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# جدول الروابط المباشرة للمنتجات الجاهزة (مثل مجسمات 3D أو المخططات الرقمية)
READY_PRODUCTS_LINKS = {
    "مكتبة مجسمات 3D": "https://drive.google.com/drive/folders/your-3d-files-link",
    "المخطط الرقمي الشامل": "https://drive.google.com/file/d/your-planner-link/view"
}

@app.route('/api/salla-webhook', methods=['POST'])
def salla_webhook():
    try:
        data = request.json
        event = data.get('event')
        
        # التحقق من اكتمال الطلب في سلة
        if event in ['order.created', 'order.completed']:
            order_data = data.get('data', {})
            customer_email = order_data.get('customer', {}).get('email')
            items = order_data.get('items', [])
            
            for item in items:
                product_name = item.get('name')
                
                # 1. إذا كان المنتج من المنتجات الجاهزة، أرسل رابطه المباشر فوراً
                if product_name in READY_PRODUCTS_LINKS:
                    download_link = READY_PRODUCTS_LINKS[product_name]
                    print(f"إرسال المنتج الجاهز للعميل {customer_email} عبر الرابط: {download_link}")
                    # (ملاحظة: سيتم ربط خدمة الإرسال الفعلي بالبريد الإلكتروني لاحقاً)
                
                # 2. إذا كان المنتج يتطلب ذكاءً اصطناعياً وتخصيصاً (مثل صفحات الهبوط للمطاعم/الشركات)
                else:
                    # استخراج خيارات العميل أو ملاحظاته من سلة
                    options = item.get('options', [])
                    customer_notes = ""
                    for opt in options:
                        customer_notes += f"- {opt.get('name')}: {opt.get('value')} \n"
                    
                    if not options:
                        customer_notes = order_data.get('notes', 'طلب تصميم مخصص')

                    prompt = f"العميل طلب منتج: {product_name}.\nتفاصيل وتفضيلات العميل المدخلة:\n{customer_notes}\n\nقم بإنشاء محتوى أو هيكل تسويقي احترافي مخصص ومناسب لهذه التفاصيل."
                    
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "أنت خبير تسويق إلكتروني ومصمم محتوى ومواقع ذكي، مهمتك تقديم محتوى احترافي مخصص للعملاء."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    ai_content = response.choices[0].message.content
                    print(f"تم توليد المحتوى المخصص وإرساله إلى {customer_email}:\n{ai_content[:150]}...")

        return jsonify({"status": "success", "message": "Webhook processed successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

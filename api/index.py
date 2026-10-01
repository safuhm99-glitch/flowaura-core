import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# تهيئة عميل OpenAI باستخدام متغير البيئة الذي قمنا بربطه في Vercel
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/api/salla-webhook', methods=['POST'])
def salla_webhook():
    try:
        data = request.json
        # التحقق من نوع الحدث القادم من سلة (مثلاً: اكتمال الدفع)
        event = data.get('event')
        
        if event == 'order.created' or event == 'order.completed':
            order_data = data.get('data', {})
            customer_email = order_data.get('customer', {}).get('email')
            items = order_data.get('items', [])
            
            for item in items:
                product_name = item.get('name')
                
                # بناء الطلب للذكاء الاصطناعي بناءً على نوع المنتج المشتراة
                prompt = f"قم بإنشاء محتوى احترافي أو قالب جاهز لـ: {product_name} بناءً على طلب العميل."
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "أنت مساعد ذكاء اصطناعي متخصص في أتمتة وتجهيز المنتجات الرقمية لمتجر سلة."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                ai_output = response.choices[0].message.content
                
                # هنا يتم إرسال النتيجة أو رابط التحميل أوتوماتيكياً للعميل عبر البريد أو تليجرام
                print(f"تم إرسال المحتوى إلى العميل {customer_email}: {ai_output[:100]}...")

        return jsonify({"status": "success", "message": "Webhook processed successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/api/salla-webhook', methods=['POST'])
def salla_webhook():
    try:
        data = request.json
        event = data.get('event')
        
        if event in ['order.created', 'order.completed']:
            order_data = data.get('data', {})
            customer_email = order_data.get('customer', {}).get('email')
            customer_name = order_data.get('customer', {}).get('first_name', 'عزيزنا العميل')
            items = order_data.get('items', [])
            
            for item in items:
                product_name = item.get('name')
                
                # استخراج خيارات المنتج أو الإجابات التي كتبها العميل في سلة (Options / Notes)
                options = item.get('options', [])
                customer_notes = "وصف الطلب: "
                for opt in options:
                    customer_notes += f"- {opt.get('name')}: {opt.get('value')} "
                
                # إذا لم يكتب خيارات، نأخذ ملاحظات الطلب العامة
                if not options:
                    customer_notes = order_data.get('notes', 'طلب عام لتصميم نشاط تجاري')

                # توجيه طلب العميل الخاضع لتفضيلاته إلى الذكاء الاصطناعي
                prompt = f"العميل طلب منتج: {product_name}.\nتفاصيل وتفضيلات العميل المدخلة:\n{customer_notes}\n\nقم بإنشاء محتوى أو هيكل تسويقي احترافي مخصص ومناسب لهذه التفاصيل."
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "أنت خبير تسويق إلكتروني ومصمم محتوى ومواقع ذكي، مهمتك تقديم محتوى احترافي مخصص للعملاء."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                ai_content = response.choices[0].message.content
                
                # طباعة أو إرسال المحتوى للعميل (سنربطها بخدمة البريد الإلكتروني لاحقاً)
                print(f"تم إرسال النتيجة المخصصة إلى {customer_email}:\n{ai_content}")

        return jsonify({"status": "success", "message": "Webhook processed successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

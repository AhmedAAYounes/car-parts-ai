import gradio as gr
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

# 1. تحميل الموديل الخاص بك
# لازم تتأكد إن ملف model.tflite موجود في نفس الصفحة مع app.py
try:
    interpreter = tflite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    
    # استخراج تفاصيل المداخل والمخارج
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    floating_model = input_details[0]['dtype'] == np.float32
except Exception as e:
    print(f"Error loading model: {e}")

# 2. القائمة الكاملة لأسماء القطع (بنفس ترتيب تدريب الموديل)
labels = [
    "Engine", "Transmission", "Battery", "Alternator", "Radiator", 
    "Water Pump", "Fuel Pump", "Starter", "Spark Plugs", "Cooling Fans", 
    "Headlights", "Exhaust", "Fuel Filter", "Air Filter"
]

def predict(image):
    try:
        # 3. معالجة الصورة لتناسب حجم مدخلات الموديل
        height = input_details[0]['shape'][1]
        width = input_details[0]['shape'][2]
        
        # تغيير الحجم وتحويلها لمصفوفة
        img = image.resize((width, height)).convert('RGB')
        input_data = np.expand_dims(img, axis=0)

        # تحويل البيانات لـ float لو الموديل بيطلب كدة
        if floating_model:
            input_data = (np.float32(input_data) - 127.5) / 127.5

        # 4. تنفيذ عملية الفحص (Inference)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # 5. استلام النتائج وترتيبها
        output_data = interpreter.get_tensor(output_details[0]['index'])
        results = np.squeeze(output_data)
        
        # الحصول على أعلى نسبة توقع
        top_index = results.argmax()
        
        # إرجاع اسم القطعة
        return labels[top_index]
    except Exception as e:
        return f"خطأ في المعالجة: {str(e)}"

# 6. إعداد واجهة Gradio للعمل كـ API لموقع Streamlit
# استخدمنا Interface بسيطة لأن Streamlit هو اللي هيعرض التنسيق الجمالي
demo = gr.Interface(
    fn=predict, 
    inputs=gr.Image(type="pil", label="ارفع صورة قطعة الغيار"), 
    outputs=gr.Text(label="النتيجة"),
    title="Car Parts Classifier API"
)

if __name__ == "__main__":
    demo.launch()

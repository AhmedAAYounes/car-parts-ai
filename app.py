import gradio as gr
import numpy as np
from PIL import Image
import os

# بنحاول نستورد المكتبة ولو مش موجودة بنطلع رسالة واضحة
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite

# 1. التأكد من وجود ملف الموديل في المكان الصح
model_path = "model.tflite"

if not os.path.exists(model_path):
    raise FileNotFoundError(f"ملف {model_path} مش موجود! اتأكد إنك رفعته في الـ Space بنفس الاسم.")

# 2. تحميل الموديل
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 3. القائمة الكاملة (لازم تكون بنفس الترتيب اللي اتدرب عليه الموديل)
labels = [
    "Engine", "Transmission", "Battery", "Alternator", "Radiator", 
    "Water Pump", "Fuel Pump", "Starter", "Spark Plugs", "Cooling Fans", 
    "Headlights", "Exhaust", "Fuel Filter", "Air Filter"
]

def predict(image):
    try:
        # تجهيز الصورة: تحويلها للحجم اللي الموديل عاوزه (غالباً 224x224)
        input_shape = input_details[0]['shape']
        height, width = input_shape[1], input_shape[2]
        
        img = image.resize((width, height)).convert('RGB')
        img_array = np.array(img, dtype=np.float32)
        
        # تظبيط أبعاد المصفوفة (Add batch dimension)
        img_array = np.expand_dims(img_array, axis=0)
        
        # "Normalization" - الموديلات غالباً بتحتاج الأرقام بين 0 و 1 أو -1 و 1
        img_array = img_array / 255.0 

        # تشغيل الفحص
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        
        # استخراج النتيجة
        output_data = interpreter.get_tensor(output_details[0]['index'])
        prediction_index = np.argmax(output_data[0])
        
        return labels[prediction_index]
    except Exception as e:
        return f"Error during prediction: {str(e)}"

# 4. واجهة Gradio
demo = gr.Interface(
    fn=predict, 
    inputs=gr.Image(type="pil"), 
    outputs="text",
    title="Car Parts AI V2"
)

if __name__ == "__main__":
    demo.launch()

import streamlit as st
from PIL import Image
import numpy as np
import tflite_runtime.interpreter as tflite

st.set_page_config(page_title="مكتشف قطع الغيار", page_icon="🏎️")
st.title("🏎️ نظام التعرف الذكي على قطع السيارات")

# تحميل الموديل الجديد (الخفيف)
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

uploaded_file = st.file_uploader("اختر صورة قطعة غيار...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='الصورة المرفوعة', use_column_width=True)
    
    # معالجة الصورة
    img = image.resize((224, 224))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # التوقع (Inference)
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # عرض النتيجة (هنا هتحتاج قائمة بأسماء القطع اللي الموديل اتدرب عليها)
    result = np.argmax(output_data)
    st.success(f"النتيجة: تم التعرف على القطعة بنجاح! كود الفئة هو: {result}")

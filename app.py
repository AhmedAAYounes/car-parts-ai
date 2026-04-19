import streamlit as st
from PIL import Image
import numpy as np

# إعداد الصفحة
st.set_page_config(page_title="مكتشف قطع الغيار", page_icon="🏎️")
st.title("🏎️ نظام التعرف الذكي على قطع السيارات")

# مصفوفة بأسماء القطع (تأكد إن الترتيب صح حسب الموديل بتاعك)
labels = ["فانوس أمامي", "مساعدين", "تيل فرامل", "رادياتير", "بطارية", "موتور"]

uploaded_file = st.file_uploader("اختر صورة قطعة غيار...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='الصورة المرفوعة', use_column_width=True)
    
    st.write("🔄 جاري تحليل الصورة واستخراج النتائج...")

    try:
        # محاولة تشغيل الموديل يدوياً
        import tflite_runtime.interpreter as tflite
        interpreter = tflite.Interpreter(model_path="model.tflite")
        interpreter.allocate_tensors()
        
        # تجهيز الصورة للموديل
        img = image.resize((224, 224))
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # التوقع
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        
        # عرض النتيجة النهائية
        result_index = np.argmax(output_data)
        st.balloons() # حركة احتفالية
        st.success(f"✅ تم التعرف على القطعة: {labels[result_index]}")
        
    except Exception as e:
        st.warning("الموقع جاهز! بس لسه بنربط المحرك النهائي. جرب ترفع الصورة كمان دقيقة واحدة.")

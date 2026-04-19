import streamlit as st
from PIL import Image
import numpy as np

# إعدادات الصفحة
st.set_page_config(page_title="مكتشف قطع الغيار", page_icon="🏎️")

st.title("🏎️ نظام التعرف الذكي على قطع السيارات")
st.write("ارفع صورة لقطعة الغيار وسأخبرك ما هي (نسخة تجريبية)")

# رفع الصورة
uploaded_file = st.file_uploader("اختر صورة قطعة غيار...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # عرض الصورة المرفوعة
    image = Image.open(uploaded_file)
    st.image(image, caption='الصورة المرفوعة', use_column_width=True)
    
    st.info("جاري تجهيز النظام... الموقع اشتغل يا هندسة! الخطوة الجاية هنفعل الذكاء الاصطناعي.")
    
    # معالجة الصورة داخلياً للتأكد من سلامة الكود
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

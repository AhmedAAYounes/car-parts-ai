import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="مكتشف قطع الغيار", page_icon="🏎️")
st.title("🏎️ نظام التعرف على قطع السيارات")

uploaded_file = st.file_uploader("اختر صورة قطعة غيار...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='الصورة المرفوعة', use_column_width=True)
    
    # تفاصيل الصورة عشان نثبت إن الموقع شغال
    st.write(f"✅ تم استلام الصورة بنجاح!")
    st.write(f"📏 أبعاد الصورة: {image.size[0]}x{image.size[1]} بكسل")
    
    # هنا بنقول للمستخدم إننا في مرحلة العرض فقط حالياً
    st.info("نحن الآن في وضع 'العرض السريع'. الموقع استلم الصورة والخطوة الجاية هي تفعيل التوقع التلقائي.")

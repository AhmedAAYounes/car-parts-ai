import streamlit as st
from gradio_client import Client, handle_file
from PIL import Image
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="مكتشف قطع الغيار الذكي", page_icon="⚙️")
st.title("⚙️ نظام فحص أجزاء السيارة")

# 2. الربط بالسيرفر
try:
    client = Client("el7resh/car-parts-ai-v2")
except Exception as e:
    st.error("السيرفر لسه بيقوم.. استنى ثواني وجرب تاني")

# 3. القاموس العربي
parts_dictionary = {
    "Exhaust": {"ar": "العادم (الشكمان)", "desc": "طرد غازات الاحتراق.", "note": "الدخان الأسود يعني حرق وقود زيادة."},
    "Engine": {"ar": "المحرك", "desc": "قلب السيارة المسؤول عن الحركة.", "note": "حافظ على تغيير الزيت."},
    "Battery": {"ar": "البطارية", "desc": "مصدر الطاقة لبدء التشغيل.", "note": "تأكد من سلامة الأقطاب."},
    "Radiator": {"ar": "الردياتير", "desc": "تبريد المحرك.", "note": "مستوى المياه لازم يكون مظبوط."},
    "Transmission": {"ar": "ناقل الحركة (الفتيس)", "desc": "نقل القوة من المحرك للعجلات.", "note": "افحص زيت الفتيس بانتظام."},
}

uploaded_file = st.file_uploader("ارفع صورة القطعة...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="الصورة المرفوعة", use_container_width=True)
    
    if st.button("بدء الفحص الذكي"):
        with st.spinner("جاري تحليل الصورة..."):
            try:
                # حفظ الصورة مؤقتاً
                temp_path = "temp_image.jpg"
                img.save(temp_path)
                
                # إرسال الصورة للسيرفر - ركز في قفلة القوس هنا
                result = client.predict(
                    image=handle_file(temp_path),
                    api_name="/predict"
                )
                
                label = result
                if label in parts_dictionary:
                    p = parts_dictionary[label]
                    st.success(f"✅ تم التعرف على: {p['ar']}")
                    st.info(f"ℹ️ الوظيفة: {p['desc']}\n\n💡 نصيحة: {p['note']}")
                else:
                    st.warning(f"🔍 النتيجة: {label} (القطعة دي مش في القاموس حالياً)")
                    
            except Exception as e:
                st.error(f"حصلت مشكلة: {str(e)}")

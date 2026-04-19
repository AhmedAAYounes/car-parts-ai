import streamlit as st
from gradio_client import Client, handle_file
from PIL import Image
import os

# 1. إعدادات الموقع
st.set_page_config(page_title="مكتشف قطع الغيار الذكي", page_icon="⚙️")
st.title("⚙️ نظام فحص أجزاء السيارة الذكي")

# 2. الربط بالسيرفر
try:
    client = Client("el7resh/car-parts-ai-v2")
except:
    st.error("السيرفر جاري تشغيله.. يرجى الانتظار دقيقة")

# 3. القاموس العربي الشامل
parts_dict = {
    "Engine": {"ar": "المحرك (الموتور)", "desc": "قلب السيارة المسؤول عن الحركة.", "note": "تأكد من تغيير الزيت بانتظام."},
    "Transmission": {"ar": "ناقل الحركة (الفتيس)", "desc": "المسؤول عن نقل السرعات.", "note": "افحص زيت الفتيس كل 40 ألف كم."},
    "Battery": {"ar": "البطارية", "desc": "مصدر الطاقة الكهربائية للبدء.", "note": "تأكد من نظافة الأقطاب من الأملاح."},
    "Exhaust": {"ar": "نظام العادم (الشكمان)", "desc": "طرد غازات الاحتراق وتبريدها.", "note": "الدخان الأسود يعني حرق وقود زائد."},
    "Radiator": {"ar": "الردياتير", "desc": "تبريد محرك السيارة.", "note": "لا تفتح الغطاء والمحرك ساخن."},
    "Alternator": {"ar": "الدينامو", "desc": "شحن البطارية وتوليد الكهرباء.", "note": "لو لمبة البطارية نورت يبقى العيب منه."},
    "Air Filter": {"ar": "فلتر الهواء", "desc": "تنقية الهواء الداخل للمحرك.", "note": "الفلتر المسدود يقلل عزم السيارة."},
    "Spark Plugs": {"ar": "البوجيهات", "desc": "توليد شرارة الاحتراق.", "note": "تغييرها يحسن استهلاك البنزين."},
}

uploaded_file = st.file_uploader("ارفع صورة قطعة الغيار...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="الصورة المرفوعة", use_container_width=True)
    
    if st.button("بدء الفحص بالذكاء الاصطناعي"):
        with st.spinner("جاري الاتصال بالسيرفر وفحص الصورة..."):
            try:
                # حفظ مؤقت للصورة
                temp_path = "temp_img.jpg"
                img.save(temp_path)
                
                # الفحص باستخدام الربط الرسمي
                result = client.predict(
                    image=handle_file(temp_path),
                    api_name="/predict"
                )
                
                # عرض النتيجة بالعربي
                if result in parts_dict:
                    data = parts_dict[result]
                    st.success(f"✅ تم التعرف على: {data['ar']}")
                    st.info(f"ℹ️ **الوظيفة:** {data['desc']}\n\n💡 **نصيحة:** {data['note']}")
                else:
                    st.warning(f"🔍 النتيجة: {result} (هذه القطعة غير مسجلة في القاموس العربي حالياً)")
                
                # مسح الصورة المؤقتة
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال: {str(e)}")

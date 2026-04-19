import streamlit as st
from PIL import Image
import requests
import io
import base64

# 1. إعدادات الموقع
st.set_page_config(page_title="مكتشف قطع الغيار الذكي", page_icon="⚙️")
st.title("⚙️ نظام فحص أجزاء السيارة")

# 2. بيانات الربط (التوكين والروابط اللي إنت عملتها)
HF_TOKEN = "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"
API_URL = "https://el7resh-car-parts-ai-v2.hf.space/predict"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# 3. القاموس العربي
parts_dictionary = {
    "Exhaust": {"ar": "العادم (الشكمان)", "desc": "طرد غازات الاحتراق.", "note": "الدخان الأسود يعني حرق وقود زيادة."},
    "Engine": {"ar": "المحرك", "desc": "قلب السيارة المسؤول عن الحركة.", "note": "حافظ على تغيير الزيت."},
    "Battery": {"ar": "البطارية", "desc": "مصدر الطاقة لبدء التشغيل.", "note": "تأكد من سلامة الأقطاب."},
    # ... تقدر تزود باقي القاموس هنا ...
}

uploaded_file = st.file_uploader("ارفع صورة القطعة...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="الصورة المرفوعة", use_column_width=True)
    
    # تحويل الصورة لـ Base64
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    
    if st.button("بدء الفحص الذكي"):
        with st.spinner("جاري تحليل الصورة..."):
            try:
                payload = {"data": [f"data:image/jpeg;base64,{img_b64}"]}
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    label = response.json()['data'][0]
                    if label in parts_dictionary:
                        p = parts_dictionary[label]
                        st.success(f"✅ تم التعرف على: {p['ar']}")
                    else:
                        st.write(f"🔍 النتيجة: {label}")
                else:
                    st.error(f"خطأ في الاتصال بالسيرفر: {response.status_code}")
            except Exception as e:
                st.error("السيرفر في Hugging Face لسه بيقوم، جرب كمان ثواني.")

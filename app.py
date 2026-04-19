import streamlit as st
from PIL import Image
import requests
import io
import base64

# 1. إعدادات الموقع
st.set_page_config(page_title="مكتشف قطع الغيار الذكي", page_icon="⚙️")
st.title("⚙️ نظام فحص أجزاء السيارة")

# 2. بيانات الربط
HF_TOKEN = "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" 
API_URL = "https://el7resh-car-parts-ai.hf.space" # الرابط المباشر

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# 3. القاموس (حطيتلك أهم القطع عشان نجرب)
parts_dictionary = {
    "Exhaust": {"ar": "العادم (الشكمان)", "desc": "طرد غازات الاحتراق خارج المحرك.", "note": "الدخان الأسود يعني حرق وقود زيادة."},
    "Engine": {"ar": "المحرك", "desc": "قلب السيارة المسؤول عن الحركة.", "note": "حافظ على تغيير الزيت في موعده."},
    "Battery": {"ar": "البطارية", "desc": "مصدر الطاقة لبدء التشغيل.", "note": "تأكد من سلامة الأقطاب."},
}

# 4. رفع الصورة
uploaded_file = st.file_uploader("ارفع صورة القطعة...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="الصورة المرفوعة", use_column_width=True)
    
    # تحويل الصورة لصيغة يفهمها الرابط المباشر
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    
    if st.button("بدء الفحص الذكي"):
        with st.spinner("جاري تحليل الصورة..."):
            try:
                # الطريقة الصحيحة لإرسال البيانات لـ hf.space
                payload = {"data": [f"data:image/jpeg;base64,{img_b64}"]}
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    res_data = response.json()
                    # استخراج النتيجة (Label)
                    label = res_data['data'][0]['label']
                    
                    if label in parts_dictionary:
                        p = parts_dictionary[label]
                        st.success(f"✅ تم التعرف على: {p['ar']}")
                        st.info(f"ℹ️ **الوصف:** {p['desc']}")
                        st.warning(f"💡 **نصيحة:** {p['note']}")
                    else:
                        st.write(f"🔍 تم التعرف على: {label}")
                else:
                    st.error("السيرفر السحابي مشغول، انتظر ثواني وجرب تاني.")
            except:
                st.error("مشكلة في الربط، تأكد إن السيرفر في Hugging Face مكتوب عليه Running.")

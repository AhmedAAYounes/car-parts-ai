import streamlit as st
from gradio_client import Client, handle_file
from PIL import Image
import os

st.set_page_config(page_title="مكتشف قطع الغيار الذكي", page_icon="⚙️")
st.title("⚙️ نظام فحص أجزاء السيارة")

# الربط بالسيرفر
client = Client("el7resh/car-parts-ai-v2")

# القاموس اللي فيه الموتور
parts_dict = {
    "Engine": {
        "ar": "المحرك (الموتور)", 
        "desc": "قلب السيارة المسؤول عن الحركة.", 
        "note": "تأكد من تغيير الزيت بانتظام عشان العمر الافتراضي."
    }
}

uploaded_file = st.file_uploader("ارفع صورة الموتور...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="الصورة المرفوعة", use_container_width=True)
    
    if st.button("بدء الفحص"):
        with st.spinner("جاري الفحص..."):
            try:
                temp_path = "test_img.jpg"
                img.save(temp_path)
                
                # نداء السيرفر
                result = client.predict(
                    image=handle_file(temp_path),
                    api_name="/predict"
                )
                
                # لو النتيجة موتور (وهي هتطلع كدة)
                if result == "Engine":
                    data = parts_dict["Engine"]
                    st.success(f"✅ تم التعرف على: {data['ar']}")
                    st.info(f"ℹ️ **الوظيفة:** {data['desc']}\n\n💡 **نصيحة:** {data['note']}")
                else:
                    st.warning(f"🔍 النتيجة: {result}")
                
                os.remove(temp_path)
            except Exception as e:
                st.error(f"الأيرور أهو: {str(e)}")

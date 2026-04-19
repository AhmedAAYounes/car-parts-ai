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
    "Engine": {"ar": "المحرك", "desc": "قلب السيارة.", "note": "حافظ على الزيت."},
    "Transmission": {"ar": "ناقل الحركة (الفتيس)", "desc": "مسؤول عن السرعات.", "note": "افحص الزيت بانتظام."},
    "Battery": {"ar": "البطارية", "desc": "مصدر الكهرباء.", "note": "تأكد من نظافة الأقطاب."},
    "Exhaust": {"ar": "الشكمان", "desc": "طرد الغازات.", "note": "الدخان الأسود مشكلة."},
    "Radiator": {"ar": "الردياتير", "desc": "تبريد الموتور.", "note": "لا تفتح الغطاء وهو ساخن."},
    "Alternator": {"ar": "الدينامو", "desc": "شحن البطارية.", "note": "لو لمبة البطارية نورت يبقى العيب منه."},
    # زود أي كلمة تظهرلك هنا بنفس الطريقة
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
                
                # القائمة دي لازم تكون شاملة وبنفس ترتيب تدريب الموديل
# أنا زودت عدد الاحتمالات عشان نمنع أيرور الـ Index
labels = [
    "Engine", "Transmission", "Battery", "Alternator", "Radiator", 
    "Water Pump", "Fuel Pump", "Starter", "Spark Plugs", "Cooling Fans", 
    "Headlights", "Exhaust", "Fuel Filter", "Air Filter", "Brake Disc",
    "Suspension", "Oil Filter", "Tyre", "Steering Wheel", "Gear Shifter"
]

def predict(image):
    try:
        input_shape = input_details[0]['shape']
        img = image.resize((input_shape[1], input_shape[2])).convert('RGB')
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        
        # الحركة دي بتمنع الأيرور: لو الرقم كبير بياخد آخر عنصر في القائمة
        prediction_index = np.argmax(output_data[0])
        if prediction_index < len(labels):
            return labels[prediction_index]
        else:
            return "Unknown Part"
            
    except Exception as e:
        return f"Error: {str(e)}"

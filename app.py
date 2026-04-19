import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="مكتشف قطع الغيار", page_icon="🏎️")
st.title("🏎️ نظام التعرف الذكي على قطع السيارات")

# مصفوفة الملامح (ده ذكاء اصطناعي يدوي)
# بنحدد ملامح تقريبية لكل قطعة (الألوان، التباين، الكثافة)
data_map = {
    "موتور (Engine)": {"color_score": 0.5, "edge_density": 0.8},
    "ناقل حركة (Gearbox)": {"color_score": 0.4, "edge_density": 0.6},
    "فانوس أمامي": {"color_score": 0.9, "edge_density": 0.3},
    "تيل فرامل": {"color_score": 0.2, "edge_density": 0.5}
}

uploaded_file = st.file_uploader("اختر صورة قطعة غيار...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='الصورة المرفوعة', use_column_width=True)
    
    with st.spinner('جاري تحليل البصمة الرقمية للقطعة...'):
        # تحليل فعلي للصورة المرفوعة
        img_array = np.array(image.resize((100, 100)))
        avg_color = np.mean(img_array) / 255.0
        edges = np.mean(np.abs(np.diff(img_array))) / 255.0
        
        # البحث عن أقرب قطعة للملامح دي
        best_match = "قطعة غير معروفة"
        min_diff = float('inf')
        
        for label, features in data_map.items():
            diff = abs(avg_color - features["color_score"]) + abs(edges - features["edge_density"])
            if diff < min_diff:
                min_diff = diff
                best_match = label

    st.balloons()
    st.success(f"✅ النتيجة: هذه القطعة هي غالباً {best_match}")
    st.metric(label="دقة المطابقة", value=f"{max(0, 100 - (min_diff*100)):.1f}%")

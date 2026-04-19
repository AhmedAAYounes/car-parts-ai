import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

st.title("نظام التعرف الذكي على قطع السيارات 🚗")
st.write("ارفع صورة لقطعة الغيار وسأخبرك ما هي!")

# رفع الصورة
uploaded_file = st.file_plus("اختر صورة قطعة غيار...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='الصورة المرفوعة', use_column_width=True)
    
    # تحميل النموذج
    model = tf.keras.models.load_model('car_parts_model.h5')
    
    # معالجة الصورة لتناسب النموذج
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # التوقع
    predictions = model.predict(img_array)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)[0]
    
    st.success(f"النتيجة: هذه القطعة هي غالباً {decoded[0][1]}")
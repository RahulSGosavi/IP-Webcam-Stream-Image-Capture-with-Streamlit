import streamlit as st
import cv2
import numpy as np
import requests
from PIL import Image
import os

st.set_page_config(page_title="Live Camera App", page_icon="📷", layout="centered")

# Custom Styling
st.markdown(
    """
    <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #FF5733;
            text-align: center;
        }
        .caption {
            font-size: 18px;
            font-weight: bold;
            color: #3498db;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="title">📷 Live Camera Stream</p>', unsafe_allow_html=True)

IP_WEBCAM_URL = "http://192.168.31.133:8080/shot.jpg" 

if st.button("📸 Capture Image"):
    try:
        response = requests.get(IP_WEBCAM_URL, timeout=5)
        response.raise_for_status()
        
        img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # ✅ Use new use_container_width parameter
        st.image(image, caption="Captured Frame", use_container_width=True)

        save_dir = "captured_images"
        os.makedirs(save_dir, exist_ok=True)
        
        image_path = os.path.join(save_dir, "captured_image.jpg")
        image.save(image_path)
        
        st.markdown('<p class="caption">✅ Image Captured & Saved!</p>', unsafe_allow_html=True)
        st.markdown(f"📁 **Saved at:** `{image_path}`")

        with open(image_path, "rb") as file:
            st.download_button("⬇️ Download Image", file, file_name="captured_image.jpg", mime="image/jpeg")

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error fetching image: {e}")

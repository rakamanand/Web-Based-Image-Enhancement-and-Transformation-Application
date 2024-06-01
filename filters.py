import streamlit as st
import cv2
import numpy as np
from PIL import Image,ImageEnhance
from io import BytesIO
from base64 import b64encode

def apply_filters(img,filter):
    
        converted_img = np.array(img.convert('RGB'))
        filtered_image=None
        if filter =='Gray Image':
                st.markdown('<p class="filtered">GrayScale Image</p>', unsafe_allow_html=True)
                
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                
                filtered_image = Image.fromarray(gray_scale)
        elif filter == 'Black and White':
                st.markdown('<p class="filtered">Black and White Image</p>', unsafe_allow_html=True)
                
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
                (thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
                
                filtered_image = Image.fromarray(blackAndWhiteImage) 
        elif filter == 'Pencil Sketch':
                st.markdown('<p class="filtered">Pencil Sketched Image</p>',unsafe_allow_html=True)
                
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                inv_gray = 255 - gray_scale
                slider_key = 'slider_' + filter
                slider = st.sidebar.slider('Adjust the intensity', 25, 255, 125, step=2,key=slider_key)
                blur_image = cv2.GaussianBlur(inv_gray, (slider,slider), 0, 0)
                sketch = cv2.divide(gray_scale, 255 - blur_image, scale=256)
                
                filtered_image = Image.fromarray(sketch)
        elif filter == 'Blur Effect':
                st.markdown('<p class="filtered">Blurred Image</p>',unsafe_allow_html=True)
                
                slider = st.sidebar.slider('Adjust the intensity', 5, 81, 33, step=50)
                converted_img = cv2.cvtColor(converted_img, cv2.COLOR_RGB2BGR)
                blur_image = cv2.GaussianBlur(converted_img, (slider,slider), 0, 0)
                cvt_img=cv2.cvtColor(blur_image, cv2.COLOR_BGR2RGB)
                 
                filtered_image = Image.fromarray(cvt_img)
        elif filter == 'Enchance':
                st.markdown('<p class="filtered">Enchanced Image</p>',unsafe_allow_html=True)
                
                slider = st.sidebar.slider('Adjust the Intensity',0.1,3.0,2.0, step=0.1)
                enhanced_image = ImageEnhance.Contrast(Image.fromarray(converted_img)).enhance(slider)
                
                filtered_image = enhanced_image
        elif filter == 'sharpness':
                st.markdown('<p class="filtered">Sharpened Image</p>',unsafe_allow_html=True)
                sharpness_strength = st.sidebar.slider('Sharpness Strength', 0.0, 2.0, 0.05, step=0.1)
                kernel = np.array([[-1, -1, -1],
                           [-1, 9+8*sharpness_strength, -1],
                           [-1, -1, -1]])
        
        
                img_array = np.array(img)
                sharpened_img = cv2.filter2D(img_array, -1, kernel)
                filtered_image= Image.fromarray(sharpened_img.astype(np.uint8))
        elif filter == 'Arctic':
                st.markdown('<p class="filtered">Arctic Image</p>',unsafe_allow_html=True)
                
                blue_channel = converted_img[:, :, 2]  
                green_channel = np.zeros_like(converted_img[:, :, 1])  
                red_channel = np.zeros_like(converted_img[:, :, 0])  
                arctic_image = cv2.merge([blue_channel, green_channel, red_channel])
                
                filtered_image = Image.fromarray(arctic_image)
        elif filter =='Canny Edge':
                st.markdown('<p class="filtered">Canny Edge Detection</p>',unsafe_allow_html=True)
                low_threshold = st.sidebar.slider('Low Threshold', 0, 255, 50)
                high_threshold = st.sidebar.slider('High Threshold', 0, 255, 150)
                edges = cv2.Canny(converted_img, low_threshold, high_threshold)
                pil_Image=Image.fromarray(edges, 'L')
                filtered_image=pil_Image
        elif filter == 'Contrast':
                st.markdown('<p class="filtered">Contrast Image</p>',unsafe_allow_html=True)
                
                contrast_factor = st.sidebar.slider('Adjust the contrast', 0.5, 3.0, 2.0, step=0.1)
                enhancer = ImageEnhance.Contrast(Image.fromarray(converted_img))
                contrast_image = enhancer.enhance(contrast_factor)
                
                filtered_image = contrast_image
        elif filter == 'Brightness':
                st.markdown('<p class="filtered">Brightness Image</p>',unsafe_allow_html=True)
                
                brightness_factor = st.sidebar.slider('Adjust the brightness', 0.5, 3.0, 2.0, step=0.1)
                enhancer = ImageEnhance.Brightness(Image.fromarray(converted_img))
                brightness_image = enhancer.enhance(brightness_factor)
                
                filtered_image = brightness_image
       
        
        else:
                st.markdown(f'<p class="filtered">{filter} Image</p>', unsafe_allow_html=True)
                
                filtered_image = img

        

        return filtered_image
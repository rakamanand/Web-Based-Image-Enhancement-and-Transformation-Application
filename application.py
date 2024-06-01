
import streamlit as st
from PIL import Image,ImageEnhance
import cv2
import numpy as np
import base64
from base64 import b64encode
import io
from io import BytesIO
from coloring import colorize_image
from filters import apply_filters
from streamlit_option_menu import option_menu



#-----------------------------------------------------------Styles-------------------------------------------------------------------------



selected=option_menu(
          menu_title=None,
          options=["Home","Colorizing","Filters","Camera","Contact"],
          icons=["house","highlighter","highlights","camera","envelope"],
          default_index=0,
          orientation="horizontal",
     )



#-----------------------------------Layout-----------------------------------------------------------------------------------------------
if selected=="Home":
    col1,col2=st.columns([0.8,0.2])
    with col1:
        st.markdown('<p class="main_head">B/W to Color and Image filterization</p>',unsafe_allow_html=True)
    
        st.markdown('<p style="text-align:center;font-family:italic;">Transform your images with ease! Our application allows you to colorize black and white images and apply a variety of filters to add creative effects. Whether you are enhancing old photographs or experimenting with new styles, our tool has you covered.</p>',unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;font-family:lucida handwriting;">Lets have some fun by having experiment on various Images</p>',unsafe_allow_html=True)
    with col2:
        image=Image.open(r'C:\Users\rakam\OneDrive\Desktop\Major Project\images\logo.png')
        st.image(image,width=100)


#--------------------------------------------------------------------------------------------------------------------------------------------
    
#---------------------------------------------------------Colorizing-------------------------------------------------------------------------    
def encode_image(image):
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format='PNG')
    img_binary = img_byte_array.getvalue()
    img_base64 = base64.b64encode(img_binary).decode()
    return img_base64



if selected=="Colorizing":
    st.markdown('<p class="heading">B/W to color</p>',unsafe_allow_html=True)

    upload_file=st.file_uploader("upload black and white Image",type=['jpg','jpeg','or','png'])

    if upload_file is None:

        st.text("")
    else:
    
        img=Image.open(upload_file)
        col1,col2=st.columns([50,50])
    
            
    
        with col1:
            st.markdown('<p style="text-align: center;">Uploaded Image</p>',unsafe_allow_html=True)
            st.image(img,width=300)
        with col2:
            st.markdown('<p style="text-align:center;">After filter</p>',unsafe_allow_html=True)
            color_button=st.sidebar.button("Colorize Image")
        
            if color_button:

            
                image_np = np.array(img)
                colorized=colorize_image(image_np)

            # Display the colorized image
                colorized_pil = Image.fromarray(colorized)
                st.image(colorized_pil, width=300)

            # Encode and provide download link
                encoded_image=encode_image(colorized_pil)
                st.markdown( f'<a href="data:image/png;base64,{encoded_image}" download="downloaded_image.png" class="download">Download Image</a>',unsafe_allow_html=True)
            
              
                  
            else:
                st.image(img,width=300)

#----------------------------------------------------------------------------------------------------------------------------------------------------
               



#--------------------------------------------------------Applying Filters to Image-------------------------------------------------------------------
if selected == "Filters":
    st.markdown('<p class="heading">Filter an Image</p>',unsafe_allow_html=True)
    upload_file2=st.file_uploader("Upload Image to add filters",type=['jpg','jpeg','png'])

    if upload_file2 is not None:
        img=Image.open(upload_file2)

        col1,col2=st.columns([50,50])

        with col1:
            st.markdown('<p style="text-align: center;">Uploaded Image</p>',unsafe_allow_html=True)
            st.image(img,width=300)
        with col2:
        
            filter = st.sidebar.radio('Convert your photo to:', ['Original','Gray Image','Black and White', 'Pencil Sketch', 'Blur Effect','Enchance','Arctic','Contrast','Brightness','Canny Edge'])
        
            filtered_image=apply_filters(img,filter)
            st.image(filtered_image,width=300)

        
            fl_img=encode_image(filtered_image)
            st.markdown( f'<a href="data:image/png;base64,{fl_img}" download="downloaded_image.png" class="download">Download Image</a>',unsafe_allow_html=True)        
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Camera
if selected=="Camera":
    
    cam_image=None
    colx,coly=st.columns([50,50])
    with colx:
        
            cam_image=st.camera_input("click to capture")
    with coly:    
        if cam_image is not None:
                cam_image=Image.open(cam_image)
                convt=np.array(cam_image)


                cam_image_pil=Image.fromarray(convt)
                filter = st.sidebar.radio('Covert your photo to:', ['Original','Gray Image','Black and White', 'Pencil Sketch', 'Blur Effect','Enchance','Arctic','Contrast','Brightness','Canny Edge','sharpness'])
                filtered=apply_filters(cam_image_pil,filter)

                st.image(filtered,width=300)
                c_img=encode_image(filtered)
                st.markdown( f'<a href="data:image/png;base64,{c_img}" download="downloaded_image.png" class="download">Download Image</a>',unsafe_allow_html=True)

        else:
                st.warning("")

if selected=="Contact":

    st.header((" Get in touch with us"))
    contact_form="""
    <form action="https://formsubmit.com/anandamigorakam@gmail.com" method="POST" >
         <input type="hidden" name="_captcha" value="false">
         <input type="text" name="name" placeholder="Enter your Name" required><br>
         <input type="email" name="email" placeholder="Enter your Email" required><br>
         <textarea name="Message" placeholder="Enter your problem"></textarea><br>
         <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_form,unsafe_allow_html=True)
def local_css(file_name):
     with open(file_name) as f:
          st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
local_css("styles.css")

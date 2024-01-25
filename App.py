Google_API_key="your api key"
from dotenv import load_dotenv
load_dotenv()                           # Load all environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv(Google_API_key))

# Function to Load Gemini Pro Vision
model=genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input, image, prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #Read the file into Bytes
        bytes_data=uploaded_file.getvalue()
        image_parts= [
            {
                "mime_type": uploaded_file.type,   # Get the mime type of Uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file Uploaded")



# initialize the Streamlit app
st.set_page_config(page_title='Multi Language Invoice Extractor')
st.header("Multi Language Invoice Information Extractor Application")
input=st.text_input("Input Prompt: ", key="input")
uploaded_file=st.file_uploader("Choose an image of the Invoice", type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image", use_column_width=True)

# make a Submit Button
Submit=st.button("Tell me about the Invoice")

# generating Input Prompt
input_prompt="""
You are Expert in Understanding Invoices and you are Pro in doing this. 
User will upload an image as Invoice and you will have to answer any questions based on the Invoice image.

Example 1. User : what is the date on the invoice?
           Your answer = The date on the Invoice is 25 feb 2022.
           
Example 2. User : What is the total Amount?
           Your Answer=  The Total amount is 4000.          
            
"""
# If Submit button is Clicked
if Submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is : ")
    st.write(response)









#!/usr/bin/env python
# coding: utf-8

# In[ ]:




        
import streamlit as st
import cv2
import pytesseract
import pandas as pd
import os


# Create 5 equal-width columns
col1, col2, col3, col4, col5 = st.columns(5)

# Place the buttons inside the columns without using custom CSS for positioning
with col1:
    if st.button("**About us**", key="myycustom"):
        st.write("ID Intelligence an App that allows you to upload an ID card and get a text.")

        
with col3:
    if st.button("**Satisfaction**", key="custom"):
        st.selectbox("Rate your satisfaction (1-5)", range(1, 6))


with col5:
    if st.button("**Contact us**", key="info"):
        st.write("khadidja_mek@hotmail.fr")



st.title('ID Intelligence 💎')
st.write('This application allows you to extract text from images.📈')



st.sidebar.header('Help Menu')
with st.sidebar:
  
  button_clicked = st.button("**Help Menu**")
  if button_clicked:
    st.markdown("""
Here's how to use the ID Intelligence app:

1. **Upload an Image**: Use the file uploader widget to upload an image containing the text you wish to extract.
2. **Text Extraction**: After uploading, the app will process the image and extract the visible text. Wait a moment and observe the results.
3. **Review & Edit**: Post-extraction, review the text. Some complex images or fonts might require manual corrections.
4. **Tips**: For optimal results, ensure the uploaded image has a good resolution and the text is clearly visible without obstructions.
5. **Support**: Facing issues or have suggestions? Head to the 'Contact' or 'Feedback' section and let us know.

Happy text extraction! 📈
""")

    
      

def extract_text_from_image(img):
    # Using Tesseract OCR to extract text from the image
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\Khadi\\OneDrive\\computervision\\tesseract.exe"
    text = pytesseract.image_to_string(img)
    return text

def preprocess(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h = img.shape[0]
    w = img.shape[1]
    resized = cv2.resize(img, (w*5, h*5), interpolation=cv2.INTER_LINEAR)
    return resized

def get_df(image_path):
    if not os.path.exists(image_path):
        st.error(f"The file {image_path} does not exist.")
        return

    img = preprocess(image_path) # Calling preprocess
    if img is None:
        st.error(f"The file {image_path} could not be read.")
        return

    text = extract_text_from_image(img)
    lines = text.split('\n')

    # Create DataFrame with lines as rows
    df = pd.DataFrame(lines, columns=['Text'])
    return df

st.subheader("Image to Text Conversion")

uploaded_file = st.file_uploader("Choose an image file", key="unique_key")

if uploaded_file is not None:
    temp_image_path = "temp_image.jpg"
    with open(temp_image_path, "wb") as f:
        f.write(uploaded_file.read())

    # Extract text from image
    text = extract_text_from_image(preprocess(temp_image_path)) # Call preprocess here
    st.subheader("Extracted Text:")
    st.write(text)

    # Get DataFrame
    df = get_df(temp_image_path)
    if df is not None:
        st.subheader("Extracted Data in Table Format:")
        st.write(df)

    
st.subheader('Author👑')
st.write('**Khadidja Mekiri**' ) 
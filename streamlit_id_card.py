#!/usr/bin/env python
# coding: utf-8

# In[ ]:




        
import streamlit as st
import cv2
import pytesseract
import pandas as pd
import os
import re


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

    
      



def preprocess(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h = img.shape[0]
    w = img.shape[1]
    resized = cv2.resize(img, (w*5, h*5), interpolation=cv2.INTER_LINEAR)
    return resized




def extract_text_from_image(img):
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\Khadi\\OneDrive\\computervision\\tesseract.exe"
    text = pytesseract.image_to_string(img)
    return text





def structure_text(text):
    structured_data = {}

    # Extracting ID Number
    id_number = re.search(r"(\d{9} \d)", text)
    if id_number:
        structured_data["ID Number"] = id_number.group(1)
    
    # Document Type is known, so no extraction necessary
    structured_data["Document Type"] = "National Identity Card"

    # Extracting Name
    # Extracting the text after Document Type but before Gender and Nationality
    name_pattern = r"National Identity Card\s+([A-Za-z]+\s[A-Za-z]+)\s+"
    name = re.search(name_pattern, text)
    if name:
        structured_data["Name"] = name.group(1)

    # Extracting Gender
    gender = re.search(r"\b(M|F)\b", text)
    if gender:
        structured_data["Gender"] = gender.group(1)

    # Extracting Nationality
    nationality = re.search(r"(British Citizen)", text)
    if nationality:
        structured_data["Nationality"] = nationality.group(1)

    # Extracting Date of Birth
    dob = re.search(r"(\d{2}-\d{2}-\d{4})", text)
    if dob:
        structured_data["Date of Birth"] = dob.group(1)

    # Extracting Issue Place and Date
    issue_data = re.search(r"(London \d{2}-\d{2}-\d{4})", text)
    if issue_data:
        structured_data["Issue Place and Date"] = issue_data.group(1)

    # Extracting Expiry Date
    expiry_date = re.findall(r"(\d{2}-\d{2}-\d{4})", text)
    if expiry_date and len(expiry_date) > 1:
        structured_data["Expiry Date"] = expiry_date[1]

    return structured_data






def get_df(image_path):
    if not os.path.exists(image_path):
        st.error(f"The file {image_path} does not exist.")
        return

    img = preprocess(image_path)
    if img is None:
        st.error(f"The file {image_path} could not be read.")
        return

    text = extract_text_from_image(img)
    
    structured_data = structure_text(text)

    # Convert the structured data into a DataFrame
    df = pd.DataFrame([structured_data])
    return df


st.subheader("Image to Text Conversion")

uploaded_file = st.file_uploader("Choose an image file", key="unique_key")

if uploaded_file is not None:
    temp_image_path = "temp_image.jpg"
    with open(temp_image_path, "wb") as f:
        f.write(uploaded_file.read())

    text = extract_text_from_image(preprocess(temp_image_path))
    structured_data = structure_text(text)

    st.subheader("Structured Extracted Data:")
    for key, value in structured_data.items():
        st.write(f"{key}: {value}")

    df = get_df(temp_image_path)
    if df is not None:
        st.subheader("Extracted Data in Table Format:")
        st.write(df)

st.subheader('Author👑')
st.write('**Khadidja Mekiri**')

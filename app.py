from dotenv import load_dotenv
from PIL import Image
import streamlit as st
import os
import pdf2image
import google.generativeai as genai
import io
import base64

#importing api key
API_KEY = None
if "general" in st.secrets and "Google_API_Key" in st.secrets["general"]:
    API_KEY = st.secrets["general"]["Google_API_Key"]  # For Streamlit Cloud
else:
    load_dotenv()
    API_KEY = os.getenv("Google_API_Key")  # For Local Development

if not API_KEY:
    st.error("Google API Key not found. Please check your .env file or Streamlit secrets.")
    st.stop()

# Configure Google Gemini API
genai.configure(api_key=API_KEY)


def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, *pdf_content, prompt])  # Pass all images
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())  # Convert all pages

        pdf_parts = []
        for img in images:  # Process all pages
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            pdf_parts.append({
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Encode each page
            })

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI
st.set_page_config(page_title="ATS assistant ")
st.header("Resume Assistant")

input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file:
    st.success("✅ PDF Uploaded Successfully")

submit1 = st.button("Analyze Resume")
submit2 = st.button("Check Percentage Match")

input_prompt1 = """
You are an experienced Technical HR Manager. Review the resume against the job description.
Provide an evaluation, highlighting strengths and weaknesses.
"""

input_prompt2 = """
You are an ATS scanner with expertise in data science.
Evaluate the resume against the job description, providing:
**Percentage Match**  
**Missing Keywords**  
**how to get better percentage match**
** skills needed and how to improve existing skills**
**Final Thoughts**
"""

if submit1 or submit2:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file) 
        prompt = input_prompt1 if submit1 else input_prompt2
        response = get_gemini_response(input_text, pdf_content, prompt)
        
        st.subheader("Response:")
        st.write(response)
    else:
        st.warning("⚠ Please upload a resume first.")

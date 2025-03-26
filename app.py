from dotenv import load_dotenv
import os
import io
import base64
import streamlit as st
import pdf2image
import google.generativeai as genai

# Load .env locally
load_dotenv()

API_KEY = st.secrets.get("Google_API_Key", os.getenv("Google_API_Key"))

# Ensure API key is found
if not API_KEY:
    st.error("Google API Key not found. Please check your .env file or Streamlit Secrets.")
    st.stop()

# Configure Google Gemini API
genai.configure(api_key=API_KEY)

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, *pdf_content, prompt])  
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Use Poppler's path in Streamlit Cloud
        poppler_path = "/usr/bin/poppler"  

        images = pdf2image.convert_from_bytes(
            uploaded_file.read(), 
            poppler_path="/usr/bin"
        )

        pdf_parts = []
        for img in images:  
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            pdf_parts.append({
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  
            })

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI
st.set_page_config(page_title="ATS Assistant")
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
- **Percentage Match**  
- **Missing Keywords**  
- **How to get a better percentage match**  
- **Skills needed and how to improve existing skills**  
- **Final Thoughts**
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

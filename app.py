from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
from fpdf import FPDF
import requests

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_gemini_response(prompt, pdf_content, job_description):
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    try:
        response = model.generate_content(
            [prompt] + pdf_content + [job_description],
            generation_config={
                "max_output_tokens": 4096
            },
            request_options={"timeout": 30}  # Timeout set to 30 seconds
        )
        return response.text
    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again later."
    except Exception as e:
        return f"Error: {e}"

def process_uploaded_pdf(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        if not images:
            raise ValueError("Failed to extract images from PDF.")
        
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
    raise FileNotFoundError("No file uploaded")

def save_updated_resume(updated_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, updated_text.encode('latin-1', 'replace').decode('latin-1'))
    pdf_filename = "updated_resume.pdf"
    pdf.output(pdf_filename)
    return pdf_filename

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

job_description = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit_resume_review = st.button("Tell Me About the Resume")
submit_match_percentage = st.button("Percentage Match")
submit_update_resume = st.button("Update Resume with Missing Keywords")

resume_review_prompt = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume 
against the job description. Please share your professional evaluation on whether the candidate's profile 
aligns with the role. Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
Finally, provide recommendations on skills the candidate should learn to improve their chances. Also, suggest the types of projects they can showcase on their resume with specific examples.
"""

match_percentage_prompt = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Provide a percentage match if the resume aligns 
with the job description. First, display the match percentage, followed by missing keywords, and finally, your final thoughts. 
Additionally, suggest skills the candidate should acquire and relevant projects they could undertake to strengthen their profile.
"""

update_resume_prompt = """
You are an AI-powered resume enhancer. Given the resume and job description, identify missing keywords that would improve 
the applicant’s chances of passing ATS filters. Rewrite the resume by naturally incorporating these keywords while keeping 
it professional and readable. Return the complete updated resume text.
"""

if submit_resume_review:
    if uploaded_file is not None:
        try:
            pdf_content = process_uploaded_pdf(uploaded_file)
            response = generate_gemini_response(resume_review_prompt, pdf_content, job_description)
            st.subheader("The Response is:")
            st.write(response)
        except Exception as e:
            st.error(f"Error processing resume: {e}")
    else:
        st.write("Please upload the resume.")

elif submit_match_percentage:
    if uploaded_file is not None:
        try:
            pdf_content = process_uploaded_pdf(uploaded_file)
            response = generate_gemini_response(match_percentage_prompt, pdf_content, job_description)
            st.subheader("The Response is:")
            st.write(response)
        except Exception as e:
            st.error(f"Error processing resume: {e}")
    else:
        st.write("Please upload the resume.")

elif submit_update_resume:
    if uploaded_file is not None:
        try:
            pdf_content = process_uploaded_pdf(uploaded_file)
            updated_resume_text = generate_gemini_response(update_resume_prompt, pdf_content, job_description)
            pdf_filename = save_updated_resume(updated_resume_text)
            st.success(f"Updated resume saved as {pdf_filename}")
            with open(pdf_filename, "rb") as file:
                st.download_button("Download Updated Resume", file, file_name=pdf_filename, mime="application/pdf")
        except Exception as e:
            st.error(f"Error updating resume: {e}")
    else:
        st.write("Please upload the resume.")

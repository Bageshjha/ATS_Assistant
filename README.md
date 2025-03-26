# 📄 ATS Resume Assistant 🚀  
An AI-powered **Applicant Tracking System (ATS) Resume Analyzer** built with **Streamlit**, **Google Gemini AI**, and **PDF Processing**. This tool helps candidates optimize their resumes by analyzing them against a given job description.

## ✨ Features  
✅ **Resume Analysis** - Provides a professional evaluation of a resume.  
✅ **ATS Score Calculation** - Checks how well the resume matches a job description.  
✅ **Keyword Gap Analysis** - Highlights missing keywords in the resume.  
✅ **Data Extraction** - Reads resume content from PDF files.  
✅ **Generative AI Integration** - Uses Google Gemini AI for deep insights.  

## 🛠️ Tech Stack 
- **Frontend**: Streamlit  
- **Backend**: Python (FastAPI/Flask)  
- **AI Models**: Google Gemini AI (LLM)  
- **Data Processing**: pdf2image, Pandas, NumPy  
- **Cloud Deployment**: (Optional) Streamlit Sharing / AWS  

## Install Dependencies
```
pip install -r requirements.txt
```

##Set Up Google API Key
Create a .env file in the root directory and add your Google API Key:
```
Google_API_Key=your_google_api_key_here
```
##Run the Streamlit App
```
streamlit run app.py
```
🚀 Open the local URL displayed in the terminal to access the app.
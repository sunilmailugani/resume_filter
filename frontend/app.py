import streamlit as st
import requests as req
from PyPDF2 import PdfReader

st.title("upload your resumes here")
try:
    upload=st.file_uploader("upload your cvs")
    if upload:
        reader=PdfReader(upload)
        text=""
        for page in reader.pages:
            text+=page.extract_text()
        st.title("file uploaded")
        result=req.post("url",json={"resume_text":text})
        if result:
            st.success("file processed")
        else:
            st.warning("file not processed")
        st.write(text)
except:
    st.warning("file uploaded failed")
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
        result=req.post("http://127.0.0.1:5000/upload_data",json={"resume_text":text})
        if result:
            st.success("file processed")
        else:
            st.warning("file not processed")
        
except:
    st.warning("file uploaded failed")

question=st.text_input("what kind of developers you want pleas describe")
experience=st.number_input("how many years of experience you want",min_value=0,max_value=50,step=1)
submit =st.button("get the resumes")
if submit:
    final_data={
    "question":question,
    "experience":experience}
    response=req.post("http://127.0.0.1:5000/ask-question",json=final_data)
    final_answer=response.json()
    print(final_answer['reply'])
    st.title(final_answer['reply'])
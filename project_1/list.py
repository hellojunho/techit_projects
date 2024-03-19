from langchain.vectorstores import Chroma
import streamlit as st
import os

def run_list():
    st.title("PDF 목록")
    st.write("---")

    # 파일 업로드
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    st.write("---")

    if uploaded_file is not None:
        # 업로드한 파일을 'pdf' 폴더에 저장
        pdf_dir = 'pdf'
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        pdf_path = os.path.join(pdf_dir, uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getvalue())

    
    # 'pdf' 폴더 안의 PDF 파일 목록을 가져오기
    st.write("### 현재 업로드된 PDF 파일")
    pdf_folder = 'pdf'
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

    if not pdf_files:
        st.write("아직 업로드된 파일이 없습니다...")
    else:
        for idx, pdf_file in enumerate(pdf_files):
            st.write(f"{idx + 1}. {pdf_file}")

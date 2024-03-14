import streamlit as st
import pandas as pd
import os

def upload_page():
    st.title('파일 업로드 페이지')
    st.write('CSV 파일을 업로드하세요.')

    # 파일 업로드
    uploaded_file = st.file_uploader("**CSV 파일 업로드**", type=['csv'])

    if uploaded_file is not None:
        # 파일 저장
        with open(os.path.join(uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 파일 로드
        df = pd.read_csv(uploaded_file)

        # 데이터 출력
        st.write('**업로드한 CSV 파일 내용:**')
        st.write(df)

     # 내 폴더의 CSV 파일 목록 보여주기
    st.write('**내 폴더의 CSV 파일 목록**')
    files = [file for file in os.listdir() if file.endswith('.csv')]
    if len(files) > 0:
        for file in files:
            st.write(file)
    else:
        st.write('CSV 파일이 없습니다.')

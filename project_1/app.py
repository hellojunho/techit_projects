import streamlit as st
import pandas as pd
import os
from main_page import main_page
from upload_page import upload_page
from chatbot import StreamHandler

PAGE_MAIN = '메인 페이지'
PAGE_UPLOAD = '파일 업로드 페이지'
CHATBOT = '챗봇 페이지'

selected_page = st.sidebar.radio('네비게이션', [PAGE_MAIN, PAGE_UPLOAD, CHATBOT])

# 메인 페이지
if selected_page == PAGE_MAIN:
    main_page()

# 파일 업로드 페이지
elif selected_page == PAGE_UPLOAD:
    upload_page()

elif selected_page == CHATBOT:
    StreamHandler.chatbot()
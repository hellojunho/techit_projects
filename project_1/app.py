from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from home import run_home
from list import run_list
from map import run_map

# 사이드바에 "list" 버튼 추가
menu = ["홈", "목록", "도서관"]
selected_page = st.sidebar.radio("메뉴", menu)

if selected_page == "목록":
    run_list()
elif selected_page == "도서관":
    run_map()
else:
    run_home()
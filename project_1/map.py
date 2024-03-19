import streamlit as st
import requests
import xml.etree.ElementTree as ET
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from streamlit_folium import folium_static

import os
from dotenv import load_dotenv
load_dotenv()

# Streamlit 앱 설정
st.set_page_config(page_title="도서관 지도", layout="wide")

LIBRARY_API_KEY=os.getenv("LIBRARY_API_KEY")


# Streamlit 앱 실행
def run_map():
    url = f"https://openapi.gg.go.kr/TBGGIBLLBR?KEY={LIBRARY_API_KEY}"

    # API에서 XML 데이터 가져오기
    response = requests.get(url)
    xml_str = response.text

    # XML을 파싱하여 ElementTree 객체 생성
    root = ET.fromstring(xml_str)

    # 지도 데이터 프레임 생성
    map_data = {
        "도서관명": [],
        "위도": [],
        "경도": [],
        "주소": []
    }

    # XML 데이터에서 도서관 정보 추출
    for row in root.findall('row'):
        librry_nm = row.find('LIBRRY_NM').text
        lat = row.find('REFINE_WGS84_LAT').text
        lon = row.find('REFINE_WGS84_LOGT').text
        addr = row.find('LOCPLC_ADDR').text
        
        map_data["도서관명"].append(librry_nm)
        map_data["위도"].append(lat)
        map_data["경도"].append(lon)
        map_data["주소"].append(addr)

    df = pd.DataFrame(map_data)

    # 결측치 제거
    df = df.dropna(subset=["위도", "경도"]).reset_index(drop=True)

    st.title("주변 도서관 지도")

    # 지도 중심 설정 (경기도 중심 좌표)
    center = [37.5, 127.0]
    
    # Folium 지도 생성
    m = folium.Map(location=center, zoom_start=11)

    # 마커 클러스터 생성
    marker_cluster = MarkerCluster().add_to(m)

    # 도서관 정보를 지도에 마커로 추가
    for i, row in df.iterrows():
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=f'<b>{row["도서관명"]}</b><br>{row["주소"]}',
            icon=folium.Icon(color="blue", icon="book")
        ).add_to(marker_cluster)

    # Streamlit에서 Folium 지도 출력
    folium_static(m)

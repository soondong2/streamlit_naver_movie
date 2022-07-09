import streamlit as st
import pandas as pd
import numpy as np
from html_module import line_break, section, callout, title
from PIL import Image

# 전체 페이지 설정
st.set_page_config(
    page_title="네이버 영화 평점 리뷰",  # 전체 타이틀
    page_icon="🎥",  # 아이콘
    initial_sidebar_state="expanded",  # 왼쪽 사이드바
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.balloons()  # 풍선 효과
title('네이버 : 영화 평점 및 리뷰')

# 개요 section
section('개요')
image = Image.open('Images/Untitled.png')
st.image(image,)
callout([
    '안녕하세요! 네이버 영화 사이트의 평점 및 리뷰를 웹 스크래핑 했습니다.',
    '원하는 영화의 영화 코드를 입력하면 해당 영화의 평점 및 리뷰를 가져옵니다.',
    '스크래핑한 평점 및 리뷰를 간략하게 시각화하였습니다.'
])
line_break()

# other section ...
section('Web Scraping')
link = 'https://movie.naver.com/'
st.markdown(link, unsafe_allow_html=True)
st.caption('네이버 영화 사이트로 이동하기')
line_break()

section('Notion')
notion_link = 'https://www.notion.so/soondong/2754e6169db9476892f4ee2235539190'
st.markdown(notion_link, unsafe_allow_html=True)
st.caption('프로젝트 노션 페이지로 이동하기')

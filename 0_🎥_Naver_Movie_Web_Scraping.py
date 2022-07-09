import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
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
section('Summary')
image = Image.open('Images/Untitled.png')
st.image(image,)
callout([
    '안녕하세요! 🙂 네이버 영화 사이트에서 네티즌 평점 및 리뷰를 웹 스크래핑하였습니다.',
    '각 영화마다 고유의 영화 코드가 부여되어 있으며, 영화 코드를 입력했을 때 해당하는 영화의 평점 및 리뷰를 가져옵니다.'
    '수집한 데이터를 기반으로 평점의 분포를 간략하게 시각화하여 Streamlit을 이용해 만들어보았습니다.'
])
line_break()

page_no = 1
 
def get_html(page_no):
    url = f"https://movie.naver.com/movie/point/af/list.naver?st=&target=after&page={page_no}"
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
    response = requests.get(url, headers=headers)

    html = bs(response.content, 'lxml')
    
    return html

@st.cache  
# movie list  
def movie_list():
    html = get_html(page_no)
    movie_list = html.select("#current_movie > option")

    df = pd.DataFrame()
    
    제목 = []
    영화코드 = []

    for idx, content in enumerate(movie_list[1:]):
        제목.append(content.text)
        영화코드.append(content["value"])

    df = pd.DataFrame(dict(제목 = 제목, 영화코드 = 영화코드))
    
    return df

# movie title & movie code
section('Movie List')
callout([
    '현재 네이버 영화 사이트에서 평점 및 리뷰를 확인해볼 수 있는 영화 제목과 영화 코드 목록들을 나타냅니다. 원하는 영화의 코드를 확인하신 후 다음 페이지에서 선택해주세요! 👀'
])

line_break()

st.dataframe(movie_list())
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

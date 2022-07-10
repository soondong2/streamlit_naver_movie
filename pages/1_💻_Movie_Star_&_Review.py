import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import re
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import seaborn as sns
from html_module import section, callout, line_break, title

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

page_no = 1
code = '187347'

def get_html(code, page_no):
    url = f"https://movie.naver.com/movie/point/af/list.naver?st=mcode&sword={code}&target=after&page={page_no}"
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
    response = requests.get(url, headers=headers)

    html = bs(response.content, 'lxml')
    
    return html

@st.cache
# movie list  
def movie_list():
    html = get_html(code, page_no)
    movie_list = html.select("#current_movie > option")

    df = pd.DataFrame()
    
    제목 = []
    영화코드 = []

    for idx, content in enumerate(movie_list[1:]):
        제목.append(content.text)
        영화코드.append(content["value"])

    df = pd.DataFrame(dict(제목 = 제목, 영화코드 = 영화코드))
    
    return df


# movie content
def get_star_review(code, page_no):
    html = get_html(code, page_no)
    reviews = html.select("#old_content > table > tbody > tr > td.title")
    dates = html.select("#old_content > table > tbody > tr > td.num")
    
    star_list = []
    review_list = []
    num_list = []
    date_list = []
    title_list = []
    
    for review in reviews:
        title_list.append(review.select_one("a.movie").text)
        star_list.append(review.select_one("div.list_netizen_score > em").text)

        for i in review.select("a"):
            i.decompose()
        review.select_one("div").decompose()
        
        if len(review.text.strip()) == 0:
            review_list.append("리뷰가 존재하지 않습니다.")
        
        else:
            review_list.append(review.text.strip())
            
    for i, j in enumerate(dates):
        if (i % 2 == 0) or (i == 0):
            num_list.append(j.text)
        else:
            date_list.append(re.findall("<br/>(.*)</td>", str(j))[0])
            
    return star_list, review_list, num_list, date_list, title_list
  

# one page  
def get_one_page(code, page_no):
    content = get_star_review(code, page_no)
    
    star = content[0]
    review = content[1]
    num = content[2]
    date = content[3]
    title = content[4]
    
    one_page = pd.DataFrame(dict(번호=num, 날짜=date, 제목=title, 평점=star, 리뷰=review))
    
    return one_page
  

# all page
def all_review(code, page_no):
    page_list = []
    prev = []
    
    while True:
        page = get_one_page(code, page_no)
        curr = list(get_one_page(code, page_no)["번호"])
        
        if curr == prev:
            break
            
        else:
            page_list.append(page)
            prev = curr
            time.sleep(0.005)
            
            page_no += 1
      
    result = pd.concat(page_list, axis=0).reset_index(drop=True)

    return result

# movie impormation
def movie_info(code, page_no):
    url = f"https://movie.naver.com/movie/point/af/list.naver?st=mcode&sword={code}&target=after&page={page_no}"
    
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    html = get_html(code, page_no)
    reviews = html.select("#old_content > table > tbody > tr > td.title")

    movie_code = reviews[0].select_one("a.movie.color_b")["href"].split("=")[-1]
    
    df = pd.read_html(response.text)[0]
    movie_info_df = pd.DataFrame()
    
    movie_info_df.loc["제목", "정보"] = get_star_review(code, page_no)[4][0]
    movie_info_df.loc["장르", "정보"] = df.loc[0, 1].split("|")[0].strip()
    movie_info_df.loc["감독", "정보"] = df.loc[1, 1]
    movie_info_df.loc["개봉날짜", "정보"] = df.loc[0, 1].split("|")[-1].split(" ")[-1]
    movie_info_df.loc["영화코드", "정보"] = movie_code
    
    return movie_info_df

# seaborn - count plot 그리기
def sns_count_plot(data, x):
    fig = plt.figure(figsize=(10, 4))
    sns.countplot(data=data, x=x)
    st.pyplot(fig)
    
# seaborn - kde plot 그리기
def sns_count_plot(data, x):
    fig = plt.figure(figsize=(10, 4))
    sns.kdeplot(data=data, x=x)
    st.pyplot(fig)

title('영화 정보와 평점 및 리뷰 확인하기')
section('영화 코드')
select_movie_code = st.sidebar.selectbox(
    "🔎 확인하고 싶은 영화 코드를 선택해주세요.",
    movie_list()['영화코드'].tolist()
)
st.write('선택한 영화코드는 ', select_movie_code, '입니다.')
         
line_break()

# movie info
section('영화 정보')
if select_movie_code in movie_list()['영화코드'].tolist():
    st.dataframe(movie_info(select_movie_code, page_no))

line_break()

# star & review
section('평점 및 리뷰')
if select_movie_code in movie_list()['영화코드'].tolist():
    data_load_state = st.text('Loading data...')
    st.dataframe(all_review(select_movie_code, page_no))
    data_load_state.text("")
    
# visualization
section('평점 시각화')
plot = st.sidebar.selectbox(
    "📊 시각화할 그래프를 선택해주세요.",
    ['Count Plot',
    'Kde Plot']
    )

if plot == "Count Plot":
    sns_count_plot(all_review(select_movie_code, page_no), '평점')
    
elif plot == 'Kde Plot':
    sns_kde_plot(all_review(select_movie_code, page_no), '평점')

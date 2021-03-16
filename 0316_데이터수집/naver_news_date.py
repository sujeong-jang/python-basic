# 날짜를 인자로 받아서 해당하는 날짜의 뉴스 보여주기
# 실행: naver_news_date 20210316
import os
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image

def main(string):
    date = string
    for page in range(1,4):
        url = "https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001&date=" + str(date) + "&page=" + str(page)
        news(url)
        
def news(news_url):
    headers = { "User-Agent":"Mozilla/5.0" }
    url = news_url
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html, "html.parser")
    type06= soup.find("ul", {"class": "type06_headline"})
    dl = type06.find_all("dl")
    news_img = []
    news_link = []
    news_title = []
    news_content = []

    for item2 in dl:
        try:
            # 이미지
            img = item2.find("dt", {"class": "photo"}).find("img")
            news_img.append(img["src"])

            # 뉴스 링크
            link = item2.find("dt", {"class": ""}).find("a")
            news_link.append(link["href"])

            # 뉴스 제목
            title = link.text.replace("\t", "").replace("\n", "").replace("\r", "")
            news_title.append(title)

            # 뉴스 내용
            dd =item2.find("dd")
            content = dd.text.replace("\t", "").replace("\t","").replace("\n", "").split("…")[0]

            # 리스트에 추가
            news_content.append(content)
        except:
            print("No image")


    # 이미지를 다운받을 폴더 생성
    if not os.path.isdir('./img_down'):
        os.mkdir('./img_down')

    # 이미지 폴더에 저장
    for i in news_img:
        r = requests.get(i)
        name = i.split("?")
        img_name = name[0].split("/")[-1]
        print(name)
        file = open('./img_down/'+img_name+'.jpg', "wb")
        file.write(r.content)
        file.close()

    # 가져온 데이터 DataFrame에 저장
    df = pd.DataFrame(
                {"이미지":news_img,
                "기사 링크":news_link,
                "기사 제목":news_title,
                "기사 내용":news_content},
                columns=["이미지", "기사 링크", "기사 제목", "기사 내용"])

        
if __name__ == "__main__":
    main(sys.argv[1])
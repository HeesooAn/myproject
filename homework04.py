import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017) # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

# 타겟 url을 읽어서 html을 받아옵니다.
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908',headers=headers)

# html을 추출하기 편리하게 파싱합니다.
soup = BeautifulSoup(data.text, 'html.parser')

genieSongs = soup.select('.list-wrap > tbody > tr > td.number')

genieSongs = soup.select('.list-wrap > tbody > tr')

for song in genieSongs:
    rank = song.select_one('td.number').text.split()[0]
    # print(rank) # 순위(1~50)를 출력합니다.

    title = song.select_one('td.info > a').text.split()
    title = " ".join(title) # 제목을 출력합니다.
    # print(rank, title)

    # 같은 등급(위치)내의 첫번째 태그가 아닌 두세번째 태그에 접근할때는 []인덱스를 사용하여 접근합니다.
    singer = song.select('td.info > a')[1].text # 가수명을 출력합니다.
    print(rank, title, singer)
    doc = {
        'rank': rank,
        'title': title,
        'singer': singer
    }
    db.genieSongs.insert_one(doc) # 이렇게 선언하면 바로 robo3T에 genieSongs라는 콜렉션이 생성됩니다.
    # 실행을 여러번 할수록 db에 계속 누적될 것입니다.





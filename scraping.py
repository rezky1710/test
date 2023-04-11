import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb+srv://rezky:rezky@cluster0.iazo17z.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
url = "https://www.bilibili.tv/id/anime"

data = requests.get(url=url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

anime = soup.select("li > .bstar-video-card")

for data in anime:
    title = data.select_one(".bstar-video-card__text-wrap > .bstar-video-card__text > .bstar-video-card__text-content >p").text
    view_genre = data.select_one(".bstar-video-card__text-wrap > .bstar-video-card__text > .bstar-video-card__text-content > .bstar-video-card__text-desc >p").text
    view_genre_tmp = view_genre.split('Â·')
    genre = view_genre_tmp.pop()
    cover_tmp = data.find('img', class_='bstar-image__img')['src']
    cover_tmp = cover_tmp.split('@')
    cover = cover_tmp[0]

    doc = {
        'Title' : title,
        'Genre' : genre,
        'CoverURL' : cover
    }

    db.anime.insert_one(doc)

    # print(f"{title}  || {genre} || {cover}")
from bs4 import BeautifulSoup
import json
import requests



filePath = 'data.json'

for i in range(10):
    url = f'https://teksciory.interia.pl/szukaj?page={i}&q=darmowe+teksty+i+nuty+polskich+piosenek&t=lyric&sort=score&dr=all'
    songs = {}
    json.dumps(songs)
    pageContent = requests.get(url, timeout=8).text

    soup = BeautifulSoup(pageContent, 'html5lib')
    title = soup.find_all(class_="title d-md-inline")
    artist = soup.find_all(class_="artist -inline")

    for t, a in zip(title, artist):
        print(t.text, a.text.split('- ')[1])
        with open (filePath, 'r+', encoding="utf-8") as f:
            oldData = json.load(f)
            oldData.append({"artist": a.text.split('- ')[1],
                                        "songName": t.text})
            f.seek(0)
            json.dump(oldData, f, indent=2, ensure_ascii=False)
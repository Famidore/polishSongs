from bs4 import BeautifulSoup
import json
import requests
import os

class CitSong():
    def __init__(self, pageLimit:int = 1, filePath:str = 'data.json'):
        self.pageLimit = pageLimit
        self.filePath = filePath
        if not os.path.exists(self.filePath):
            self.makeFile()

    def getData(self, page:int):
        self.url = f'https://teksciory.interia.pl/szukaj?page={page + 1}&q=darmowe+teksty+i+nuty+polskich+piosenek&t=lyric&sort=score&dr=all'
        pageContent = requests.get(self.url, timeout=8).text

        self.soup = BeautifulSoup(pageContent, 'html5lib')
        title = self.soup.find_all(class_="title d-md-inline")
        artist = self.soup.find_all(class_="artist -inline")
        link = self.soup.find_all(class_="title d-md-inline", href=True)

        return (title, artist, link)

    def storeData(self, title, artist, link):
        for t, a, l in zip(title, artist, link):
            with open (self.filePath, 'r+', encoding="utf-8") as f:
                oldData = json.load(f)
                if [{"artist": a.text.split('- ')[1],
                                 "songName": t.text,
                                 "link": l["href"]}] not in oldData:
                    oldData.append([{"artist": a.text.split('- ')[1],
                                    "songName": t.text,
                                    "link": l["href"]}])
                f.seek(0)
                json.dump(oldData, f, indent=2, ensure_ascii=False)

    def eraseData(self):
        os.remove('data.json')
        self.makeFile()
        

    def makeFile(self, name:str = 'data'):
        with open(f'{name}.json', 'w+') as fp:
            d = []
            json.dump(d, fp)
            pass

    def __call__(self):
        for p in range(self.pageLimit):
            t, a, l = self.getData(p)
            self.storeData(t, a, l)
            print(f"Done page {p + 1}!")
        print("\nFinished!")
        # self.eraseData()
        
if __name__ == "__main__":
    model = CitSong(3, 'data.json')
    model()



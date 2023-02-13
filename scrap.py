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

        return (title, artist)

    def storeData(self, title, artist):
        for t, a in zip(title, artist):
            with open (self.filePath, 'r+', encoding="utf-8") as f:
                oldData = json.load(f)
                oldData.append([{"artist": a.text.split('- ')[1],
                                "songName": t.text}])
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
            self.storeData(self.getData(p)[0], self.getData(p)[1])
        print("Finished!")
        # self.eraseData()
        
if __name__ == "__main__":
    model = CitSong(3, 'data.json')
    model()



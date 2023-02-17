from bs4 import BeautifulSoup
import json
import requests
import os
import jellyfish

class CitSong():
    def __init__(self, pageLimit:int = 2, filePath:str = os.path.dirname(__file__) + "/data.json", citiesPath:str = os.path.dirname(__file__) + "/cities.json"):
        self.pageLimit = pageLimit
        self.filePath = filePath
        self.citiesPath = citiesPath
        self.citiesNames = []

        if not os.path.exists(self.filePath):
            self.makeFile()

        try:
            with open(self.citiesPath, 'r+', encoding="utf-8") as c:
                self.citiesData = json.load(c)
                for n in self.citiesData:
                    self.citiesNames.append(n["name"])
        except FileNotFoundError:
            raise FileNotFoundError("File not found!") from None
            
    def getData(self, page:int):
        self.url = f'https://teksciory.interia.pl/szukaj?page={page + 1}&q=darmowe+teksty+i+nuty+polskich+piosenek&t=lyric&sort=score&dr=all'
        pageContent = requests.get(self.url, timeout=8).text

        soup = BeautifulSoup(pageContent, 'html5lib')
        title = soup.find_all(class_="title d-md-inline")
        artist = soup.find_all(class_="artist -inline")
        link = soup.find_all(class_="title d-md-inline", href=True)

        return (title, artist, link)

    def storeData(self, title, artist, link):
        for t, a, l in zip(title, artist, link):
            with open (self.filePath, 'r+', encoding="utf-8") as f:
                oldData = json.load(f)
                newData = { "artist": a.text.split('- ')[1],
                            "songName": t.text,
                            "link": l["href"]}

                for n in self.findNames(self.getText(l)):
                    # print(t.text)
                    self.saveMentions(t.text, a.text.split('- ')[1], n[1])

                if newData not in oldData:
                    oldData.append(newData)

                f.seek(0)
                json.dump(oldData, f, indent=2, ensure_ascii=False)

    def getText(self, link):
        pageContent = requests.get('https://teksciory.interia.pl' + link["href"], timeout=8).text
        soup = BeautifulSoup(pageContent, 'html5lib')

        textData = soup.find(class_="lyrics--text").text
        return textData

    def findNames(self, textData:str):
        mentioned = []
        for index, cName in enumerate(self.citiesNames):
            for word in textData.split():
                prob = self.calcSimillarity(cName, word)
                if (len(word) > 3) and (word[0] == cName[0]) and prob > 0.96:
                    mentioned.append([index, cName])
                    print(f"Found Match with {cName} and {word}, probability: {prob}")
        return mentioned

    def saveMentions(self, songTitle:str, artist:str, cityName:str, mentionsDataPath:str = os.path.dirname(__file__) + "/mentions.json"):
        with open(mentionsDataPath, "r+", encoding="utf-8") as s:
            cData = json.load(s)
            cData.append({"cityName" : cityName,
                          "mentionedIn" : f"{songTitle} by {artist}"})
            s.seek(0)
            json.dump(cData, s, indent=2, ensure_ascii=False)


    def calcSimillarity(self, cityName:str, word:str):
        # print(jellyfish.jaro_winkler_similarity(cityName.lower(), word.lower()))
        return jellyfish.jaro_winkler_similarity(cityName.lower(), word.lower())

    def eraseData(self):
        os.remove(self.filePath)
        self.makeFile()
        

    def makeFile(self):
        with open(self.filePath, 'w+') as fp:
            d = []
            json.dump(d, fp)
            pass


    def __call__(self):
        for p in range(self.pageLimit):
            t, a, l = self.getData(p)
            self.storeData(t, a, l)
            print(f"Done page {p + 1}!")
        print("\nFinished!")
        self.eraseData()
        
if __name__ == "__main__":
    model = CitSong(10)
    model()



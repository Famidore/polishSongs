from bs4 import BeautifulSoup
import json
import requests
import os
import jellyfish
import time

class CitSong():
    def __init__(self, start:int = 0, pageLimit:int = 2, filePath:str = os.path.dirname(__file__) + "/data.json", citiesPath:str = os.path.dirname(__file__) + "/cities.json", mentionsPath:str = os.path.dirname(__file__) + "/mentions.json"):
        self.pageLimit = pageLimit
        self.filePath = filePath
        self.citiesPath = citiesPath
        self.mentionsPath = mentionsPath
        self.start = start
        self.citiesNames = []

        print(f'Searching from {self.start} to {self.pageLimit} pages!')

        if not os.path.exists(self.filePath):
            self.makeFile(self.filePath)

        if not os.path.exists(self.mentionsPath):
            self.makeFile(self.mentionsPath)

        try:
            with open(self.citiesPath, 'r+', encoding="utf-8") as c:
                self.citiesData = json.load(c)
                for n in self.citiesData:
                    self.citiesNames.append(n["name"])
        except FileNotFoundError:
            raise FileNotFoundError("File not found!") from None
            
    def getData(self, page:int):
        for i in range(5):
            pageContent = None
            try:
                time.sleep(2)
                self.url = f'https://teksciory.interia.pl/szukaj?page={page + 1}&q=darmowe+teksty+i+nuty+polskich+piosenek&t=lyric&sort=score&dr=all'
                pageContent = requests.get(self.url, timeout=300).text

            except requests.exceptions.Timeout:
                pass

            if pageContent:
                break

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
        for i in range(5):
            textData = None
            try:
                time.sleep(1)
                pageContent = requests.get('https://teksciory.interia.pl' + link["href"], timeout=300).text
                soup = BeautifulSoup(pageContent, 'html5lib')

                textData = soup.find(class_="lyrics--text").text

                if textData:
                    break

            except requests.exceptions.Timeout:
                pass
        return textData

    def findNames(self, textData:str):
        mentioned = []
        for index, cName in enumerate(self.citiesNames):
            for word in textData.split():
                prob = self.calcSimillarity(cName, word)
                if (word[0].isupper()) and (len(word) > 3) and (word[0] == cName[0]) and (prob > 0.96):
                    mentioned.append([index, cName])
                    print(f"\t\tFound Match with\t {cName} and {word}, \tprobability: {prob:.3f}")
        return mentioned

    def saveMentions(self, songTitle:str, artist:str, cityName:str, mentionsDataPath:str = os.path.dirname(__file__) + "/mentions.json"):
        with open(mentionsDataPath, "r+", encoding="utf-8") as s:
            cData = json.load(s)
            cData.append((cityName, artist))
            s.seek(0)
            json.dump(cData, s, indent=1, ensure_ascii=False)


    def calcSimillarity(self, cityName:str, word:str):
        # print(jellyfish.jaro_winkler_similarity(cityName.lower(), word.lower()))
        return jellyfish.jaro_winkler_similarity(cityName.lower(), word.lower())

    def eraseData(self):
        os.remove(self.filePath)
        self.makeFile()
        print("Erased Data!")
        

    def makeFile(self, path):
        with open(path, 'w+') as fp:
            d = []
            json.dump(d, fp)
            print(f'Created file at {path}')
            pass


    def __call__(self):
        for p in range(self.start, self.pageLimit):
            t, a, l = self.getData(p)
            self.storeData(t, a, l)
            print(f"\033[92m \nDone page {p + 1}!\n \033[0m")
        print("\nFinished!")
        # self.eraseData()
      
if __name__ == "__main__":
    # start_time = time.perf_counter()
    model = CitSong(start=20174, pageLimit=100000)
    model()
    # end_time = time.perf_counter()
    # total_time = end_time - start_time
    # print(total_time)


# print(jellyfish.jaro_winkler_similarity("Warszawa", "Warszawkaa"))

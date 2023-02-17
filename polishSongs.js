let bg, mentionsData, cityData
let cities = []

// ratio = 1,33

function preload() {
  bg = loadImage('img/background2.png')
  mentionsData = loadJSON('scraper\\mentions.json')
  cityData = loadJSON('scraper\\cities.json')
}

function setup() {
  createCanvas(900, 850);
  for (i in cityData) {
    cities.push(new City(cityData[i]["x"], cityData[i]["y"], 3, cityData[i]["name"]))
    for (j in mentionsData){
      if (mentionsData[j][0] == cities.at(-1).cityName){
        cities.at(-1).size += 3;
        cities.at(-1).songArtist.push(mentionsData[j][1])
      }
    }
  }
}

function draw() {
  background(bg);
  background(51, 150)

  for (i of cities) {
    i.show()
    i.showInfo(mouseX, mouseY)
  }
  
}

let bg, songData, cityData
let cities = []

// ratio = 1,33

function preload() {
  bg = loadImage('img/background2.png')
  songData = loadJSON('scraper\\data.json')
  cityData = loadJSON('scraper\\cities.json')
}

function setup() {
  createCanvas(445, 423);
  for (i in cityData) {
    cities.push(new City(cityData[i]["x"], cityData[i]["y"], 5, "Mokronos"))
  }
}

function draw() {
  background(bg);
  background(51, 150)

  for (i of cities) {
    i.show()
  }
}

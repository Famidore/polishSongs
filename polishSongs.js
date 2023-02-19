let bg, mentionsData, cityData;
let cities = [];
let blackList = ['Dobra', 'Bardo', 'Police'];
let mentionScore = 2;
let baseScore = 5;


function preload() {
  bg = loadImage('img/background2.png');
  mentionsData = loadJSON('scraper\\mentions.json');
  cityData = loadJSON('scraper\\cities.json');
}

function setup() {
  createCanvas(min(windowHeight, windowWidth), min(windowHeight, windowWidth));
  for (i in cityData) {
    cities.push(new City(cityData[i]["x"], cityData[i]["y"], baseScore, cityData[i]["name"]));
    for (j in mentionsData) {
      if (mentionsData[j][0] == cities.at(-1).cityName && !(blackList.includes(mentionsData[j][0]))) {
        cities.at(-1).size += mentionScore;
        cities.at(-1).active = true;
        cities.at(-1).songArtist.push(mentionsData[j][1]);
      }
    }
  }

  cities.sort(function (a, b) {
    return b.size - a.size;
  });

  console.log("TOP 10:")
  for (i of cities.slice(0, 10)) {
    console.log((i.size - baseScore) / mentionScore, i.cityName)
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


function windowResized() {
  resizeCanvas(min(windowHeight, windowWidth), min(windowHeight, windowWidth));
  for (i of cities) {
    i.calculatePos()
  }
}

function mousePressed() {
  for (i of cities) {
    i.showArtists(mouseX, mouseY)
  }
}
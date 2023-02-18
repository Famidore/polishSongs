let bg, mentionsData, cityData
let cities = []
let blackList = ['Dobra', 'Bardo', 'Police']

function preload() {
  bg = loadImage('img/background2.png')
  mentionsData = loadJSON('scraper\\mentions.json')
  cityData = loadJSON('scraper\\cities.json')
}

function setup() {
  createCanvas(windowHeight*1.05, windowHeight);
  for (i in cityData) {
    cities.push(new City(cityData[i]["x"], cityData[i]["y"], 3, cityData[i]["name"]));
    for (j in mentionsData) {
      if (mentionsData[j][0] == cities.at(-1).cityName && !(blackList.includes(mentionsData[j][0]))) {
        cities.at(-1).size += 2;
        cities.at(-1).active = true;
        cities.at(-1).songArtist.push(mentionsData[j][1]);
      }
    }
  }
  
  
  cities.sort(function(a, b) {
    return b.size - a.size;
});

for (i of cities.slice(0, 10)){
  print(i.size, i.cityName)
}
}

function draw() {
  background(bg);
  background(51, 150)

  for (i of cities) {
    i.show()
    i.showInfo(mouseX, mouseY)
    i.showArtists(mouseX, mouseY)
  }

}

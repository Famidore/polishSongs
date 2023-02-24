class City {
    constructor(tempX, tempY, tempSize, tempCityName) {
        this.x = tempX;
        this.y = tempY;
        this.size = tempSize;

        this.active = false

        this.cityName = tempCityName;
        this.songName = [];
        this.songArtist = [];

        this.startSize = min(windowHeight, windowWidth)

        this.calculatePos()
    }

    show() {
        if (this.active) {
            fill(255, 0, 0);
        } else {
            fill(0)
        }

        noStroke();
        ellipse(this.x2, this.y2, this.size, this.size);
    }

    calculatePos() {
        this.x2 = map(this.y, 14.117, 24.15, 0, width)
        this.y2 = map(this.x, 49, 54.8333, height, 7)
    }

    showInfo(mx, my) {
        if (dist(mx, my, this.x2, this.y2) < this.size / 2 || this.active) {
            fill(0)
            textAlign(CENTER, BASELINE)
            textSize(this.size + 3)
            text(this.cityName, this.x2, this.y2)
        }
    }

    showArtists(mx, my) {
        if (dist(mx, my, this.x2, this.y2) < this.size / 2 && this.active) {
            print(this.songArtist)
        }
    }
}
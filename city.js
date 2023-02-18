class City {
    constructor(tempX, tempY, tempSize, tempCityName) {
        this.x = tempX;
        this.y = tempY;
        this.size = tempSize;

        this.active = false

        this.cityName = tempCityName;
        this.songName = [];
        this.songArtist = [];
        this.x2 = this.calculatePos()[0]
        this.y2 = this.calculatePos()[1]

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
        let newY = map(this.y, 14.117, 24.15, 0, width)
        let newX = map(this.x, 49, 54.8333, height, 0)

        return [newY, newX]
    }

    showInfo(mx, my) {
        // print(dist(mx, my, this.x2, this.y2), this.cityName)
        if (dist(mx, my, this.x2, this.y2) < this.size / 2 || this.active) {
            fill(0)
            textAlign(CENTER, BASELINE)
            textSize(this.size + 5)
            text(this.cityName, this.x2, this.y2)
        }
    }

    showArtists(mx, my){
        if (dist(mx, my, this.x2, this.y2) < this.size / 2 && this.active && mouseIsPressed){
            print(this.songArtist)

        }
    }
}
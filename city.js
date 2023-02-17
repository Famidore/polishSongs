class City {
    constructor(tempX, tempY, tempSize, tempCityName) {
        this.x = tempX;
        this.y = tempY;
        this.size = tempSize;

        this.cityName = tempCityName;
        this.songName = [];
        this.songArtist = [];
        this.x2 = this.calculatePos()[0]
        this.y2 = this.calculatePos()[1]

    }

    show() {
        fill(255, 0, 0);
        noStroke();
        ellipse(this.x2, this.y2, this.size, this.size);
    }

    calculatePos() {
        let newY = map(this.y, 14.07, 24.09, 0, width)
        let newX = map(this.x, 49, 54.50, height, 30)

        return [newY, newX]
    }

    showInfo(mx, my){
        // print(dist(mx, my, this.x2, this.y2), this.cityName)
        if (dist(mx, my, this.x2, this.y2) < this.size){
            fill(0)
            textAlign(CENTER, CENTER)
            textSize(this.size)
            text(this.cityName, this.x2, this.y2)
        }
    }
}
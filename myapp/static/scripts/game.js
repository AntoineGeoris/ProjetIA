const GAME_BOARD_WIDTH = 5;
const GAME_BOARD_HEIGHT = 5;

class Player {
    constructor(name, line, box) {
        this._name = name;
        this._line = line;
        this._box = box;
    }

    /*---getters---*/

    get name() {
        return this._name;
    }

    get line() {
        return this._line;
    }

    get box() {
        return this._box;
    }

    /*---setters---*/

    set line(line) {
        if (line < GAME_BOARD_WIDTH && line >= 0) {
            this._line = line;
        } else {
            throw "Position invalide."
        }
    }

    set box(box) {
        if (box < GAME_BOARD_HEIGHT && box >= 0) {
            this._box = box;
        } else {
            throw "Position invalide."
        }
    }

    set name(name) {
        this._name = name;
    }
}

class GameBoard {
    constructor(player1, player2) {
        this.player1 = player1;
        this.player2 = player2;
        this.players = [player1, player2];
        this.grid = [];
        this.p = 0;
    }

    display() {
        let directions = ["down", "up", "left", "right"];
        document.write('<table id="gameBoard">');

        for (let iLine = 0; iLine < GAME_BOARD_HEIGHT; iLine++) {
            document.write('<tr>');
            this.grid.push([]);
            for (let iBox = 0; iBox < GAME_BOARD_WIDTH; iBox++) {
                let box = document.createElement("td");
                box.classList.add("gameBoardBox")
                document.body.getElementsByTagName("tr")[iLine].appendChild(box);
                this.grid[iLine].push(box);
                document.write('</td>');
            }
            document.write('</tr>');
        }
        this.grid[0][0].classList.add("playerOne")
        this.grid[0][0].classList.toggle("playerOn");
        this.grid[4][4].classList.add("playerTwo")
        this.grid[4][4].classList.toggle("playerOn");
        document.write('</table>');

        document.write("<div id='arrow_div'>");
        for (let i = 0; i < 4; i++) {
            let arrow = document.createElement("a");
            arrow.classList.add("arrow");
            arrow.id = directions[i];
            arrow.addEventListener('click', () => this.move(arrow.id));
            document.getElementById("arrow_div").appendChild(arrow);
        }
        document.write("</div>");
    }

    move(direction) {
        if (this.#allowedMove(direction)) {
            let box = this.players[this.p % 2].box;
            let line = this.players[this.p % 2].line;

            this.grid[line][box].classList.toggle("playerOn");
            
            switch(direction){
                case "left":
                    this.grid[line][box - 1].classList.add(this.p % 2 == 0 ? "playerOne" : "playerTwo");
                    this.grid[line][box - 1].classList.toggle("playerOn");
                    this.players[this.p % 2].box--;
                    break;
                case "right":
                    this.grid[line][box + 1].classList.add(this.p % 2 == 0 ? "playerOne" : "playerTwo");
                    this.grid[line][box + 1].classList.toggle("playerOn");
                    this.players[this.p % 2].box++;
                    break;
                case "down":
                    this.grid[line + 1][box].classList.add(this.p % 2 == 0 ? "playerOne" : "playerTwo");
                    this.grid[line + 1][box].classList.toggle("playerOn");
                    this.players[this.p % 2].line++;
                    break;
                default:
                    this.grid[line - 1][box].classList.add(this.p % 2 == 0 ? "playerOne" : "playerTwo");
                    this.grid[line - 1][box].classList.toggle("playerOn");
                    this.players[this.p % 2].line--;
                    break;
            }
            this.p++;
        }
        else
            alert("Déplacement non autorisé");
    }

    #allowedMove(direction) {
        let box = this.players[this.p % 2].box;
        let line = this.players[this.p % 2].line;
        let color = this.players[this.p % 2].color;

        if (direction == "left") 
            return box - 1 >= 0 && !this.grid[line][box - 1].classList.contains(this.p % 2 != 0 ? "playerOne" : "playerTwo");

        if (direction == "right") 
            return box + 1 < GAME_BOARD_WIDTH && !this.grid[line][box + 1].classList.contains(this.p % 2 != 0 ? "playerOne" : "playerTwo");

        if (direction == "down") 
            return line + 1 < GAME_BOARD_HEIGHT && !this.grid[line + 1][box].classList.contains(this.p % 2 != 0 ? "playerOne" : "playerTwo");

        return line - 1 >= 0 && !this.grid[line - 1][box].classList.contains(this.p % 2 != 0 ? "playerOne" : "playerTwo");
    }
}

/* window.onload = function () {
    let player1 = new Player("Natan", 0, 0, "#2ACAEA");
    let player2 = new Player("Antoine", 4, 4, "#F62B2B");
    let game_board = new GameBoard(player1, player2);
    game_board.display();
} */
const GAME_BOARD_WIDTH = 5;
const GAME_BOARD_HEIGHT = 5;

class Player {
    constructor(name, line, box, color) {
        this._name = name;
        this._line = line;
        this._box = box;
        this._color = color;
    }

    get name() {
        return this._name;
    }

    get color() {
        return this._color;
    }

    get line() {
        return this._line;
    }

    get box() {
        return this._box;
    }

    set line(line) {
        if (line < GAME_BOARD_WIDTH && line >= 0) {
            this._line = line;
        } else {
            throw "Vous ne pouvez pas vous déplacez par là."
        }
    }

    set box(newBox) {
        if (newBox < GAME_BOARD_HEIGHT && newBox >= 0) {
            this._box = newBox;
        } else {
            throw "Vous ne pouvez pas vous déplacez par là."
        }
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

    /* init_grid () {
        for (let iLine = 0; iLine)
    } */

    display() {
        document.write('<table id="gameBoard">');
        
        for(let iLine = 0; iLine < GAME_BOARD_HEIGHT; iLine++)
        {
            document.write('<tr>');
            this.grid.push([]);
            for(let iBox = 0; iBox < GAME_BOARD_WIDTH; iBox++)
            {
                let box = document.createElement("td");
                box.classList.add("gameBoardBox")
                document.body.getElementsByTagName("tr")[iLine].appendChild(box);
                this.grid[iLine].push(box);
                document.write('</td>');
            }
			document.write('</tr>');
		}
        this.grid[0][0].style.background = this.player1.color;
        this.grid[4][4].style.background = this.player2.color;
        document.write('</table>');

        document.write("<div id='arrow_div'>");
            this.#init_arrows();
        document.write("</div>");
    }

    #init_arrows () {
        let directions = ["down", "up", "left", "right"];
        let self = this;
    
        for (let i = 0; i < 4; i++) {
            let arrow = document.createElement("a");
            arrow.classList.add("arrow");
            arrow.id = directions[i];
            arrow.addEventListener('click', () => this.step(event));
            document.getElementById("arrow_div").appendChild(arrow);
        }
    }

    step(event) {        
        let source = event.target;
        let line = this.players[this.p % 2].line;
        let box = this.players[this.p % 2].box;
        
        try {
            switch(source.id) {
                case "left" :
                    this.players[this.p % 2].box = box - 1;
                    this.grid[line][box - 1].style.background = this.players[this.p % 2].color;
                    break;
                case "right" :
                    this.players[this.p % 2].box = box + 1;
                    this.grid[line][box + 1].style.background = this.players[this.p % 2].color;
                    break;
                case "down" :
                    this.players[this.p % 2].line = line + 1;
                    this.grid[line + 1][box].style.background = this.players[this.p % 2].color;
                    break;
                case "up" :
                    this.players[this.p % 2].line = line - 1;
                    this.grid[line - 1][box].style.background = this.players[this.p % 2].color;
                    break;
            }

        this.p++;
        } catch (e) {
            alert(e);
        }
    }
}
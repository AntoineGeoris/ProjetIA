/* const GAME_BOARD_HEIGHT = 5;
const GAME_BOARD_WIDTH = 5;

class Player {
    constructor(line, box, color) {
        this.line = line;
        this.box = box;
        this.color = color;
    }
}

let players1 = new Player(0, 0, "#2ACAEA");
let players2 = new Player(4, 4, "#F62B2B");
let p = 0;
let players = [players1, players2];
let gameBoard = [];

function createGameBoard() {
    document.write('<table id="gameBoard">');
        
        for(let iLine = 0; iLine < GAME_BOARD_HEIGHT; iLine++)
        {
            document.write('<tr>');
            gameBoard.push([]);
            for(let iBox = 0; iBox < GAME_BOARD_WIDTH; iBox++)
            {
                let box = document.createElement("td");
                box.classList.add("gameBoardBox")
                document.body.getElementsByTagName("tr")[iLine].appendChild(box);
                gameBoard[iLine].push(box);
                document.write('</td>');
            }
			document.write('</tr>');
		}
    gameBoard[0][0].style.background = "#2ACAEA";
    gameBoard[4][4].style.background = "#F62B2B";
    document.write('</table>');

    document.write("<div id='arrow_div'>");
        init_arrows();
    document.write("</div>");
}

function init_arrows () {
    let directions = ["down", "up", "left", "right"];

    for (let i = 0; i < 4; i++) {
        let arrow = document.createElement("a");
        arrow.classList.add("arrow");
        arrow.id = directions[i];
        arrow.addEventListener('click', move);
        document.getElementById("arrow_div").appendChild(arrow);
    }
}
function move(event) {
    let source = event.target;
    let line = players[p % 2].line;
    let box = players[p % 2].box;

    switch (source.id) {
        case "down":
            gameBoard[line + 1][box].style.background = players[p % 2].color;
            players[p % 2].line = line + 1;
            break;
        case "up":
            gameBoard[line - 1][box].style.background = players[p % 2].color;
            players[p % 2].line = line - 1;
            break;
        case "left":
            gameBoard[line][box - 1].style.background = players[p % 2].color;
            players[p % 2].box = box - 1;
            break;
        case "right":
            gameBoard[line][box + 1].style.background = players[p % 2].color;
            players[p % 2].box = box + 1;
            break;
    }

    p++
    
} */
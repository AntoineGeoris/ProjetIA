const GAME_BOARD_HEIGHT = 5;
const GAME_BOARD_WIDTH = 5;

function createGameBoard() {
    document.write('<table id="gameBoard">');
        let gameBoard = [];
        for(var iLine = 0; iLine < GAME_BOARD_HEIGHT; iLine++)
        {
            document.write('<tr>');
            gameBoard.push([]);
            for(var iBox = 0; iBox < GAME_BOARD_WIDTH; iBox++)
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
}  
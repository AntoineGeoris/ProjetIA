(function () {
    const { Component, mount } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;
    const { useState } = owl.hooks;

    const GAME_TEMPLATE = xml /* xml */ `
        <div>
            <button t-on-click="newGame">Nouvelle partie</button>
            <GameBoard gameBoard="gameBoard"/>
            <div id="arrow_div" t-att-class="gameBoard.gameID == null ? 'notVisible' : ''">
                <a class="arrow" id="left" t-on-click="arrowClick('left')"></a>
                <a class="arrow" id="right" t-on-click="arrowClick('right')"></a>
                <a class="arrow" id="up" t-on-click="arrowClick('up')"></a>
                <a class="arrow" id="down" t-on-click="arrowClick('down')"></a>
            </div>
        </div>
    `;

    const GAME_BOARD_TEMPLATE = xml /* xml */ `
        <div>
            <table id="gameBoard">
                <t t-foreach="props.gameBoard.board" t-as="line">
                    <tr>
                        <t t-foreach="line" t-as="box">
                            <td class="gameBoardBox" t-att-class="box == 1 ? 'playerOne' : (box == 2 ? 'playerTwo' : '')"></td>
                        </t>
                    </tr>
                </t>
            </table>
        </div>`;

    class GameBoard extends Component {
        static template = GAME_BOARD_TEMPLATE;
        static props = ["gameBoard"];
    }

    class Game extends Component {
        static template = GAME_TEMPLATE;
        static components = { GameBoard };

        gameBoard = useState({
            gameID: null,
            players: null,
            activePlayer: null,
            turn_no: null,
            board: [],
        });

        async newGame() {
            const response = await this.jsonRPC("/game/new/", {
                player1ID: 1,
                //player2ID: 2,
            });
            this.gameBoard.gameID = response.gameID;
            this.gameBoard.players = [response.player1, response.player2];
            this.gameBoard.activePlayer = response.player1;
            this.gameBoard.turn_no = response.turn_no;
            this.gameBoard.board = response.board;
        }

        async arrowClick(movement) {
            const newState = await this.jsonRPC("/game/move/", {
                gameID: this.gameBoard.gameID,
                move: movement,
                playerID: this.gameBoard.activePlayer,
            });

            this.gameBoard.turn_no = newState.turn_no;
            this.gameBoard.board = newState.board;
            this.activePlayer = newState.activePlayer;
        }

        jsonRPC(url, data) {
            return new Promise(function (resolve, reject) {
                let xhr = new XMLHttpRequest();
                xhr.open("POST", url);
                xhr.setRequestHeader("Content-type", "application/json");
                    xhr.onload = function () {
                    if (this.status >= 200 && this.status < 300) {
                        resolve(JSON.parse(xhr.response));
                    }
                    else {
                        reject({
                            status: this.status,
                            statusText: xhr.statusText,
                        });
                    }                                   
                };
                xhr.onerror = function () {
                    reject({
                        status: this.status,
                        statusText: xhr.statusText,
                    });
                }
                xhr.send(JSON.stringify(data))           
            });
    }
}

    function setup() {
        owl.config.mode = "dev";
        mount(Game, { target: document.body });
    }

    whenReady(setup);
    
}) ();



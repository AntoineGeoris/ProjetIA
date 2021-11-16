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
            <t t-set="numLine" t-value="0" />
            <table id="gameBoard">
                <t t-foreach="props.gameBoard.board" t-as="line">
                    <t t-set="numColumn" t-value="0" />
                    <tr>
                        <t t-foreach="line" t-as="box">
                            <td class="gameBoardBox" t-att-class="box == 1 ? (props.gameBoard.player1_pos[0] == numLine and props.gameBoard.player1_pos[1] == numColumn ? 'playerOne playerOn' : 'playerOne')
                                                                 : (box == 2 ? (props.gameBoard.player2_pos[0] == numLine and props.gameBoard.player2_pos[1] == numColumn ? 'playerTwo playerOn' : 'playerTwo') : '')"></td>
                            <t t-set="numColumn" t-value="numColumn+1" />
                        </t>
                    </tr>
                    <t t-set="numLine" t-value="numLine+1" />
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
            player1_pos: "44",
            player2_pos: null,
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
            this.gameBoard.player1_pos = response.player1_pos;
            this.gameBoard.player2_pos = response.player2_pos;
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
            this.gameBoard.activePlayer = newState.activePlayer;
            this.gameBoard.player1_pos = newState.player1_pos;
            this.gameBoard.player2_pos = newState.player2_pos;
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



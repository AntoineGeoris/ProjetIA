(function () {
    const { Component, mount } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;
    const { useState } = owl.hooks;

    const GAME_TEMPLATE = xml /* xml */ `
        <div id="game">
            <t t-if="gameBoard.gameID == null">
                <t t-set="style" t-value="'display: none'"/>
            </t>
            <t t-if="gameBoard.gameID != null">
                <t t-set="style" t-value="''"/>
            </t>
            <button class="btn btn-primary" t-on-click="newGame">Nouvelle partie</button>
            <GameBoard gameBoard="gameBoard"/>
            <div id="arrow_div" t-att-style="style">
                <span class="arrow" id="left" t-on-click="arrowClick('left')"></span>
                <span class="arrow" id="right" t-on-click="arrowClick('right')"></span>
                <span class="arrow" id="up" t-on-click="arrowClick('up')"></span>
                <span class="arrow" id="down" t-on-click="arrowClick('down')"></span>
            </div>
            <Scoreboard scoreboard="scoreboard" t-att-style="style"/>
            <div class="modal fade" id="endGameModal" tabindex="-1" aria-labelledby="endGameModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="endGameModalLabel">Fin de partie</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <t t-if="scoreboard.player1 > scoreboard.player2">
                        <p>Le joueur 1 à gagner avec un score de <span><t t-esc="scoreboard.player1"/></span> !</p>
                    </t>
                    <t t-else="">
                        <p>Le joueur 2 à gagner avec un score de <span><t t-esc="scoreboard.player2"/></span> !</p>
                    </t>
                </div>
                <div class="modal-footer">
                    <form action="POST">
                        <button type="button" class="btn btn-primary" t-on-click="newGame" data-bs-dismiss="modal" aria-label="Close">Rejouer</button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" aria-label="Close">Fermer</button>
                    </form>
                </div>
                </div>
            </div>
            </div>
        </div>
    `;

    const SCOREBOARD_TEMPLATE = xml /* xml */`
        <div id="scoreboard" >
            <table>
                <tr>
                    <th>Joueur 1</th><th>Joueur 2</th>
                </tr>
                <tr>
                    <td><t t-esc="props.scoreboard.player1"/></td><td><t t-esc="props.scoreboard.player2"/></td>
                </tr>
            </table>
        </div>
    `;

    const GAME_BOARD_TEMPLATE = xml /* xml */ `
        <div id="gameBoard">
            <t t-set="numLine" t-value="0" />
            <table>
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
    
    class Scoreboard extends Component {
        static template = SCOREBOARD_TEMPLATE;
        static props = ["scoreboard"];
    }

    class Game extends Component {
        static template = GAME_TEMPLATE;
        static components = { GameBoard, Scoreboard };

        gameBoard = useState({
            gameID: null,
            players: null,
            player1_pos: "44",
            player2_pos: null,
            activePlayer: null,
            turn_no: null,
            board: [],
            isGameover: false,
        });

        scoreboard = useState({
            player1: null,
            player2: null,
        })

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
            this.scoreboard.player1 = 1;
            this.scoreboard.player2 = 1;
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
            this.scoreboard.player1 = newState.player1_score;
            this.scoreboard.player2 = newState.player2_score;
            
            if (newState.is_gameover)
                this.endGame();
        }

        endGame() {
            var myModal = new bootstrap.Modal(document.getElementById('endGameModal'))

            myModal.show();
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



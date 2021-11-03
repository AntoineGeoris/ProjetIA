(function () {
    const { Component, Store, mount } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;
    const { useRef, useDispatch, useState, useStore } = owl.hooks;

    const GAME_TEMPLATE = xml /* xml */ `
        <div>
            <form action="/game/" method="POST">
                <button>Nouvelle partie</button>
            </form>
        </div>
    `;

    const GAME_BOARD_TEMPLATE = xml /* xml */ `
        <div>
            <table id="gameBoard">
                <t t-foreach="table" t-as="line">
                    <tr>
                        <t t-foreach="line" t-as="box">
                            <td class="gameBoardBox"></td>
                        </t>
                    </tr>
                </t>
            </table>
            <div id="arrow_div">
                <a class="arrow" id="left" t-on-click="arrowClick('left')"></a>
                <a class="arrow" id="right" t-on-click="arrowClick('right')"></a>
                <a class="arrow" id="up" t-on-click="arrowClick('up')"></a>
                <a class="arrow" id="down" t-on-click="arrowClick('down')"></a>
            </div>
        </div>`;

    class GameBoard extends Component {
        static template = GAME_BOARD_TEMPLATE;

        table = [[0,0,0,0,0]]

        constructor(gameID, board, turn_no, player1, player2) {
            super();
            this.gameID = gameID;
            this.players = [player1, player2];
            this.activePlayer = this.players[turn_no % 2];
            this.turn_no = turn_no;
            this.board = board;
        }

        async arrowClick(movement) {
            const newState = await this.jsonRPC("/game/move/", {
                gameID: this.gameID,
                movement,
                
            });
        }

        jsonRPC(url, data) {
            return new Promise(function (resolve, reject) {
                let xhr = new XMLHttpRequest();
                xhr.open("POST", url);
                xhr.setRequestHeader("Content-type", "application/json");
                /* xhr.onload = function () {
                    if (this.status >= 200 && this.status < 300)
                        resolve(JSON.parse(xhr.response));
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
                } */
                xhr.send(JSON.stringify(data))           
            });
        }

          /* gameID = this.props.gameID;

          state = useState({
              players: this.porps.players,
              board: this.props.board,
              activePlayer: this.props.activePlayer,
          }); */
    }

    class Game extends Component {
        static template = GAME_TEMPLATE;
    }

    function setup() {
        owl.config.mode = "dev";
        mount(Game, { target: document.body });
    }

    whenReady(setup);
    
}) ();



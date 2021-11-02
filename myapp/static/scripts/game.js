(function () {
    const { Component, Store, mount } = owl;
    const { xml } = owl.tags;
    const { whenReady } = owl.utils;
    const { useRef, useDispatch, useState, useStore } = owl.hooks;

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

        table = [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]];

        async arrowClick(movement) {
            let move = false;

            if (movement === "left")
                move = movement;
            else if (movement === "right")
                move = movement;
            else if (movement === "up")
                move = movement;
            else if (movement === "down")
                move = movement;

            if (move) {
                console.log(move);
            }
        }
    }

    function setup() {
        owl.config.mode = "dev";
        mount(GameBoard, { target: document.body });
    }

    whenReady(setup);
    
}) ();



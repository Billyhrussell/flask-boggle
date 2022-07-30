"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure
  // i = [["C","A","T","X", "X"],
  //            ["C","A","T","X", "X"], ["C","A","T","X", "X"],
  //            ["C","A","T","X", "X"], ["C","A","T","X", "X"]]

  for (let i = 0; i < board.length(); i++) {
    const $tr = $("<tr>");
    for (let j = 0; j < board.length(); j++) {
      const $td = ($("<td>"))
      $tr.append($td)
      $td.text(`${board[i][j]}`)
    }
    $table.append($tr)
  }
}




start();
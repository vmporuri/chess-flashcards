let board;
let game = new Chess();
let solved = false;

const turnStatus = document.querySelector("#turn");
const newPuzzleButton = document.querySelector("#new-puzzle");
const config = {
  draggable: true,
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd,
  pieceTheme: "/static/img/{piece}.png",
};

async function setupNewPuzzle() {
  try {
    const response = await fetch("get-fen");
    const data = await response.json();
    game = new Chess(data.fen);
    config.position = data.fen;
    board = Chessboard("board", config);
    solved = false;
    newPuzzleButton.style.display = "none";
    const moveColor = game.turn() === "b" ? "Black" : "White";
    turnStatus.innerText = `${moveColor} to move`;
  } catch (error) {
    console.error("Error setting up game:", error);
  }
}

function onDragStart(source, piece, position, orientation) {
  if (solved || game.game_over()) return false;

  if (
    (game.turn() === "w" && piece.search(/^b/) !== -1) ||
    (game.turn() === "b" && piece.search(/^w/) !== -1)
  ) {
    return false;
  }
}

async function onDrop(source, target) {
  const move = game.move({
    from: source,
    to: target,
    promotion: "q",
  });

  if (move === null) return "snapback";

  const uciMove = `${source}${target}${move.promotion ? move.promotion : ""}`;

  try {
    const response = await fetch("/validate-move", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ move: uciMove }),
    });
    const data = await response.json();
    if (data.isValidMove) {
      solved = true;
      newPuzzleButton.style.display = "inline";
    } else {
      game.undo();
      board.position(game.fen());
    }
  } catch (error) {
    console.error("Error validating move:", error);
    game.undo();
    board.position(game.fen());
  }
}

function onSnapEnd() {
  board.position(game.fen());
}

newPuzzleButton.addEventListener("click", setupNewPuzzle);
setupNewPuzzle();

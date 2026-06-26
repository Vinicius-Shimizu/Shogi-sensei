const piecesImagesMap = {
    "P": "/pieces/pawn.svg",
    "+P": "/pieces/promoted_pawn.svg",
    "L": "/pieces/lance.svg",
    "+L": "/pieces/promoted_lance.svg",
    "N": "/pieces/knight.svg",
    "+N": "/pieces/promoted_knight.svg",
    "G": "/pieces/gold_general.svg",
    "S": "/pieces/silver_general.svg",
    "+S": "/pieces/promoted_silver_general.svg",
    "R": "/pieces/rook.svg",
    "+R": "/pieces/promoted_rook.svg",
    "B": "/pieces/bishop.svg",
    "+B": "/pieces/promoted_bishop.svg",
    "K": "/pieces/white_king.svg",
    "k": "/pieces/black_king.svg",
}

const cols = ["9", "8", "7", "6", "5", "4", "3", "2", "1"];
const rows = ["a", "b", "c", "d", "e", "f", "g", "h", "i"];

function getPieceKey(piece) {
    if (piece === "K" || piece === "k")
        return piece;

    if (piece.startsWith("+"))
        return `+${piece[1].toUpperCase()}`;

    return piece.toUpperCase();
}

function isSentePiece(piece) {
    if (piece.startsWith("+"))
        return piece[1] === piece[1].toLowerCase();

    return piece === piece.toLowerCase();
}


function Piece({ piece }) {
    if(!piece) return null;
    return (<img
        src={piecesImagesMap[getPieceKey(piece)]}
        alt={piece}
        className={`w-20 h-20 ${isSentePiece(piece) ? "rotate-180" : ""}`}
    />)
}


function parseSfenBoard(sfen) {
  const boardPart = sfen.split(" ")[0];

  return boardPart.split("/").map(row => {
    const squares = [];

    let i = 0;

    while (i < row.length) {
      const char = row[i];

      if (!isNaN(char)) {
        for (let j = 0; j < Number(char); j++) {
          squares.push(null);
        }
        i++;
      }

      else if (char === "+") {
        squares.push(`+${row[i + 1]}`);
        i += 2;
      }

      else {
        squares.push(char);
        i++;
      }
    }

    return squares;
  });
}

export function Board({ sfen }) {
  const board = parseSfenBoard(sfen);

  return (
    <div className="flex justify-center p-4">
      <div className="grid grid-cols-10 border-2 border-black">
        
        {/* canto vazio */}
        <div></div>

        {/* colunas */}
        {cols.map((c) => (
          <div
            key={c}
            className="w-16 h-16 flex items-center justify-center font-bold"
          >
            {c}
          </div>
        ))}

        {/* linhas + tabuleiro */}
        {board.map((row, rIndex) => (
          <>
            {/* label da linha */}
            <div
              key={`row-${rIndex}`}
              className="w-16 h-16 flex items-center justify-center font-bold"
            >
              {rows[rIndex]}
            </div>

            {/* casas */}
            {row.map((piece, cIndex) => (
              <div
                key={`${rIndex}-${cIndex}`}
                className="w-16 h-16 border border-gray-500 flex items-center justify-center"
              >
                <Piece piece={piece} />
              </div>
            ))}
          </>
        ))}
      </div>
    </div>
  );
}
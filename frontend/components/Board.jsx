const BASE_URL = import.meta.env.BASE_URL;
const piecesImagesMap = {
    "P": `${BASE_URL}pieces/pawn.svg`,
    "+P": `${BASE_URL}pieces/promoted_pawn.svg`,
    "L": `${BASE_URL}pieces/lance.svg`,
    "+L": `${BASE_URL}pieces/promoted_lance.svg`,
    "N": `${BASE_URL}pieces/knight.svg`,
    "+N": `${BASE_URL}pieces/promoted_knight.svg`,
    "G": `${BASE_URL}pieces/gold_general.svg`,
    "S": `${BASE_URL}pieces/silver_general.svg`,
    "+S": `${BASE_URL}pieces/promoted_silver_general.svg`,
    "R": `${BASE_URL}pieces/rook.svg`,
    "+R": `${BASE_URL}pieces/promoted_rook.svg`,
    "B": `${BASE_URL}pieces/bishop.svg`,
    "+B": `${BASE_URL}pieces/promoted_bishop.svg`,
    "K": `${BASE_URL}pieces/white_king.svg`,
    "k": `${BASE_URL}pieces/black_king.svg`,
    "E": `${BASE_URL}pieces/empty.svg`
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
        className={`w-[85%] h-[85%] ${isSentePiece(piece) ? "rotate-180" : ""}`}
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

export default function Board({ sfen }) {
  const board = parseSfenBoard(sfen);
  
  return (
    <div className="flex justify-center p-4">
      <div className="grid grid-cols-10 grid-rows-10 aspect-square w-[40vw] md:w-[30vw]">
        
        {/* canto vazio */}
        <div></div>

        {/* colunas */}
        {cols.map((c) => (
          <div
            key={c}
            className="flex items-center justify-center font-bold text-sm sm:text-base"
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
              className="flex items-center justify-center font-bold text-sm sm:text-base"
            >
              {rows[rIndex]}
            </div>

            {/* casas */}
            {row.map((piece, cIndex) => (
              <div
                key={`${rIndex}-${cIndex}`}
                className="border border-gray-500 flex items-center justify-center"
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
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


function HandPiece({ piece, qty, side }) {
    return (
        <div className="flex flex-col items-center w-[10%]">
            <img
                src={piecesImagesMap[piece]}
                className={`w-full aspect-square object-contain ${
                    side !== "sente" ? "rotate-180" : ""
                }`}
                alt={piece}
            />

            <span className="text-sm">
                x{qty}
            </span>
        </div>
    );
}

export default function Hand({ pieces, side }) {
    if (!pieces) return null;

    return (
        <div className="flex gap-1 justify-center p-2 w-[80vw] md:w-[30vw]">
            {Object.entries(pieces).map(([piece, qty]) => (
                <HandPiece
                    key={piece}
                    piece={piece}
                    qty={qty}
                    side={side}
                />
            ))}
        </div>
    );
}
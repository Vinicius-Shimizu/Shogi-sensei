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
        className={`w-12 h-12 ${isSentePiece(piece) ? "rotate-180" : ""}`}
    />)
}


function HandPiece({ piece, qty }) {
    return (
        <div className="flex-col">
            <div className="flex items-center gap-2">
                <img
                    src={piecesImagesMap[piece]}
                    className="w-20 h-20"
                    alt={piece}
                />
            </div>
            <span className="text-sm">x{qty}</span>

        </div>
    );
}

export default function Hand({ pieces }) {
    if (!pieces) return null;

    return (
        <div className="flex gap-4 justify-center p-2">
            {Object.entries(pieces).map(([piece, qty]) => (
                <HandPiece
                    key={piece}
                    piece={piece}
                    qty={qty}
                />
            ))}
        </div>
    );
}
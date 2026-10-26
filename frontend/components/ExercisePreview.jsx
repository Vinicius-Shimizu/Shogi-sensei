import Hand from "./Hand";
import Board from "./Board";
import BoardWithMovement from "./BoardWithMovement";
import CheckmateBoard from "./CheckmateBoard";

export default function ExercisePreview({ result }) {
    switch (result.exercise_type) {
        case "recon":
            const pos = result.solution.split(":")[1]
            return (
                <div className="flex flex-col justify-center">
                    <p className="text-center"> Qual é a peça na posição {pos}?</p>
                    <Board sfen={result.sfen} />
                </div>
            );

        case "movement1":
            return (
                <div className="flex flex-col justify-center">
                    <p className="text-center"> Qual é a peça na casa vermelha que pode se mover para as casas verdes?</p>
                    <BoardWithMovement
                        sfen={result.sfen}
                        moves={result.solution.split(":")[1]}
                    />
                </div>
            );

        case "movement2":
            return (
                <div className="flex flex-col justify-center">
                    <p className="text-center"> Qual é a peça na casa vermelha que pode se mover para as casas verdes? </p>
                    <BoardWithMovement
                        sfen={result.sfen}
                        moves={result.solution.split(":")[1]}
                    />
                </div>
            );

        case "promotion":
            return (
                <div className="flex flex-col justify-center">
                    <p className="text-center"> Qual movimento abaixo pode resultar numa promoção? </p>
                    <Board
                        sfen={result.sfen}
                        moves={result.solution.split(":")[1]}
                    />
                </div>
            );
        
        case "drop":
            let PIECES_DICT = {
                "P": "o Peão",
                "L": "a Lança",
                "N": "o Cavalo",
                "S": "o General de Prata",
                "B": "o Bispo",
                "R": "a Torre",
                "G": "o General de Ouro",
                "+P": "o Peão Promovido",
                "+L": "a Lança Promovida",
                "+N": "o Cavalo Promovido",
                "+S": "o General de Prata Promovido",
                "+B": "o Bispo Promovido",
                "+R": "a Torre Promovida",
            };
            const piece = PIECES_DICT[result.solution.split("*")[0]];
            return (
                <div className="flex flex-col justify-center">
                    <p className="text-center"> Qual é a casa do tabuleiro na qual você pode corretamente posicionar {piece} da sua mão?</p>
                    <div>
                        <Hand pieces={result.hands.gote} side={"gote"} />
                        <CheckmateBoard sfen={result.sfen} />
                        <Hand pieces={result.hands.sente} side={"sente"} />
                    </div>
                </div>
            );

        case "checkmate-in-one":
            return (
                <div className="flex flex-col justify-center">
                    <p className="text-center"> Qual movimento abaixo leva ao chequemate?</p>
                    <div>
                        <Hand pieces={result.hands.gote} side={"gote"} />
                        <CheckmateBoard sfen={result.sfen} />
                        <Hand pieces={result.hands.sente} side={"sente"} />
                    </div>
                </div>
            );

        default:
            return null;
    }
}
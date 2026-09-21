import Hand from "./Hand";
import Board from "./Board";
import BoardWithMovement from "./BoardWithMovement";

export default function ExercisePreview({ result }) {
    switch (result.exercise_type) {
        case "recon":
            return (
                <div className="flex justify-center">
                    <Board sfen={result.sfen} />
                </div>
            );

        case "movement2":
            return (
                <div className="flex justify-center">
                    <BoardWithMovement
                        sfen={result.sfen}
                        moves={result.solution.split(":")[1]}
                    />
                </div>
            );

        case "checkmate-in-one":
            return (
                <div className="flex justify-center">
                    <div>
                        <Hand pieces={result.hands?.gote} />
                        <Board sfen={result.sfen} />
                        <Hand pieces={result.hands?.sente} />
                    </div>
                </div>
            );

        default:
            return null;
    }
}